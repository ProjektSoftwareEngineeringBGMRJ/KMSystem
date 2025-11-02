from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify # für Nachricht bei Route /setup-admin
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.datenbank import db #  -> SQLAlchemy()
from models.meldung import Meldung
from models.enums import Kategorie, Status, Sichtbarkeit, Benutzer_rolle
from models.benutzer import Benutzer
from models.admin import Admin
from models.studierende import Studierende
from models.lehrende import Lehrende
from models.modul import Modul
from models.rollen_liste import get_rolle_klasse
import os
from models.kommentar import Kommentar

app = Flask(__name__)

if os.getenv("RENDER") == "true":
    db_url = os.getenv("DATABASE_URL") # Render-DB (Umgebungsvariable auf Render)
else:
    db_url = "sqlite:///kmsystem.db" # -> lokale installation: SQLite verwenden

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
print("Datenbank-URL:", db_url) # debug (verwendete Datenbank)

app.secret_key = "irgendein_geheimer_schlüssel_123" # unsicher! sollte in .env

db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Benutzer.query.get(int(user_id)) # SQLAlchemy lädt richtige Unterklasse von Benutzer


# Controller: @app.route(...) reagiert auf HTTP-Anfragen:
@app.route("/setup-admin") # Admin in die Datenbank bringen (wenn leer): Einmal "App-URL/setup-admin" aufrufen. 
def setup_admin():
    admin_email = "admin@example.org" # sollte in .env
    admin_passwort = "admin123" # sollte in .env
    if not Admin.query.filter_by(email=admin_email).first():
        admin = Admin(name="Admin", email=admin_email, passwort=admin_passwort)
        db.session.add(admin)
        db.session.commit()
        return jsonify({"status": "Admin erstellt."})
    return jsonify({"status": "Admin existiert bereits. Login unter http://127.0.0.1:5000/"})

@app.route("/") # bei Aufruf von https://kmsystem.onrender.com/ zu login weiterleiten
def index():
    return redirect("/login") # Startseite

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        passwort = request.form["passwort"]
        user = Benutzer.query.filter_by(email=email).first() #direkte SQL-Abfrage
        if user and user.check_passwort(passwort):
            login_user(user)
            flash(f"Login erfolgreich als {user.type}.")
            return redirect(url_for("uebersicht"))
        else:
            flash("Login fehlgeschlagen")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    flash("Erfolgreich ausgeloggt.")
    return redirect(url_for("login"))

# Übersichtsseite (acd Übersicht anzeigen)
@app.route("/uebersicht") # GET-Anfrage in Template: <form method="get" action="/uebersicht">
@login_required
def uebersicht():
    # Parameter aus Filter-Anfrage: 
    alle_meldungen = request.args.get("alle_meldungen") == "true" # anfangs eigene Meldungen zeigen
    selected_modul = request.args.get("modul") or None # holen von Werten aus HTML-Formular (z.B. aus Feld name="modul")
    selected_status = request.args.get("status") or None    
    selected_kategorie = request.args.get("kategorie") or None
    
    # abhängig von Button
    if isinstance(current_user, Studierende):
        # Liste mit allen Modulen
        module = db.session.query(Modul).all()
        # alle_meldungen false: nur eigene zeigen 
        meldungen = db.session.query(Meldung).all() if alle_meldungen else current_user.meldungen#.all()
    elif isinstance(current_user, Lehrende):
        if alle_meldungen:
            # alle module anzeigen
            module = db.session.query(Modul).all()
        else:
            # zugewiesene Module des Lehrenden zeigen
            module = current_user.module
        # alle_meldungen flase: nur Meldungen eigener Module zeigen  
        meldungen = db.session.query(Meldung).all() if alle_meldungen else current_user.get_eigene_meldungen()
    elif isinstance(current_user, Admin):
        # Liste mit allen Modulen
        module = db.session.query(Modul).all()
        # Alle Meldungen aller Module zeigen (Methode von Admin)
        meldungen = current_user.get_alle_meldungen() 
        #meldungen = admin.get_alle_meldungen() if alle_meldungen else current_user.get_eigene_meldungen()
    
    #Filter
    if selected_modul:
        meldungen = [m for m in meldungen if m.modul.titel == selected_modul]
    if selected_status:
        meldungen = [m for m in meldungen if m.status.name == selected_status]
    if selected_kategorie:
        meldungen = [m for m in meldungen if m.kategorie.name == selected_kategorie]
    
    return render_template("uebersicht.html",
        user = current_user,
        meldungen = meldungen,
        alle_meldungen = alle_meldungen,
        module = module,
        status_enum = Status,
        kategorie_enum = Kategorie, 
        selected_modul = selected_modul,
        selected_status = selected_status,
        selected_kategorie = selected_kategorie
    )
    
