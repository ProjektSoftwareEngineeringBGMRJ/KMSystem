import pytest
from sqlalchemy.exc import NoResultFound
from models import Studierende, Lehrende, Modul, Benutzer, Admin #, Meldung, Kategorie

@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_create_update_delete_nutzer(session):
    """
    Testart: Integrationstest
    Testkategorie: Funktionstest (F-06 Benutzerverwaltung)

    - Prüft CRUD-Operationen auf Modellebene.
    - Erwartung: Benutzer kann erstellt, geändert und gelöscht werden.
      (Ändern technisch möglich, in Prototyp nicht vorgesehen)
    """
    user = Studierende("Test", "test@test.org", "pw123")
    session.add(user)
    session.commit()

    # Create
    assert session.query(Benutzer).filter_by(email="test@test.org").one()

    # Update
    user.name = "Neuer Name"
    session.commit()
    session.refresh(user)
    assert user.name == "Neuer Name"

    # Delete
    session.delete(user)
    session.commit()
    with pytest.raises(NoResultFound):
        session.query(Benutzer).filter_by(email="test@test.org").one()


@pytest.mark.integration
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_module_zuweisen_model(session):
    """
    Testart: Integrationstest
    Testkategorie: Funktionstest (F-06 Modulzuordnung)

    - Prüft, dass Lehrenden Module zugeordnet werden können.
    - Erwartung: Zuordnung bleibt nach Commit persistent.
    """
    lehrende = Lehrende("Lehrkraft", "lehrende@test.org", "pw123")
    modul = Modul("Testmodul")
    session.add_all([lehrende, modul])
    session.commit()

    lehrende.module.append(modul)
    session.commit()
    session.refresh(lehrende)
    assert modul in lehrende.module


@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_erstelle_modul_bereits_vorhanden(session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Modulverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass beim Versuch ein Modul mit bereits vorhandenem Titel zu erstellen
      ein ValueError ausgelöst wird.
    - Erwartung: Exception mit Meldung 'Modul "Testmodul" bereits vorhanden.'
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    session.add_all([admin, modul]); session.commit()

    # Erneuter Versuch mit gleichem Titel → sollte ValueError werfen
    with pytest.raises(ValueError) as excinfo:
        admin.erstelle_modul("Testmodul")

    assert 'Modul "Testmodul" bereits vorhanden.' in str(excinfo.value)


# @pytest.mark.system
# @pytest.mark.funktion
# @pytest.mark.requirement_F07
# def test_loesche_modul_erfolgreich(session):
#     """
#     Testart: Systemtest
#     Testkategorie: Funktional (F-07 Modulverwaltung)

#     - Prüft, dass ein Modul ohne Meldungen erfolgreich gelöscht wird.
#     - Erwartung: Methode gibt True zurück und Modul ist nicht mehr in der DB.
#     """
#     admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
#     modul = Modul(titel="Testmodul")
#     session.add_all([admin, modul])
#     session.commit()

#     result = admin.loesche_modul(modul)

#     assert result is True
#     assert Modul.query.filter_by(titel="Testmodul").first() is None


# @pytest.mark.system
# @pytest.mark.funktion
# @pytest.mark.requirement_F07
# def test_loesche_modul_mit_meldungen(session):
#     """
#     Testart: Systemtest
#     Testkategorie: Funktional (F-07 Modulverwaltung)

#     - Prüft, dass ein Modul mit Meldungen nicht gelöscht wird.
#     - Erwartung: Methode gibt False zurück und Modul bleibt in der DB.
#     """
#     admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
#     modul = Modul(titel="Testmodul")
#     student = Studierende(name="Student", email="stud@example.org", passwort="secret")
#     meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul)

#     session.add_all([admin, modul, student, meldung])
#     session.commit()

#     result = admin.loesche_modul(modul)

#     assert result is False
#     assert Modul.query.filter_by(titel="Testmodul").first() is not None
