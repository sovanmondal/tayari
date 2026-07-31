"""Anticipatory-action playbook engine (FR-4.1).

Maps a fired trigger's severity to a ranked list of anticipatory actions from the
real drought AA playbook. Deterministic (no LLM).
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from app.domain.models import EvidenceLink, ImpactEstimate, Recommendation, Trigger

PLAYBOOK_PATH = Path(__file__).resolve().parent.parent / "data" / "playbook_drought.yaml"


@lru_cache(maxsize=1)
def _playbook() -> dict:
    return yaml.safe_load(PLAYBOOK_PATH.read_text())


def recommend(trigger: Trigger, impact: ImpactEstimate | None = None) -> list[Recommendation]:
    """Return ranked anticipatory actions for the trigger's severity.

    If not triggered, returns the 'watch'/monitor actions (preparatory).
    """
    pb = _playbook()["actions_by_severity"]
    severity = trigger.severity.value
    actions = pb.get(severity) or pb.get("watch", [])

    ranked = sorted(actions, key=lambda a: a.get("priority", 0), reverse=True)
    recs: list[Recommendation] = []
    for i, a in enumerate(ranked, start=1):
        recs.append(
            Recommendation(
                rank=i,
                action=a["action"],
                lead_time_days=int(a["lead_time_days"]),
                cost_band=a["cost_band"],
                actor=a["actor"],
                window=a["window"],
                evidence=[],  # attached by evidence.build_chain in the service layer
            )
        )
    return recs
