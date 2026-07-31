"""Deterministic unit tests for the trigger engine (FR-2.2), CDI class legend."""
from app.domain.models import HazardSignal, Severity
from app.domain.trigger_engine import class_info, classify_severity, evaluate


def test_class_legend_names_and_severity():
    assert class_info(0)["name"] == "No drought"
    assert class_info(0)["severity"] == Severity.NONE
    assert class_info(1)["severity"] == Severity.WATCH
    assert class_info(2)["severity"] == Severity.WARNING
    assert class_info(3)["severity"] == Severity.ALERT
    assert class_info(6)["severity"] == Severity.NONE          # recovery
    assert class_info(9)["severity"] == Severity.ALERT
    assert class_info(9)["assumed"] is True                     # extended class flagged


def test_warning_class_triggers_action():
    t = evaluate(HazardSignal(value=2))
    assert t.triggered is True
    assert t.severity == Severity.WARNING
    assert t.exceedance == 0.0
    assert "at or above" in t.rationale


def test_alert_class_triggers_with_positive_margin():
    t = evaluate(HazardSignal(value=3))
    assert t.triggered is True
    assert t.severity == Severity.ALERT
    assert t.exceedance == 1.0


def test_watch_class_does_not_trigger():
    t = evaluate(HazardSignal(value=1))
    assert t.triggered is False
    assert t.severity == Severity.WATCH
    assert "monitor" in t.rationale.lower()


def test_recovery_class_does_not_trigger():
    t = evaluate(HazardSignal(value=6))  # Recovery -> none
    assert t.triggered is False
    assert t.severity == Severity.NONE


def test_deterministic_repeatable():
    assert evaluate(HazardSignal(value=2)).model_dump() == evaluate(HazardSignal(value=2)).model_dump()
