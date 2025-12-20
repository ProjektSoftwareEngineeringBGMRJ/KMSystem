import pytest
from models import Modul, Meldung, Studierende, Kategorie

@pytest.mark.id_T62
@pytest.mark.unit
@pytest.mark.funktion
@pytest.mark.requirement_F07
def test_modul_initialisierung():
    '''
    Testart: Unit-Test
    Testkategorie: Funktionstest (F-07 Modulverwaltung)
    
    - Prüft die Initialisierung eines Moduls
    - Ist der Titel korrekt gesetzt?
    '''
    modul = Modul(titel="Software Engineering")
    assert modul.titel == "Software Engineering"


@pytest.mark.id_T08
@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F01
@pytest.mark.requirement_F02
@pytest.mark.requirement_F07
def test_modul_meldung_beziehung(session):
    '''
    Testart: Integrationstest
    Testkategorie: 
        Funktionstest (F-01 Meldung erfassen, F-02 Meldung anzeigen, F-07 Modulverwaltung)

    - Prüft die Beziehung zwischen Modul, Meldung und Studierendem
    - Wird die Meldung korrekt mit Modul und Ersteller verknüpft?
    - Funktioniert Cascade-Delete (Löschung des Moduls entfernt abhängige Meldungen)?
    '''
    # Modul und Studierenden anlegen
    modul = Modul(titel="Software Engineering")
    session.add(modul)

    student = Studierende("Test Student", "test@testen.org", "test_passwort")
    session.add(student)
    session.commit()

    # Meldung erstellen (verwendet Beziehungen zu modul und ersteller)
    meldung = Meldung(
        beschreibung="Fehler im Skript",
        kategorie=Kategorie.ONLINESKRIPT,
        ersteller=student,
        modul=modul
    )

    session.add(meldung)
    session.commit()

    # Aus der DB neu laden und Beziehungen prüfen
    session.refresh(modul)
    session.refresh(meldung)
    assert meldung in modul.meldungen
    assert meldung.ersteller == student

    # Cascade-Delete prüfen
    meldung_id = meldung.id
    session.delete(modul)
    session.commit()
    assert session.query(Meldung).filter_by(id=meldung_id).first() is None
