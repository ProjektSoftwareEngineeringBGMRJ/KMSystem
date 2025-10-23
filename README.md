# Korrekturmanagementsystem (KMSystem)

Ein webbasiertes System zum Melden von Fehlern, Verbesserungsvorschlägen und Ergänzungen zu Lerninhalten im akademischen Kontext.

## Technologien
- **Python 3.13.1**
- **Flask** – Webframework
- **SQLAlchemy** – ORM für Datenbankmodellierung
- **Jinja2** – Template-Engine
- **VS Code** – Entwicklungsumgebung
- **GitHub** – Versionskontrolle
- **Render** – Deployment-Plattform

## Projektstruktur
```plaintext
KMSystem/
├── instance/                # SQLite-Datenbank
|   └── kmsyststem.db
├── models/                  # alle SQLAlchemy-Datenmodelle
│   ├── __init__.py          # definiert Verzeichnis als Python-Paket  
│   ├── benutzer.py          # 
|   ├── admin.py             # 
|   ├── lehrende.py          # 
|   ├── studierende.py       # 
|   ├── meldung.py           # 
│   ├── kommentar.py         # 
│   ├── modul.py             # 
│   └── enums.py             # 
├── templates/               # Jinja2-HTML-Dateien für Benutzeroberfläche
│   ├── benutzer_erstellen.html
|   ├── login.html
|   ├── meldung_detail.html
|   ├── meldung_formular.html
|   ├── module_verwalten.html
|   ├── nutzerverwaltung.html
│   └── uebersicht.html
├── (static/             # CSS, JS, Bilder - optional)
├── controller.py        # Flask-Routen und Logik
├── Procfile             # Für Deployment auf Render
├── README.md            # Projektdokumentation
├── requirements.txt     # alle Abhängigkeiten
└── setup_admin.py       # Initialisierung der Datenbank und eines Admins
```
Die Projektstruktur von `KMSystem` ist modular und übersichtlich aufgebaut. 
Die Datenmodelle befinden sich im Ordner `models/`, die Templates im Ordner `templates/`, und die zentrale Logik in `controller.py`. 
Die Datenbank wird im Ordner `instance/` gespeichert. 
Ein separates Skript `setup_admin.py` dient zur Initialisierung eines ersten Admin-Benutzers. 
Die `requirements.txt` enthält alle notwendigen Abhängigkeiten, und ein `Procfile` ermöglicht das Deployment auf Plattformen wie Render.

Die Datenbank wird direkt über `db.create_all()` aus den SQLAlchemy-Modellen erzeugt. 
Es wird kein Migrationsframework verwendet.


## Rollen und Zugriff
| Rolle	| Zugriff auf Meldungen | Zusatzfunktionen |
| ----- | --------------------- | ---------------- |
| Studierende | Eigene oder alle lesen (umschaltbar) | Meldung erstellen, auf Kommentare eigener Meldungen antworten |
| Lehrende | Meldungen eigener/ aller Module lesen | Kommentieren und Status ändern eigener Meldungen |
| Admin | Alle Meldungen, Kommentare und Antworten lesen | Module verwalten, Benutzer verwalten |

## Projekt starten (lokal)
```bash
git clone https://github.com/moechtegern90/KMSystem.git
cd KMSystem

Virtuelle Umgebung - optional, aber empfohlen:
python -m venv venv
source venv/bin/activate # auf macOS/Linux
venv\Scripts\activate # auf Windows
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

pip install -r requirements.txt

python setup_admin.py

#flask run
flask --app=controller.py run


git clone https://github.com/moechtegern90/KMSystem.git
cd KMSystem
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
export FLASK_APP=controller.py
export FLASK_ENV=development
python init_db.py               # einmalig zur DB-Erzeugung
flask run
