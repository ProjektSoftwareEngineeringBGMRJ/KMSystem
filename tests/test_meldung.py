from datetime import datetime
import pytest
from models import Meldung, Modul, Studierende, Kategorie, Status, Kommentar, Sichtbarkeit

@pytest.mark.id_T06
@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F01
@pytest.mark.requirement_F02
def test_meldung_initialisierung(session):
    '''
    Testart: Integrationstest
    Testkategorie: Funktionstest (F-01 Meldung erfassen, F-02 Meldung anzeigen)
    
    - Prüft die Initialisierung einer Meldung
    - Wird Meldung korrekt mit Modul und Studierendem verknüpft?
    - Ist die Meldung über DB abrufbar?
    '''
    # Modul und Studierenden anlegen
    modul = Modul(titel="Software Engineering")
    session.add(modul)

    student = Studierende("Test Student", "test@testen.org", "test_passwort")
    session.add(student)
    session.commit()

    meldung = Meldung(
        beschreibung="Fehler im Video.",
        kategorie=Kategorie.VIDEO,
        ersteller=student,
        modul=modul
    )
    session.add(meldung)
    session.commit()

    session.refresh(meldung)
    assert meldung in modul.meldungen
    meldung_id = meldung.id
    assert session.query(Meldung).filter_by(id=meldung_id).first()

@pytest.mark.id_T07
@pytest.mark.unit
@pytest.mark.funktion
@pytest.mark.requirement_F01
def test_meldung_defaults(session):
    '''
    Testart: Unit-Test
    Testkategorie: Funktionstest (F-01 Meldung erfassen)
    
    - Prüft, ob Defaultwerte korrekt gesetzt werden
    - Status = OFFEN
    - Zeitstempel = datetime
    '''
    modul = Modul(titel="Software Engineering")
    student = Studierende("Test Student", "test@testen.org","test_passwort")
    session.add_all([modul, student])
    session.commit()

    meldung = Meldung("Testbeschreibung", Kategorie.PDFSKRIPT, student, modul)
    session.add(meldung)
    session.commit()

    assert meldung.status == Status.OFFEN
    assert isinstance(meldung.zeitstempel, datetime)

@pytest.mark.id_T12
@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F02
def test_meldung_ersteller_beziehung(session):
    '''
    Testart: Integrationstest
    Testkategorie: Funktionstest (F-02 Meldung anzeigen)
    
    - Prüft, ob die Beziehung zwischen Meldung und Ersteller korrekt ist
    - Name und Email des Erstellers müssen abrufbar sein
    '''
    modul = Modul(titel="Software Engineering")
    student = Studierende("Test Student", "test@testen.org","test_passwort")
    session.add_all([modul, student])
    session.commit()

    meldung = Meldung("Testbeschreibung", Kategorie.FOLIENSÄTZE, student, modul)
    session.add(meldung)
    session.commit()

    assert meldung.ersteller.name == "Test Student"
    assert meldung.ersteller.email == "test@testen.org"


@pytest.mark.id_T61
@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F07
def test_meldung_cascade_delete(session):
    '''
    Testart: Integrationstest
    Testkategorie: Funktionstest (F-07 Modulverwaltung)
    
    - Prüft Cascade-Delete Verhalten
    - Wird eine Meldung gelöscht, wenn der Studierende entfernt wird?
    '''
    modul = Modul(titel="Software Engineering")
    student = Studierende("Testerin", "test@example.org", "pw46")
    meldung = Meldung("Testmeldung", Kategorie.MUSTERKLAUSUR, student, modul)

    session.add_all([modul, student, meldung])
    session.commit()

    meldung_id = meldung.id
    assert session.query(Meldung).filter_by(id=meldung_id).first() is not None
    session.delete(student)
    session.commit()
    assert session.query(Meldung).filter_by(id=meldung_id).first() is None


@pytest.mark.id_T29
@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F05
def test_meldung_kommentare(session):
    '''
    Testart: Integrationstest
    Testkategorie: Funktionstest (F-05 Kommentarfunktion)
    
    Prüft die Kommentarfunktion und Cascade-Delete
    - Wird ein Kommentar korrekt mit einer Meldung verknüpft?
    - Wird der Kommentar gelöscht, wenn die Meldung entfernt wird?
    '''
    modul = Modul(titel="Tolles Modul")
    student = Studierende("Name Studierende", "name@namensgebung.org", "super_sicheres-Passwört18%")
    meldung = Meldung("Diese Meldung soll kommentiert werden.", Kategorie.PDFSKRIPT, student, modul)

    kommentar = Kommentar(
        text="Super!",
        meldung=meldung,
        sichtbarkeit=Sichtbarkeit.ÖFFENTLICH,
        verfasser=student.name
    )

    session.add_all([modul, student, meldung, kommentar])
    session.commit()
    assert kommentar in meldung.kommentare
    assert kommentar.verfasser == "Name Studierende"

    session.delete(meldung)
    session.commit()
    assert session.query(Kommentar).filter_by(id=kommentar.id).first() is None
