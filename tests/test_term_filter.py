"""Tests du filtre de termes interdits (contenant)."""
from pathlib import Path

from cockpit.config import CockpitConfig
from cockpit.term_filter import TermFilter

CONFIG_DIR = Path(__file__).parent.parent / "config"


def test_filter_loaded_from_config():
    config = CockpitConfig.load(CONFIG_DIR)
    term_filter = TermFilter.from_config(config.forbidden_terms)
    assert term_filter.terms


def test_filter_detects_forbidden_term_case_insensitive():
    term_filter = TermFilter(["TDAH", "dyslexie", "autisme"])
    assert term_filter.has_forbidden_terms("suspicion de tdah")
    assert term_filter.has_forbidden_terms("Dyslexie éventuelle")


def test_filter_accepts_clean_text():
    term_filter = TermFilter(["TDAH", "dyslexie", "autisme"])
    assert not term_filter.has_forbidden_terms("Texte sans terme médical.")


def test_filter_empty_terms_accepts_everything():
    assert not TermFilter([]).has_forbidden_terms("TDAH")
