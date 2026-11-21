"""Rendu de la roadmap (contenant).

Les jalons et leurs actions concrètes sont chargés depuis la configuration
(roadmap.json). Le moteur garantit uniquement la structure (jalons + action) ;
il n'invente aucun contenu.
"""
from __future__ import annotations

import html as _html
from dataclasses import dataclass


@dataclass(frozen=True)
class Milestone:
    """Un jalon de la roadmap, chargé depuis la configuration."""

    id: str
    title: str
    action: str


@dataclass
class Roadmap:
    """Liste de jalons."""

    milestones: list[Milestone]

    @classmethod
    def from_config(cls, data: dict) -> Roadmap:
        """Construit la roadmap depuis le dictionnaire de configuration."""
        milestones = [
            Milestone(
                id=str(item["id"]),
                title=str(item["title"]),
                action=str(item["action"]),
            )
            for item in data.get("milestones", [])
        ]
        return cls(milestones)

    @property
    def count(self) -> int:
        """Nombre de jalons."""
        return len(self.milestones)

    def render(self) -> str:
        """Rend la roadmap en texte simple (sans contenu de domaine ajouté)."""
        lines = ["Roadmap"]
        for milestone in self.milestones:
            lines.append(f"- {milestone.title} : {milestone.action}")
        return "\n".join(lines)

    def render_html(self) -> str:
        """Rend la roadmap sous forme de liste HTML (échappée)."""
        items = "".join(
            f"<li>{_html.escape(milestone.title)} : {_html.escape(milestone.action)}</li>"
            for milestone in self.milestones
        )
        return f"<ul>{items}</ul>"
