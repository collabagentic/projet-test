"""Filtre de termes interdits (contenant uniquement).

La liste des termes est chargée depuis un fichier de configuration ;
aucune liste de termes n'est écrite en dur dans le code.
"""
from __future__ import annotations

import json
from pathlib import Path


def load_forbidden_terms(path: str | Path) -> list[str]:
    """Charge la liste des termes interdits depuis un fichier JSON.

    Le fichier doit contenir une clé 'termes' (liste de chaînes).
    Les termes sont normalisés (espaces retirés, minuscules).
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = data.get("termes", [])
    if not isinstance(raw, list):
        raise TypeError("la configuration 'termes_interdits' doit contenir une liste 'termes'")
    return [str(item).strip().lower() for item in raw if str(item).strip()]


def find_forbidden_terms(text: str, terms: list[str]) -> list[str]:
    """Retourne les termes interdits présents dans 'text' (insensible à la casse)."""
    lowered = text.lower()
    return sorted({term for term in terms if term in lowered})


def is_clean(text: str, terms: list[str]) -> bool:
    """Vrai si 'text' ne contient aucun terme interdit."""
    return not find_forbidden_terms(text, terms)
