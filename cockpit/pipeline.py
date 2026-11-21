"""Pipeline de bout en bout du parcours P1 (contenant uniquement)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .questionnaire import collect_profile, load_questionnaire
from .site import generate_site


def run_pipeline(
    questionnaire_path: str | Path,
    answers: dict[str, str],
    site_config: dict[str, Any],
    roadmap_config: dict[str, Any],
    forbidden_terms: list[str],
    template_path: str | Path,
) -> dict[str, Any]:
    """Exécute le parcours P1 : questionnaire -> profil -> site + roadmap.

    Le profil est validé par collect_profile (aucune réponse inconnue ni
    manquante), puis le site standalone et la roadmap sont générés.
    """
    questionnaire = load_questionnaire(questionnaire_path)
    profile = collect_profile(questionnaire, answers)
    site = generate_site(
        profile,
        site_config,
        roadmap_config,
        forbidden_terms,
        template_path,
    )
    return {
        "profil": profile,
        "site_html": site["html"],
        "jalons": site["jalons"],
        "elapsed_seconds": site["elapsed_seconds"],
    }
