from datetime import datetime
import importlib
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models import Modul, Benutzer, Studierende, Lehrende, Admin, Meldung, Kategorie, Sichtbarkeit, Kommentar
from controller import load_user

@pytest.mark.id_T13
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F03
@pytest.mark.requirement_F08
@pytest.mark.requirement_F09
def test_uebersicht_studierende(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest 
        (F-03 Meldungsübersicht, F-08 Rollen- und Rechteverwaltung, F-09 Dashboard-Ansicht)

    - Prüft die Übersichtsseite aus Sicht eines Studierenden.
    - Szenarien:
    1. Zugriff ohne Parameter → nur eigene Meldungen sichtbar.
    2. Zugriff mit alle_meldungen=true → alle Meldungen sichtbar.
    3. Zugriff mit Filter 'modul' → nur Meldungen des gewählten Moduls sichtbar.
    4. Zugriff mit Filter 'status' → nur Meldungen mit gewähltem Status sichtbar.
    5. Zugriff mit Filter 'kategorie' → nur Meldungen der gewählten Kategorie sichtbar.
    '''
    # Testdaten
    modul1 = Modul("Modul 1")
    modul2 = Modul("Modul 2")
    student1 = Studierende("Student 1", "mail1@test.org", "123456")
    student2 = Studierende("Student 2", "mail2@test.org", "123456")
    meldung1 = Meldung("Fehler im Skript", Kategorie.ONLINESKRIPT, student1, modul1)
    meldung2 = Meldung("Zweite Meldung!", Kategorie.MUSTERKLAUSUR, student2, modul2)
    session.add_all([modul1, modul2, student1, student2, meldung1, meldung2])
    session.commit()

    # Login über echten Endpoint
    response = client.post("/login", data={
        "email": "mail1@test.org",
        "passwort": "123456"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Zugriff auf Übersicht #####
    response = client.get("/uebersicht")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht eigene Meldung
    assert "Fehler im Skript" in html
    assert "Zweite Meldung!" not in html

    # Zugriff auf Übersicht mit allen Meldungen #####
    response = client.get("/uebersicht?alle_meldungen=true")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht alle Meldungen
    assert "Fehler im Skript" in html
    assert "Zweite Meldung!" in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter modul = "Modul 2" #####
    response = client.get("/uebersicht?alle_meldungen=true&modul=Modul 2")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 2
    assert "Zweite Meldung!" in html
    assert "Fehler im Skript" not in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter status = "in Bearbeitung" #####
    response = client.get("/uebersicht?alle_meldungen=true&status=BEARBEITUNG")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 2
    assert "Fehler im Skript" not in html
    assert "Zweite Meldung!" not in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter kategorie = "Online Skript" #####
    response = client.get("/uebersicht?alle_meldungen=true&kategorie=ONLINESKRIPT")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 2
    assert "Fehler im Skript" in html
    assert "Zweite Meldung!" not in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter kategorie = "Musterklausur" #####
    response = client.get("/uebersicht?alle_meldungen=true&kategorie=MUSTERKLAUSUR")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 2
    assert "Fehler im Skript" not in html
    assert "Zweite Meldung!" in html


@pytest.mark.id_T14
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F03
@pytest.mark.requirement_F08
@pytest.mark.requirement_F09
def test_uebersicht_lehrende(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest 
        (F-03 Meldungsübersicht, F-08 Rollen- und Rechteverwaltung, F-09 Dashboard-Ansicht)

    - Prüft die Übersichtsseite aus Sicht einer Lehrenden.
    - Szenarien:
      1. Zugriff ohne Parameter → nur Meldungen aus eigenen Modulen sichtbar.
      2. Zugriff mit alle_meldungen=true → alle Meldungen sichtbar.
      3. Zugriff mit Filter 'modul' → nur Meldungen des gewählten Moduls sichtbar.
      4. Zugriff mit Filter 'status' → nur Meldungen mit gewähltem Status sichtbar.
      5. Zugriff mit Filter 'kategorie' → nur Meldungen der gewählten Kategorie sichtbar.
    '''
    modul_1 = Modul("Modul 1")
    modul_2 = Modul("Modul 2")
    lehrende = Lehrende("Lehrkraft", "lehrende@test.org", "pw123")
    student = Studierende("Student", "student@test.org", "pw123")

    lehrende.module.append(modul_1)
    meldung_1 = Meldung("Fehler im Modul 1", Kategorie.FOLIENSÄTZE, student, modul_1)
    meldung_2 = Meldung("Fehler im Modul 2", Kategorie.MUSTERKLAUSUR, student, modul_2)
    session.add_all([modul_1, modul_2, lehrende, student, meldung_1, meldung_2])
    session.commit()

    # Login über echten Endpoint
    response = client.post("/login", data={
        "email": "lehrende@test.org",
        "passwort": "pw123"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Zugriff auf Übersicht #####
    response = client.get("/uebersicht")
    html = response.data.decode("utf-8")

    # Erwartung: Lehrende sieht nur Meldungen aus eigenem Modul
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" not in html

    # Zugriff auf Übersicht mit allen Meldungen #####
    response = client.get("/uebersicht?alle_meldungen=true")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Lehrende sieht alle Meldungen
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter modul = "Modul 1" #####
    response = client.get("/uebersicht?alle_meldungen=true&modul=Modul 1")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 1
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" not in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter status = "abgeschlossen" #####
    response = client.get("/uebersicht?alle_meldungen=true&status=GESCHLOSSEN")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 2
    assert "Fehler im Modul 1" not in html
    assert "Fehler im Modul 2" not in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter kategorie = "Musterklausur" #####
    response = client.get("/uebersicht?alle_meldungen=true&kategorie=MUSTERKLAUSUR")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 2
    assert "Fehler im Modul 1" not in html
    assert "Fehler im Modul 2" in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter kategorie = "Foliensätze" #####
    response = client.get("/uebersicht?alle_meldungen=true&kategorie=FOLIENSÄTZE")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Student sieht Meldung von Modul 2
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" not in html


@pytest.mark.id_T15
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F03
@pytest.mark.requirement_F08
@pytest.mark.requirement_F09
def test_uebersicht_admin(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest 
        (F-03 Meldungsübersicht, F-08 Rollen- und Rechteverwaltung, F-09 Dashboard-Ansicht)

    Zweck:
    - Prüft die Übersichtsseite aus Sicht eines Admins.
    - Szenarien:
      1. Zugriff ohne Parameter → alle Meldungen und alle Module sichtbar.
      2. Zugriff mit alle_meldungen=true → Verhalten identisch, da Admin immer alle Meldungen sieht.
      3. Zugriff mit Filter 'modul' → nur Meldungen des gewählten Moduls sichtbar.
      4. Zugriff mit Filter 'status' → nur Meldungen mit gewähltem Status sichtbar.
      5. Zugriff mit Filter 'kategorie' → nur Meldungen der gewählten Kategorie sichtbar.
    '''
    modul_1 = Modul("Modul 1")
    modul_2 = Modul("Modul 2")
    admin = Admin("Admin", "admin@test.org", "pw_admin")
    student = Studierende("Student", "student@test.org", "pw123")

    meldung_1 = Meldung("Fehler im Modul 1", Kategorie.FOLIENSÄTZE, student, modul_1)
    meldung_2 = Meldung("Fehler im Modul 2", Kategorie.MUSTERKLAUSUR, student, modul_2)
    session.add_all([modul_1, modul_2, admin, student, meldung_1, meldung_2])
    session.commit()

    # Login über echten Endpoint
    response = client.post("/login", data={
        "email": "admin@test.org",
        "passwort": "pw_admin"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Zugriff auf Übersicht ####
    response = client.get("/uebersicht")
    html = response.data.decode("utf-8")

    # Erwartung: Admin sieht alle Meldungen
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" in html

    # Zugriff auf Übersicht mit allen Meldungen #####
    response = client.get("/uebersicht?alle_meldungen=true")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Admin sieht alle Meldungen
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter modul = "Modul 1" #####
    response = client.get("/uebersicht?alle_meldungen=true&modul=Modul 1")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Admin sieht Meldung von Modul 1
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" not in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter status = "abgeschlossen" #####
    response = client.get("/uebersicht?alle_meldungen=true&status=GESCHLOSSEN")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Admin sieht Meldung von Modul 2
    assert "Fehler im Modul 1" not in html
    assert "Fehler im Modul 2" not in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter kategorie = "Musterklausur" #####
    response = client.get("/uebersicht?alle_meldungen=true&kategorie=MUSTERKLAUSUR")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Admin sieht Meldung von Modul 2
    assert "Fehler im Modul 1" not in html
    assert "Fehler im Modul 2" in html

    # Zugriff auf Übersicht mit allen Meldungen und Filter kategorie = "Foliensätze" #####
    response = client.get("/uebersicht?alle_meldungen=true&kategorie=FOLIENSÄTZE")
    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # Erwartung: Admin sieht Meldung von Modul 2
    assert "Fehler im Modul 1" in html
    assert "Fehler im Modul 2" not in html


@pytest.mark.id_T16
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
def test_status_aendern_lehrende(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-04 Status ändern)

    - Lehrende können den Status einer Meldung auf "in Bearbeitung" oder "abgeschlossen" setzen.
    - Szenarien:
      1. Statusänderung auf "in Bearbeitung".
      2. Statusänderung auf "abgeschlossen".
    '''
    # Testdaten
    modul = Modul("Test Modul")
    lehrende = Lehrende("Lehrkraft", "lehrende@test.org", "pw123")
    student = Studierende("Student", "student@test.org", "pw123")
    lehrende.module.append(modul)
    meldung = Meldung("Fehler im Modul", Kategorie.FOLIENSÄTZE, student, modul)
    session.add_all([modul, lehrende, student, meldung])
    session.commit()

    # Login über echten Endpoint
    response = client.post("/login", data={
        "email": "lehrende@test.org",
        "passwort": "pw123"
    }, follow_redirects=True)
    assert response.status_code == 200

    # Statusänderung auf "in Bearbeitung"
    response = client.post(f"/meldung/{meldung.id}/status_aendern", data={
        "status": "BEARBEITUNG",
        "kommentar": "",
        "sichtbarkeit": "PRIVAT"
    }, follow_redirects=True)
    assert response.status_code == 200
    session.refresh(meldung)
    assert meldung.status.name == "BEARBEITUNG"

    # Status -> GESCHLOSSEN ohne Kommentar, ohne Sichtbarkeit (Default greift)
    response = client.post(f"/meldung/{meldung.id}/status_aendern", data={
        "status": "GESCHLOSSEN",
        "kommentar": "",
        "sichtbarkeit": "ÖFFENTLICH"
    }, follow_redirects=True)
    assert response.status_code == 200
    session.refresh(meldung)
    assert meldung.status.name == "GESCHLOSSEN"

@pytest.mark.id_T17
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
def test_status_aendern_admin_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-04 Status ändern)

    - Prüft, dass Admins den Status einer Meldung NICHT ändern dürfen.
    - Szenarien:
      1. Admin loggt sich ein.
      2. Admin versucht Statusänderung → Status bleibt unverändert.
      3. Erwartung: Flash-Meldung über fehlende Berechtigung.
    '''
    modul = Modul("Test Modul")
    admin = Admin("Admin", "admin@test.org", "pw_admin")
    student = Studierende("Student", "student@test.org", "pw123")
    meldung = Meldung("Fehler im Modul", Kategorie.FOLIENSÄTZE, student, modul)
    session.add_all([modul, admin, student, meldung])
    session.commit()

    # Login als Admin
    response = client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw_admin"
        },
        follow_redirects=True
    )
    assert response.status_code == 200

    # Versuch: Status ändern
    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
        "status": "BEARBEITUNG",
        "kommentar": "",
        "sichtbarkeit": "PRIVAT"
        },
        follow_redirects=True
    )
    assert response.status_code == 200

    # Erwartung: Status bleibt unverändert (OFFEN)
    session.refresh(meldung)
    assert meldung.status.name == "OFFEN"

    # Prüfen ob PermissionError abgefangen und erwartete Flash-Meldung gesetzt wird
    html = response.data.decode("utf-8")
    assert "Nur Lehrende dürfen den Status ändern." in html


@pytest.mark.id_T25
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F05
@pytest.mark.requirement_F08
def test_antwort_speichern(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-05 Kommentarfunktion, F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass Studierende als Melder auf Kommentare von Lehrenden antworten können.
    - Szenarien:
      1. Lehrende loggt sich ein und erstellt einen Kommentar zu einer Meldung.
         → Erwartung: Kommentar gespeichert, Zeitstempel und steuerbare Sichtbarkeit.
      2. Studierende (Melder der Meldung) loggt sich ein und fügt eine Antwort hinzu.
         → Erwartung: Antwort, Zeitstempel, Sichtbarkeit gespeichert und mit Kommentar verknüpft.
      3. Negativfall: Antwort mit leerem Textfeld.
         → Erwartung: Keine Speicherung, Flash-Meldung.
    '''
    modul = Modul("Testmodul")
    lehrende = Lehrende("Lehrkraft", "l@l.org", "passwort123")
    lehrende.module.append(modul)
    student = Studierende("Student", "student@test.org", "pw123")
    meldung = Meldung("Fehler im Modul", Kategorie.ONLINETESTS, student, modul)

    session.add_all([modul, student, lehrende, meldung])
    session.commit()

    # Login als Lehrende
    client.post("/login",
        data={
            "email": "l@l.org",
            "passwort": "passwort123"
            },
        follow_redirects=True
    )

    # Kommentar eines Lehrenden hinzufügen #####
    client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
            "status": "OFFEN",
            "kommentar": "Feedback von Lehrenden",
            "sichtbarkeit": "PRIVAT"            
            },
        follow_redirects=True
    )

    # Lehrenden-Kommentar aus DB holen
    kommentar = session.execute(
        select(Kommentar).filter_by(meldung_id=meldung.id)
        ).scalars().first()

    assert kommentar is not None
    assert isinstance(kommentar.zeitstempel, datetime)
    assert kommentar.sichtbarkeit == Sichtbarkeit.PRIVAT

    # Login als Student (Ersteller der Meldung)
    client.post("/login",
        data={
            "email": "student@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    # Antwort des Studierenden hinzufügen #####
    response = client.post(f"/antwort_speichern/{kommentar.id}",
        data={
            "antwort_text": "Danke für die Rückmeldung!"
            },
        follow_redirects=True
    )
    assert response.status_code == 200

    session.refresh(kommentar)

    # Erwartung: Antwort ist gespeichert
    assert any("Danke für die Rückmeldung!" in a.text for a in kommentar.antworten)

    antwort = kommentar.antworten[-1] # letzte Antwort
    assert isinstance(antwort.zeitstempel, datetime)
    assert antwort.sichtbarkeit == Sichtbarkeit.PRIVAT
    assert "Danke für die Rückmeldung!" in antwort.text
    assert antwort.antwort_auf == kommentar

    # Versuch Kommentar mit leerem Textfeld hinzuzufügen #####
    response = client.post(f"/antwort_speichern/{kommentar.id}",
        data={
            "antwort_text": ""
            },
        follow_redirects=True
    )
    assert response.status_code == 200

    session.refresh(kommentar)

    # Prüfen ob erwartete Flash-Meldung gesetzt wird
    html = response.data.decode("utf-8")
    assert "Antwort darf nicht leer sein." in html


@pytest.mark.id_T26
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F05
def test_antwort_speichern_nicht_melder_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-05 Kommentarfunktion / Antworten)

    - Prüft, dass nur der Melder einer Meldung antworten darf.
    - Szenarien:
      1. Lehrende erstellt einen Kommentar zu einer Meldung.
      2. Anderer Studierender (nicht der Melder) versucht zu antworten.
      3. Erwartung: Keine Antwort gespeichert, Flash-Meldung.
    '''
    modul = Modul("Testmodul")
    lehrende = Lehrende("Lehrkraft", "l@l.org", "pw123")
    student_melder = Studierende("Melder", "melder@test.org", "pw123")
    student_andere = Studierende("Anderer", "anderer@test.org", "pw123")
    meldung = Meldung("Fehler im Modul", Kategorie.ONLINETESTS, student_melder, modul)
    kommentar = Kommentar("Feedback von Lehrenden",
                          meldung=meldung,
                          sichtbarkeit=Sichtbarkeit.ÖFFENTLICH,
                          verfasser="Lehrkraft",
                          lehrende=lehrende
                          )

    session.add_all([modul, lehrende, student_melder, student_andere, meldung, kommentar])
    session.commit()

    # Login als anderer Student (nicht Melder)
    client.post("/login",
        data={
            "email": "anderer@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    # Versuch zu antworten
    response = client.post(f"/antwort_speichern/{kommentar.id}",
        data={
            "antwort_text": "Ich antworte trotzdem!"
            },
        follow_redirects=True
    )
    assert response.status_code == 200

    session.refresh(kommentar)
    # Erwartung: Keine Antwort gespeichert
    assert not any("Ich antworte trotzdem!" in a.text for a in kommentar.antworten)

    # Prüfen ob erwartete Flash-Meldung gesetzt wird
    html = response.data.decode("utf-8")
    assert "Nur Melder darf antworten." in html


@pytest.mark.id_T65
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F08
def test_benutzer_erstellen(client, session):
    '''
    Testart: Systemtest
    Testkatekorie: Funktionstest (F-08 Rollen- und Rechteverwaltung)
    
    - Prüft, dass nur Admin über Formular zum Erstellen eines neuen Benutzers sehen darf.
    - Erwartung: HTML enthält Überschrift und Formularfelder.
    '''
    admin = Admin("Administrator", "admin@example.org", "sicheresPW123")
    lehrende = Lehrende("Tutor", "tutor@example.org", "pw123")
    session.add_all([admin, lehrende])
    session.commit()

    # Login als Admin
    client.post("/login",
        data={
            "email": "admin@example.org", 
            "passwort": "sicheresPW123"
            },
        follow_redirects=True
    )

    response = client.get("/benutzer_erstellen", follow_redirects=True)
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    # Prüfen, ob Überschrift und Formular enthalten sind
    assert all(text in html for text in [
        "Neuen Benutzer anlegen",
        '<form method="post" action="/benutzer_speichern">', 
        "Name:", 
        "E-Mail", 
        "Rolle:",
        "Passwort:",
        "Benutzer speichern"
        ]
    )

    # Login als Lehrende (nicht Admin)
    client.post("/login",
        data={
            "email": "tutor@example.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.get("/benutzer_erstellen", follow_redirects=False)

    # Erwartung: Redirect zur Übersicht
    assert response.status_code == 302
    assert "/uebersicht" in response.headers["Location"]


@pytest.mark.id_T36
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_F08
def test_benutzer_speichern_admin(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-06 Benutzerverwaltung, F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass Admin über Controller neuen Benutzer anlegen kann.
    - Erwartung: Benutzer wird gespeichert und ist abrufbar.
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    session.add(admin)
    session.commit()

    client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )
    response = client.post("/benutzer_speichern",
        data={
            "name": "Neu", 
            "email": "neu@test.org", 
            "rolle": "STUDIERENDE",
            "passwort": "passwort123"
            },
        follow_redirects=True
    )
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert all(text in html for text in ["Benutzer", "Neu", "als", "hinzugefügt."])

    assert session.execute(select(Benutzer).filter_by(email="neu@test.org")).scalars().one()


@pytest.mark.id_T37
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_F08
def test_benutzer_speichern_nicht_admin_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-06 Benutzerverwaltung, F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass Nicht-Admins keine Benutzer anlegen dürfen.
    - Erwartung: Keine Speicherung, Flash "Keine Berechtigung".
    '''
    student = Studierende("Student", "student@test.org", "pw123")
    session.add(student)
    session.commit()

    client.post("/login",
        data={
            "email": "student@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=False
    )
    response = client.post("/benutzer_speichern",
        data={
            "name": "Neu", 
            "email": "neu@test.org", 
            "passwort": "pw12345", 
            "rolle": "STUDIERENDE"
            },
        follow_redirects=False
    )
    # Erwartung: Redirect zur Übersicht
    assert "/uebersicht" in response.headers["Location"]
    assert response.status_code == 302

    # Erwartung: Benutzer nicht gespeichert
    assert session.execute(
        select(Benutzer).filter_by(email="neu@test.org")
        ).scalars().first() is None


@pytest.mark.id_T66
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F08
def test_benutzer_loeschen_admin(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass ein Admin einen Benutzer löschen darf.
    - Erwartung: Flash-Meldung.
    - Erwartung: Der gelöschte Benutzer ist nicht mehr in der Datenbank vorhanden.
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    student = Studierende("Student", "student@test.org", "pw123")
    session.add_all([admin, student])
    session.commit()

    # Login als Admin
    client.post("/login",
        data={
            "email": "admin@test.org",
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/benutzer_loeschen",
        data={
            "benutzer_id": student.id
            },
        follow_redirects=True
    )
    html = response.data.decode("utf-8")
    assert "Benutzer Student gelöscht." in html
    # Student ist entfernt
    assert session.execute(
        select(Studierende).filter_by(email="student@test.org")
        ).scalars().first() is None


@pytest.mark.id_T67
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F08
def test_benutzer_loeschen_nicht_admin_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass ein Nicht-Admin keine Benutzer löschen darf.
    - Erwartung: Flash-Meldung "Keine Berechtigung." erscheint.
    - Erwartung: Der angegebene Admin bleibt in der Datenbank erhalten.
    '''
    student = Studierende("Student", "student@test.org", "pw123")
    admin = Admin("Admin", "admin@test.org", "pw123")
    admin2 = Admin("Admin2", "admin2@test.org", "pw123")
    session.add_all([student, admin, admin2])
    session.commit()

    # Login als Student
    client.post("/login",
        data={
            "email": "student@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/benutzer_loeschen",
        data={
            "benutzer_id": admin.id
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Keine Berechtigung." in html
    # Admin bleibt erhalten
    assert session.execute(
        select(Admin).filter_by(email="admin@test.org")
        ).scalars().first() is not None


@pytest.mark.id_T68
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F08
def test_admin_selbst_loeschen_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass ein Admin sich nicht selbst löschen darf.
    - Erwartung: Flash-Meldung "Nicht erlaubt, sich selbst zu löschen!" erscheint.
    - Erwartung: Der Admin bleibt in der Datenbank erhalten.
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    admin2 = Admin("Admin2", "admin2@test.org", "pw123")
    session.add_all([admin, admin2])
    session.commit()

    # Login als Admin
    client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/benutzer_loeschen",
        data={
            "benutzer_id": admin.id
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Nicht erlaubt, sich selbst zu löschen!" in html
    # Admin bleibt erhalten
    assert session.execute(
        select(Admin).filter_by(email="admin@test.org")
        ).scalars().first() is not None


@pytest.mark.id_T69
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F08
def test_letzten_admin_loeschen_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass der letzte verbleibende Admin nicht gelöscht werden darf.
    - Erwartung: Flash-Meldung "Mindestens ein Admin muss erhalten bleiben." erscheint.
    - Erwartung: Der Admin bleibt in der Datenbank erhalten.
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    session.add(admin)
    session.commit()

    # Login als Admin
    client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/benutzer_loeschen",
        data={
            "benutzer_id": admin.id
            },
        follow_redirects=True
        )

    html = response.data.decode("utf-8")
    assert "Mindestens ein Admin muss erhalten bleiben." in html
    # Admin bleibt erhalten
    assert session.execute(
        select(Admin).filter_by(email="admin@test.org")
        ).scalars().first() is not None


@pytest.mark.id_T38
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_F08
def test_modul_aktion(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-06 Modulzuordnung, F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass Admin Lehrenden Module zuordnen darf.
    - Erwartung: Flash-Meldung "Modul wurde zugewiesen."
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    lehrende = Lehrende("Lehrkraft", "lehrende@test.org", "pw123")
    modul = Modul("Testmodul")
    session.add_all([admin, lehrende, modul])
    session.commit()

    client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )
    response = client.post("/modul_aktion",
        data={
            "lehrende_id": lehrende.id, 
            "modul_id": modul.id, 
            "aktion": "zuweisen"
            },
        follow_redirects=True
    )
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert all(text in html for text in ["Modul", "wurde", "zugewiesen."])

    # Erwartung: Modul ist zugewiesen
    session.refresh(lehrende)
    assert modul in lehrende.module


@pytest.mark.id_T39
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_F08
def test_modul_aktion_entziehen(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-06 Modulzuordnung, F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass Admin Lehrenden ein Modul entziehen darf.
    - Erwartung: Flash-Meldung "Modul ... wurde ... entzogen."
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    lehrende = Lehrende("Lehrkraft", "lehrende@test.org", "pw123")
    modul = Modul("Testmodul")
    lehrende.module.append(modul)
    session.add_all([admin, lehrende, modul])
    session.commit()

    # Login als Admin
    client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/modul_aktion",
        data={
            "lehrende_id": lehrende.id, 
            "modul_id": modul.id, 
            "aktion": "entziehen"
            },
        follow_redirects=True
    )
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert all(text in html for text in ["Modul", "wurde", "entzogen."])

    # Erwartung: Modul ist entzogen
    session.refresh(lehrende)
    assert modul not in lehrende.module


@pytest.mark.id_T40
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_F08
def test_modul_aktion_nicht_admin_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-06 Modulzuordnung, F-08 Rollen- und Rechteverwaltung)

    - Prüft, dass Nicht-Admins keine Module zuweisen dürfen.
    - Erwartung: Redirect zur Übersicht + Flash "Keine Berechtigung."
    '''
    student = Studierende("Student", "student@test.org", "pw123")
    lehrende = Lehrende("Lehrkraft", "lehrende@test.org", "pw123")
    modul = Modul("Testmodul")
    session.add_all([student, lehrende, modul])
    session.commit()

    # Login als Student
    client.post("/login",
        data={
            "email": "student@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/modul_aktion",
        data={
            "lehrende_id": lehrende.id, 
            "modul_id": modul.id, 
            "aktion": "zuweisen"
            },
        follow_redirects=True
    )
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Keine Berechtigung." in html

    # Erwartung: Modul nicht zugewiesen
    session.refresh(lehrende)
    assert modul not in lehrende.module


@pytest.mark.id_T41
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_benutzer_speichern_gleiche_email_verboten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-06 Benutzerverwaltung)

    - Prüft, dass Admin keine Benutzer mit doppelter Email anlegen darf.
    - Erwartung: Flash-Meldung "Benutzer mit dieser Email existiert bereits."
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    existing = Studierende("Alt", "alt@test.org", "pw123")
    session.add_all([admin, existing])
    session.commit()

    # Login als Admin
    client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/benutzer_speichern",
        data={
            "name": "Neu",
            "email": "alt@test.org",  # gleiche Email
            "passwort": "pw123456",
            "rolle": "STUDIERENDE"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Benutzer mit dieser Email existiert bereits." in html


@pytest.mark.id_T42
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_benutzer_speichern_passwort_zu_kurz(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktionstest (F-06 Benutzerverwaltung)

    - Prüft, dass Admin keinen Benutzer mit zu kurzem Passwort anlegen darf.
    - Erwartung: Flash-Meldung "Passwort muss mindestens 6 Zeichen lang sein."
    '''
    admin = Admin("Admin", "admin@test.org", "pw123")
    session.add(admin)
    session.commit()

    # Login als Admin
    client.post("/login",
        data={
            "email": "admin@test.org", 
            "passwort": "pw123"
            },
        follow_redirects=True
    )

    response = client.post("/benutzer_speichern",
        data={
            "name": "Neu",
            "email": "neu@test.org",
            "passwort": "123456",  # zu kurz (nicht 7 Zeichen)
            "rolle": "STUDIERENDE"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Passwort muss mindestens 7 Zeichen lang sein." in html

    # Erwartung: Benutzer nicht gespeichert
    assert session.execute(
        select(Benutzer).filter_by(email="neu@test.org")
        ).scalars().first() is None


@pytest.mark.id_T75
@pytest.mark.integration
@pytest.mark.requirement_NF09
def test_render_db_url(monkeypatch):
    '''
    Testart: Integrationstest
    Testkategorie: Konfigurations-/Umgebungsvariable (NF-09 Wartbarkeit)

    - Prüft, dass bei gesetzter RENDER-Umgebungsvariable die Render-DB-URL übernommen wird.
    - Erwartung: DB_URL befinnt entsprechend gesetzter DATABASE_URL.
    '''
    # Umgebung simulieren
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.setenv(
        "DATABASE_URL", 
        "postgresql://korrektur_system_db_user:abc12&@d/korrektur_system_db"
    )

    # Modul neu laden, damit die Bedingung ausgeführt wird
    controller = importlib.reload(importlib.import_module("controller"))

    assert controller.DB_URL == "postgresql://korrektur_system_db_user:abc12&@d/korrektur_system_db"


@pytest.mark.id_T71
@pytest.mark.integration
@pytest.mark.requirement_NF06
def test_load_user_returns_correct_user(app_context, session):
    '''
    Testart: Integrationstest
    Testkategorie: Authentifizierung (NF-06 Authentifizierung)

    - Prüft, dass load_user() den richtigen Benutzer zurückgibt.
    - Erwartung: Benutzer mit gegebener ID wird geladen.
    '''
    # Benutzer anlegen
    benutzer = Benutzer(name="TestUser", email="test@example.com", passwort="pw123")
    session.add(benutzer)
    session.commit()

    # load_user direkt aufrufen
    loaded = load_user(benutzer.id)

    assert loaded.id == benutzer.id
    assert loaded.name == "TestUser"

@pytest.mark.id_T70
@pytest.mark.system
@pytest.mark.requirement_NF01
@pytest.mark.requirement_NF02
def test_index_leitet_zu_login(client):
    '''
    Testart: Systemtest
    Testkategorie: Usability (NF-01 Browser-Zugänglichkeit, NF-02 Intuitive Oberfläche)

    - Prüft, dass die Startseite "/" erreichbar ist.
    - Erwartung: Redirect zur Login-Seite.
    '''
    response = client.get("/", follow_redirects=False)

    # Statuscode für Redirect
    assert response.status_code == 302
    # Ziel-Location prüfen
    assert "/login" in response.headers["Location"]


@pytest.mark.id_T72
@pytest.mark.system
@pytest.mark.requirement_NF06
def test_login_rendert_login_seite(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Authentifizierung (NF-06 Sicherheit)

    - Prüft, dass ein GET-Request auf /login die Login-Seite rendert.
    - Erwartung: Statuscode 200, HTML enthält Formular.
    '''
    response = client.get("/login")
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "<h2>Login</h2>" in html  # grober Check: Formular vorhanden
    assert "E-Mail:" in html
    assert "Passwort:" in html
    assert "Einloggen" in html

@pytest.mark.id_T73
@pytest.mark.system
@pytest.mark.requirement_NF06
def test_login_flasche_zugangsdaten(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Authentifizierung (NF-06 Sicherheit)

    - Prüft, dass bei falschen Zugangsdaten eine Fehlermeldung erscheint.
    - Erwartung: Flash "Login fehlgeschlagen", Seite bleibt /login.
    '''
    # POST mit falschen Daten
    response = client.post("/login",
        data={"email": "falsch@example.org", "passwort": "falsch"},
        follow_redirects=True
    )

    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "Login" in html
    assert "Login fehlgeschlagen" in html


@pytest.mark.id_T74
@pytest.mark.system
@pytest.mark.requirement_NF06
@pytest.mark.requirement_NF11
def test_logout_weiterleitung_und_flashes(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Authentifizierung (NF-06 Sicherheit), Zuverlässigkeit (NF-11)

    - Prüft, dass ein Logout den Benutzer abmeldet.
    - Erwartung: Redirect zur Login-Seite und Flash-Meldung.
    '''
    # Testbenutzer anlegen und einloggen
    benutzer = Benutzer(name="TestNutzer", email="test@example.org", passwort="sicher")
    session.add(benutzer)
    session.commit()

    # Login simulieren
    client.post("/login", data={"email": "test@example.org", "passwort": "sicher"})

    # Logout aufrufen
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "Erfolgreich ausgeloggt." in html
    assert "<h2>Login</h2>" in html

    with client.session_transaction() as session:
        assert "_user_id" not in session

@pytest.mark.id_T09
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F02
@pytest.mark.requirement_NF11
def test_meldung_anzeigen_ohne_meldungen(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktion (F-02 Meldung anzeigen), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass Fehlerfall erreicht wird, wenn keine Meldung vorhanden ist.
    - Erwartung: Seite rendert trotzdem.
    - Flash-Meldung und Redirect zur Übersicht bei Aufruf über URL.
    '''
    # Benutzer anlegen
    benutzer = Benutzer(name="Test Nutzer", email="test@example.org", passwort="geheim")
    session.add(benutzer)
    session.commit()

    # Login simulieren
    client.post("/login", data={"email": "test@example.org", "passwort": "geheim"})

    # Übersicht ohne Meldungen
    response = client.get("/uebersicht", follow_redirects=True)
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    for text in [
        "Keine Meldungen vorhanden.",
        "Meldungen von",
        "Module:",
        "Status:",
        "Kategorie:",
        "Filter anwenden"
    ]:
        assert text in html

    # Direkter URL-Aufruf einer nicht existierenden Meldung
    response = client.get("/meldung/9999", follow_redirects=True)
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "Das ist nicht erlaubt." in html


@pytest.mark.id_T18
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
@pytest.mark.requirement_NF11
def test_status_aendern_meldung_nicht_vorhanden(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-04 Status ändern), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass ein Statuswechsel auf eine nicht existierende Meldung korrekt abgefangen wird.
    - Erwartung: Redirect zur Übersicht, Meldung "Keine Meldungen vorhanden." erscheint.
    '''
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    session.add(lehrender)
    session.commit()

    client.post("/login", data={"email": "dozent@example.org", "passwort": "secret"})

    response = client.post("/meldung/9999/status_aendern",
        data={
            "status":"BEARBEITUNG",
            "kommentar":"",
            "sichtbarkeit":"PRIVAT"
            },
        follow_redirects=True
        )

    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "Keine Meldungen vorhanden." in html


@pytest.mark.id_T19
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
@pytest.mark.requirement_NF07
def test_status_aendern_nur_lehrende(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-04 Status ändern), Sicherheit (NF-07 Rollenbasierte Rechtevergabe)

    - Prüft, dass Studierende den Status einer Meldung nicht ändern dürfen.
    - Erwartung: Fehlermeldung "Nur Lehrende dürfen den Status ändern." erscheint im Formular.
    '''
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul)
    session.add_all([student, modul, meldung])
    session.commit()

    client.post("/login", data={"email": "stud@example.org", "passwort": "secret"})

    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
            "status":"BEARBEITUNG",
            "kommentar":"",
            "sichtbarkeit":"PRIVAT"
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Nur Lehrende dürfen den Status ändern." in html


@pytest.mark.id_T20
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
@pytest.mark.requirement_NF07
def test_status_aendern_fremdes_modul(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-04 Status ändern), Sicherheit (NF-07 Rollenbasierte Rechtevergabe)

    - Prüft, dass ein Lehrender den Status einer Meldung in einem fremden Modul
      nicht ändern darf.
    - Erwartung: Fehlermeldung "Dies ist nur für Meldungen eigener Module möglich."
      erscheint im Formular.
    '''
    modul1 = Modul(titel="Eigenes Modul")
    modul2 = Modul(titel="Fremdes Modul")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="unkreativ")
    lehrender.module.append(modul1)
    student = Studierende("Student", "s@t.udent", "d!3s_15t-S1(h9R?")
    meldung = Meldung("Testmeldung", Kategorie.ONLINESKRIPT, student, modul2)
    session.add_all([lehrender, modul1, modul2, meldung])
    session.commit()

    client.post("/login", data={"email": "dozent@example.org", "passwort": "unkreativ"})

    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
            "status":"BEARBEITUNG",
            "kommentar":"",
            "sichtbarkeit":"PRIVAT"},
        follow_redirects=True)
    html = response.data.decode("utf-8")
    assert "Dies ist nur für Meldungen eigener Module möglich." in html


@pytest.mark.id_T21
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
def test_status_aendern_erlaubt_ohne_kommentar(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-04 Status ändern)

    - Prüft, dass ein Lehrender den Status einer Meldung von "offen" auf "in Bearbeitung"
      ändern kann, auch wenn kein Kommentar angegeben wird.
    - Erwartung: Meldung "Status ohne Kommentar zu \"in Bearbeitung\" gewechselt."
      erscheint im Formular.
    '''
    modul = Modul(titel="Testmodul")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    lehrender.module.append(modul)
    student = Studierende("Student", "s@t.udent", "d!3s_15t-S1(h9R?")
    meldung = Meldung("Testmeldung", Kategorie.MUSTERKLAUSUR, student, modul)
    session.add_all([lehrender, modul, meldung])
    session.commit()

    client.post("/login", data={"email": "dozent@example.org", "passwort": "secret"})

    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
            "status":"BEARBEITUNG",
            "kommentar":"",
            "sichtbarkeit":"PRIVAT"
            },
        follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Status ohne Kommentar zu &#34;in Bearbeitung&#34; gewechselt." in html


@pytest.mark.id_T22
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
def test_status_aendern_erlaubt_mit_kommentar(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-04 Status ändern)

    - Prüft, dass ein Lehrender den Status einer Meldung von "offen" auf "in Bearbeitung"
      ändern und gleichzeitig einen privaten Kommentar hinzufügen kann.
    - Erwartung: 
        Meldung "Neuen privaten Kommentar hinzugefügt und Status zu \"in Bearbeitung\" gewechselt."
        erscheint im Formular.
    '''
    modul = Modul(titel="Testmodul")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    lehrender.module.append(modul)
    student = Studierende("Student", "s@t.udent", "d!3s_15t-S1(h9R?")
    meldung = Meldung("Testmeldung", Kategorie.PDFSKRIPT, student, modul)
    session.add_all([lehrender, modul, meldung])
    session.commit()

    client.post("/login", data={"email": "dozent@example.org", "passwort": "secret"})

    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={"status":"BEARBEITUNG",
              "kommentar":"Bitte prüfen",
              "sichtbarkeit":"PRIVAT"},
        follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Neuen privaten Kommentar hinzugefügt und Status zu &#34;in Bearbeitung&#34; gewechselt." in html


@pytest.mark.id_T27
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F05
def test_status_aendern_nur_kommentar(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-05 Kommentarfunktion)

    - Prüft, dass ein Lehrender einen privaten Kommentar hinzufügen kann,
      ohne den Status der Meldung zu ändern.
    - Erwartung: Meldung "Neuen privaten Kommentar ohne Statuswechsel hinzugefügt."
      erscheint im Formular.
    '''
    modul = Modul(titel="Testmodul")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    lehrender.module.append(modul)
    student = Studierende("Student", "s@t.udent", "d!3s_15t-S1(h9R?")
    meldung = Meldung("Testmeldung", Kategorie.VIDEO, student, modul)
    session.add_all([lehrender, modul, meldung])
    session.commit()

    client.post("/login", data={"email": "dozent@example.org", "passwort": "secret"})

    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
            "status":"OFFEN",
            "kommentar":"Nur Kommentar",
            "sichtbarkeit":"PRIVAT"},
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Neuen privaten Kommentar ohne Statuswechsel hinzugefügt." in html


@pytest.mark.id_T23
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
def test_status_aendern_keine_aenderung(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-04 Status ändern)

    - Prüft, dass ein Statuswechsel ohne Änderung (Status bleibt "OFFEN" und kein Kommentar)
      korrekt abgefangen wird.
    - Erwartung: Fehlermeldung "Status nicht gewechselt." erscheint im Formular.
    '''
    modul = Modul(titel="Testmodul")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    lehrender.module.append(modul)
    student = Studierende("Student", "s@t.udent", "d!3s_15t-S1(h9R?")
    meldung = Meldung("Testmeldung", Kategorie.FOLIENSÄTZE, student, modul)
    session.add_all([lehrender, modul, meldung])
    session.commit()

    client.post("/login", data={"email": "dozent@example.org", "passwort": "secret"})

    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
            "status":"OFFEN",
            "kommentar":"",
            "sichtbarkeit":"PRIVAT"},
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Status nicht gewechselt." in html

@pytest.mark.id_T24
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F04
def test_status_aendern_nicht_erlaubt(client, session):
    '''
    Testart: Systemtest
    Testkategorie: Funktional (F-04 Status ändern)

    - Prüft, dass ein unzulässiger Statuswechsel (von "offen" zu "abgeschlossen")
      korrekt abgefangen wird.
    - Erwartung: Fehlermeldung "Statuswechsel von \"offen\" zu \"abgeschlossen\" ist nicht erlaubt."
      erscheint im Formular.
    '''
    modul = Modul(titel="Testmodul")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    lehrender.module.append(modul)
    student = Studierende("Student", "s@t.udent", "d!3s_15t-S1(h9R?")
    meldung = Meldung("Testmeldung", Kategorie.MUSTERKLAUSUR, student, modul)
    session.add_all([lehrender, modul, meldung])
    session.commit()

    client.post("/login", data={"email": "dozent@example.org", "passwort": "secret"})

    response = client.post(f"/meldung/{meldung.id}/status_aendern",
        data={
            "status":"GESCHLOSSEN",
            "kommentar":"",
            "sichtbarkeit":"PRIVAT"},
        follow_redirects=True
        )

    html = response.data.decode("utf-8")
    assert "Statuswechsel von &#34;offen&#34; zu &#34;abgeschlossen&#34; ist nicht erlaubt." in html

@pytest.mark.id_T02
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F01
def test_meldung_erstellen_get(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-01 Meldung erfassen)

    - Prüft, dass die Route /meldung/neu per GET erreichbar ist.
    - Erwartung: Formular "Neue Meldung erstellen" wird angezeigt (Statuscode 200).
    """
    benutzer = Studierende(name="Student", email="stud@example.org", passwort="secret")
    session.add(benutzer)
    session.commit()

    client.post("/login", data={"email":"stud@example.org","passwort":"secret"})

    response = client.get("/meldung/neu")
    assert response.status_code == 200

    html = response.data.decode("utf-8")
    assert "<h2>Neue Meldung erstellen</h2>" in html

@pytest.mark.id_T03
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F01
def test_meldung_erstellen_erfolg(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-01 Meldung erfassen)

    - Prüft, dass eine Meldung mit gültigen Eingaben erfolgreich erstellt wird.
    - Erwartung: Flash-Meldung "Meldung erfolgreich erstellt." erscheint nach POST.
    """
    modul = Modul(titel="Testmodul")
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    session.add_all([modul, student])
    session.commit()
    client.post("/login", data={"email":"stud@example.org","passwort":"secret"})

    response = client.post("/meldung/neu", data={
        "modul":"Testmodul",
        "kategorie":"ONLINESKRIPT",
        "beschreibung":"Fehler im Skript"
    }, follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Meldung erfolgreich erstellt." in html

@pytest.mark.id_T04
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F01
@pytest.mark.requirement_NF11
def test_meldung_erstellen_post_integrityerror(client, session, monkeypatch):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-01 Meldung erfassen), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass bei einem simulierten Datenbankfehler (IntegrityError)
      eine Flash-Meldung angezeigt wird.
    - Erwartung: Meldung "Fehler: Meldung konnte nicht gespeichert werden (Integritätsproblem)."
      erscheint im Formular.
    """
    modul = Modul(titel="Testmodul")
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    session.add_all([modul, student])
    session.commit()

    client.post("/login", data={"email":"stud@example.org","passwort":"secret"})

    # simulieren von Datenbankfehler
    def fake_erstelle_meldung(*args, **kwargs):
        raise IntegrityError("stmt", "params", "orig")

    # ersetzten der Mehtode 'erstelle_meldung' durch fake-Funktion
    monkeypatch.setattr(student, "erstelle_meldung", fake_erstelle_meldung)

    response = client.post("/meldung/neu",
        data={
            "modul":"Testmodul",
            "kategorie":"ONLINESKRIPT",
            "beschreibung":"Fehler im Skript"
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Fehler: Meldung konnte nicht gespeichert werden." in html

@pytest.mark.id_T05
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F01
@pytest.mark.requirement_NF11
def test_meldung_erstellen_post_exception(client, session, monkeypatch):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-01 Meldung erfassen), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass bei einem unerwarteten Fehler im Erstellungsprozess
      eine Flash-Meldung angezeigt wird.
    - Erwartung: Meldung "Unerwarteter Fehler: Warnung!" erscheint,
      Formular bleibt vorausgefüllt.
    """
    modul = Modul(titel="Testmodul")
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    session.add_all([modul, student])
    session.commit()
    client.post("/login", data={"email":"stud@example.org","passwort":"secret"})

    # Simulieren eines Fehlers
    def fake_erstelle_meldung(*args, **kwargs):
        raise Exception("Warnung!")

    # ersetzten der Mehtode 'erstelle_meldung' durch fake-Funktion
    monkeypatch.setattr(student, "erstelle_meldung", fake_erstelle_meldung)

    response = client.post("/meldung/neu",
        data={
            "modul":"Testmodul",
            "kategorie":"ONLINESKRIPT",
            "beschreibung":"Fehler im Skript"
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Unerwarteter Fehler: Warnung!" in html
    assert "Fehler im Skript" in html  # vorausgefülltes Feld


@pytest.mark.id_T43
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_nutzerverwaltung_redirect(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass ein POST auf /nutzerverwaltung korrekt verarbeitet wird.
    - Erwartung: Redirect zur Übersicht (/uebersicht).
    """
    # Vorbereiten: einen Lehrenden oder Admin einloggen
    admin = Lehrende(name="Admin", email="admin@example.org", passwort="secret")
    session.add(admin)
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    # POST an /nutzerverwaltung auslösen
    response = client.post("/nutzerverwaltung",
        data={
            "aktion":"speichern"   # Beispiel: irgendein Formularfeld
            },
        follow_redirects=False
    )

    # Erwartung: Redirect zur Übersicht
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/uebersicht")


@pytest.mark.id_T44
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_benutzer_speichern_fehlgeschlagen(client, session, monkeypatch):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass beim Speichern eines Benutzers mit ungültiger Rolle
      die Fehlermeldung "Benutzer hinzufügen fehlgeschlagen." angezeigt wird.
    - Erwartung: Redirect zur Nutzerverwaltung, Flash-Meldung erscheint.
    """
    # Admin vorbereiten und einloggen
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    session.add(admin)
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    # Monkeypatch: get_rolle_klasse liefert None zurück → Fehlerfall
    monkeypatch.setattr("controller.get_rolle_klasse", lambda rolle_enum: None)

    response = client.post("/benutzer_speichern",
        data={
            "name":"Testuser",
            "email":"neu@example.org",
            "rolle":"STUDIERENDE",   # gültiger Enum, aber Mapping liefert None
            "passwort":"geheim123"
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Benutzer hinzufügen fehlgeschlagen." in html


@pytest.mark.id_T45
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_benutzer_loeschen_nicht_vorhanden(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass beim Löschen eines nicht existierenden Benutzers
      die Fehlermeldung "Benutzer nicht gefunden." angezeigt wird.
    - Erwartung: Redirect zur Nutzerverwaltung, Flash-Meldung erscheint.
    """
    # Admin vorbereiten und einloggen
    admin = Admin(name="Admin", email="admin@example.org", passwort="geheim")
    session.add(admin)
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"geheim"})

    # POST mit nicht existierender Benutzer-ID
    response = client.post("/benutzer_loeschen",
        data={
            "benutzer_id": 9999  # ID existiert nicht
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Benutzer nicht gefunden." in html


@pytest.mark.id_T57
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F07
@pytest.mark.requirement_NF07
def test_module_verwalten_keine_berechtigung(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-07 Modulverwaltung), 
                   Sicherheit (NF-07 Rollenbasierte Rechtevergabe)

    - Prüft, dass ein Nicht-Admin keinen Zugriff auf die Modulverwaltung hat.
    - Erwartung: Flash-Meldung "Keine Berechtigung." erscheint.
    """
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    session.add(student)
    session.commit()

    client.post("/login", data={"email":"stud@example.org","passwort":"secret"})

    response = client.get("/module_verwalten", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert "Keine Berechtigung." in html


@pytest.mark.id_T46
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_module_verwalten_modul_erfolgreich(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Modulverwaltung)

    - Prüft, dass ein Admin ein neues Modul erfolgreich erstellen kann.
    - Erwartung: Flash-Meldung "Modul \"Testmodul\" wurde erfolgreich erstellt." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    session.add(admin)
    session.commit()
    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    response = client.post("/module_verwalten", data={"titel":"Testmodul"}, follow_redirects=True)
    html = response.data.decode("utf-8")
    assert "Modul &#34;Testmodul&#34; wurde erfolgreich erstellt." in html


@pytest.mark.id_T47
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_module_verwalten_modul_fehler(client, session, monkeypatch):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Modulverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass ein Fehler beim Erstellen eines Moduls korrekt abgefangen wird.
    - Erwartung: Flash-Meldung "Fehler: ..." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    session.add(admin)
    session.commit()
    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    # Monkeypatch: erstelle_modul wirft ValueError
    monkeypatch.setattr(Admin, "erstelle_modul", lambda self, titel: (_ for _ in ()).throw(ValueError("Titel ungültig")))

    response = client.post("/module_verwalten", data={"titel":"FehlerModul"}, follow_redirects=True)
    html = response.data.decode("utf-8")
    assert "Fehler: Titel ungültig" in html


@pytest.mark.id_T58
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F07
@pytest.mark.requirement_NF07
def test_modul_loeschen_keine_berechtigung(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-07 Modulverwaltung), 
                   Sicherheit (NF-07 Rollenbasierte Rechtevergabe)

    - Prüft, dass ein Nicht-Admin kein Modul löschen darf.
    - Erwartung: Flash-Meldung "Keine Berechtigung." erscheint.
    """
    student = Studierende(name="Student", email="stud@example.org", passwort="secret")
    session.add(student)
    session.commit()

    client.post("/login", data={"email":"stud@example.org","passwort":"secret"})

    response = client.post("/modul_loeschen", data={"modul_id": 1}, follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Keine Berechtigung." in html


@pytest.mark.id_T59
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F07
def test_modul_loeschen_erfolgreich(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-07 Modulverwaltung)

    - Prüft, dass ein Admin ein existierendes Modul löschen kann.
    - Erwartung: Flash-Meldung "Modul \"Testmodul\" gelöscht" erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    session.add_all([admin, modul])
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    response = client.post("/modul_loeschen", data={"modul_id": modul.id}, follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Modul &#34;Testmodul&#34; gelöscht" in html


@pytest.mark.id_T60
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F07
@pytest.mark.requirement_NF11
def test_modul_loeschen_nicht_vorhanden(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-07 Modulverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass beim Löschen eines nicht existierenden Moduls
      die Fehlermeldung "Modul nicht gefunden." angezeigt wird.
    - Erwartung: Redirect zur Modulverwaltung, Flash-Meldung erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    session.add(admin)
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    response = client.post("/modul_loeschen", data={"modul_id": 9999}, follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Modul nicht gefunden." in html


@pytest.mark.id_T48
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_modul_aktion_keine_module(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass bei fehlenden Modulen die Meldung "Bitte zuerst Module anlegen." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    session.add(admin)
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    # POST ohne modul_id, keine Module in DB
    response = client.post("/modul_aktion", data={"lehrende_id":1}, follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Bitte zuerst Module anlegen." in html


@pytest.mark.id_T49
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_modul_aktion_modul_nicht_vorhanden(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass beim Zuweisen eines nicht existierenden Moduls
      die Meldung "Lehrende oder Modul nicht gefunden." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    session.add_all([admin, lehrender])
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    response = client.post("/modul_aktion",
        data={
            "lehrende_id": lehrender.id,
            "modul_id": 9999,   # Modul existiert nicht
            "aktion": "zuweisen"
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Lehrende oder Modul nicht gefunden." in html


@pytest.mark.id_T50
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_modul_aktion_modul_nicht_ausgewaehlt(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung)

    - Prüft, dass bei vorhandenen Modulen, aber fehlender Auswahl
      die Meldung "Bitte zuerst Modul auswählen." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    session.add_all([admin, modul])
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    # POST ohne modul_id, aber Modul existiert
    response = client.post("/modul_aktion", data={"lehrende_id":1}, follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Bitte zuerst Modul auswählen." in html


@pytest.mark.id_T51
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_modul_aktion_lehrende_nicht_vorhanden(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass beim Zuweisen eines Moduls an einen nicht existierenden Lehrenden
      die Meldung "Lehrende oder Modul nicht gefunden." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    session.add_all([admin, modul])
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    response = client.post("/modul_aktion", data={
        "lehrende_id": 9999,   # Lehrende existiert nicht
        "modul_id": modul.id,
        "aktion": "zuweisen"
    }, follow_redirects=True)

    html = response.data.decode("utf-8")
    assert "Lehrende oder Modul nicht gefunden." in html


@pytest.mark.id_T52
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_modul_aktion_modul_bereits_zugewiesen(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung)

    - Prüft, dass beim erneuten Zuweisen eines bereits zugewiesenen Moduls
      die Meldung "Modul bereits zugewiesen." erscheint.
    """
    # Admin und Lehrender vorbereiten
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")

    # Modul initial zuweisen
    lehrender.module.append(modul)
    session.add_all([admin, lehrender, modul])
    session.commit()

    # Admin einloggen
    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    # Erneut zuweisen → sollte Flash "Modul bereits zugewiesen." auslösen
    response = client.post("/modul_aktion",
        data={
            "lehrende_id": lehrender.id,
            "modul_id": modul.id,
            "aktion": "zuweisen"
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Modul bereits zugewiesen." in html


@pytest.mark.id_T53
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_modul_aktion_modul_war_nicht_zugewiesen(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung)

    - Prüft, dass beim Entziehen eines nicht zugewiesenen Moduls
      die Meldung "Modul war nicht zugewiesen." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    session.add_all([admin, lehrender, modul])
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    response = client.post("/modul_aktion",
        data={
            "lehrende_id": lehrender.id,
            "modul_id": modul.id,
            "aktion": "entziehen"   # Modul wurde nie zugewiesen
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Modul war nicht zugewiesen." in html


@pytest.mark.id_T54
@pytest.mark.system
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_modul_aktion_ungueltige_aktion(client, session):
    """
    Testart: Systemtest
    Testkategorie: Funktional (F-06 Benutzerverwaltung)

    - Prüft, dass bei einer ungültigen Aktion die Meldung "Ungültige Aktion." erscheint.
    """
    admin = Admin(name="Admin", email="admin@example.org", passwort="secret")
    lehrender = Lehrende(name="Dozent", email="dozent@example.org", passwort="secret")
    modul = Modul(titel="Testmodul")
    session.add_all([admin, lehrender, modul])
    session.commit()

    client.post("/login", data={"email":"admin@example.org","passwort":"secret"})

    response = client.post("/modul_aktion",
        data={
            "lehrende_id": lehrender.id,
            "modul_id": modul.id,
            "aktion": "falsch"   # ungültige Aktion
            },
        follow_redirects=True
    )

    html = response.data.decode("utf-8")
    assert "Ungültige Aktion." in html
