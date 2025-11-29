from models.datenbank import db

modul_lehrende = db.Table("modul_lehrende",
                          db.Column(
                              "modul_id", 
                              db.Integer,
                              db.ForeignKey("modul.id")
                              ),
                          db.Column(
                              "lehrende_id", 
                              db.Integer,
                              db.ForeignKey("lehrende.id")
                              )
                          )

class Modul(db.Model):
    '''
    Repräsentiert ein Modul.

    Attribute:
        id (int): Primärschlüssel zur eindeutigen Identifikation des Moduls.
        titel (str): Titel bzw. Name des Moduls.
        meldungen (List[Meldung]): 1:n-Beziehung zu Meldungen, die diesem Modul zugeordnet sind.
        lehrende (List[Lehrende]): n:m-Beziehung zu Lehrenden, die das Modul betreuen.

    Hinweise:
        - Die Beziehung zu `Meldung` verwendet ein Cascade-Delete, sodass Meldungen beim Löschen
          des Moduls ebenfalls entfernt werden.
        - Die Beziehung zu `Lehrende` wird über die Zwischentabelle `modul_lehrende` abgebildet.
    '''
    __tablename__ = "modul"

    id = db.Column(db.Integer, primary_key=True)

    titel = db.Column(db.String(200), nullable=False)

    # Beziehungen
    meldungen = db.relationship(
        "Meldung", 
        back_populates="modul",
        cascade="all, delete-orphan"
        )

    # Many to Many-Beziehung zu Lehrende
    lehrende = db.relationship(
        "Lehrende", 
        secondary=modul_lehrende,
        back_populates="module"
        )

    def __init__(self, titel:str):
        self.titel = titel
