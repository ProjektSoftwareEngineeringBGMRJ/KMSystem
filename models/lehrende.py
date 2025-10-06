from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
from typing import TYPE_CHECKING # vermeidet Zirkelimporte
if TYPE_CHECKING: # Import nur für Typprüfung
    from models.meldung import Meldung
from models.benutzer import Benutzer
from models.kommentar import Kommentar # benötigt, da Instanziierung
from models.enums import Sichtbarkeit

class Lehrende(Benutzer):
     
    def __init__(self, benutzer_id:int, name:str, email:str):
        super().__init__(benutzer_id, name, email)
        self.module = []   # Liste von Modul-Objekten

    def get_sichtbare_kommentare(self, meldung:Meldung) -> list[Kommentar]:
        '''
        Implementiert abstrakte Methode von Benutzer:
        Gibt alle sichtbaren Kommentare einer Meldung für einen Lehrenden zurück
        '''
        sichtbare: list[Kommentar] = []
        for kommentar in meldung.kommentare:
            # Eigene Kommentare immer sichtbar
            if kommentar.lehrende == self:
                sichtbare.append(kommentar)
            # Kommentare öffentlich oder selbst erstellt
            elif meldung.modul in self.module and kommentar.sichtbarkeit == Sichtbarkeit.ÖFFENTLICH:
                sichtbare.append(kommentar)
        return sichtbare

    def add_kommentar(self, meldung:Meldung, text:str, sichtbarkeit:Sichtbarkeit = Sichtbarkeit.PRIVAT):
        # Prüfen, ob das Modul der Meldung vom Lehrenden betreut wird
        if meldung.modul not in self.module:
            raise PermissionError("Lehrende dürfen nur zu ihren eigenen Modulen kommentieren.")
        kommentar = Kommentar(
            kommentar_id=len(meldung.kommentare) + 1, 
            text = text, 
            sichtbarkeit = sichtbarkeit, 
            lehrende = self,
            meldung = meldung
        )
        meldung.kommentare.append(kommentar)
        
    