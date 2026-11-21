"""Tests du générateur de site standalone (contenant)."""
import time
from pathlib import Path

import pytest

from cockpit.config import CockpitConfig
from cockpit.questionnaire import Question, Questionnaire
from cockpit.roadmap import Milestone, Roadmap
from cockpit.site_generator import SiteGenerationError, SiteGenerator
from cockpit.term_filter import TermFilter

FIXTURES = Path(__file__).parent / "fixtures"


def _fictif_profile():
    questionnaire = Questionnaire([Question(id="q1", label="FICTIF q1", kind="text")])
    return questionnaire.build_profile("FICTIF John Doe", {"q1": "FICTIF"})


def test_generated_site_is_available_quickly():
    config = CockpitConfig.load(FIXTURES)
    generator = SiteGenerator(
        config.site, TermFilter.from_config(config.forbidden_terms)
    )
    roadmap = Roadmap.from_config(config.roadmap)
    start = time.monotonic()
    html = generator.generate(_fictif_profile(), roadmap)
    elapsed = time.monotonic() - start
    assert html
    assert elapsed < 300  # critère 8c6b7f37 : moins de 5 minutes


def test_generated_site_has_no_forbidden_terms():
    config = CockpitConfig.load(FIXTURES)
    term_filter = TermFilter.from_config(config.forbidden_terms)
    generator = SiteGenerator(config.site, term_filter)
    roadmap = Roadmap.from_config(config.roadmap)
    html = generator.generate(_fictif_profile(), roadmap)
    assert not term_filter.has_forbidden_terms(html)  # critère 00107720


def test_generator_refuses_forbidden_content():
    config = CockpitConfig.load(FIXTURES)
    generator = SiteGenerator(
        config.site, TermFilter.from_config(config.forbidden_terms)
    )
    roadmap = Roadmap([Milestone(id="j1", title="FICTIF", action="FICTIF TDAH")])
    with pytest.raises(SiteGenerationError):
        generator.generate(_fictif_profile(), roadmap)


def test_generator_rejects_invalid_color():
    config = CockpitConfig.load(FIXTURES)
    bad_config = dict(config.site, accent_color="red; color: blue")
    generator = SiteGenerator(
        bad_config, TermFilter.from_config(config.forbidden_terms)
    )
    with pytest.raises(SiteGenerationError):
        generator.generate(_fictif_profile(), Roadmap.from_config(config.roadmap))
