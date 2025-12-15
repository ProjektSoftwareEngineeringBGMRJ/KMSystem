"""
Zentrale Model-Imports für Tests und App.

Wenn `import models` ausgeführt wird, werden hier alle Modellmodule
geladen, sodass SQLAlchemy alle Mapper/Tables registriert sind.
"""
from .datenbank import db

# explizite Importe aller Modelle, damit Mapper vor Aufruf von create_all()
# oder vor Instanziierung gemappter Klassen bekannt sind.
from .benutzer import Benutzer
from .admin import Admin
from .studierende import Studierende
from .lehrende import Lehrende
from .modul import Modul
from .meldung import Meldung
from .kommentar import Kommentar
from .rollen_liste import get_rolle_klasse
from .enums import Kategorie, Status, Sichtbarkeit, Benutzer_rolle

__all__ = [
	"db",
	"Benutzer",
	"Admin",
	"Studierende",
	"Lehrende",
	"Modul",
	"Meldung",
	"Kommentar",
	"get_rolle_klasse",
	"Kategorie",
	"Status",
	"Sichtbarkeit",
	"Benutzer_rolle",
]
