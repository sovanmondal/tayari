"""Trigger engine — deterministic CDI-class -> severity -> trigger (FR-2).

NO LLM involvement. Pure, unit-testable. Loads the real EDO/EADW CDI class legend
from data/thresholds.yaml.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from app.domain.models import HazardSignal, Severity, Trigger

THRESHOLDS_PATH = Path(__file__).resolve().parent.parent / "data" / "thresholds.yaml"


@lru_cache(maxsize=1)
def _config() -> dict:
    return yaml.safe_load(THRESHOLDS_PATH.read_text())


def _rank(sev: Severity) -> int:
    return _config()["severity_rank"][sev.value]


def class_info(value: float) -> dict:
    """Return {name, severity} for a CDI class value (nearest integer class)."""
    legend = _config()["class_legend"]
    key = int(round(value))
    if key not in legend:
        # Out-of-legend high classes are treated as the top defined class.
        key = max(k for k in legend if isinstance(k, int))
    entry = legend[key]
    return {"name": entry["name"], "severity": Severity(entry["severity"]),
            "assumed": bool(entry.get("assumed", False))}


def classify_severity(value: float) -> Severity:
    return class_info(value)["severity"]


def evaluate(signal: HazardSignal) -> Trigger:
    """Evaluate a CDI hazard signal against the class legend -> Trigger (deterministic)."""
    cfg = _config()
    trigger_sev = Severity(cfg["trigger_severity"])
    trigger_rank = _rank(trigger_sev)

    value = float(signal.value)
    info = class_info(value)
    severity = info["severity"]
    sev_rank = _rank(severity)
    triggered = sev_rank >= trigger_rank
    exceedance = sev_rank - trigger_rank

    assumed_note = " (extended class — mapping assumed)" if info["assumed"] else ""
    if triggered:
        rationale = (
            f"{signal.indicator} class {int(round(value))} = '{info['name']}'{assumed_note}, "
            f"severity '{severity.value}', at or above the anticipatory-action trigger "
            f"('{trigger_sev.value}'). Severity margin {exceedance:+d}."
        )
    else:
        rationale = (
            f"{signal.indicator} class {int(round(value))} = '{info['name']}'{assumed_note}, "
            f"severity '{severity.value}', below the trigger ('{trigger_sev.value}'). "
            f"{trigger_rank - sev_rank} severity step(s) to trigger — monitor."
        )

    return Trigger(
        triggered=triggered,
        severity=severity,
        indicator=signal.indicator,
        observed_value=value,
        threshold=float(trigger_rank),
        exceedance=float(exceedance),
        distance_to_trigger=float(trigger_rank - sev_rank),
        rationale=rationale,
    )
