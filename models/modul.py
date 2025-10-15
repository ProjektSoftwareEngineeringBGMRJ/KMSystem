#from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
#from typing import TYPE_CHECKING # vermeidet Zirkelimporte
#if TYPE_CHECKING: # Import nur für Typprüfung
#    from models.lehrende import Lehrende
#    from models.benutzer import Benutzer
#    from models.admin import Admin
#from models.meldung import Meldung

from models.datenbank import db
from models.enums import Kategorie
#from models.lehrende import Lehrende
from models.meldung import Meldung
from typing import TYPE_CHECKING # vermeidet Zirkelimporte

if TYPE_CHECKING: # Import nur für Typprüfung
    from models.lehrende import Lehrende

modul_lehrende = db.Table("modul_lehrende",
                          db.Column(
                              "modul_id", 
                              db.Integer, 
                              db.ForeignKey("modul.id")
                              ),
                          db.Column(
                              "lehrende_id", 
                              db.Integer, 
                              db.ForeignKey("lehrende.id")
                              )
                          )

class Modul(db.Model):
    __tablename__ = "modul"
    
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(200), nullable=False)
    
    # Beziehungen
    meldungen = db.relationship(
        "Meldung", 
        back_populates="modul", 
        cascade="all, delete-orphan"
        )
    
    # Many to Many-Beziehung zu Lehrende
    lehrende = db.relationship(
        "Lehrende", 
        secondary=modul_lehrende, 
        back_populates="module"
        )
    
    def __init__(self, titel:str):
        self.titel = titel
      
    # private Methode, nur für Admin erlaubt (Konvention: "_" vor Methodenname)
    #def _weise_lehrende_zu(self, lehrende:"Lehrende", aufrufer):
    #    """
    #    Fügt Lehrenden Modul & Modul Lehrenden hinzu. 
    #    Darf nur von Admin aufgerufen werden!
    #    """
    #    from models.admin import Admin
    #    
    #    if not isinstance(aufrufer, Admin):
    #        raise PermissionError("Nur Admins dürfen Lehrenden Module zuweisen.")
    #    
    #    if self not in lehrende.module:
    #        lehrende.module.append(self) # SQLAlchemy Beziehung über relationship(..., back_populates=...) definiert.
    #        # modul.lehrende wird automatisch synchronisiert 
    #        #self.lehrende.append(lehrende) # Lehrperson zur Liste des Moduls hinzufügen