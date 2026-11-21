"""Générateur de site standalone (contenant).

Le site est généré à partir d'un gabarit vide et de valeurs chargées depuis la
configuration (titre, couleur). Aucun contenu de domaine n'est codé en dur.
Le générateur refuse de produire un site contenant un terme interdit
(critère 00107720).
"""
from __future__ import annotations

import html as _html
import re

from .questionnaire import Profile
from .roadmap import Roadmap
from .term_filter import TermFilter

_COLOR_RE = re.compile(r"[a-zA-Z0-9#_(),.% -]{1,64}")


class SiteGenerationError(ValueError):
    """Levée quand le site généré ne respecte pas les contraintes du contenant."""


class SiteGenerator:
    """Génère un site HTML standalone pour un profil et une roadmap."""

    def __init__(self, site_config: dict, term_filter: TermFilter) -> None:
        self._site_config = site_config
        self._term_filter = term_filter

    def generate(self, profile: Profile, roadmap: Roadmap) -> str:
        """Retourne le HTML du site standalone, ou lève SiteGenerationError."""
        site_title = str(self._site_config.get("site_title", ""))
        accent_color = str(self._site_config.get("accent_color", ""))
        if not site_title:
            raise SiteGenerationError("Configuration du site incomplète (site_title).")
        if not accent_color or not _COLOR_RE.fullmatch(accent_color):
            raise SiteGenerationError("Configuration du site invalide (accent_color).")
        rendered = self._render(profile, roadmap, site_title, accent_color)
        if self._term_filter.has_forbidden_terms(rendered):
            raise SiteGenerationError(
                "Le site généré contient un terme interdit (critère 00107720)."
            )
        return rendered

    @staticmethod
    def _render(
        profile: Profile, roadmap: Roadmap, site_title: str, accent_color: str
    ) -> str:
        title = _html.escape(site_title)
        child_name = _html.escape(profile.child_name)
        roadmap_html = roadmap.render_html()
        return (
            "<!doctype html>\n"
            '<html lang="fr">\n'
            "<head>\n"
            '<meta charset="utf-8">\n'
            f"<title>{title}</title>\n"
            "<style>\n"
            "body { font-family: sans-serif; margin: 2rem; }\n"
            f"h1 {{ color: {accent_color}; }}\n"
            "</style>\n"
            "</head>\n"
            "<body>\n"
            f"<h1>{title}</h1>\n"
            "<section>\n"
            "<h2>Profil</h2>\n"
            f"<p>{child_name}</p>\n"
            "</section>\n"
            "<section>\n"
            "<h2>Roadmap</h2>\n"
            f"{roadmap_html}\n"
            "</section>\n"
            "</body>\n"
            "</html>\n"
        )
