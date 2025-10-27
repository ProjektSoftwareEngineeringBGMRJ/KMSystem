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

source venv/bin/activate        # macOS/Linux

venv\Scripts\activate           # Windows
# wenn Ausführung von Skripts auf System deaktiviert ist:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass 
# dann vorherigen Befehl wiederholen

pip install -r requirements.txt # Abhängigkeitren installieren

python init_db.py               # einmalig zur DB-Erzeugung
flask --app=controller run      # App sarten

# Aufrufen im Browser:
http://127.0.0.1:5000/setup-admin # Admin beim ersten Start initialisieren (email: admin@example.org, pw: admin123)

http://127.0.0.1:5000/ # Login aufrufen und beim ersten Start als Admin anmelden 
```

## Voraussetzungen für die Installation und Ausführung

### Systemvoraussetzungen
- Windows-Betriebssystem (Anleitung basiert auf Windows-Konsole)
- Schreibrechte im Zielverzeichnis (z. B. `documents/uni/`)
- Internetzugang für GitHub-Zugriff

### Nötige Vorinstallierte Software:
- [x] **Python 3.x** (empfohlen: ≥ 3.8)
    # prüfen, ob Python installiert und im PATH verfügbar ist: 
    python --version
    # falls nicht vorhanden: Python installieren:
        https://www.python.org/downloads/ # -> Installer .exe herunterladen
            # Wichtig: 
            # Beim Setup unbedingt die Option „Add Python to PATH“ aktivieren.
        python --version # -> erneut prüfen
    
    # Pip prüfen:
    pip --version 
    # falls nicht vorhanden: installieren
        python -m pip install --upgrade pip

- [x] **Git** (für `git clone`)
    # prüfen, ob Git vorhanden ist:
    git --version
    # falls nicht vorhanden: installieren
        https://git-scm.com/downloads # -> Installer ausführen



