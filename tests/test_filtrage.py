"""Tests du filtre de termes interdits (contenant)."""
from pathlib import Path

from cockpit.filtrage import find_forbidden_terms, is_clean, load_forbidden_terms

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "termes_interdits.json"


def test_load_forbidden_terms():
    assert load_forbidden_terms(CONFIG) == ["tdah", "dyslexie", "autisme"]


def test_detects_forbidden_term_case_insensitive():
    terms = ["tdah", "dyslexie", "autisme"]
    assert find_forbidden_terms("Un contenu mentionnant TDAH", terms) == ["tdah"]


def test_clean_text_has_no_forbidden_term():
    terms = ["tdah", "dyslexie", "autisme"]
    assert is_clean("Texte sans terme interdit", terms)


def test_detects_multiple_terms_sorted():
    terms = ["tdah", "dyslexie", "autisme"]
    assert find_forbidden_terms("Dyslexie et autisme", terms) == ["autisme", "dyslexie"]
