import enum
import pytest
from models import get_rolle_klasse, Benutzer_rolle, Studierende, Lehrende, Admin

@pytest.mark.id_T55
@pytest.mark.unit
@pytest.mark.funktion
@pytest.mark.requirement_F06
def test_get_rolle_klasse_bekannte_rollen():
    """
    Testart: Unittest
    Testkategorie: Funktional (F-06 Benutzerverwaltung)

    - Prüft, dass für jede bekannte Rolle die richtige Klasse zurückgegeben wird.
    """
    assert get_rolle_klasse(Benutzer_rolle.STUDIERENDE) is Studierende
    assert get_rolle_klasse(Benutzer_rolle.LEHRENDE) is Lehrende
    assert get_rolle_klasse(Benutzer_rolle.ADMIN) is Admin


@pytest.mark.id_T56
@pytest.mark.unit
@pytest.mark.funktion
@pytest.mark.requirement_F06
@pytest.mark.requirement_NF11
def test_get_rolle_klasse_unbekannte_rolle():
    """
    Testart: Unittest
    Testkategorie: Funktional (F-06 Benutzerverwaltung), Zuverlässigkeit (NF-11 Verfügbarkeit)

    - Prüft, dass bei einer unbekannten Rolle None zurückgegeben wird.
    """
    class FakeRolle(enum.Enum):
        GAST = "GAST"

    result = get_rolle_klasse(FakeRolle.GAST)
    assert result is None
