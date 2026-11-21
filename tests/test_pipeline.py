"""Test du parcours P1 de bout en bout (contenant)."""
from pathlib import Path

from cockpit.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]
QUESTIONNAIRE = ROOT / "config" / "questionnaire.json"
TEMPLATE = ROOT / "templates" / "site.html"

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


def test_full_pipeline():
    answers = {"q1": "FICTIF_R1", "q2": "FICTIF_R2", "q3": "FICTIF_R3"}
    result = run_pipeline(
        QUESTIONNAIRE,
        answers,
        SITE_FICTIF,
        ROADMAP_FICTIF,
        ["tdah", "dyslexie", "autisme"],
        TEMPLATE,
    )
    assert result["profil"]["reponses"] == answers
    assert len(result["jalons"]) >= 3
    assert "<html" in result["site_html"]
    assert result["elapsed_seconds"] < 300
