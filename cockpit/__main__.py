"""Point d'entrée de démonstration (FICTIF, environnement non exposé).

Usage : python -m cockpit [config_dir] [output_dir] [child_name]
"""
from __future__ import annotations

import sys
from pathlib import Path

from .config import CockpitConfig
from .pipeline import run_pipeline
from .questionnaire import Questionnaire


def main(argv: list[str] | None = None) -> int:
    """Génère un site de démonstration FICTIF à partir de la configuration."""
    args = list(sys.argv[1:] if argv is None else argv)
    config_dir = Path(args[0]) if args else Path("config")
    output_dir = Path(args[1]) if len(args) > 1 else Path("demo_output")
    child_name = args[2] if len(args) > 2 else "FICTIF John Doe"

    config = CockpitConfig.load(config_dir)
    questionnaire = Questionnaire.from_config(config.questionnaire)
    answers = {q.id: f"FICTIF réponse {q.id}" for q in questionnaire.questions}
    profile = questionnaire.build_profile(child_name, answers)

    result = run_pipeline(config_dir, profile, output_dir)
    print(f"Profil enregistré : {result.profile_path}")
    print(f"Site standalone : {result.site_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
