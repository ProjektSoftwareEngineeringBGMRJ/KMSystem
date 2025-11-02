from models.modul import Modul
from models.meldung import Meldung

def test_modul_initialisierung():
    modul = Modul(titel="Software Engineering")
    assert modul.titel == "Software Engineering"