"""Tests du moteur de questionnaire (contenant)."""
import time
from pathlib import Path

import pytest

from cockpit.config import CockpitConfig
from cockpit.questionnaire import (
    MAX_QUESTIONS,
    Question,
    Questionnaire,
    TooManyQuestionsError,
)

CONFIG_DIR = Path(__file__).parent.parent / "config"


def test_shipped_questionnaire_respects_max_questions():
    config = CockpitConfig.load(CONFIG_DIR)
    questionnaire = Questionnaire.from_config(config.questionnaire)
    assert questionnaire.question_count <= MAX_QUESTIONS


def test_questionnaire_accepts_exactly_fifteen_questions():
    questions = [
        Question(id=f"q{i}", label=f"FICTIF question {i}", kind="text")
        for i in range(15)
    ]
    assert Questionnaire(questions).question_count == 15


def test_questionnaire_rejects_more_than_fifteen_questions():
    questions = [
        Question(id=f"q{i}", label=f"FICTIF question {i}", kind="text")
        for i in range(16)
    ]
    with pytest.raises(TooManyQuestionsError):
        Questionnaire(questions)


def test_build_profile_keeps_known_answers_only():
    questionnaire = Questionnaire([Question(id="q1", label="FICTIF q1", kind="text")])
    profile = questionnaire.build_profile(
        "FICTIF John Doe", {"q1": "FICTIF", "inconnue": "ignorée"}
    )
    assert profile.answers == {"q1": "FICTIF"}


def test_profile_fill_completes_under_ten_minutes():
    questions = [
        Question(id=f"q{i}", label=f"FICTIF question {i}", kind="text")
        for i in range(15)
    ]
    questionnaire = Questionnaire(questions)
    start = time.monotonic()
    answers = {q.id: f"FICTIF réponse {q.id}" for q in questions}
    profile = questionnaire.build_profile("FICTIF John Doe", answers)
    elapsed = time.monotonic() - start
    assert profile.answers
    assert elapsed < 600  # critère 6f7b35fa : moins de 10 minutes
