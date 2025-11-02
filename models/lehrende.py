from models.benutzer import Benutzer
from models.datenbank import db
from models.modul import modul_lehrende
from models.enums import Sichtbarkeit
from models.kommentar import Kommentar
from typing import TYPE_CHECKING # vermeidet Zirkelimporte

if TYPE_CHECKING: # Import nur für Typprüfung
    from models.meldung import Meldung

class Lehrende(Benutzer):
    __tablename__ = "lehrende"
    id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "lehrende"
    }
    
    # Beziehungen
    
    # Many to Many-Beziehung zu Modul
    module = db.relationship(
        "Modul", 
        secondary=modul_lehrende, 
        back_populates="lehrende"
        )
    
    kommentare = db.relationship(
        "Kommentar", 
        back_populates="lehrende", 
        cascade="all, delete-orphan"
        )
    
    

    def __init__(self, name:str, email:str, passwort:str):
        super().__init__(name, email, passwort)
        #self.module = []   # Liste von Modul-Objekten

    def get_sichtbare_kommentare(self, meldung:"Meldung") -> list[Kommentar]:
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

    def add_kommentar(self, meldung:"Meldung", text:str, sichtbarkeit:Sichtbarkeit = Sichtbarkeit.PRIVAT) -> Kommentar:
        # Prüfen, ob das Modul der Meldung vom Lehrenden betreut wird
        if meldung.modul not in self.module:
            raise PermissionError("Dies ist nur für eigene Module möglich.")
        
        kommentar = Kommentar(
            text = text, 
            meldung = meldung,
            sichtbarkeit = sichtbarkeit,
            verfasser = self.name,
            lehrende = self,
            antwort_auf = None
        )
        return kommentar
        
    def get_eigene_meldungen(self) -> list["Meldung"]:
        meldungen: list[Meldung] = []
        for modul in self.module: 
            meldungen.extend(modul.meldungen)
        return meldungen
        # sortieren nach Erstellungsdatum
        # return sorted(meldungen, key=lambda m: m.erstellt_am, reverse=True)
 
        
    