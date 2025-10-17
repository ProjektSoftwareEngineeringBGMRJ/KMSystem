from models.benutzer import Benutzer
from models.datenbank import db
from flask import flash
from typing import TYPE_CHECKING#, Type
#from models.enums import Benutzer_rolle

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
            
    # alle Kommentare von Meldungen sehen
    def get_sichtbare_kommentare(self, meldung:"Meldung") -> list["Kommentar"]:
        return meldung.kommentare
    
    def erstelle_modul(self, titel:str) -> "Modul":
        from models.modul import Modul
        
        modul_vorhanden = Modul.query.filter_by(titel=titel).first()
        print(modul_vorhanden)
        if modul_vorhanden:
            raise ValueError(f"Modul \"{titel}\" bereits vorhanden.")
        else: 
            neues_modul = Modul(titel=titel) 
            #self.__module.append(neues_modul)
            db.session.add(neues_modul)
            db.session.commit()
            return neues_modul
        
            
        
    
    def loesche_modul(self, modul: "Modul") -> bool:
        if modul.meldungen:
            # Modul enhält Meldungen: nicht löschen
            return False
        db.session.delete(modul)
        db.session.commit()
        return True

        # im Controller:
        #if not current_user.loesche_modul(modul):
        #   flash("Modul enthält noch Meldungen und kann nicht gelöscht werden.")
        #else:
        #   flash(f"Modul '{modul.titel}' wurde gelöscht.")
    
    def modul_zuweisen(self, modul: "Modul", lehrende: "Lehrende"):
        # if modul is None:
        #     raise ValueError("Bitte erst Module anlegen.") # wenn noch kein Modul vorhanden
            
        if lehrende in modul.lehrende:
            return False # wenn bereits zugewiesen
        
        #modul._weise_lehrende_zu(lehrende, aufrufer=self) 
        modul.lehrende.append(lehrende)
        db.session.commit()
        return True   
    
    
    def modul_entziehen(self, modul: "Modul", lehrende: "Lehrende"):
        # if modul is None:
        #     raise ValueError("Bitte erst Module anlegen.") # wenn noch kein Modul vorhanden
        
        if lehrende not in modul.lehrende:
            return False # wenn bereits zugewiesen
        
        modul.lehrende.remove(lehrende)
        db.session.commit()
        return True
        
        
    def get_alle_meldungen(self) -> list["Meldung"]:
        from models.meldung import Meldung
        return db.session.query(Meldung).all()
        
    def get_alle_benutzer(self) -> list[Benutzer]:
        return db.session.query(Benutzer).all() #self.__benutzer_liste