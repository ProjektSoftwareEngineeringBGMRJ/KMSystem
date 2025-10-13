#from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
#from typing import TYPE_CHECKING # vermeidet Zirkelimporte
#if TYPE_CHECKING: # Import nur für Typprüfung    
#    from models.kommentar import Kommentar
#    from models.lehrende import Lehrende
#    from models.meldung import Meldung
#from models.benutzer import Benutzer
#from models.modul import Modul
#from typing import Type
#from models.datenbank import db

from models.benutzer import Benutzer
from models.datenbank import db
from typing import TYPE_CHECKING, Type
from models.enums import Benutzer_rolle

if TYPE_CHECKING:
    from models.kommentar import Kommentar
    from models.lehrende import Lehrende
    from models.meldung import Meldung
    from models.modul import Modul


class Admin(Benutzer):
    __tablename__ = "admin"
    id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "admin"
    }
    
    def __init__(self, name:str, email:str, passwort: str):
        super().__init__(name, email, passwort)
        #self.__module: list[Modul] = []
        #self.__benutzer_liste: list[Benutzer] = [] 

    #@property
    #def module(self) -> list[Modul]:
    #    return self.__module
    
    # alle Kommentare von Meldungen sehen
    def get_sichtbare_kommentare(self, meldung:"Meldung") -> list["Kommentar"]:
        return meldung.kommentare
    
    # darf keine Kommentare erstellen
    #def add_kommentar(self, *args, **kwargs):
    #    raise PermissionError("Admins dürfen keine Kommentare verfassen.")

    def erstelle_modul(self, titel:str) -> "Modul":
        from models.modul import Modul
        neues_modul = Modul(titel=titel) 
        #self.__module.append(neues_modul)
        db.session.add(neues_modul)
        db.session.commit()
        return neues_modul
    
    def modul_zuweisen(self, modul: "Modul", lehrende: "Lehrende"):
        modul._weise_lehrende_zu(lehrende, aufrufer=self)    
        
    # Rollen zuweisen: Klassen Studierende, Lehrende, Admin
    def rolle_zuweisen(self, benutzer:Benutzer, neue_rolle_klasse:Type[Benutzer]) -> Benutzer:
        neuer_benutzer = neue_rolle_klasse(benutzer.name, benutzer.email, benutzer.passwort)
        neuer_benutzer.id = benutzer.id # ID übernehmen
        # Benutzerliste aktualisieren
        db.session.delete(benutzer)
        db.session.add(neuer_benutzer)
        db.session.commit()
        #self.__benutzer_liste = [
        #neuer_benutzer if b.benutzer_id == benutzer.benutzer_id else b
        #for b in self.__benutzer_liste]
        
        # angegebender Klasse benutzernamen übergeben
        return neuer_benutzer
        #Logging/ Validierung
        #Datenbank pflegen z.B.:
        #benutzer_liste.remove(benutzer)
        #benutzer_liste.append(neuer_benutzer)
        

    def get_alle_meldungen(self) -> list["Meldung"]:
        #from models.modul import Modul
        #meldungen = []
        #alle_module = db.session.query(Modul).all()
        #for modul in alle_module:
        #    meldungen.extend(modul.meldungen)
        #return meldungen
        from models.meldung import Meldung
        return db.session.query(Meldung).all()
        
    
    def get_alle_benutzer(self) -> list[Benutzer]:
        return db.session.query(Benutzer).all() #self.__benutzer_liste