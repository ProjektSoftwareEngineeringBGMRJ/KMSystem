#from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
#from typing import TYPE_CHECKING # vermeidet Zirkelimporte
#if TYPE_CHECKING: # Import nur für Typprüfung
#    from models.studierende import Studierende
#    from models.kommentar import Kommentar
#    from models.modul import Modul
## Klasse: Meldung
#from datetime import datetime
#from models.enums import Kategorie, Status

from models.datenbank import db
from models.enums import Kategorie, Status
from datetime import datetime

class Meldung(db.Model):
    __tablename__ = "meldung"
    
    id = db.Column(db.Integer, primary_key=True)
    beschreibung = db.Column(db.String(500), nullable=False)
    kategorie = db.Column(db.Enum(Kategorie), nullable=False)
    status = db.Column(db.Enum(Status), default=Status.OFFEN, nullable=False)
    zeitstempel = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    # Beziehungen
    # beim löschen von Studierendem mit löschen
    ersteller_id = db.Column(
        db.Integer, 
        db.ForeignKey("studierende.id", ondelete="CASCADE"), 
        nullable=False
        )
    
    ersteller = db.relationship("Studierende", back_populates="meldungen")
    
    modul_id = db.Column(
        db.Integer, 
        db.ForeignKey("modul.id", ondelete="CASCADE"), 
        nullable=False)
     
    modul = db.relationship("Modul", back_populates="meldungen")
    
    kommentare = db.relationship(
        "Kommentar", 
        back_populates="meldung", 
        cascade="all, delete-orphan"
        )
    #kommentare = db.relationship("Kommentar", backref="autor", cascade="all, delete-orphan")
    
    def __init__(self, beschreibung:str, kategorie:Kategorie, ersteller, modul):
        self.beschreibung = beschreibung 
        self.kategorie = kategorie 
        self.ersteller = ersteller # Referenz auf Objekt (ein Studierender)
        self.modul = modul # Modul-Objekt