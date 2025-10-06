from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
from typing import TYPE_CHECKING # vermeidet Zirkelimporte
if TYPE_CHECKING: # Import nur für Typprüfung
    from models.lehrende import Lehrende
    from models.meldung import Meldung
from datetime import datetime
from models.enums import Sichtbarkeit

# Klasse: Kommentar
class Kommentar:
    def __init__(self, kommentar_id:int, text:str, lehrende:Lehrende, meldung:Meldung, sichtbarkeit:Sichtbarkeit): # Konstruktor
        self.__kommentar_id = kommentar_id
        self.__text = text
        self.__zeitstempel = datetime.now() # Erstellungszeitpunkt
        self.__lehrende = lehrende # Verfasser
        self.__meldung = meldung
        self.__sichtbarkeit = sichtbarkeit # .value -> öffentlich oder privat
        
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
    