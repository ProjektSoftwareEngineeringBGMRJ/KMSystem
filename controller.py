from flask import Flask, render_template, request, redirect, url_for, flash # insall
from flask_migrate import Migrate
from models.datenbank import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from models.meldung import Meldung
from models.enums import Kategorie, Status, Sichtbarkeit, Benutzer_rolle
from models.benutzer import Benutzer
from models.admin import Admin
from models.studierende import Studierende
from models.lehrende import Lehrende
from models.modul import Modul
from models.rollen_liste import get_rolle_klasse
from models.kommentar import Kommentar

import os

app = Flask(__name__)
print(type(app))

# import os
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") # Render: PostgreSQL

# Lokale Fallback-URL, falls DATABASE_URL nicht gesetzt ist
db_url = os.getenv("DATABASE_URL", "sqlite:///kmsystem.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kmsystem.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# aus .env-Datei oder Umgebungsvariablen laden
app.secret_key = "irgendein_geheimer_schlüssel_123" 

db.init_app(app)

migrate = Migrate(app, db)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



@login_manager.user_loader
def load_user(user_id):
    return Benutzer.query.get(int(user_id)) # SQLAlchemy lädt richtige Subklasse (Vererbung)

# Dummy Daten (einmal ausführen):
with app.app_context():
#     #db.drop_all()
    db.create_all()

#     if not Admin.query.first():
#         admin = Admin(name="Administrator", email="admin@example.com", passwort="admin123")
#         student_1 = Studierende(name="Jens Müller", email="jmueller@example.com", passwort="pw1")
#         student_2 = Studierende(name="Horst Lichter", email="lichter@example.org", passwort="pw2")
#         prof_1 = Lehrende(name="Dr. Motte", email="motte@example.org", passwort="pw3")

#         db.session.add_all([admin, student_1, student_2, prof_1])
#         db.session.commit()

#         modul_1 = admin.erstelle_modul("Ufologie")
#         modul_2 = admin.erstelle_modul("Kunstgeschichte")
#         admin.modul_zuweisen(modul_1, prof_1)

#         student_1.erstelle_meldung("Fehler in Zeile 1", Kategorie.MUSTERKLAUSUR, modul_1)
#         student_1.erstelle_meldung("Fehler in Zeile 2", Kategorie.PDFSKRIPT, modul_1)
#         student_1.erstelle_meldung("Fehler in Zeile 3", Kategorie.FOLIENSÄTZE, modul_1)
#         student_1.erstelle_meldung("Fehler in Geschichte", Kategorie.VIDEO, modul_2)
#         student_2.erstelle_meldung("Meldung von Lichter", Kategorie.ONLINETESTS, modul_1)

#         db.session.commit()

# Dummy User für Tests:
# @app.before_request
# def setze_dummy_user():
#     global current_user
    
#     #current_user = Lehrende.query.first()
    
#     #current_user = Lehrende.query.filter_by(name="Prof1").first()
    
#     #current_user = Studierende.query.first()
#     #current_user = Studierende.query.filter_by(name="Studi1").first()
    
#     current_user = Admin.query.first()  # später: Session-basiert


# Controller: @app.route(...) reagiert auf HTTP-Anfragen: 

# bei Aufruf von https://kmsystem.onrender.com/ zu login weiterleiten
@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        passwort = request.form["passwort"]
        user = Benutzer.query.filter_by(email=email).first()
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
@app.route("/uebersicht") # GET-Anfrage <form method="get" action="/uebersicht">
@login_required
def uebersicht():
    
    # für Session-Login
    #if not current_user:
    #    flash("Kein Benutzer eingeloggt.")
    #    return redirect(url_for("login"))

    # Parameter aus Filter-Anfrage: 
    # holen von Werten aus HTML-Formular (z.B. aus Feld name="modul")
    alle_meldungen = request.args.get("alle_meldungen") == "true" # anfangs eigene Meldungen zeigen
    selected_modul = request.args.get("modul") or None 
    selected_status = request.args.get("status") or None    
    selected_kategorie = request.args.get("kategorie") or None
    
    # abhängig von Button ""
    if isinstance(current_user, Studierende):
        # List mit allen Modulen
        module = db.session.query(Modul).all()
        # alle_meldungen flase: nur eigene zeigen 
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
    # später Datenbank
    # admin.get_alle_meldungen() -> list[Meldung]:
    meldung = next((m for m in db.session.query(Meldung).all() if m.id == meldungs_id), None)
    
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
    
    meldung = next((m for m in db.session.query(Meldung).all() if m.id == meldungs_id), None)
    if not meldung:
        return redirect(url_for("uebersicht"))
    
    neuer_status_name = request.form.get("status") # holt Wert aus Formular
    kommentar_text = request.form.get("kommentar")
    sichtbarkeit_name = request.form.get("sichtbarkeit")
    sichtbarkeit = Sichtbarkeit[sichtbarkeit_name]
    
            
    neuer_status = Status[neuer_status_name]
    erlaubte_wechsel = {
        Status.OFFEN: [Status.BEARBEITUNG],
        Status.BEARBEITUNG: [Status.GESCHLOSSEN],
        Status.GESCHLOSSEN: []
    }
    
    try:
        if meldung.modul not in current_user.module:
            raise PermissionError("Dies ist nur für eigene Module möglich.")
        else:
            # Statuswechsel: offen -> in Bearbeitung -> abgeschlossen
            if neuer_status in erlaubte_wechsel[meldung.status]:
                meldung.status = neuer_status # Setter von Meldung nutzen
                
                # Status ändern und kommentieren
                if kommentar_text.strip():
                    current_user.add_kommentar(meldung, kommentar_text.strip(), sichtbarkeit)
                    flash(f"Neuen {sichtbarkeit.value}en Kommentar hinzugefügt und Status zu \"{neuer_status.value}\" gewechselt.")
            
                # nur Status ändern
                else:
                    flash(f"Status ohne Kommentar zu \"{neuer_status.value}\" gewechselt.")
            
            # Status nicht ändern
            elif neuer_status == meldung.status:
            
                # Nur Kommentieren
                if kommentar_text.strip():
                    current_user.add_kommentar(meldung, kommentar_text.strip(), sichtbarkeit)
                    flash(f"Neuen {sichtbarkeit.value}en Kommentar ohne Statuswechsel hinzugefügt.")
                
                else: 
                    flash("Status nicht gewechselt.")
                #return redirect(url_for("meldung_anzeigen", meldungs_id = meldungs_id))
            
            else:
                flash(f"Statuswechsel von \"{meldung.status.value}\" zu \"{neuer_status.value}\" ist nicht erlaubt.")
    
    # von add_kommentar (Lehrende)
    except PermissionError as e:
        flash(f"{e}")
        
    # erzeugt URL
    return redirect(url_for("meldung_anzeigen", meldungs_id = meldungs_id))
    
@app.route("/meldung/neu", methods=["GET", "POST"])
@login_required
def meldung_erstellen():
    if request.method == "POST":
        # holen von Werten aus HTML-Formular
        modul_titel = request.form.get("modul")
        kategorie_name = request.form.get("kategorie")
        beschreibung = request.form.get("beschreibung")

        # Modul und Kategorie aus Enum (oder Datenbank) holen
        #modul = next((m for m in db.session.query(Modul).all() if m.titel == modul_titel), None)
        modul = db.session.query(Modul).filter_by(titel=modul_titel).first()
        kategorie = Kategorie[kategorie_name]
        
        #meldungs_id = len(admin.get_alle_meldungen()) + 1
        
        try:
            #neue_meldung = 
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
    return render_template("benutzer_erstellen.html", user=current_user)

@app.route("/benutzer_speichern", methods=["POST"])
@login_required
def benutzer_speichern():
    if not isinstance(current_user, Admin):
        return redirect(url_for("uebersicht"))

    name = request.form.get("name")
    email = request.form.get("email")
    rolle = request.form.get("rolle")
    rolle_enum = Benutzer_rolle(rolle)
    passwort = request.form.get("passwort")

    # prüfen ob E-Mail schon existiert
    if db.session.query(Benutzer).filter_by(email=email).first():
        flash("Benutzer mit dieser Email existiert bereits.")
        return redirect(url_for("benutzer_erstellen"))

    if not passwort or len(passwort) < 6:
        flash("Passwort muss mindestens 6 Zeichen lang sein.")
        return redirect(url_for("benutzer_erstellen"))

    neue_rolle_klasse = get_rolle_klasse(rolle_enum)
    if neue_rolle_klasse:
        neuer_benutzer = neue_rolle_klasse(name, email, passwort)
        #current_user.get_alle_benutzer().append(neuer_benutzer)
        db.session.add(neuer_benutzer)
        db.session.commit()
        flash(f"Benutzer {name} als {rolle} hinzugefügt.")

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
        if isinstance(benutzer, Admin): # ??? vielleicht nur wenn dann kein Admin mehr da ist?
            anzahl_admins = Admin.query.count()
            if anzahl_admins <= 1:    
                flash("Mindestens ein Admin muss erhalten bleiben.")
                return redirect(url_for("nutzer_verwalten"))
        else:
            # Alle Meldungen und Kommentare des Benutzers löschen
            #for meldung in benutzer.meldungen:
            #    db.session.delete(meldung)
            #
            #for kommentar in benutzer.kommentare:
            #    db.session.delete(kommentar)
            
            # Benutzer löschen
            db.session.delete(benutzer)
            db.session.commit()
            
            flash(f"Benutzer {benutzer.name} gelöscht.")
    else:
        flash("Benutzer nicht gefunden.")

    return redirect(url_for("nutzer_verwalten"))


    # Alle Meldungen und Kommentare des Benutzers löschen
    #for meldung in benutzer.meldungen:
    #    db.session.delete(meldung)
    #
    #for kommentar in benutzer.kommentare:
    #    db.session.delete(kommentar)
    #
    #db.session.delete(benutzer)
    #db.session.commit()
    #
    # in Benutzer-Modell müssen dafür Backrefs definiert sein: 
    #meldungen = db.relationship("Meldung", backref="ersteller", cascade="all, delete-orphan")
    #kommentare = db.relationship("Kommentar", backref="autor", cascade="all, delete-orphan")

@app.route("/module_verwalten", methods=["GET", "POST"])
@login_required
def module_verwalten():
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))
    
    from models.modul import Modul
    
    if request.method == "POST":
        # Modul erstellen
        titel = request.form.get("titel")
        # evtl. weitere (z.B. beschreibung)...
        
        #neues_modul = Modul(titel=titel)
        #db.session.add(neues_modul)
        #db.session.commit()
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

    lehrende_id = int(request.form.get("lehrende_id"))
    modul_id = int(request.form.get("modul_id"))
    aktion = request.form.get("aktion")

    lehrende = Lehrende.query.get(lehrende_id)
    modul = Modul.query.get(modul_id)

    if not lehrende or not modul:
        flash("Lehrende oder Modul nicht gefunden.")
        return redirect(url_for("nutzer_verwalten"))

    try:
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
    except ValueError as e:
        flash(f"{e}")

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
