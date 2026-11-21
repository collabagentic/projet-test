"""Stockage standalone du profil (contenant).

Le profil est enregistré dans un fichier JSON local : aucune base de données
centrale (contrainte « site standalone » de l'objectif).
"""
from __future__ import annotations

import json
from pathlib import Path

from .questionnaire import Profile


def save_profile(profile: Profile, path: str | Path) -> Path:
    """Enregistre le profil en JSON et retourne le chemin écrit."""
    file = Path(path)
    data = {"child_name": profile.child_name, "answers": profile.answers}
    file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return file


def load_profile(path: str | Path) -> Profile:
    """Recharge un profil enregistré."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Profile(child_name=data["child_name"], answers=data["answers"])
