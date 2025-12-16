from typing import TYPE_CHECKING # vermeidet Zirkelimporte
from models.benutzer import Benutzer
from models.datenbank import db
from models.modul import modul_lehrende
from models.enums import Sichtbarkeit
from models.kommentar import Kommentar

if TYPE_CHECKING: # Import nur für Typprüfung
    from models.meldung import Meldung

class Lehrende(Benutzer):
    '''
    Repräsentiert einen Lehrenden im Softwaresystem.

    Attribute:
        id (int): Primärschlüssel, verknüpft mit der Basisklasse Benutzer.
        module (List[Modul]): Liste der Module, die von diesem Lehrenden betreut werden.
        kommentare (List[Kommentar]): Liste der Kommentare, die dieser Lehrende verfasst hat.

    Hinweise:
        - Polymorphe Identität 'lehrende' für SQLAlchemy.
        - Lehrende können Kommentare verfassen und Meldungen in ihren Modulen einsehen.
    '''
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


    # def __init__(self, name:str, email:str, passwort:str):
    #     super().__init__(name, email, passwort)
    #     #self.module = []   # Liste von Modul-Objekten

    def get_sichtbare_kommentare(self, meldung:"Meldung") -> list[Kommentar]:
        '''
        Gibt alle für den Lehrenden sichtbaren Kommentare zu einer Meldung zurück.

        Regeln:
            - Eigene Kommentare sind immer sichtbar.
            - Öffentliche Kommentare sind sichtbar, wenn die Meldung zu einem Modul gehört,
              das dieser Lehrende betreut.

        Args:
            meldung (Meldung): Die Meldung, deren Kommentare geprüft werden sollen.

        Returns:
            List[Kommentar]: Liste der sichtbaren Kommentare für diesen Lehrenden.
        '''
        sichtbare: list[Kommentar] = []
        for kommentar in meldung.kommentare:
            # Eigene Kommentare immer sichtbar
            if kommentar.lehrende == self:
                sichtbare.append(kommentar)
            # Kommentare öffentlich oder selbst erstellt
            elif meldung.modul in self.module and kommentar.sichtbarkeit == Sichtbarkeit.PRIVAT: # ÖFFENTLICH
                sichtbare.append(kommentar)
            # Öffentliche Kommentare fremder Module sichtbar
            elif kommentar.sichtbarkeit == Sichtbarkeit.ÖFFENTLICH:
                sichtbare.append(kommentar)
        return sichtbare

    def add_kommentar(
        self,
        meldung:"Meldung",
        text:str,
        sichtbarkeit:Sichtbarkeit = Sichtbarkeit.PRIVAT
        ) -> Kommentar:
        '''
        Fügt einer Meldung einen neuen Kommentar durch den Lehrenden hinzu.

        Einschränkungen:
            - Nur Lehrende, die das Modul der Meldung betreuen, dürfen kommentieren.
            - Standardmäßig ist die Sichtbarkeit privat.

        Args:
            meldung (Meldung): Die Meldung, zu der der Kommentar gehört.
            text (str): Inhalt des Kommentars.
            sichtbarkeit (Sichtbarkeit, optional): Sichtbarkeit des Kommentars
                (Standard: PRIVAT).

        Returns:
            Kommentar: Neu erstellter Kommentar.

        Raises:
            PermissionError: Falls der Lehrende nicht das Modul der Meldung betreut.
        '''
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
        '''
        Gibt alle Meldungen zurück, die zu den Modulen gehören,
        die dieser Lehrende betreut.

        Args:
            None

        Returns:
            List[Meldung]: Liste der Meldungen aus den Modulen des Lehrenden.
        '''
        meldungen: list[Meldung] = []
        for modul in self.module:
            meldungen.extend(modul.meldungen)
        return meldungen # return sorted(meldungen, key=lambda m: m.erstellt_am, reverse=True)
