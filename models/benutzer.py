from models.datenbank import db
from sqlalchemy.ext.declarative import declared_attr
# Klasse: Benutzer, vererbt an: Studierende, Lehrende, Admin
from abc import abstractmethod #, ABC

class Benutzer(db.Model):#, ABC):
    #__abstract__ = True
    __tablename__ = "benutzer"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwort = db.Column(db.String(100), nullable=False)
    
    #@declared_attr
    #def type(cls):
    #    return db.Column(db.String(50))
    type = db.Column(db.String(50))
    
    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "benutzer"
    }
    
    def __init__(self, name:str, email:str, passwort:str):
        self.name = name
        self.email = email
        self.passwort = passwort
    '''
    # getter Methoden
    
    # Falls zusätzliche Getter nötig:
    @property
    def rollenname(self) -> str:
    return self.__mapper_args__["polymorphic_identity"]

    
    @property
    def benutzer_id(self) -> int:
        return self.__benutzer_id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def email(self) -> str:
        return self.__email
    
    # setter Methoden
    @benutzer_id.setter
    def benutzer_id(self, value:int):
        self.__benutzer_id = value
        
    @name.setter
    def name(self, value:str):
        self.__name = value
    
    @email.setter    
    def email(self, value:str):
        self.__email = value
    '''    
    # abstrakte Methode: muss von Unterklassen implementiert werden    
    @abstractmethod      
    def get_sichtbare_kommentare(self):
        raise NotImplementedError("Methode muss in Subklasse überschrieben werden.")
    
