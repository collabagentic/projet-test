"""Filtre de termes interdits (contenant).

La liste des termes interdits est chargée depuis la configuration
(forbidden_terms.json). Aucun terme médical n'est codé en dur dans ce module.
"""
from __future__ import annotations


class TermFilter:
    """Détecte la présence de termes interdits dans un texte."""

    def __init__(self, terms: list[str]) -> None:
        self._terms = [str(term).strip().lower() for term in terms if str(term).strip()]

    @classmethod
    def from_config(cls, data: dict) -> TermFilter:
        """Construit le filtre depuis le dictionnaire de configuration."""
        return cls(data.get("terms", []))

    @property
    def terms(self) -> list[str]:
        """Liste normalisée (minuscules) des termes interdits."""
        return list(self._terms)

    def has_forbidden_terms(self, text: str) -> bool:
        """Retourne True si `text` contient au moins un terme interdit."""
        lowered = str(text).lower()
        return any(term in lowered for term in self._terms)
