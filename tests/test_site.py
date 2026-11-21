"""Tests du moteur de génération de site (contenant)."""
from pathlib import Path

import pytest

from cockpit.site import MAX_GENERATION_SECONDS, SiteGenerationError, generate_site

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "site.html"

# Valeurs FICTIF (jamais exposées) pour exercer le moteur en test.
SITE_FICTIF = {
    "titre": "FICTIF_TITRE_SITE",
    "theme": "FICTIF_THEME",
    "logo": "FICTIF_LOGO",
    "accompagnateur": "FICTIF_ACCOMPAGNATEUR",
}
ROADMAP_FICTIF = {
    "jalons": [
        {"id": "j1", "titre": "FICTIF_JALON_1", "action": "FICTIF_ACTION_1"},
        {"id": "j2", "titre": "FICTIF_JALON_2", "action": "FICTIF_ACTION_2"},
        {"id": "j3", "titre": "FICTIF_JALON_3", "action": "FICTIF_ACTION_3"},
    ]
}


def test_generate_site_under_five_minutes():
    result = generate_site({}, SITE_FICTIF, ROADMAP_FICTIF, [], TEMPLATE)
    assert result["elapsed_seconds"] < MAX_GENERATION_SECONDS
    assert "<html" in result["html"]
    assert result["html"].count("<li>") >= 3


def test_generated_site_has_no_forbidden_term():
    result = generate_site(
        {}, SITE_FICTIF, ROADMAP_FICTIF, ["tdah", "dyslexie", "autisme"], TEMPLATE
    )
    lowered = result["html"].lower()
    assert "tdah" not in lowered
    assert "dyslexie" not in lowered
    assert "autisme" not in lowered


def test_refuses_open_placeholder():
    site_config = {
        "titre": "A_DEFINIR_TITRE_SITE",
        "theme": "FICTIF_THEME",
        "logo": "FICTIF_LOGO",
        "accompagnateur": "FICTIF_ACCOMPAGNATEUR",
    }
    with pytest.raises(SiteGenerationError):
        generate_site({}, site_config, ROADMAP_FICTIF, [], TEMPLATE)
