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
├── models/                  # alle SQLAlchemy-Datenmodelle (Benutzer, Modul, Meldung, etc.)
│   ├── benutzer.py          # 
|   ├── admin.py             # 
|   ├── lehrende.py          # 
|   ├── studierende.py       # 
|   ├── meldung.py           # 
│   ├── kommentar.py         # 
│   ├── modul.py             # 
│   └── enums.py             # 
├── templates/           # Jinja2-HTML-Templates für Benutzeroberfläche (Übersicht, Formulare, Verwaltung)
│   ├── benutzer_erstellen.html
|   ├── login.html
|   ├── meldung_detail.html
|   ├── meldung_formular.html
|   ├── module_verwalten.html
|   ├── nutzerverwaltung.html
│   └── uebersicht.html
├── (static/              # CSS, JS, Bilder - optional)
├── controller.py        # Flask-Routen und Logik
├── Procfile             # Für Deployment auf Render
├── README.md            # Projektdokumentation
├── requirements.txt     # alle Abhängigkeiten
└── setup_admin.py       # Initialisierung der Datenbank und eines Admins
```
Die Datenbank wird direkt über `db.create_all()` aus den SQLAlchemy-Modellen erzeugt. 
Es wird kein Migrationsframework verwendet.


## Rollen und Zugriff
| Rolle	| Zugriff auf Meldungen | Zusatzfunktionen |
| ----- | --------------------- | ---------------- |
| Studierende | Eigene oder alle lesen (umschaltbar) | Meldung erstellen, auf Kommentare eigener Meldungen antworten |
| Lehrende | Meldungen eigener/ aller Module lesen | Kommentieren und Status ändern eigener Meldungen |
| Admin | Alle Meldungen, Kommentare und Antworten lesen | Module erstellen/ löschen, Module zuweisen, Benutzer hinzufügen/ löschen |

## Projekt starten (lokal)
```bash
git clone https://github.com/moechtegern90/KMSystem.git
cd KMSystem
flask run
