'''
Controller-Modul der Flask-App.
- Initialisiert Datenbank und Login-Manager
- Definiert Setup-Routen für DB und Admin
- Enthält zentrale @app.route-Definitionen
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify # für Nachricht bei Route /setup-admin
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect
from models.datenbank import db #  -> SQLAlchemy()
from models.meldung import Meldung
from models.enums import Kategorie, Status, Sichtbarkeit, Benutzer_rolle
from models.benutzer import Benutzer
from models.admin import Admin
from models.studierende import Studierende
from models.lehrende import Lehrende
from models.modul import Modul
from models.rollen_liste import get_rolle_klasse
from models.kommentar import Kommentar


# ===================== App-Konfiguration =====================
app = Flask(__name__)

if os.getenv("RENDER") == "true":
    DB_URL = os.getenv("DATABASE_URL") # Render-DB (Produktivumgebung)
else:
    DB_URL = "sqlite:///kmsystem.db" # -> lokale installation: SQLite

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print("Datenbank-URL:", DB_URL) # Debug-Ausgabe

app.secret_key = "irgendein_geheimer_schlüssel_123" # sollte in .env liegen

db.init_app(app)


# ===================== Login Manager =====================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    '''
    Lädt den Benutzer beim Login.
    SQLAlchemy erkennt automatisch die richtige Unterklasse (Admin, Studierende, Lehrende).
    '''
    #return Benutzer.query.get(int(user_id))
    return db.session.get(Benutzer, int(user_id))


# ===================== Setup-Routen =====================
@app.route("/setup-db")
def setup_db():
    '''
    Initialisiert die Datenbank.
    Ruft init_db() auf und gibt eine JSON-Bestätigung zurück.
    '''
    inspector = inspect(db.engine)
    if not inspector.get_table_names():
        from init_db import init_db
        init_db()
        return jsonify({"status": "Datenbank wurde initialisiert."})
    return jsonify({"status": "Datenbank bereits initialisiert."})


#####################################################################
@app.route("/del-db")
def del_db():
    '''
    Löscht Datenbank.
    Ruft delete_db() auf und gibt eine JSON-Bestätigung zurück.
    Nur für Entwicklungszwecke genutzt, im finalen System nicht vorgesehen!
    '''
    inspector = inspect(db.engine)
    if inspector.get_table_names():
        from init_db import delete_db
        delete_db()
        return jsonify({"status": "Datenbank wurde geloescht."})
    return jsonify({"status": "Datenbank nicht vorhanden."})
#####################################################################

# Controller: @app.route(...) reagiert auf HTTP-Anfragen:
@app.route("/setup-admin")
def setup_admin():
    '''
    Erstellt einen Admin und Benutzer, falls noch keiner existiert.
    - Einmalig über "App-URL/setup-admin" aufrufen.
    - Login-Daten sollten in einer .env-Datei liegen,
      sind hier aber für lokale Installation hardcodiert.
    '''
    inspector = inspect(db.engine)
    if not inspector.get_table_names():
        setup_db()

    if not Admin.query.filter_by(email="admin@example.org").first():
        admin = Admin("Admin", "admin@example.org", "admin123")
        student1 = Studierende("Student 1", "s1@example.org", "123456")
        student2 = Studierende("Student 2", "s2@example.org", "123456")
        lehrende1 = Lehrende("Tutor 1", "l1@example.org", "123456")
        lehrende2 = Lehrende("Tutor 2","l2@example.org", "123456")
        modul = Modul("Testmodul")

        db.session.add_all([admin, student1, student2, lehrende1, lehrende2, modul])
        
        #db.session.add_all([admin, student1, student2, lehrende1, lehrende2, modul])
        db.session.commit()
        return jsonify({"status": "Admin und Benutzer erstellt."})

    return jsonify({"status": "Admin und Benutzer existieren bereits. Login unter http://127.0.0.1:5000/"})

@app.route("/fuenf")
def fuenf():
    student3 = Studierende("Student 3", "s3@example.org", "123456")
    student4 = Studierende("Student 4", "s4@example.org", "123456")
    student5 = Studierende("Student 5", "s5@example.org", "123456")
    student6 = Studierende("Student 6", "s6@example.org", "123456")
    student7 = Studierende("Student 7", "s7@example.org", "123456")
    student8 = Studierende("Student 8", "s8@example.org", "123456")
    student9 = Studierende("Student 9", "s9@example.org", "123456")
    student10 = Studierende("Student 10", "s10@example.org", "123456")
    student11 = Studierende("Student 11", "s11@example.org", "123456")
    student12 = Studierende("Student 12", "s12@example.org", "123456")
    student13 = Studierende("Student 13", "s13@example.org", "123456")
    student14 = Studierende("Student 14", "s14@example.org", "123456")
    student15 = Studierende("Student 15", "s15@example.org", "123456")
    student16 = Studierende("Student 16", "s16@example.org", "123456")
    student17 = Studierende("Student 17", "s17@example.org", "123456")
    student18 = Studierende("Student 18", "s18@example.org", "123456")
    student19 = Studierende("Student 19", "s19@example.org", "123456")
    student20 = Studierende("Student 20", "s20@example.org", "123456")
    student21 = Studierende("Student 21", "s21@example.org", "123456")
    student22 = Studierende("Student 22", "s22@example.org", "123456")
    student23 = Studierende("Student 23", "s23@example.org", "123456")
    student24 = Studierende("Student 24", "s24@example.org", "123456")
    student25 = Studierende("Student 25", "s25@example.org", "123456")
    student26 = Studierende("Student 26", "s26@example.org", "123456")
    student27 = Studierende("Student 27", "s27@example.org", "123456")
    student28 = Studierende("Student 28", "s28@example.org", "123456")
    student29 = Studierende("Student 29", "s29@example.org", "123456")
    student30 = Studierende("Student 30", "s30@example.org", "123456")
    student31 = Studierende("Student 31", "s31@example.org", "123456")
    student32 = Studierende("Student 32", "s32@example.org", "123456")
    student33 = Studierende("Student 33", "s33@example.org", "123456")
    student34 = Studierende("Student 34", "s34@example.org", "123456")
    student35 = Studierende("Student 35", "s35@example.org", "123456")
    student36 = Studierende("Student 36", "s36@example.org", "123456")
    student37 = Studierende("Student 37", "s37@example.org", "123456")
    student38 = Studierende("Student 38", "s38@example.org", "123456")
    student39 = Studierende("Student 39", "s39@example.org", "123456")
    student40 = Studierende("Student 40", "s40@example.org", "123456")
    student41 = Studierende("Student 41", "s41@example.org", "123456")
    student42 = Studierende("Student 42", "s42@example.org", "123456")
    student43 = Studierende("Student 43", "s43@example.org", "123456")
    student44 = Studierende("Student 44", "s44@example.org", "123456")
    student45 = Studierende("Student 45", "s45@example.org", "123456")
    student46 = Studierende("Student 46", "s46@example.org", "123456")
    student47 = Studierende("Student 47", "s47@example.org", "123456")
    student48 = Studierende("Student 48", "s48@example.org", "123456")
    student49 = Studierende("Student 49", "s49@example.org", "123456")
    student50 = Studierende("Student 50", "s50@example.org", "123456")

    db.session.add_all([student3, student4, student5, student6, student7, student8, student9, student10, student11, student12])
    db.session.commit()
    db.session.add_all([student13, student14, student15, student16, student17, student18, student19, student20, student21, student22])
    db.session.commit()
    db.session.add_all([student23, student24, student25, student26, student27, student28, student29, student30, student31, student32])
    db.session.commit()
    db.session.add_all([student33, student34, student35, student36, student37, student38, student39, student40, student41, student42, student43])
    db.session.commit()
    db.session.add_all([student44, student45, student46, student47, student48, student49, student50])
    db.session.commit()
    return jsonify({"status": "50 Studis mit 123456 erstellt."})
    
# ===================== Index- und Login-Routen =====================
@app.route("/")
def index():
    '''
    Startseite: leitet direkt zur Login-Seite weiter.
    '''
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Login-Routine:
    - Benutzer wird anhand der E-Mail aus der Datenbank gesucht.
    - Passwort wird mit check_passwort() geprüft.
    - Bei Erfolg: Weiterleitung zur Übersichtsseite.
    - Bei Misserfolg: Fehlermeldung über Flash.
    '''
    if not inspect(db.engine).get_table_names():
        return jsonify({"status": "Datenbankfehler, bitte wenden Sie sich an den Administrator."})
    else:
        if request.method == "POST":
            email = request.form["email"]
            passwort = request.form["passwort"]

            # Direkte SQL-Abfrage nach Benutzer
            user = Benutzer.query.filter_by(email=email).first()

            if user and user.check_passwort(passwort):
                login_user(user)
                flash(f"Login erfolgreich als {user.type}.")
                return redirect(url_for("uebersicht"))

            flash("Login fehlgeschlagen")

        return render_template("login.html")


