# Klasse: Benutzer, vererbt an: Studierende, Lehrende, Admin
from abc import ABC, abstractmethod

class Benutzer(ABC):
    def __init__(self, benutzer_id:int, name:str, email:str): # Konstruktor (aufgerufen, bei Instanziierung)
        self.__benutzer_id = benutzer_id # private
        self.__name = name # private
        self.__email = email # private
    
    # getter Methoden
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
        
    # abstrakte Methode: muss von Unterklassen implementiert werden    
    @abstractmethod      
    def get_sichtbare_kommentare(self):
        pass

