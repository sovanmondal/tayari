"""Tests for localization + SMS dispatch (FR-5)."""
import pytest

from app.domain.impact_model import estimate_impact
from app.domain.models import AdminUnit, HazardSignal, Provenance
from app.domain.playbook import recommend
from app.domain.trigger_engine import evaluate
from app.services.localization import compose_message
from app.services.llm import violates_grounding
from app.services.sms import dispatch_sms

ADMIN = AdminUnit(id="KE-GAR", name="Garissa", country="Kenya")


def _ctx(cdi=8):
    sig = HazardSignal(value=cdi, valid_from="2021-05-01")
    trig = evaluate(sig)
    impact = estimate_impact(ADMIN, 841353, {"pastoralist": 0.78, "urban": 0.22},
                             triggered=trig.triggered,
                             sources=[Provenance(source="KNBS 2019 Census", url="x", retrieved_at=0.0)])
    return trig, impact, recommend(trig, impact)


def test_pastoralist_english_sms_segments():
    trig, impact, recs = _ctx()
    msg = compose_message("Garissa", "KE-GAR", trig, impact, recs, "pastoralist", "en", "sms")
    assert msg.text
    assert all(len(s) <= 160 for s in msg.sms_segments)
    assert "".join(msg.sms_segments).replace(" ", "")  # non-empty


def test_swahili_pastoralist_message():
    trig, impact, recs = _ctx()
    msg = compose_message("Garissa", "KE-GAR", trig, impact, recs, "pastoralist", "sw")
    assert "Uza mifugo" in msg.text  # "sell livestock" in Swahili
    assert msg.voice_script.count(msg.text) >= 1


def test_drm_message_is_grounded():
    trig, impact, recs = _ctx()
    msg = compose_message("Garissa", "KE-GAR", trig, impact, recs, "drm_officer", "en")
    assert not violates_grounding(msg.text, {"exposed": "841,353", "cdi": 8,
                                             "lead": recs[0].lead_time_days})


def test_voice_script_repeats():
    trig, impact, recs = _ctx()
    msg = compose_message("Garissa", "KE-GAR", trig, impact, recs, "farmer", "en", "voice")
    assert msg.voice_script.startswith("This is an early warning")


@pytest.mark.asyncio
async def test_sms_dispatch_simulated_without_creds():
    trig, impact, recs = _ctx()
    msg = compose_message("Garissa", "KE-GAR", trig, impact, recs, "pastoralist", "en")
    result = await dispatch_sms(msg)
    assert result["status"] == "queued"
    assert result["payload"]["message"]
    assert result["payload"]["admin_id"] == "KE-GAR"
    assert result["reference"].startswith("TYR-")
