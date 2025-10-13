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
    BEARBEITUNG = "in Bearbeitung"
    GESCHLOSSEN = "abgeschlossen"
    
class Kategorie(Enum):
    ONLINESKRIPT = "Online Skript"
    PDFSKRIPT = "PDF-Skript"
    VIDEO = "Video"
    ONLINETESTS = "Online Tests"
    MUSTERKLAUSUR = "Musterklausur"
    FOLIENSÄTZE = "Foliensätze"
    # weitere.....
    
class Benutzer_rolle(Enum):
    STUDIERENDE = "Studierende"
    LEHRENDE = "Lehrende"
    ADMIN = "Admin"
    # weitere.....
   
