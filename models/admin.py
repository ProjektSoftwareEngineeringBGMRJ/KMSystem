from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
from typing import TYPE_CHECKING # vermeidet Zirkelimporte
if TYPE_CHECKING: # Import nur für Typprüfung    
    from models.kommentar import Kommentar
    from models.lehrende import Lehrende
    from models.meldung import Meldung
from models.benutzer import Benutzer
from models.modul import Modul
from typing import Type

class Admin(Benutzer):
    def __init__(self, benutzer_id:int, name:str, email:str):
        super().__init__(benutzer_id, name, email)
        self.__module: list[Modul] = []

    @property
    def module(self) -> list[Modul]:
        return self.__module
    
    # alle Kommentare von Meldungen sehen
    def get_sichtbare_kommentare(self, meldung:Meldung) -> list[Kommentar]:
        return meldung.kommentare
    
    # darf keine Kommentare erstellen
    #def add_kommentar(self, *args, **kwargs):
    #    raise PermissionError("Admins dürfen keine Kommentare verfassen.")

    def erstelle_modul(self, modul_id:int, name:str) -> Modul:
        neues_modul = Modul(modul_id, name) 
        self.__module.append(neues_modul)
        return neues_modul
    
    def modul_zuweisen(self, modul: Modul, lehrende: Lehrende):
        modul._weise_lehrende_zu(lehrende, aufrufer = self)    
        
    # Rollen zuweisen: Klassen Studierende, Lehrende, Admin
    def rolle_zuweisen(self, benutzer: Benutzer, neue_rolle_klasse: Type[Benutzer]):
        # angegebender Klasse benutzernamen übergeben
        return neue_rolle_klasse(benutzer.benutzer_id, benutzer.name, benutzer.email)
        #Logging/ Validierung
        #Datenbank pflegen z.B.:
        #benutzer_liste.remove(benutzer)
        #benutzer_liste.append(neuer_benutzer)

    def get_alle_meldungen(self) -> list[Meldung]:
        meldungen = []
        for modul in self.module:
            meldungen.extend(modul.meldungen)
        return meldungen
    