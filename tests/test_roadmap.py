"""Tests du rendu de roadmap (contenant)."""
from pathlib import Path

from cockpit.config import CockpitConfig
from cockpit.roadmap import Roadmap

CONFIG_DIR = Path(__file__).parent.parent / "config"
FIXTURES = Path(__file__).parent / "fixtures"


def test_shipped_roadmap_has_at_least_three_milestones():
    config = CockpitConfig.load(CONFIG_DIR)
    assert Roadmap.from_config(config.roadmap).count >= 3


def test_roadmap_milestones_have_concrete_actions():
    # Fixture FICTIF : jalons avec actions concrètes fictives (env. non exposé).
    config = CockpitConfig.load(FIXTURES)
    roadmap = Roadmap.from_config(config.roadmap)
    assert roadmap.count >= 3
    for milestone in roadmap.milestones:
        assert milestone.action.strip()


def test_roadmap_renders_milestones():
    config = CockpitConfig.load(FIXTURES)
    roadmap = Roadmap.from_config(config.roadmap)
    text = roadmap.render()
    for milestone in roadmap.milestones:
        assert milestone.title in text
