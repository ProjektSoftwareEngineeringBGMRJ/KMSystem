from __future__ import annotations # verzögerte Auswertung von Typen (nicht direkt importiert)
from typing import TYPE_CHECKING # vermeidet Zirkelimporte
from models.benutzer import Benutzer
from models.datenbank import db
from models.enums import Sichtbarkeit, Kategorie
from models.meldung import Meldung # wird in erstelle_meldung instanziiert

if TYPE_CHECKING: # Import nur für Typprüfung
    from models.modul import Modul
    from models.kommentar import Kommentar

class Studierende(Benutzer): # erbt von Oberklasse
    '''
    Repräsentiert einen Studierenden.

    Eigenschaften:
        id (int): Primärschlüssel, verknüpft mit der Basisklasse Benutzer.
        meldungen (List[Meldung]): Liste der Meldungen, die von diesem Studierenden erstellt wurden.

    Hinweise:
        - Polymorphe Identität 'studierende' für SQLAlchemy.
        - Beziehungen zu Meldungen sind mit Cascade-Delete versehen, sodass Meldungen beim Löschen
          des Studierenden ebenfalls entfernt werden.
    '''
    __tablename__ = "studierende"

    id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "studierende"
    }

    # Beziehung zu Meldungen
    meldungen = db.relationship(
        "Meldung", 
        back_populates="ersteller",
        cascade="all, delete-orphan"
        )

    def get_sichtbare_kommentare(self, meldung:Meldung) -> list[Kommentar]:
        '''
        Gibt alle für den Studierenden sichtbaren Kommentare zu einer Meldung zurück.

        Regeln:
            - Öffentliche Kommentare sind immer sichtbar.
            - Private Kommentare sind nur sichtbar, wenn der Studierende selbst der Ersteller
              der Meldung ist.

        Args:
            meldung (Meldung): Die Meldung, deren Kommentare geprüft werden sollen.

        Returns:
            List[Kommentar]: Liste der sichtbaren Kommentare.
        '''
        sichtbare: list[Kommentar] = []
        for kommentar in meldung.kommentare:
            if kommentar.sichtbarkeit == Sichtbarkeit.ÖFFENTLICH:
                sichtbare.append(kommentar)
            elif kommentar.sichtbarkeit == Sichtbarkeit.PRIVAT and meldung.ersteller == self:
                sichtbare.append(kommentar)
        return sichtbare

    def erstelle_meldung(self, beschreibung:str, kategorie:Kategorie, modul:Modul) -> Meldung:
        '''
        Erstellt eine neue Meldung, die diesem Studierenden zugeordnet ist.

        Args:
            beschreibung (str): Beschreibung der Meldung.
            kategorie (Kategorie): Kategorie der Meldung.
            modul (Modul): Modul, dem die Meldung zugeordnet wird.

        Returns:
            Meldung: Die neu erstellte Meldung, gespeichert in der Datenbank.
        '''
        meldung = Meldung(
            beschreibung=beschreibung,
            kategorie=kategorie,
            ersteller=self, # Als Ersteller wird mit self Objekt "Studierene" übergeben
            modul=modul
        )

        db.session.add(meldung)
        db.session.commit()

        return meldung

    # Anworten auf Kommentare
    def antworte_auf_kommentar(self, kommentar: Kommentar, text: str):
        '''
        Erstellt eine Antwort auf einen bestehenden Kommentar.

        Einschränkungen:
            - Nur Studierende dürfen antworten.
            - Antworten sind standardmäßig privat.

        Args:
            kommentar (Kommentar): Der Kommentar, auf den geantwortet wird.
            text (str): Der Antworttext.

        Raises:
            PermissionError: Falls die Methode von einem Nicht-Studierenden aufgerufen wird.
        '''
        if not isinstance(self, Studierende):
            raise PermissionError("Nur Studierende dürfen antworten.")

        antwort = Kommentar(
            text = text,
            meldung = kommentar.meldung,
            sichtbarkeit = Sichtbarkeit.PRIVAT,
            verfasser = self.name,  # oder self.email
            lehrende = None,
            antwort_auf = kommentar
        )

        db.session.add(antwort)
        db.session.commit()
