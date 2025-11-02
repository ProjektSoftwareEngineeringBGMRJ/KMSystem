from abc import abstractmethod #, ABC
from flask_login import UserMixin # Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash # Passwort als Hash
from models.datenbank import db

class Benutzer(db.Model, UserMixin ):#, ABC):  
    '''
    Benutzer vererbt an: Studierende, Lehrende, Admin.
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
        self.name = name
        self.email = email
        self.passwort_hash = generate_password_hash(passwort) # Passwort als Hash speichern
    
    def check_passwort(self, passwort:str) -> bool:
        '''
        Passwort hashen und vergleichen,
        gibt Bolean zurück
        '''
        return check_password_hash(self.passwort_hash, passwort)
        
    @abstractmethod      
    def get_sichtbare_kommentare(self):
        '''
        Abstrakte Methode: muss von Unterklassen implementiert werden.
        
        '''
        raise NotImplementedError("Methode muss in Unterklasse überschrieben werden.")
    
