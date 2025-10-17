#from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
#from typing import TYPE_CHECKING # vermeidet Zirkelimporte
#if TYPE_CHECKING: # Import nur für Typprüfung
#    from models.lehrende import Lehrende
#    from models.meldung import Meldung
#from datetime import datetime
#from models.enums import Sichtbarkeit

from models.datenbank import db
from models.enums import Sichtbarkeit
from models.meldung import Meldung
#from models.lehrende import Lehrende
from datetime import datetime
from typing import TYPE_CHECKING # vermeidet Zirkelimporte

if TYPE_CHECKING: # Import nur für Typprüfung
    from models.lehrende import Lehrende
#    from models.meldung import Meldung

# Klasse: Kommentar
class Kommentar(db.Model):
    __tablename__ = "kommentar"
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    zeitstempel = db.Column(db.DateTime, default=datetime.now, nullable=False)
    sichtbarkeit = db.Column(db.Enum(Sichtbarkeit), nullable=False)
    verfasser = db.Column(db.String(100), nullable=False)  # z. B. Name oder email
    
    # Beziehungen
    
    # beim löschen von Lehrendem mit löschen
    lehrende_id = db.Column(
        db.Integer, 
        db.ForeignKey("lehrende.id", ondelete="CASCADE"), 
        nullable=True # -> optional: Studierende dürfen Kommenare ohne speichern
        )
    lehrende = db.relationship("Lehrende", back_populates="kommentare")
    
    meldung_id = db.Column(
        db.Integer, 
        db.ForeignKey("meldung.id", ondelete="CASCADE"),
        nullable=False
        )
    meldung = db.relationship("Meldung", back_populates="kommentare")

    antwort_auf_id = db.Column(
        db.Integer, 
        db.ForeignKey("kommentar.id"), 
        nullable=True
        )
    antwort_auf = db.relationship(
        "Kommentar", 
        remote_side="Kommentar.id", 
        backref="antworten"
        )

    def __init__( 
        self, 
        text:str, 
        meldung:"Meldung", 
        sichtbarkeit:Sichtbarkeit, 
        verfasser:str,
        lehrende:"Lehrende" = None, 
        antwort_auf:"Kommentar" = None
        ): 
        #self.__kommentar_id = kommentar_id
        self.text = text
        #self.__zeitstempel = datetime.now() # Erstellungszeitpunkt
        #self.lehrende = lehrende # Verfasser
        self.meldung = meldung
        self.sichtbarkeit = sichtbarkeit # .value -> öffentlich oder privat
        self.verfasser = verfasser
        self.lehrende = lehrende
        self.antwort_auf = antwort_auf