import sys
import os

# Projekt-Root zum Pfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fixtures
import pytest
from models.datenbank import db

@pytest.fixture
def session():
   db.create_all()
   yield db.session
   db.session.rollback()
   db.drop_all()