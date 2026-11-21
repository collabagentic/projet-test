"""Moteur de génération de site dédié standalone (contenant uniquement).

Le site produit est un fichier HTML autonome (pas de base centrale). Les
textes visibles proviennent de la configuration et du gabarit ; aucun
contenu de domaine n'est écrit en dur.
"""
from __future__ import annotations

import html
import time
from pathlib import Path
from typing import Any

from .filtrage import find_forbidden_terms
from .roadmap import generate_roadmap

# Décidé par le critère 8c6b7f37 (P1) : génération en moins de 5 minutes.
MAX_GENERATION_SECONDS = 300.0

# Marqueur des emplacements non décidés (voir contrat de contenu dans tasks.md).
OPEN_PLACEHOLDER_MARKER = "A_DEFINIR_"


class SiteGenerationError(ValueError):
    """Erreur de génération du site."""


def render_template(template: str, values: dict[str, str]) -> str:
    """Remplace les jetons '[[ cle ]]' du gabarit par leurs valeurs."""
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"[[ {key} ]]", str(value))
    if "[[" in rendered:
        raise SiteGenerationError("gabarit incomplet : des jetons restent non résolus")
    return rendered


def _reject_open_placeholders(*texts: str) -> None:
    """Refuse la génération si un emplacement A_DEFINIR_* reste ouvert."""
    for text in texts:
        if OPEN_PLACEHOLDER_MARKER in text:
            raise SiteGenerationError(
                "un emplacement A_DEFINIR_* reste ouvert ; "
                "la génération est refusée tant que le contenu n'est pas décidé"
            )


def generate_site(
    profile: dict[str, Any],
    site_config: dict[str, Any],
    roadmap_config: dict[str, Any],
    forbidden_terms: list[str],
    template_path: str | Path,
) -> dict[str, Any]:
    """Génère un site HTML standalone pour un profil validé.

    Retourne un dictionnaire avec le HTML produit, les jalons rendus et le
    temps de génération mesuré.
    """
    started = time.perf_counter()

    roadmap = generate_roadmap(roadmap_config, forbidden_terms)

    values = {
        "titre": str(site_config.get("titre", "")),
        "theme": str(site_config.get("theme", "")),
        "logo": str(site_config.get("logo", "")),
        "accompagnateur": str(site_config.get("accompagnateur", "")),
    }

    jalon_blocks = []
    for jalon in roadmap["jalons"]:
        titre = html.escape(jalon["titre"])
        action = html.escape(jalon["action"])
        jalon_blocks.append(f"<li><strong>{titre}</strong> — {action}</li>")
    values["jalons"] = "".join(jalon_blocks)

    _reject_open_placeholders(
        values["titre"],
        values["theme"],
        values["logo"],
        values["accompagnateur"],
        values["jalons"],
    )

    template = Path(template_path).read_text(encoding="utf-8")
    html_content = render_template(template, values)

    hits = find_forbidden_terms(html_content, forbidden_terms)
    if hits:
        raise SiteGenerationError(f"le site généré contient un terme interdit : {hits}")

    elapsed = time.perf_counter() - started
    if elapsed > MAX_GENERATION_SECONDS:
        raise SiteGenerationError(
            f"génération trop lente : {elapsed:.1f}s "
            f"(maximum {MAX_GENERATION_SECONDS:.0f}s)"
        )

    return {
        "html": html_content,
        "jalons": roadmap["jalons"],
        "elapsed_seconds": round(elapsed, 4),
    }
