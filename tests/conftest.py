import sys
import os

# Projekt-Root zum Pfad hinzufügen, damit 'models' beim Testlauf gefunden wird
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import allure
from controller import app, db

#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#...\KMS_test\KMSystem> venv\Scripts\activate
# pytest -q -> Tests ausführen
# pytest --cov=models -> Coverage für models-Paket
# --cov=controller -> Coverage für Flask-Routen
# --cov-report=term-missing -> zeigt ungetestete Zeilen 


# Fixtures (wiederverwendbare Test‑Setups)
@pytest.fixture
def client():
    '''
    Fixture: Flask-Testclient

    - Konfiguriert die zentrale Flask-App für Testzwecke (TESTING, In-Memory-SQLite).
    - Stellt einen Testclient bereit, mit dem HTTP-Requests gegen die Routen
      des Controllers simuliert werden können.
    - Wird in Systemtests genutzt, um Endpunkte wie /login oder /uebersicht
      realistisch anzusprechen.
    '''
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app.test_client()

@pytest.fixture
def session():
    '''
    Fixture: Datenbank-Session

    - Erstellt pro Testlauf ein frisches DB-Schema in einer In-Memory-SQLite-Datenbank.
    - Stellt eine SQLAlchemy-Session bereit, über die Testdaten angelegt und
      persistiert werden können.
    - Nach jedem Test wird die Session entfernt und das Schema wieder gelöscht,
      um Seiteneffekte zwischen Tests zu vermeiden.
    '''
    with app.app_context():
        db.drop_all()
        db.engine.dispose()
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

@pytest.fixture
def app_context():
    """
    Fixture: App-Kontext

    - Stellt sicher, dass innerhalb eines Tests ein gültiger Flask-App-Kontext aktiv ist.
    - Notwendig für direkte Aufrufe wie Benutzer.query.get() oder load_user().
    """
    with app.app_context():
        yield

# Decorator zum Filtern in allure
def pytest_runtest_setup(item):
    for marker in item.iter_markers():
        name = marker.name

        # Anforderungen (funktional) → Feature
        if name.startswith("requirement_F"):
            allure.dynamic.feature(name)

        # Anforderungen (nicht-funktional) → Story
        elif name.startswith("requirement_NF"):
            #allure.dynamic.story(name)
            allure.dynamic.feature(name)

        # Teststufen → Severity
        elif name in ["unit", "integration", "system", "acceptance"]:
            level_map = {
                "unit": allure.severity_level.MINOR,
                "integration": allure.severity_level.NORMAL,
                "system": allure.severity_level.CRITICAL,
                "acceptance": allure.severity_level.BLOCKER,
            }
            allure.dynamic.severity(level_map[name])

        # Testkategorien → Tag
        elif name in ["funktion", "usability", "performance", "sicherheit", "kompatibilitaet"]:
            #allure.dynamic.tag(name)
            allure.dynamic.story(name)

        # IDs → zusätzliche Tags
        elif name.startswith("id_T"):
            allure.dynamic.tag(name)

        # Fallback: alles andere als Tag
        else:
            allure.dynamic.tag(name)
