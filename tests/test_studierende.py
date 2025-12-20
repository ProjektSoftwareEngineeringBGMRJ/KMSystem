import pytest
from models import Studierende, Modul, Meldung, Kommentar, Kategorie, Sichtbarkeit, Lehrende

@pytest.mark.id_T30
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F05
def test_antworte_auf_kommentar_erfolgreich(session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-05 Kommentarfunktion)

    - Prüft, dass ein Studierender erfolgreich auf einen Kommentar antworten kann.
    - Erwartung: Antwort wird erstellt, ist privat und mit dem ursprünglichen Kommentar verknüpft.
    """
    student = Studierende(name="Student", email="stud@example.org", passwort="geheim")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="geheim")
    modul = Modul(titel="Testmodul")
    meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul)
    kommentar = Kommentar(
        text="Basis-Kommentar",
        meldung=meldung,
        sichtbarkeit=Sichtbarkeit.ÖFFENTLICH,
        lehrende=lehrender,
        verfasser="Dozent"
        )

    session.add_all([student, modul, meldung, kommentar])
    session.commit()

    student.antworte_auf_kommentar(kommentar, "Antworttext")

    antwort = Kommentar.query.filter_by(text="Antworttext").first()
    assert antwort is not None
    assert antwort.sichtbarkeit == Sichtbarkeit.PRIVAT
    assert antwort.antwort_auf == kommentar
    assert antwort.verfasser == student.name


@pytest.mark.id_T31
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F05
@pytest.mark.requirement_NF07
def test_antworte_auf_kommentar_permission_error(session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-05 Kommentarfunktion), 
                   Sicherheit (NF-07 Rollenbasierte Rechtevergabe)

    - Prüft, dass ein Nicht-Studierender keinen Kommentar beantworten darf.
    - Erwartung: PermissionError mit Meldung "Nur Studierende dürfen antworten."
    """
    # Lehrender und Student vorbereiten
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="geheim")
    modul = Modul(titel="Testmodul")
    student = Studierende(name="Student", email="stud@example.org", passwort="geheim")
    meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul)
    kommentar = Kommentar(
        text="Basis-Kommentar",
        meldung=meldung,
        sichtbarkeit=Sichtbarkeit.ÖFFENTLICH,
        verfasser=lehrender.name,
        lehrende=lehrender
    )

    session.add_all([lehrender, modul, student, meldung, kommentar])
    session.commit()

    # Methode über ein Studierenden-Objekt aufrufen, Typ so patchen, dass es wie Lehrender wirkt
    fake_student = Lehrende(name="Fake", email="fake@example.org", passwort="geheim")

    with pytest.raises(PermissionError) as excinfo:
        Studierende.antworte_auf_kommentar(fake_student, kommentar, "Antworttext")

    assert "Nur Studierende dürfen antworten." in str(excinfo.value)
