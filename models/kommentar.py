from datetime import datetime
from typing import TYPE_CHECKING # vermeidet Zirkelimporte
from models.datenbank import db
from models.enums import Sichtbarkeit
from models.meldung import Meldung

if TYPE_CHECKING: # Import nur für Typprüfung
    from models.lehrende import Lehrende

class Kommentar(db.Model):
    '''
    Repräsentiert einen Kommentar zu einer Meldung.

    Attribute:
        id (int): Primärschlüssel zur eindeutigen Identifikation des Kommentars.
        text (str): Inhalt des Kommentars (max. 500 Zeichen).
        zeitstempel (datetime): Zeitpunkt der Erstellung des Kommentars.
        sichtbarkeit (Sichtbarkeit): Sichtbarkeit des Kommentars (z. B. öffentlich oder privat).
        verfasser (str): Name oder E-Mail des Verfassers.
        lehrende_id (int | None): Fremdschlüssel, verweist optional auf einen Lehrenden.
        meldung_id (int): Fremdschlüssel, verweist auf die zugehörige Meldung.
        antwort_auf_id (int | None): Fremdschlüssel, verweist auf einen übergeordneten Kommentar,
            falls es sich um eine Antwort handelt.

    Beziehungen:
        lehrende (Lehrende): Beziehung zu einem Lehrenden, der den Kommentar verfasst hat.
        meldung (Meldung): Beziehung zur Meldung, zu der der Kommentar gehört.
        antwort_auf (Kommentar): Beziehung zu einem übergeordneten Kommentar.
        antworten (List[Kommentar]): Liste von Antworten auf diesen Kommentar.
    '''
    __tablename__ = "kommentar"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    zeitstempel = db.Column(db.DateTime, default=datetime.now, nullable=False)
    sichtbarkeit = db.Column(db.Enum(Sichtbarkeit), nullable=False)
    verfasser = db.Column(db.String(100), nullable=False)  # z. B. Name oder email
    
    # beim löschen von Lehrendem mit löschen:
    lehrende_id = db.Column(
        db.Integer,
        db.ForeignKey("lehrende.id", ondelete="CASCADE"),
        nullable=True
        )
    meldung_id = db.Column(
        db.Integer,
        db.ForeignKey("meldung.id", ondelete="CASCADE"),
        nullable=False
        )
    antwort_auf_id = db.Column(
        db.Integer,
        db.ForeignKey("kommentar.id"),
        nullable=True
        )

    # Beziehungen
    lehrende = db.relationship("Lehrende", back_populates="kommentare")

    meldung = db.relationship("Meldung", back_populates="kommentare")

    antwort_auf = db.relationship(
        "Kommentar", 
        remote_side="Kommentar.id",
        backref="antworten"
        )

    def __init__(
        self,
        text:str,
        meldung:"Meldung",
        sichtbarkeit:Sichtbarkeit,
        verfasser:str,
        lehrende:"Lehrende" = None,
        antwort_auf:"Kommentar" = None
        ):
        '''
        Erstellt einen neuen Kommentar.

        Args:
            text (str): Inhalt des Kommentars.
            meldung (Meldung): Die Meldung, zu der der Kommentar gehört.
            sichtbarkeit (Sichtbarkeit): Sichtbarkeit des Kommentars (öffentlich oder privat).
            verfasser (str): Name oder E-Mail des Verfassers.
            lehrende (Lehrende, optional): Lehrender, der den Kommentar verfasst hat.
            antwort_auf (Kommentar, optional): Kommentar, auf den geantwortet wird.

        Hinweise:
            - Studierende können Kommentare ohne `lehrende` speichern.
            - Antworten werden über `antwort_auf` verknüpft und sind in `antworten` abrufbar.
        '''
        self.text = text
        self.meldung = meldung
        self.sichtbarkeit = sichtbarkeit
        self.verfasser = verfasser
        self.lehrende = lehrende
        self.antwort_auf = antwort_auf