# ===================== Logout =====================
@app.route("/logout")
def logout():
    '''
    Logout-Routine:
    - Meldet den aktuellen Benutzer ab.
    - Gibt eine Flash-Meldung aus.
    - Leitet zurück zur Login-Seite.
    '''
    logout_user()
    flash("Erfolgreich ausgeloggt.")
    return redirect(url_for("login"))


# ===================== Übersicht =====================
@app.route("/uebersicht")
@login_required
def uebersicht():
    '''
    Übersichtsseite:
    - Zeigt Meldungen abhängig von Benutzerrolle (Studierende, Lehrende, Admin).
    - Unterstützt Filterung nach Modul, Status und Kategorie.
    - Parameter werden aus GET-Request übernommen.
    '''
    # Parameter aus Filter-Anfrage:
    alle_meldungen = request.args.get("alle_meldungen") == "true"
    selected_modul = request.args.get("modul") or None # Werte aus HTML-Formular holen
    selected_status = request.args.get("status") or None
    selected_kategorie = request.args.get("kategorie") or None

    # Initialisierung
    module = []
    meldungen = []

    # Rollenabhängige Logik
    if isinstance(current_user, Studierende):
        module = db.session.query(Modul).all()
        meldungen = db.session.query(Meldung).all() if alle_meldungen else current_user.meldungen

    elif isinstance(current_user, Lehrende):
        module = db.session.query(Modul).all() if alle_meldungen else current_user.module
        meldungen = db.session.query(
            Meldung
        ).all() if alle_meldungen else current_user.get_eigene_meldungen()

    elif isinstance(current_user, Admin):
        module = db.session.query(Modul).all()
        meldungen = current_user.get_alle_meldungen()

    # Filter anwenden
    if selected_modul:
        meldungen = [m for m in meldungen if m.modul.titel == selected_modul]
    if selected_status:
        meldungen = [m for m in meldungen if m.status.name == selected_status]
    if selected_kategorie:
        meldungen = [m for m in meldungen if m.kategorie.name == selected_kategorie]

    # Keine Meldungen vorhanden
    if not meldungen:
        flash("Keine Meldungen vorhanden.")

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


