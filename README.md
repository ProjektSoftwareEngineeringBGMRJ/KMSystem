# Korrekturmanagementsystem (KMSystem)

Ein webbasiertes System zum Melden von Fehlern, Verbesserungsvorschlägen und Ergänzungen zu Lerninhalten im akademischen Kontext.

## Technologien
- **Python 3.11**
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

## Rollen und Zugriff
| Rolle	| Zugriff auf Meldungen |	Zusatzfunktionen |
| ----- | --------------------- | ---------------- |
| Studierende	| Eigene oder alle (umschaltbar) | Meldung erstellen |
| Lehrende | Meldungen eigener Module |	Kommentierung zu Meldungen |
| Admin | Alle Meldungen | Benutzer	Rollen ändern, Benutzer hinzufügen/ löschen |

## Projekt starten (lokal)
```bash
git clone https://github.com/moechtegern90/KMSystem.git
cd KMSystem
flask run
