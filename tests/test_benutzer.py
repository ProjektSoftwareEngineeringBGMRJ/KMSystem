import pytest
from models import Benutzer, Meldung, Kategorie, Studierende, Modul

@pytest.mark.unit
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.sicherheit
@pytest.mark.requirement_NF06
@pytest.mark.requirement_NF08
def test_benutzer_initialisierung():
    '''
    Testart: Unit-Test 
    Testkategorie:  Funktionstest (F-06 Benutzerverwaltung)
                    Sicherheitstest (NF-06 Authentifizierung, NF-08 Datenschutz)
                    
    - Prüft initialisierung und Passwort-Hashing
    - Sind name und email korrekt gesetzt?
    - Wird Passwort korrekt geprüft?
    - Wird falsches Passwort abgelehnt?
    - Ist Passwort-Hash ungleich dem Klartext-Passwort?
    '''
    benutzer = Benutzer(name="Test Nutzer", email="test@mail.org", passwort="test123")

    assert benutzer.name == "Test Nutzer"
    assert benutzer.email == "test@mail.org"

    assert benutzer.check_passwort(passwort="test123") is True
    assert benutzer.check_passwort(passwort="falsch") is False
    assert benutzer.passwort_hash != "test123"


@pytest.mark.unit
@pytest.mark.funktion
@pytest.mark.requirement_F08
def test_benutzer_get_sichtbare_kommentare_not_implemented():
    '''
    Testart: Unit-Test
    Testkategorie: Funktionstest (F-08 Rollen- und Rechteverwaltung) 
    
    - Funktion darf in Basisklasse nicht direkt nutzbar sein, 
    sondern muss von Subklassen überschrieben werden.
    '''
    benutzer = Benutzer("Test Benutzer", "test@email.org", "pw")
    meldung = Meldung(
        beschreibung="Test",
        kategorie=Kategorie.FOLIENSÄTZE,
        ersteller=Studierende("test","test","test"),
        modul=Modul("Testmodul")
    )

    with pytest.raises(NotImplementedError):
        benutzer.get_sichtbare_kommentare(meldung)


@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F08
def test_studierende_polymorphie(session):
    '''
    Testart: Integraionstest
    Testkategorie: Funktionstest (F-08 Rollen- und Rechteverwaltung)
    
    - Polymorphie/ Rollen
    - Prüfen ob type durch Unterklassen richtig gesetzt wird
    '''
    student = Studierende(name="Test Nutzer", email="test@mail.org", passwort="sicher123")
    
    session.add(student)
    session.commit()
    assert student.type == "studierende"


@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F01
@pytest.mark.requirement_F02
def test_benutzer_meldung_beziehung(session):
    '''
    Testart: Integraionstest
    Testkategorie: Funktionstest (F-01 Meldung erfassen, F-02 Meldung anzeigen)
    
    - Prüft Beziehung zwischen Benutzer und Meldung
    - Wid ersteller korrekt gesetzt? 
    '''
    student = Studierende("Test Student", "test@testen.org", "pw123")
    modul = Modul("Test Modul")
    meldung = Meldung("Hier stimmt was nicht!", Kategorie.ONLINETESTS, student, modul)

    session.add_all([student, modul, meldung])
    session.commit()

    assert meldung.ersteller == student
    assert meldung.ersteller_id == student.id
