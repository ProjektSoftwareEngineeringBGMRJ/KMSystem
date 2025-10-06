from enum import Enum

# Zugriff: 
# from models.enums import Sichtbarkeit
# Als parameter übergeben: Sichtbarkeit.PRIVAT
# String erhalten: sichtbarkeit.value
 
class Sichtbarkeit(Enum):
    ÖFFENTLICH = "öffentlich"
    PRIVAT = "privat"
    
class Status(Enum):
    OFFEN = "offen"
    BEARBIETUNG = "in Bearbeitung"
    GESCHLOSSEN = "geschlossen"
    
class Kategorie(Enum):
    ONLINESKRIPT = "Online Skript"
    PDFSKRIPT = "PDF-Skript"
    VIDEO = "Video"
    ONLINETESTS = "Online Tests"
    MUSTERKLAUSUR = "Musterklausur"
    FOLIENSÄTZE = "Foliensätze"
    # weitere.....