#from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
#from typing import TYPE_CHECKING # vermeidet Zirkelimporte
#if TYPE_CHECKING: # Import nur für Typprüfung
#    from models.lehrende import Lehrende
#    from models.meldung import Meldung
#from datetime import datetime
#from models.enums import Sichtbarkeit

from models.datenbank import db
from models.enums import Sichtbarkeit
from datetime import datetime

# Klasse: Kommentar
class Kommentar(db.Model):
    __tablename__ = "kommentar"
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    zeitstempel = db.Column(db.DateTime, default=datetime.now, nullable=False)
    sichtbarkeit = db.Column(db.Enum(Sichtbarkeit), nullable=False)
    
    # Beziehungen
    lehrende_id = db.Column(db.Integer, db.ForeignKey("lehrende.id"), nullable=False)
    lehrende = db.relationship("Lehrende", backref="kommentare")

    meldung_id = db.Column(db.Integer, db.ForeignKey("meldung.id"), nullable=False)
    meldung = db.relationship("Meldung", back_populates="kommentare")
    
    def __init__(self, text:str, lehrende, meldung, sichtbarkeit:Sichtbarkeit): # Konstruktor
        #self.__kommentar_id = kommentar_id
        self.text = text
        #self.__zeitstempel = datetime.now() # Erstellungszeitpunkt
        self.lehrende = lehrende # Verfasser
        self.meldung = meldung
        self.sichtbarkeit = sichtbarkeit # .value -> öffentlich oder privat
   
    '''    
    # Getter Methoden
    @property
    def kommentar_id(self) -> int:
        return self.__kommentar_id
    
    @property
    def text(self) -> str:
        return self.__text
    
    @property
    def sichtbarkeit(self) -> Sichtbarkeit:
        return self.__sichtbarkeit
    
    @property
    def zeitstempel(self) -> datetime:
        return self.__zeitstempel
    
    @property
    def lehrende(self) -> Lehrende:
        return self.__lehrende
    
    @property
    def meldung(self) -> Meldung:
        return self.__meldung
    
    # Setter Methoden
    @kommentar_id.setter
    def kommentar_id(self, value:int):
        self.__kommentar_id = value
        
    @text.setter
    def text(self, value:str):
        self.__text = value
        
    @sichtbarkeit.setter
    def sichtbarkeit(self, value:Sichtbarkeit):
        self.__sichtbarkeit = value
    
    # Setter deaktiviert: unveränderlich nach Erstellung
    
    #@zeitstempel.setter
    #def zeitstempel(self, value):
    #    self.__zeitstempel = value
    
    #@lehrende.setter
    #def lehrende(self, value):
    #    self.__lehrende = value
    
    #@meldung.setter
    #def meldung(self, value):
    #    self.__meldung = value
    '''