"""Moteur de roadmap (contenant uniquement).

Les jalons et leurs actions sont chargés depuis un fichier de
configuration ; aucun jalon ni aucune action n'est écrit en dur.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .filtrage import find_forbidden_terms

# Décidé par le critère 5d04a7da (P1) : au moins 3 jalons.
MIN_JALONS = 3


class RoadmapError(ValueError):
    """Erreur de structure de la roadmap."""


def load_roadmap_config(path: str | Path) -> dict[str, Any]:
    """Charge la configuration de la roadmap depuis un fichier JSON."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def generate_roadmap(config: dict[str, Any], forbidden_terms: list[str]) -> dict[str, Any]:
    """Valide et rend la roadmap depuis sa configuration.

    Chaque jalon doit avoir un 'titre' et une 'action' non vides. Le
    contenu de ces champs est du domaine (non décidé) : il est attendu
    comme emplacement A_DEFINIR_* dans la configuration.
    """
    jalons = config.get("jalons")
    if not isinstance(jalons, list):
        raise RoadmapError("la configuration doit contenir une liste 'jalons'")
    if len(jalons) < MIN_JALONS:
        raise RoadmapError(
            f"la roadmap doit contenir au moins {MIN_JALONS} jalons "
            f"(trouvé : {len(jalons)})"
        )
    rendered = []
    for jalon in jalons:
        if not isinstance(jalon, dict):
            raise RoadmapError("chaque jalon doit être un objet")
        titre = jalon.get("titre")
        action = jalon.get("action")
        if not titre or not action:
            raise RoadmapError("chaque jalon doit avoir un 'titre' et une 'action' non vides")
        hits = find_forbidden_terms(f"{titre} {action}", forbidden_terms)
        if hits:
            raise RoadmapError(f"le jalon {jalon.get('id')!r} contient un terme interdit : {hits}")
        rendered.append({"id": jalon.get("id"), "titre": titre, "action": action})
    return {"jalons": rendered}
