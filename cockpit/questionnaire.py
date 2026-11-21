"""Moteur de questionnaire de profil (contenant uniquement).

Les questions sont chargées depuis un fichier de configuration ; aucun
libellé de question n'est écrit en dur dans le code.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Décidé par le critère 6f7b35fa (P1) : maximum 15 questions.
MAX_QUESTIONS = 15


class QuestionnaireError(ValueError):
    """Erreur de structure ou de validation du questionnaire."""


def load_questionnaire(path: str | Path) -> dict[str, Any]:
    """Charge le questionnaire depuis un fichier JSON et valide sa structure."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise QuestionnaireError("le questionnaire doit contenir au moins une question")
    if len(questions) > MAX_QUESTIONS:
        raise QuestionnaireError(
            f"le questionnaire contient {len(questions)} questions "
            f"(maximum autorisé : {MAX_QUESTIONS})"
        )
    for question in questions:
        if not isinstance(question, dict):
            raise QuestionnaireError("chaque question doit être un objet")
        if not question.get("id") or not question.get("label"):
            raise QuestionnaireError("chaque question doit avoir un 'id' et un 'label'")
    return data


def list_questions(questionnaire: dict[str, Any]) -> list[dict[str, Any]]:
    """Retourne la liste des questions du questionnaire."""
    return list(questionnaire["questions"])


def collect_profile(questionnaire: dict[str, Any], answers: dict[str, str]) -> dict[str, Any]:
    """Construit un profil enfant à partir des réponses du parent.

    Le profil est une simple structure de données (contenant) : aucune
    interprétation, aucun conseil ni aucun diagnostic n'est produit ici.
    """
    valid_ids = {question["id"] for question in questionnaire["questions"]}
    unknown = set(answers) - valid_ids
    if unknown:
        raise QuestionnaireError(f"réponses inconnues : {sorted(unknown)}")
    missing = valid_ids - set(answers)
    if missing:
        raise QuestionnaireError(f"réponses manquantes : {sorted(missing)}")
    return {"reponses": dict(answers)}
