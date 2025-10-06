from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
from typing import TYPE_CHECKING # vermeidet Zirkelimporte
if TYPE_CHECKING: # Import nur für Typprüfung
    from models.modul import Modul
    from models.kommentar import Kommentar
from models.benutzer import Benutzer
from models.meldung import Meldung # wird in erstelle_meldung instanziiert
from models.enums import Sichtbarkeit, Kategorie


class Studierende(Benutzer): # erbt von Oberklasse
    
    def __init__(self, benutzer_id:int, name:str, email:str):
        super().__init__(benutzer_id, name, email) # Attribute der Oberklasse initialisieren
        self.meldungen: list[Meldung] = []  # Attribut: Liste von Meldung-Objekten
        
    def get_sichtbare_kommentare(self, meldung:Meldung) -> list[Kommentar]:
        '''
        Implementiert abstrakte Methode von Benutzer:
        Gibt alle sichtbaren Kommentare einer Meldung für ein Studierenden-Objekt zurück
        '''
        sichtbare: list[Kommentar] = []
        for kommentar in meldung.kommentare:
            if kommentar.sichtbarkeit == Sichtbarkeit.ÖFFENTLICH: # alle öffentlichen
                sichtbare.append(kommentar)
            elif kommentar.sichtbarkeit == Sichtbarkeit.PRIVAT and meldung.ersteller == self: # private bei selbst erstellten Meldungen
                sichtbare.append(kommentar)
        return sichtbare
    
    def erstelle_meldung(self, meldungs_id:int, beschreibung:str, kategorie:Kategorie, modul:Modul) -> Meldung:
        
        meldung = Meldung(meldungs_id, beschreibung, kategorie, self, modul) # Als Ersteller wird mit self Objekt "Studierene" übergeben
        self.meldungen.append(meldung) # Liste pflegen
        modul.meldungen.append(meldung) # Modul aktualisieren
        return meldung
    

    