@app.route("/meldung/<int:meldungs_id>")
@login_required
def meldung_anzeigen(meldungs_id):
    '''
    Read-Operation einer Meldung (R in CRUD):
    Direkte SQL-Abfrage, entspricht: SELECT * FROM meldung WHERE id = :meldungs_id LIMIT 1;
    '''
    meldung = Meldung.query.filter_by(id=meldungs_id).first() 
    if not meldung:
        pass
    
    return render_template("meldung_detail.html", 
                           meldung=meldung, 
                           user=current_user,
                           status_enum = Status,
                           sichtbarkeit_enum = Sichtbarkeit)

@app.route("/meldung/<int:meldungs_id>/status_aendern", methods=["POST"])
@login_required
def status_aendern(meldungs_id:int):
    '''
    Update-Operation des Meldungsstatus (U in CRUD):
    Holt Status, Kommentar, Sichtbarkeit aus HTML-Formular,
    Schreibt geänderten Status in DB, ruft add_kommentar() von Lehrende auf.
    Nur für Lehrende. Checkt, ob Meldung zu zugewiesenen Modulen gehört.
    '''
    meldung = Meldung.query.filter_by(id=meldungs_id).first()
    if not meldung:
        return redirect(url_for("uebersicht"))
    
    # Werte aus Formular holen
    neuer_status_name = request.form.get("status") # neuer Staus
    kommentar_text = request.form.get("kommentar") # optional
    sichtbarkeit_name = request.form.get("sichtbarkeit") # Enum
    sichtbarkeit = Sichtbarkeit[sichtbarkeit_name]
    
    # Statuslogik: Erlaubte Übergänge        
    neuer_status = Status[neuer_status_name]
    erlaubte_wechsel = {
        Status.OFFEN: [Status.BEARBEITUNG],
        Status.BEARBEITUNG: [Status.GESCHLOSSEN],
        Status.GESCHLOSSEN: []
    }
    
    # Kombinierte Aktionen aus Status ändern + Kommentar
    try:
        if meldung.modul not in current_user.module:
            raise PermissionError("Dies ist nur für Meldungen eigener Module möglich.")
        
        if neuer_status in erlaubte_wechsel[meldung.status]: # Statuswechsel: offen -> in Bearbeitung -> abgeschlossen
            meldung.status = neuer_status
            
            # Status ändern und kommentieren
            if kommentar_text.strip():
                db.session.add(current_user.add_kommentar(meldung, kommentar_text.strip(), sichtbarkeit))
                db.session.commit()
                flash(f"Neuen {sichtbarkeit.value}en Kommentar hinzugefügt und Status zu \"{neuer_status.value}\" gewechselt.")
            
            # nur Status ändern
            else:
                db.session.commit() # in Datenbank schreiben
                flash(f"Status ohne Kommentar zu \"{neuer_status.value}\" gewechselt.")
                
        elif neuer_status == meldung.status: # Status nicht ändern
            
            # Nur Kommentieren
            if kommentar_text.strip():
                db.session.add(current_user.add_kommentar(meldung, kommentar_text.strip(), sichtbarkeit))
                db.session.commit()
                flash(f"Neuen {sichtbarkeit.value}en Kommentar ohne Statuswechsel hinzugefügt.")
            else:
                flash("Status nicht gewechselt.")
        
        else:
            flash(f"Statuswechsel von \"{meldung.status.value}\" zu \"{neuer_status.value}\" ist nicht erlaubt.")
    
    # Error von add_kommentar (Lehrende)
    except PermissionError as e:
        flash(f"{e}")
        
    # zurück zur Detailansicht
    return redirect(url_for("meldung_anzeigen", meldungs_id = meldungs_id))
    
