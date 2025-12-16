import pytest
from models import Lehrende, Modul, Studierende, Meldung, Kommentar, Kategorie, Sichtbarkeit

@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F02
def test_get_sichtbare_kommentare_oeffentlich(session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-02 Meldung anzeigen)

    - Prüft, dass öffentliche Kommentare sichtbar sind, wenn die Meldung zu einem Modul gehört,
      das der Lehrende betreut.
    - Erwartung: Liste enthält den öffentlichen Kommentar.
    """
    # Setup: Lehrender, Modul, Student, Meldung
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    lehrender.module.append(modul)
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul)

    # Öffentlicher Kommentar von einem anderen Lehrenden
    anderer_lehrender = Lehrende(name="Kollege", email="kollege@example.org", passwort="secret")
    kommentar = Kommentar(
        text="Öffentlicher Hinweis",
        meldung=meldung,
        sichtbarkeit=Sichtbarkeit.ÖFFENTLICH,
        verfasser=anderer_lehrender.name,
        lehrende=anderer_lehrender
        )

    session.add_all([lehrender, modul, student, meldung, anderer_lehrender, kommentar])
    session.commit()

    sichtbare = lehrender.get_sichtbare_kommentare(meldung)

    assert kommentar in sichtbare
    assert sichtbare == [kommentar]

    kommentar_privat = Kommentar(
        text="Privater Hinweis",
        meldung=meldung,
        sichtbarkeit=Sichtbarkeit.PRIVAT,
        verfasser=anderer_lehrender.name,
        lehrende=anderer_lehrender
    )

    session.add(kommentar_privat)
    session.commit()

    sichtbare_anderer = anderer_lehrender.get_sichtbare_kommentare(meldung)

    assert kommentar_privat not in sichtbare
    assert kommentar_privat in sichtbare_anderer


@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F02
def test_get_sichtbare_kommentare_privat_lehrende(session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-02 Meldung anzeigen)

    - Prüft, dass private Kommentare sichtbar sind, wenn die Meldung zu einem Modul gehört,
    das der Lehrende betreut.
    - Erwartung: Liste enthält den privaten Kommentar.
    """
    # Setup: Lehrender betreut Modul
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    lehrender.module.append(modul)
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul)

    # Privater Kommentar von einem anderen Lehrenden
    anderer_lehrender = Lehrende(name="Kollege", email="kollege@example.org", passwort="secret")
    kommentar_privat = Kommentar(
        text="Privater Hinweis",
        meldung=meldung,
        sichtbarkeit=Sichtbarkeit.PRIVAT,
        verfasser=anderer_lehrender.name,
        lehrende=anderer_lehrender
    )

    session.add_all([lehrender, modul, student, meldung, anderer_lehrender, kommentar_privat])
    session.commit()

    sichtbare = lehrender.get_sichtbare_kommentare(meldung)

    # Erwartung: Lehrender sieht privaten Kommentar, da er das Modul betreut
    assert kommentar_privat in sichtbare



@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F05
@pytest.mark.requirement_NF07
def test_add_kommentar_permission_error(session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-05 Kommentarfunktion), 
                   Sicherheit (NF-07 Rollenbasierte Rechtevergabe)

    - Prüft, dass ein Lehrender keinen Kommentar zu einer Meldung eines 
      fremden Moduls hinzufügen darf.
    - Erwartung: PermissionError mit Meldung "Dies ist nur für eigene Module möglich."
    """
    # Lehrender ohne Modulzuordnung
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    modul = Modul(titel="Fremdes Modul")
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul)

    session.add_all([lehrender, modul, student, meldung])
    session.commit()

    # Versuch, Kommentar zu fremdem Modul hinzuzufügen → PermissionError
    with pytest.raises(PermissionError) as excinfo:
        lehrender.add_kommentar(meldung, "Nicht erlaubt!")

    assert "Dies ist nur für eigene Module möglich." in str(excinfo.value)
