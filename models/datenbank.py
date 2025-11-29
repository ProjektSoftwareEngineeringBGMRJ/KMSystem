'''
 Zentrales SQLAlchemy-Datenbankobjekt.

 Wird in allen Modellen importiert und stellt die Verbindung zur Datenbank her.
 Ermöglicht:
   - Definition von Tabellen (ORM-Modelle)
   - Erstellung von Beziehungen zwischen Klassen
   - Session-Management (Speichern, Abfragen, Löschen von Objekten)

 Hinweis:
   - Die konkrete Datenbank-URL wird in der Flask-App (controller) konfiguriert.
   - Dieses Objekt muss mit `db.init_app(app)` initialisiert werden.
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
