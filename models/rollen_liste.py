from typing import Type
from models.studierende import Studierende
from models.lehrende import Lehrende 
from models.admin import Admin

from models.benutzer import Benutzer
from models.enums import Benutzer_rolle

# Mapping von Enum → Klassenobjekt der Benutzerklasse
__rolle_klasse_map = {
    Benutzer_rolle.STUDIERENDE: Studierende,
    Benutzer_rolle.LEHRENDE: Lehrende,
    Benutzer_rolle.ADMIN: Admin
}

def get_rolle_klasse(rolle:Benutzer_rolle) -> Type[Benutzer]:
    '''
    Liefert die konkrete Benutzerklasse für eine gegebene Rolle.

    Args:
        rolle (Benutzer_rolle): Die Benutzerrolle (z. B. STUDIERENDE, LEHRENDE, ADMIN).

    Returns:
        Type[Benutzer] | None: Die entsprechende Klassenreferenz der Benutzerrolle.
        Gibt None zurück, falls die Rolle nicht im Mapping enthalten ist.

    Hinweise:
        - Das Mapping wird über __rolle_klasse_map definiert.
        - Ermöglicht die dynamische Instanziierung der richtigen Benutzerklasse
          basierend auf der Rolle.
    '''
    try:
        return __rolle_klasse_map[rolle]
    except KeyError:
        return None
