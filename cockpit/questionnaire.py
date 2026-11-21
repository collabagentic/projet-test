"""Moteur de questionnaire (contenant).

Le questionnaire est chargé depuis la configuration : aucune question, aucun
libellé ni seuil n'est codé en dur. Le moteur impose uniquement la contrainte
structurale « au maximum 15 questions » (critère 6f7b35fa).
"""
from __future__ import annotations

from dataclasses import dataclass

MAX_QUESTIONS = 15


class TooManyQuestionsError(ValueError):
    """Levée quand le questionnaire dépasse le maximum autorisé de questions."""


@dataclass(frozen=True)
class Question:
    """Une question du questionnaire, chargée depuis la configuration."""

    id: str
    label: str
    kind: str


@dataclass(frozen=True)
class Profile:
    """Profil enfant : nom et réponses au questionnaire."""

    child_name: str
    answers: dict


@dataclass
class Questionnaire:
    """Liste de questions et construction d'un profil."""

    questions: list[Question]

    def __post_init__(self) -> None:
        if len(self.questions) > MAX_QUESTIONS:
            raise TooManyQuestionsError(
                f"{len(self.questions)} questions, maximum autorisé : "
                f"{MAX_QUESTIONS} (critère 6f7b35fa)."
            )

    @classmethod
    def from_config(cls, data: dict) -> Questionnaire:
        """Construit le questionnaire depuis le dictionnaire de configuration."""
        questions = [
            Question(
                id=str(item["id"]),
                label=str(item["label"]),
                kind=str(item.get("kind", "text")),
            )
            for item in data.get("questions", [])
        ]
        return cls(questions)

    @property
    def question_count(self) -> int:
        """Nombre de questions du questionnaire."""
        return len(self.questions)

    def build_profile(self, child_name: str, answers: dict) -> Profile:
        """Construit un profil en ne conservant que les réponses connues."""
        known = {question.id for question in self.questions}
        filtered = {key: value for key, value in answers.items() if key in known}
        return Profile(child_name=child_name, answers=filtered)
