from flask import Flask, render_template, request
from models.meldung import Meldung
from models.enums import Kategorie, Status
from models.admin import Admin
from models.studierende import Studierende
from models.modul import Modul

app = Flask(__name__)


admin_1 = Admin(1, "Administrator", "admin@example.com")
modul_1 = admin_1.erstelle_modul(1, "Ufologie")
modul_2 = admin_1.erstelle_modul(2, "Kunstgeschichte")


#admin_1.modul_zuweisen()

student_1 = Studierende(1, "Jens Müller", "jmüller@example.com")
student_2 = Studierende(2, "Horst Lichter", "lichter@example.org")

student_1.erstelle_meldung(1, "Hier ist ein großartiger Fehler in Zeile 1!", Kategorie.MUSTERKLAUSUR, modul_1)
student_1.erstelle_meldung(2, "Hier ist ein großartiger Fehler in Zeile 2!", Kategorie.PDFSKRIPT, modul_1)
student_1.erstelle_meldung(3, "Hier ist ein großartiger Fehler in Zeile 3!", Kategorie.FOLIENSÄTZE, modul_1)
student_1.erstelle_meldung(4, "Die Geschichte ist fehlerhaft!", Kategorie.VIDEO, modul_2)
student_2.erstelle_meldung(1, "Meldung 1 von Lichter", Kategorie.ONLINETESTS, modul_1)

#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"

#def index():
#    student_1.erstelle_meldung(1, "Hier ist ein großartiger Fehler in Zeile 1!", Kategorie.MUSTERKLAUSUR, modul_1)
#    student_1.erstelle_meldung(2, "Hier ist ein großartiger Fehler in Zeile 2!", Kategorie.PDFSKRIPT, modul_1)
#    student_1.erstelle_meldung(3, "Hier ist ein großartiger Fehler in Zeile 3!", Kategorie.FOLIENSÄTZE, modul_1)
#    student_1.erstelle_meldung(4, "Die Geschichte ist fehlerhaft!", Kategorie.VIDEO, modul_2) 
#    student_2.erstelle_meldung(1, "Meldung 1 von Lichter", Kategorie.ONLINETESTS, modul_1)
#    return render_template("uebersicht.html", meldungen = student_1.meldungen, melder = student_1) # ruft HTML-Datei aus Verzeichnis "templates" auf
    
@app.route("/uebersicht")
def uebersicht():
    
    # Dummy-Login
    current_user = student_1 
    
    # Meldungen
    alle_meldungen = admin_1.module 
    
    # Parameter aus Filter-Anfrage
    eigene = request.args.get("eigene") == "on"
    selected_modul = request.args.get("modul")
    selected_status = request.args.get("status")    
    selected_kategorie = request.args.get("kategorie")
    
    meldungen = admin_1.get_alle_meldungen() if not eigene else current_user.meldungen
    
    #Filter
    if selected_modul:
        meldungen = [m for m in meldungen if m.modul.titel == selected_modul]
    if selected_status:
        meldungen = [m for m in meldungen if m.status.name == selected_status]
    if selected_kategorie:
        meldungen = [m for m in meldungen if m.kategorie.name == selected_kategorie]
    
    return render_template("uebersicht.html",
        melder = current_user.name,
        meldungen = meldungen,
        eigene = eigene,
        module = admin_1.module,
        status_enum = Status,
        kategorie_enum = Kategorie, 
        selected_modul = selected_modul,
        selected_status = selected_status,
        selected_kategorie = selected_kategorie
    )

if __name__ == "__main__":
    app.run(debug=True)
