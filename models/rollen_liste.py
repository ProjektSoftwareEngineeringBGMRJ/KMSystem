from models.studierende import Studierende
from models.lehrende import Lehrende 
from models.admin import Admin
from typing import Type
from models.benutzer import Benutzer
from models.enums import Benutzer_rolle

# Mapping von Enum → Klassenobjekt der Benutzerklasse
__rolle_klasse_map = {
    Benutzer_rolle.STUDIERENDE: Studierende,
    Benutzer_rolle.LEHRENDE: Lehrende,
    Benutzer_rolle.ADMIN: Admin
}

def get_rolle_klasse(rolle:Benutzer_rolle) -> Type[Benutzer]:
    try:
        return __rolle_klasse_map[rolle]
    except (KeyError):
        return None 