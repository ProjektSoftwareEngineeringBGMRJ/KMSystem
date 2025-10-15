from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
from models.benutzer import Benutzer
from models.datenbank import db
from models.enums import Sichtbarkeit, Kategorie
from models.meldung import Meldung # wird in erstelle_meldung instanziiert
from typing import TYPE_CHECKING # vermeidet Zirkelimporte

if TYPE_CHECKING: # Import nur für Typprüfung
    from models.modul import Modul
    from models.kommentar import Kommentar

class Studierende(Benutzer): # erbt von Oberklasse
    __tablename__ = "studierende"
    id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "studierende"
    }
    
    # Beziehung zu Meldungen
    #meldungen = db.relationship("Meldung", back_populates="ersteller", lazy="dynamic")
    meldungen = db.relationship(
        "Meldung", 
        back_populates="ersteller", 
        cascade="all, delete-orphan"
        )
    
    def __init__(self, name:str, email:str, passwort:str):
        super().__init__(name, email, passwort) # Attribute der Oberklasse initialisieren
        
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
    
    def erstelle_meldung(self, beschreibung:str, kategorie:Kategorie, modul:Modul) -> Meldung:
        meldung = Meldung(beschreibung=beschreibung, kategorie=kategorie, ersteller=self, modul=modul) # Als Ersteller wird mit self Objekt "Studierene" übergeben
        #self.meldungen.append(meldung) # Liste pflegen
        #modul.meldungen.append(meldung) # Modul aktualisieren
        db.session.add(meldung)
        db.session.commit()
        return meldung
    
    # Anworten auf Kommentare
    def antworte_auf_kommentar(self, kommentar: "Kommentar", text: str):
        if not isinstance(self, Studierende):
            raise PermissionError("Nur Studierende dürfen antworten.")
        
        antwort = Kommentar(
            text = text,
            #lehrende=
            meldung = kommentar.meldung,
            sichtbarkeit = Sichtbarkeit.PRIVAT,
            verfasser = self.name,  # oder self.email
            antwort_auf = kommentar
        )
        
        db.session.add(antwort)
        db.session.commit()
    

    