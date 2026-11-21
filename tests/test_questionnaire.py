"""Tests du moteur de questionnaire (contenant)."""
import json
from pathlib import Path

import pytest

from cockpit.questionnaire import (
    MAX_QUESTIONS,
    QuestionnaireError,
    collect_profile,
    list_questions,
    load_questionnaire,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "questionnaire.json"


def test_load_questionnaire_valid():
    questionnaire = load_questionnaire(CONFIG)
    assert len(list_questions(questionnaire)) == 3


def test_questionnaire_respects_max_questions():
    questionnaire = load_questionnaire(CONFIG)
    assert len(list_questions(questionnaire)) <= MAX_QUESTIONS


def test_rejects_too_many_questions(tmp_path):
    data = {"questions": [{"id": f"q{i}", "label": f"FICTIF_Q{i}"} for i in range(16)]}
    path = tmp_path / "q.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(QuestionnaireError):
        load_questionnaire(path)


def test_collect_profile_complete():
    questionnaire = load_questionnaire(CONFIG)
    answers = {"q1": "FICTIF_R1", "q2": "FICTIF_R2", "q3": "FICTIF_R3"}
    assert collect_profile(questionnaire, answers) == {"reponses": answers}


def test_collect_profile_rejects_unknown_answer():
    questionnaire = load_questionnaire(CONFIG)
    with pytest.raises(QuestionnaireError):
        collect_profile(questionnaire, {"inconnue": "x"})


def test_collect_profile_rejects_missing_answer():
    questionnaire = load_questionnaire(CONFIG)
    with pytest.raises(QuestionnaireError):
        collect_profile(questionnaire, {"q1": "x"})
