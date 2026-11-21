"""Tests du moteur de roadmap (contenant)."""
from pathlib import Path

import pytest

from cockpit.roadmap import MIN_JALONS, RoadmapError, generate_roadmap, load_roadmap_config

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "roadmap.json"


def test_roadmap_has_at_least_min_jalons():
    roadmap = generate_roadmap(load_roadmap_config(CONFIG), [])
    assert len(roadmap["jalons"]) >= MIN_JALONS
    assert all(j["titre"] and j["action"] for j in roadmap["jalons"])


def test_rejects_fewer_than_min_jalons():
    config = {"jalons": [{"id": "j1", "titre": "FICTIF", "action": "FICTIF"}]}
    with pytest.raises(RoadmapError):
        generate_roadmap(config, [])


def test_rejects_jalon_with_forbidden_term():
    config = {
        "jalons": [
            {"id": "j1", "titre": "FICTIF", "action": "FICTIF"},
            {"id": "j2", "titre": "FICTIF", "action": "FICTIF"},
            {"id": "j3", "titre": "FICTIF", "action": "FICTIF sur TDAH"},
        ]
    }
    with pytest.raises(RoadmapError):
        generate_roadmap(config, ["tdah"])
