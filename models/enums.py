from enum import Enum

# Zugriff auf enums z.B.: 
# from models.enums import Sichtbarkeit
# Als parameter übergeben: Sichtbarkeit.PRIVAT
# String erhalten: sichtbarkeit.value


class Sichtbarkeit(Enum):
    '''
    Definiert die Sichtbarkeit von Kommentaren oder Meldungen im System.

    Werte:
        ÖFFENTLICH (str): Kommentar/Meldung ist für alle sichtbar.
        PRIVAT (str): Kommentar/Meldung ist nur für bestimmte Rollen oder den Ersteller sichtbar.
    '''
    ÖFFENTLICH = "öffentlich"
    PRIVAT = "privat"

class Status(Enum):
    '''
    Definiert den Bearbeitungsstatus einer Meldung.

    Werte:
        OFFEN (str): Meldung wurde erstellt und ist noch unbearbeitet.
        BEARBEITUNG (str): Meldung befindet sich in Bearbeitung.
        GESCHLOSSEN (str): Meldung wurde abgeschlossen.
    '''
    OFFEN = "offen"
    BEARBEITUNG = "in Bearbeitung"
    GESCHLOSSEN = "abgeschlossen"

class Kategorie(Enum):
    '''
    Definiert die Kategorien, in die Meldungen eingeordnet werden können.

    Werte:
        ONLINESKRIPT (str): Meldung bezieht sich auf ein Online-Skript.
        PDFSKRIPT (str): Meldung bezieht sich auf ein PDF-Skript.
        VIDEO (str): Meldung bezieht sich auf ein Video.
        ONLINETESTS (str): Meldung bezieht sich auf Online-Tests.
        MUSTERKLAUSUR (str): Meldung bezieht sich auf eine Musterklausur.
        FOLIENSÄTZE (str): Meldung bezieht sich auf Foliensätze.
        # Erweiterbar um weitere Kategorien.
    '''
    ONLINESKRIPT = "Online Skript"
    PDFSKRIPT = "PDF-Skript"
    VIDEO = "Video"
    ONLINETESTS = "Online Tests"
    MUSTERKLAUSUR = "Musterklausur"
    FOLIENSÄTZE = "Foliensätze"

class Benutzer_rolle(Enum):
    '''
    Definiert die Rollen von Benutzern im System.

    Werte:
        STUDIERENDE (str): Rolle für Studierende.
        LEHRENDE (str): Rolle für Lehrende.
        ADMIN (str): Rolle für Administratoren.
        - Erweiterbar um weitere Rollen.
    '''
    STUDIERENDE = "Studierende"
    LEHRENDE = "Lehrende"
    ADMIN = "Admin"