@app.route("/meldung/neu", methods=["GET", "POST"]) # CREATE-Operation (C in CRUD)
@login_required
def meldung_erstellen():
    if request.method == "POST":
        
        # holen von Werten aus HTML-Formular
        modul_titel = request.form.get("modul")
        kategorie_name = request.form.get("kategorie")
        beschreibung = request.form.get("beschreibung")

        # Modul und Kategorie aus Enum (oder Datenbank) holen
        modul = db.session.query(Modul).filter_by(titel=modul_titel).first() # direkte SQL-Abfrage
        kategorie = Kategorie[kategorie_name]
        
        try:
            # neue Meldung erzeugen (wird in erstelle_meldung in Datenbank geschrieben)
            current_user.erstelle_meldung(beschreibung, kategorie, modul)
            flash(" Meldung erfolgreich erstellt. ")
            return redirect(url_for("uebersicht"))
        
        except Exception as e:
            flash(f"Fehler beim Erstellen der Meldung: {e}")
            
            # Rückgabe bei Fehler
            return render_template("meldung_formular.html",
                                    module = db.session.query(Modul).all(),
                                    kategorie_enum = Kategorie,
                                    beschreibung = beschreibung,
                                    selected_modul = modul_titel,
                                    selected_kategorie = kategorie_name
                                    )
        
    return render_template("meldung_formular.html",
                           module = db.session.query(Modul).all(),
                           kategorie_enum = Kategorie
                           )
    
@app.route("/nutzerverwaltung", methods=["GET", "POST"])
@login_required
def nutzer_verwalten():
    if not isinstance(current_user, Admin):
        return redirect(url_for("uebersicht"))
    
    alle_nutzer = current_user.get_alle_benutzer()
    alle_module = Modul.query.all()
    
    return render_template("nutzerverwaltung.html",
                           user = current_user,
                           benutzer_liste = alle_nutzer,
                           module = alle_module
                           )

@app.route("/benutzer_erstellen", methods=["GET"])
@login_required
def benutzer_erstellen():
    if not isinstance(current_user, Admin):
        return redirect(url_for("uebersicht"))
    return render_template("benutzer_erstellen.html", 
                           user=current_user, 
                           rolle_enum = Benutzer_rolle
                           )

@app.route("/benutzer_speichern", methods=["POST"])
@login_required
def benutzer_speichern():
    if not isinstance(current_user, Admin):
        return redirect(url_for("uebersicht"))

    name = request.form.get("name")
    email = request.form.get("email")
    rolle = request.form.get("rolle")
    rolle_enum = Benutzer_rolle[rolle]
    passwort = request.form.get("passwort")

    # prüfen ob E-Mail bereits existiert
    if db.session.query(Benutzer).filter_by(email=email).first(): # direkte SQL-Abfrage
        flash("Benutzer mit dieser Email existiert bereits.")
        return redirect(url_for("benutzer_erstellen"))

    if not passwort or len(passwort) < 6:
        flash("Passwort muss mindestens 6 Zeichen lang sein.")
        return redirect(url_for("benutzer_erstellen"))

    # Mapping von Enum → Klassenobjekt (in models/rollen_liste.py)
    neue_rolle_klasse = get_rolle_klasse(rolle_enum)
    if neue_rolle_klasse:
        neuer_benutzer = neue_rolle_klasse(name, email, passwort)
        db.session.add(neuer_benutzer)
        db.session.commit()
        flash(f"Benutzer {name} als {rolle_enum.value} hinzugefügt.")
    else:
        flash("Benutzer hinzufügen fehlgeschlagen.")

    return redirect(url_for("nutzer_verwalten"))

