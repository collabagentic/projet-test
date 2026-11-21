"""Pipeline de bout en bout (contenant).

Enchaîne les trois étapes du périmètre P1 :
1. remplir le questionnaire -> profil,
2. valider le profil -> générer le site standalone,
3. consulter le site et la roadmap.

Aucun contenu de domaine n'est inventé : tout vient de la configuration.
"""
from __future__ import annotations

from pathlib import Path

from .config import CockpitConfig
from .profile_store import save_profile
from .questionnaire import Profile
from .roadmap import Roadmap
from .site_generator import SiteGenerator
from .term_filter import TermFilter


class PipelineResult:
    """Résultat d'une exécution du pipeline."""

    def __init__(self, site_html: str, profile_path: Path, site_path: Path) -> None:
        self.site_html = site_html
        self.profile_path = profile_path
        self.site_path = site_path


def run_pipeline(
    config_dir: str | Path,
    profile: Profile,
    output_dir: str | Path,
) -> PipelineResult:
    """Exécute le parcours P1 et écrit le profil + le site standalone."""
    config = CockpitConfig.load(config_dir)
    roadmap = Roadmap.from_config(config.roadmap)
    term_filter = TermFilter.from_config(config.forbidden_terms)
    generator = SiteGenerator(config.site, term_filter)

    site_html = generator.generate(profile, roadmap)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    profile_path = save_profile(profile, out / "profil.json")
    site_path = out / "site.html"
    site_path.write_text(site_html, encoding="utf-8")
    return PipelineResult(site_html=site_html, profile_path=profile_path, site_path=site_path)
