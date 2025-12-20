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
│── instance/                # SQLite-Datenbank
│   └── kmsystem.db
├── models/                  # alle SQLAlchemy-Datenmodelle
│   ├── __init__.py              # definiert Verzeichnis als Python-Paket
│   ├── admin.py                 # Klasse Admin, erbt von Benutzer
│   ├── benutzer.py              # Basisklasse für Benutzer (gemeinsame Attribute und Methoden)
│   │── datenbank.py             # Zentrales SQLAlchemy-Datenbankobjekt 
│   │── enums.py                 # Definition von Auflistzungen (z. B. Rollen, Statuswerte)
│   ├── kommentar.py             # Datenmodell für Kommentare zu Meldungen
│   ├── lehrende.py              # Klasse Lehrende, erbt von Benutzer
│   ├── meldung.py               # Datenmodell für Meldungen
│   ├── modul.py                 # Datenmodell für Module (Zuordnung von Meldungen und Lehrenden)
│   ├── rollen_liste.py          # Mapping von Benutzerklasse für Rollen
│   └── studierende.py           # Klasse Studierende, erbt von Benutzer
├── templates/               # Jinja2-HTML-Dateien für Benutzeroberfläche
│   ├── benutzer_erstellen.html  # Formular zur Erstellung neuer Benutzer
│   ├── login.html               # Login-Seite für alle Rollen
│   ├── meldung_detail.html      # Detailansicht einer Meldung inkl. Kommentare
│   ├── meldung_formular.html    # Formular zum Erstellen einer Meldung
│   ├── module_verwalten.html    # Oberfläche für Admins zur Verwaltung von Modulen
│   ├── nutzerverwaltung.html    # Oberfläche für Admins zur Verwaltung von Benutzern
│   └── uebersicht.html          # Übersicht aller Meldungen (rollenabhängig gefiltert)
├── tests/                   # alle Tests mit Pytest 
│   ├── conftest.py              # Pytest-Konfiguration und Fixtures 
│   ├── test_admin.py            # Tests für Admin-Funktionalität 
│   ├── test_benutzer.py         # Tests für Basisklasse Benutzer 
│   ├── test_controller.py       # Tests für Flask-Routen und Logik 
│   ├── test_lehrende.py         # Tests für Lehrende-Rolle 
│   ├── test_meldung.py          # Tests für Meldungsmodell 
│   ├── test_modul.py            # Tests für Modul-Zuordnung und Logik 
│   ├── test_rollen_liste.py     # Tests für Rollen-Mapping
│   └── test_studierende.py      # Tests für Studierenden-Rolle
├── static/                  # (CSS, JS, Bilder - optional, bisher nicht vorhanden)
├── .gitignore               # Ausschlussregeln für Git (z. B. __pycache__, reports) 
├── Procfile                 # Deployment-Konfiguration für Render 
├── README.md                # Projektdokumentation 
├── controller.py            # zentrale Flask-Routen und Logik 
├── init_db.py               # Initialisierung der Datenbank aus Modellen 
├── pytest.ini               # Pytest-Konfiguration (z. B. Marker, Filter)
├── report.html              # generierter HTML-Testreport (optional)
├── requirements.txt         # Python-Abhängigkeiten für das Projekt 
└── setup_admin.py           # Skript zur Erstellung eines ersten Admin-Benutzers
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
# Windows:
Win+r -> cmd eingeben # Commandline öffnen

# in cmd:
cd documents/uni/ # Beispiel: zu Pfad, wo installiert werden soll navigieren
mkdir KMStest # neuen, leeren Ordner an dem Ort anlegen
dir # prüfen, ob Ordner existiert
cd KMStest # in erstellten Ordner navigieren

git clone https://github.com/moechtegern90/KMSystem.git # lädt Programm herunter
cd KMSystem
python -m venv venv             # Virtuelle Umgebung installieren (empfohlen)

# macOS/Linux:
source venv/bin/activate        

venv\Scripts\activate           # Windows
# wenn Ausführung von Skripts auf System deaktiviert ist:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass # erlaubt Skripte für die eine Session
# dann vorherigen Befehl wiederholen

pip install -r requirements.txt # Abhängigkeitren installieren

python init_db.py               # einmalig zur DB-Erzeugung
flask --app=controller run      # App sarten

# Aufrufen im Browser (URL, die in cmd angezeigt wird) z.B.:
http://127.0.0.1:5000/setup-admin # Admin beim ersten Start initialisieren 

http://127.0.0.1:5000/ # Login aufrufen und als Admin anmelden (email: admin@example.org, pw: admin123)
-> Als Admin können Module und User erstellt werden.

# Schließen der App:
In cmd: Strg+c
```

## Voraussetzungen für die Installation und Ausführung

### Systemvoraussetzungen
- Windows-Betriebssystem (Anleitung basiert auf Windows-Konsole)
- Schreibrechte im Zielverzeichnis (z. B. `documents/uni/`)
- Internetzugang für GitHub-Zugriff

### Nötige Vorinstallierte Software:
- [x] **Python 3.x** (empfohlen: ≥ 3.8)
    #### Prüfen, ob Python installiert und im PATH verfügbar ist: 
        python --version

    ##### falls nicht vorhanden: Python installieren:
        https://www.python.org/downloads/ 
        
    - Installer .exe herunterladen
    - Beim Setup unbedingt die Option „Add Python to PATH“ aktivieren.
    - erneut prüfen:
    python --version
    
    #### Pip prüfen:
        pip --version

    ##### falls nicht vorhanden: installieren
        python -m pip install --upgrade pip

- [x] **Git** (für `git clone`)
    #### prüfen, ob Git vorhanden ist:
        git --version

    ##### falls nicht vorhanden: installieren
        https://git-scm.com/downloads
        
    -> Installer ausführen


## Troubleshooting

- **`python` wird nicht gefunden**  
  → Prüfen, ob Python installiert ist und beim Setup „Add Python to PATH“ aktiviert wurde.  
  → Alternativ `py --version` oder `python3 --version` ausprobieren.

- **`flask` wird nicht gefunden**  
  → Sicherstellen, dass die virtuelle Umgebung aktiv ist.  
  → Alternativ: `python -m flask --app=controller run`.

- **Fehler bei `pip install -r requirements.txt`**  
  → `pip install --upgrade pip` ausführen und erneut versuchen.

- **Port 5000 bereits belegt**  
  → Anwendung mit anderem Port starten:  
    `flask --app=controller run -p 5001`


