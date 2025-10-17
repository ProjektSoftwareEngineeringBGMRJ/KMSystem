from models.datenbank import db
#from models.enums import Kategorie
#from models.lehrende import Lehrende
#from models.meldung import Meldung
#from typing import TYPE_CHECKING # vermeidet Zirkelimporte

# if TYPE_CHECKING: # Import nur für Typprüfung
#     from models.lehrende import Lehrende

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