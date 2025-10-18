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
│
├── controller.py          # Routing und Rollenlogik
├── models/                # Datenbankmodelle (Benutzer, Modul, Meldung, etc.)
├── templates/             # HTML-Templates (Übersicht, Formulare, Verwaltung)
├── static/                # CSS und JS-Dateien
├── datenbank.py           # SQLAlchemy-Initialisierung
└── README.md              # Projektbeschreibung
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