@app.route("/benutzer_loeschen", methods=["POST"])
@login_required
def benutzer_loeschen():
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))

    benutzer_id = int(request.form.get("benutzer_id"))
    benutzer = db.session.query(Benutzer).get(benutzer_id)

    if benutzer:
        if isinstance(benutzer, Admin):
            anzahl_admins = Admin.query.count()
            if anzahl_admins <= 1:    
                flash("Mindestens ein Admin muss erhalten bleiben.")
                return redirect(url_for("nutzer_verwalten"))
            elif(benutzer.id == current_user.id):
                flash("Nicht erlaubt, sich selbst zu löschen!")
                return redirect(url_for("nutzer_verwalten")) 
            else:
                db.session.delete(benutzer)
                db.session.commit()
                flash(f"Benutzer {benutzer.name} gelöscht.")
        else:            
            db.session.delete(benutzer)
            db.session.commit()
            flash(f"Benutzer {benutzer.name} gelöscht.")
    else:
        flash("Benutzer nicht gefunden.")

    return redirect(url_for("nutzer_verwalten"))

@app.route("/module_verwalten", methods=["GET", "POST"])
@login_required
def module_verwalten():
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))
    
    # Modul erstellen
    if request.method == "POST":    
        titel = request.form.get("titel")
        try:
            current_user.erstelle_modul(titel=titel)
            flash(f"Modul \"{titel}\" wurde erfolgreich erstellt.")
        except ValueError as e:
            flash(f"Fehler: {e}")    
        
    alle_module = Modul.query.all()
    return render_template("module_verwalten.html", module=alle_module)

@app.route("/modul_loeschen", methods=["POST"])
@login_required
def modul_loeschen():
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))
    
    modul_id = int(request.form.get("modul_id"))
    modul = Modul.query.get(modul_id)
    
    if modul:
        db.session.delete(modul)
        db.session.commit()
        flash(f"Modul \"{modul.titel}\" gelöscht")
    else:
        flash("Modul nicht gefunden.")
        
    return redirect(url_for("module_verwalten"))

@app.route("/modul_aktion", methods=["POST"])
@login_required
def modul_aktion():
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))

    modul_id_raw = request.form.get("modul_id")
    
    # Prüfen ob Module vorhanden sind
    if not modul_id_raw:
        flash ("Bitte zuerst Module anlegen.")
        return redirect(url_for("nutzer_verwalten"))
    
    lehrende_id = int(request.form.get("lehrende_id"))
    modul_id = int(modul_id_raw)
    aktion = request.form.get("aktion")

    lehrende = Lehrende.query.get(lehrende_id)
    modul = Modul.query.get(modul_id)

    if not lehrende or not modul:
        flash("Lehrende oder Modul nicht gefunden.")
        return redirect(url_for("nutzer_verwalten"))

    if aktion == "zuweisen":
        if current_user.modul_zuweisen(modul, lehrende):
            flash(f"Modul \"{modul.titel}\" wurde \"{lehrende.name}\" zugewiesen.")
        else:
            flash("Modul bereits zugewiesen.")
    elif aktion == "entziehen":
        if current_user.modul_entziehen(modul, lehrende):
            flash(f"Modul \"{modul.titel}\" wurde \"{lehrende.name}\" entzogen.")
        else:
            flash("Modul war nicht zugewiesen.")
    else:
        flash("Ungültige Aktion.")

    return redirect(url_for("nutzer_verwalten"))

@app.route("/antwort_speichern/<int:kommentar_id>", methods=["POST"])
@login_required
def antwort_speichern(kommentar_id):
    kommentar = Kommentar.query.get_or_404(kommentar_id)

    if not isinstance(current_user, Studierende) or current_user.id != kommentar.meldung.ersteller.id:
        flash("Nur Melder darf  antworten.")
        return redirect(url_for("meldung_anzeigen", meldungs_id=kommentar.meldung.id))

    antwort_text = request.form.get("antwort_text", "").strip()
    if not antwort_text:
        flash("Antwort darf nicht leer sein.")
        return redirect(url_for("meldung_anzeigen", meldungs_id=kommentar.meldung.id))

    antwort = Kommentar(
        text=antwort_text,
        meldung=kommentar.meldung,
        sichtbarkeit=Sichtbarkeit.PRIVAT,
        verfasser=current_user.name,
        antwort_auf=kommentar
    )
    db.session.add(antwort)
    db.session.commit()
    flash("Antwort gespeichert.")
    return redirect(url_for("meldung_anzeigen", meldungs_id=kommentar.meldung.id))

if __name__ == "__main__":
    app.run(debug=True)
