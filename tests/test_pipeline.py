"""Tests du pipeline de bout en bout (contenant)."""
from pathlib import Path

from cockpit.config import CockpitConfig
from cockpit.pipeline import run_pipeline
from cockpit.questionnaire import Questionnaire

FIXTURES = Path(__file__).parent / "fixtures"


def test_pipeline_writes_profile_and_site(tmp_path):
    config = CockpitConfig.load(FIXTURES)
    questionnaire = Questionnaire.from_config(config.questionnaire)
    answers = {q.id: f"FICTIF réponse {q.id}" for q in questionnaire.questions}
    profile = questionnaire.build_profile("FICTIF John Doe", answers)

    result = run_pipeline(FIXTURES, profile, tmp_path)

    assert result.profile_path.is_file()
    assert result.site_path.is_file()
    assert result.site_path.read_text(encoding="utf-8") == result.site_html


def test_pipeline_site_contains_roadmap(tmp_path):
    config = CockpitConfig.load(FIXTURES)
    questionnaire = Questionnaire.from_config(config.questionnaire)
    answers = {q.id: f"FICTIF réponse {q.id}" for q in questionnaire.questions}
    profile = questionnaire.build_profile("FICTIF John Doe", answers)

    result = run_pipeline(FIXTURES, profile, tmp_path)

    html = result.site_path.read_text(encoding="utf-8")
    assert "<h2>Roadmap</h2>" in html
    assert "<li>" in html
