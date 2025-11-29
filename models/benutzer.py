from abc import abstractmethod
from flask_login import UserMixin # Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash
from models.datenbank import db
from models.meldung import Meldung

class Benutzer(db.Model, UserMixin):
    '''
    Abstrakte Basisklasse für alle Benutzer.

    Rollen:
        - Studierende
        - Lehrende
        - Admin

    Attribute:
        id (int): Primärschlüssel zur eindeutigen Identifikation des Benutzers.
        name (str): Name des Benutzers.
        email (str): E-Mail-Adresse des Benutzers (eindeutig).
        passwort_hash (str): Gehashter Wert des Passworts.
        type (str): Polymorphe Identität für SQLAlchemy, zur Unterscheidung der Rollen.

    Hinweise:
        - Verwendet Flask-Login (UserMixin) für Authentifizierung.
        - Passwort wird nicht im Klartext gespeichert, sondern mit Werkzeug gehasht.
        - Abstrakte Methode 'get_sichtbare_kommentare' muss von Unterklassen implementiert werden.
    '''
    __tablename__ = "benutzer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwort_hash = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "benutzer"
    }

    def __init__(self, name:str, email:str, passwort:str):
        '''
        Erstellt einen neuen Benutzer.

        Args:
            name (str): Name des Benutzers.
            email (str): E-Mail-Adresse des Benutzers.
            passwort (str): Passwort im Klartext, wird gehasht gespeichert.
        '''
        self.name = name
        self.email = email
        self.passwort_hash = generate_password_hash(passwort)

    def check_passwort(self, passwort:str) -> bool:
        '''
        Prüft, ob ein eingegebenes Passwort mit dem gespeicherten Hash übereinstimmt.

        Args:
            passwort (str): Passwort im Klartext.

        Returns:
            bool: True, wenn das Passwort korrekt ist, sonst False.
        '''
        return check_password_hash(self.passwort_hash, passwort)

    @abstractmethod
    def get_sichtbare_kommentare(self, meldung:Meldung):
        '''
        Abstrakte Methode: Muss von Unterklassen implementiert werden.

        Zweck:
            - Definiert die Schnittstelle, wie jede Rolle (Studierende, Lehrende, Admin)
              die für sie sichtbaren Kommentare einer Meldung erhält.

        Args:
            meldung (Meldung): Die Meldung, deren Kommentare geprüft werden sollen.

        Raises:
            NotImplementedError: Wenn die Methode nicht in einer Unterklasse überschrieben wird.
        
        '''
        raise NotImplementedError("Methode muss in Unterklasse überschrieben werden.")
