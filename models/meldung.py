from datetime import datetime
from models.datenbank import db
from models.enums import Kategorie, Status

class Meldung(db.Model):
    '''
    Repräsentiert eine Meldung.

    Attribute:
        id (int): Primärschlüssel zur eindeutigen Identifikation der Meldung.
        beschreibung (str): Textliche Beschreibung der Meldung (max. 500 Zeichen).
        kategorie (Kategorie): Kategorie der Meldung (z. B. Fehler, Verbesserung).
        status (Status): Aktueller Bearbeitungsstatus der Meldung (Standard: OFFEN).
        zeitstempel (datetime): Zeitpunkt der Erstellung der Meldung.
        ersteller_id (int): Fremdschlüssel, verweist auf den Studierenden, der die Meldung erstellt hat.
        modul_id (int): Fremdschlüssel, verweist auf das zugehörige Modul.

    Beziehungen:
        ersteller (Studierende): 1:n-Beziehung, ein Studierender kann mehrere Meldungen erstellen.
        modul (Modul): 1:n-Beziehung, ein Modul kann mehrere Meldungen enthalten.
        kommentare (List[Kommentar]): 1:n-Beziehung, eine Meldung kann mehrere Kommentare haben.
    '''
    __tablename__ = "meldung"

    id = db.Column(db.Integer, primary_key=True)
    beschreibung = db.Column(db.String(500), nullable=False)
    kategorie = db.Column(db.Enum(Kategorie), nullable=False)
    status = db.Column(db.Enum(Status), default=Status.OFFEN, nullable=False)
    zeitstempel = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # beim löschen von Studierendem mit löschen:
    ersteller_id = db.Column(
        db.Integer,
        db.ForeignKey("studierende.id", ondelete="CASCADE"),
        nullable=False
        )
    modul_id = db.Column(
        db.Integer,
        db.ForeignKey("modul.id", ondelete="CASCADE"),
        nullable=False)

    # Beziehungen
    ersteller = db.relationship("Studierende", back_populates="meldungen")

    modul = db.relationship("Modul", back_populates="meldungen")

    kommentare = db.relationship(
        "Kommentar", 
        back_populates="meldung",
        cascade="all, delete-orphan"
        )

    def __init__(self, beschreibung:str, kategorie:Kategorie, ersteller, modul):
        '''
        Erstellt eine neue Meldung.

        Args:
            beschreibung (str): Beschreibung der Meldung.
            kategorie (Kategorie): Kategorie der Meldung.
            ersteller (Studierende): Der Studierende, der die Meldung erstellt.
            modul (Modul): Das Modul, dem die Meldung zugeordnet wird.
        '''
        self.beschreibung = beschreibung 
        self.kategorie = kategorie
        self.ersteller = ersteller
        self.modul = modul