# ===================== Meldung anzeigen =====================
@app.route("/meldung/<int:meldungs_id>")
@login_required
def meldung_anzeigen(meldungs_id):
    '''
    Detailansicht einer Meldung (Read-Operation in CRUD):
    - Holt Meldung per SQL-Abfrage anhand ID.
    - Rendert Detailtemplate mit Status- und Sichtbarkeits-Enums.
    '''
    meldung = Meldung.query.filter_by(id=meldungs_id).first()
    if not meldung:
        flash("Das ist nicht erlaubt.")
        return redirect("/uebersicht")

    return render_template("meldung_detail.html",
        meldung=meldung,
        user=current_user,
        status_enum = Status,
        sichtbarkeit_enum = Sichtbarkeit
    )


# ===================== Status ändern =====================
@app.route("/meldung/<int:meldungs_id>/status_aendern", methods=["POST"])
@login_required
def status_aendern(meldungs_id:int):
    '''
    Update-Operation des Meldungsstatus (Update in CRUD):
    - Holt Status, Kommentar und Sichtbarkeit aus Formular.
    - Prüft erlaubte Statuswechsel.
    - Fügt optional Kommentar hinzu.
    - Nur für Lehrende, und nur für Meldungen eigener Module.
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
        if isinstance(current_user, Lehrende):
            if meldung.modul not in current_user.module:
                raise PermissionError("Dies ist nur für Meldungen eigener Module möglich.")
        else:
            raise PermissionError("Nur Lehrende dürfen den Status ändern.")

        # Statuswechsel mit optionalem Kommentar
        if neuer_status in erlaubte_wechsel[meldung.status]:
            meldung.status = neuer_status

            if kommentar_text.strip():
                db.session.add(current_user.add_kommentar(
                    meldung,
                    kommentar_text.strip(),
                    sichtbarkeit
                    )
                )
                db.session.commit()
                flash(f"Neuen {sichtbarkeit.value}en Kommentar hinzugefügt und Status zu \"{neuer_status.value}\" gewechselt.")
            else:
                db.session.commit() # in Datenbank schreiben
                flash(f"Status ohne Kommentar zu \"{neuer_status.value}\" gewechselt.")

        elif neuer_status == meldung.status:
            # Nur Kommentieren
            if kommentar_text.strip():
                db.session.add(current_user.add_kommentar(
                    meldung,
                    kommentar_text.strip(),
                    sichtbarkeit
                    )
                )
                db.session.commit()
                flash(f"Neuen {sichtbarkeit.value}en Kommentar ohne Statuswechsel hinzugefügt.")
            else:
                flash("Status nicht gewechselt.")
        else:
            flash(f"Statuswechsel von \"{meldung.status.value}\" zu \"{neuer_status.value}\" ist nicht erlaubt.")

    except PermissionError as e:
        flash(str(e))

    return redirect(url_for("meldung_anzeigen", meldungs_id = meldungs_id))


# ===================== Meldung erstellen =====================
@app.route("/meldung/neu", methods=["GET", "POST"])
@login_required
def meldung_erstellen():
    '''
    CREATE-Operation (C in CRUD):
    - Erstellt eine neue Meldung zu einem Modul.
    - Holt Werte aus Formular (Modul, Kategorie, Beschreibung).
    - Speichert Meldung über current_user.erstelle_meldung().
    - Bei Fehler: Formular mit Fehlermeldung erneut anzeigen.
    '''
    if request.method == "POST":
        modul_titel = request.form.get("modul")
        kategorie_name = request.form.get("kategorie")
        beschreibung = request.form.get("beschreibung", type=str)

        modul = db.session.query(Modul).filter_by(titel=modul_titel).first() # SQL-Abfrage
        kategorie = Kategorie[kategorie_name]

        try:
            current_user.erstelle_meldung(beschreibung, kategorie, modul)
            flash(" Meldung erfolgreich erstellt. ")
            return redirect(url_for("uebersicht"))

        except IntegrityError:
            db.session.rollback()
            flash("Fehler: Meldung konnte nicht gespeichert werden.")

        except Exception as e:
            flash(f"Unerwarteter Fehler: {e}")

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


# ===================== Nutzerverwaltung =====================
@app.route("/nutzerverwaltung", methods=["GET", "POST"])
@login_required
def nutzer_verwalten():
    '''
    Admin-Funktion:
    - Zeigt Übersicht aller Benutzer und Module.
    - Nur für Admins zugänglich.
    '''
    if not isinstance(current_user, Admin):
        return redirect(url_for("uebersicht"))

    alle_nutzer = current_user.get_alle_benutzer()
    alle_module = Modul.query.all()

    return render_template("nutzerverwaltung.html",
        user = current_user,
        benutzer_liste = alle_nutzer,
        module = alle_module
    )


# ===================== Benutzer erstellen =====================
@app.route("/benutzer_erstellen", methods=["GET"])
@login_required
def benutzer_erstellen():
    '''
    Admin-Funktion:
    - Zeigt Formular zum Erstellen eines neuen Benutzers.
    - Nur für Admins zugänglich.
    '''
    if not isinstance(current_user, Admin):
        return redirect(url_for("uebersicht"))

    return render_template("benutzer_erstellen.html",
        user = current_user,
        rolle_enum = Benutzer_rolle
    )

@app.route("/benutzer_speichern", methods=["POST"])
@login_required
def benutzer_speichern():
    '''
    Admin-Funktion:
    - Speichert neuen Benutzer in der Datenbank.
    - Prüft E-Mail auf Einzigartigkeit.
    - Prüft Passwortlänge.
    - Erstellt Benutzer basierend auf Rolle (Enum → Klasse).
    '''
    if not isinstance(current_user, Admin):
        return redirect(url_for("uebersicht"))

    name = request.form.get("name")
    email = request.form.get("email")
    rolle = request.form.get("rolle")
    rolle_enum = Benutzer_rolle[rolle]
    passwort = request.form.get("passwort")

    # Validierung: E-Mail darf nicht doppelt sein
    if db.session.query(Benutzer).filter_by(email=email).first(): # direkte SQL-Abfrage
        flash("Benutzer mit dieser Email existiert bereits.")
        return redirect(url_for("benutzer_erstellen"))

    # Validierung: Passwort muss mindestens 7 Zeichen haben
    if not passwort or len(passwort) < 7:
        flash("Passwort muss mindestens 7 Zeichen lang sein.")
        return redirect(url_for("benutzer_erstellen"))

    # Mapping von Enum → Klassenobjekt
    neue_rolle_klasse = get_rolle_klasse(rolle_enum)
    if neue_rolle_klasse:
        neuer_benutzer = neue_rolle_klasse(name, email, passwort)
        db.session.add(neuer_benutzer)
        db.session.commit()
        flash(f"Benutzer {name} als {rolle_enum.value} hinzugefügt.")
    else:
        flash("Benutzer hinzufügen fehlgeschlagen.")

    return redirect(url_for("nutzer_verwalten"))


# ===================== Benutzer löschen =====================
@app.route("/benutzer_loeschen", methods=["POST"])
@login_required
def benutzer_loeschen():
    '''
    Admin-Funktion:
    - Löscht einen Benutzer aus der Datenbank.
    - Prüft Sonderfälle:
      * Mindestens ein Admin muss erhalten bleiben.
      * Admin darf sich nicht selbst löschen.
    '''
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))

    benutzer_id = int(request.form.get("benutzer_id"))
    benutzer = db.session.get(Benutzer, benutzer_id)
    #benutzer = db.session.query(Benutzer).get(benutzer_id)

    if benutzer:
        if isinstance(benutzer, Admin):
            anzahl_admins = Admin.query.count()
            if anzahl_admins <= 1:
                flash("Mindestens ein Admin muss erhalten bleiben.")
                return redirect(url_for("nutzer_verwalten"))
            if benutzer.id == current_user.id:
                flash("Nicht erlaubt, sich selbst zu löschen!")
                return redirect(url_for("nutzer_verwalten"))

        db.session.delete(benutzer)
        db.session.commit()
        flash(f"Benutzer {benutzer.name} gelöscht.")
    else:
        flash("Benutzer nicht gefunden.")

    return redirect(url_for("nutzer_verwalten"))


# ===================== Modulverwaltung =====================
@app.route("/module_verwalten", methods=["GET", "POST"])
@login_required
def module_verwalten():
    '''
    Admin-Funktion:
    - Anzeige und Verwaltung von Modulen.
    - Ermöglicht das Erstellen neuer Module.
    '''
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
    '''
    Admin-Funktion:
    - Löscht ein Modul anhand der ID.
    - Gibt Feedback über Flash-Meldungen.
    '''
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))

    modul_id = int(request.form.get("modul_id"))
    modul = db.session.get(Modul, modul_id)
    # modul = Modul.query.get(modul_id)

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
    '''
    Admin-Funktion:
    - Weist Lehrenden Module zu oder entzieht sie.
    - Prüft Eingaben und gibt Feedback über Flash-Meldungen.
    '''
    if not isinstance(current_user, Admin):
        flash("Keine Berechtigung.")
        return redirect(url_for("uebersicht"))

    modul_id_raw = request.form.get("modul_id")

    # Prüfen ob Module vorhanden sind
    if not modul_id_raw:
        if db.session.query(Modul).first() is None:
            flash ("Bitte zuerst Module anlegen.")
        else:
            flash ("Bitte zuerst Modul auswählen.")
        return redirect(url_for("nutzer_verwalten"))

    lehrende_id = int(request.form.get("lehrende_id"))
    modul_id = int(modul_id_raw)
    aktion = request.form.get("aktion")

    lehrende = db.session.get(Lehrende, lehrende_id)
    # lehrende = Lehrende.query.get(lehrende_id)
    modul = db.session.get(Modul, modul_id)
    # modul = Modul.query.get(modul_id)

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


# ===================== Antworten auf Kommentare =====================
@app.route("/antwort_speichern/<int:kommentar_id>", methods=["POST"])
@login_required
def antwort_speichern(kommentar_id):
    '''
    Studierenden-Funktion:
    - Als Melder kann auf Kommentare von Lehrenden geantwortet werden.
    - Antwort wird als Kommentar gespeichert (Sichtbarkeit = privat).
    '''
    kommentar = Kommentar.query.get_or_404(kommentar_id)

    if not isinstance(current_user, Studierende) or current_user.id != kommentar.meldung.ersteller.id:
        flash("Nur Melder darf antworten.")
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


# ===================== App-Start =====================
if __name__ == "__main__":
    app.run(debug=True)
