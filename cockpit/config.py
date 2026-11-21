"""Chargement de la configuration (contenant).

Le contenu de domaine (questions, jalons, thèmes, termes interdits) n'est
jamais codé en dur : il est chargé depuis des fichiers JSON situés dans un
répertoire de configuration.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class ConfigError(ValueError):
    """Erreur de configuration (fichier absent, JSON invalide)."""


def load_json(path: str | Path) -> dict:
    """Charge un fichier JSON et retourne son contenu sous forme de dict."""
    file = Path(path)
    if not file.is_file():
        raise ConfigError(f"Fichier de configuration introuvable : {file}")
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"JSON invalide dans {file} : {exc}") from exc


@dataclass(frozen=True)
class CockpitConfig:
    """Regroupe les quatre fichiers de configuration du contenant."""

    questionnaire: dict
    roadmap: dict
    site: dict
    forbidden_terms: dict

    @classmethod
    def load(cls, config_dir: str | Path) -> CockpitConfig:
        """Charge l'ensemble de la configuration depuis `config_dir`."""
        base = Path(config_dir)
        return cls(
            questionnaire=load_json(base / "questionnaire.json"),
            roadmap=load_json(base / "roadmap.json"),
            site=load_json(base / "site.json"),
            forbidden_terms=load_json(base / "forbidden_terms.json"),
        )
