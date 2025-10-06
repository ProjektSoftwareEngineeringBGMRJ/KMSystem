from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
from typing import TYPE_CHECKING # vermeidet Zirkelimporte
if TYPE_CHECKING: # Import nur für Typprüfung
    from models.lehrende import Lehrende
    from models.benutzer import Benutzer
    from models.admin import Admin
from models.meldung import Meldung

# Klasse: Modul
class Modul:
    def __init__(self, modul_id:int, titel:str):
        self.__modul_id = modul_id
        self.__titel = titel
        self.__meldungen = [] # Liste der Meldungen
        self.__lehrende = [] # Liste der Lehrenden
        
    
    # getter Methoden    
    @property
    def modul_id(self) -> int:
        return self.__modul_id
            
    @property
    def titel(self) -> str:
        return self.__titel
    
    @property
    def meldungen(self) -> list[Meldung]:
        return self.__meldungen
    
    @property
    def lehrende(self) -> list[Lehrende]:
        return self.__lehrende
    
    # setter Methoden 
    @modul_id.setter
    def modul_id(self, value:int):
        self.__modul_id = value
    
    @titel.setter
    def titel(self, value:str):
        self.__titel = value
        
    #@meldungen.setter
    #def meldungen(self, value):
    #    self.__meldungen = value
        
    #@lehrende.setter
    #def lehrende(self, value):
    #    self.__lehrende = value
    
    # private Methode, nur für Admin erlaubt (Konvention: "_" vor Methodenname)
    def _weise_lehrende_zu(self, lehrende:Lehrende, aufrufer:Benutzer):
        """
        Fügt Lehrenden Modul & Modul Lehrenden hinzu. 
        Darf nur von Admin aufgerufen werden!
        """
        from models.admin import Admin
        
        if not isinstance(aufrufer, Admin):
            raise PermissionError("Nur Admins dürfen Lehrenden Module zuweisen.")
        
        if self not in lehrende.module:
            lehrende.module.append(self) # Modul zu Liste hinzufügen
            self.lehrende.append(lehrende) # Lehrperson zur Liste des Moduls hinzufügen