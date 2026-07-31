"""Tests for playbook ranking, evidence chain, and LLM grounding guard (FR-4)."""
from app.domain.evidence import build_chain
from app.domain.impact_model import estimate_impact
from app.domain.models import AdminUnit, HazardSignal, Provenance
from app.domain.playbook import recommend
from app.domain.trigger_engine import evaluate
from app.services.llm import violates_grounding
from app.services.narrative import compose_ibf_narrative

ADMIN = AdminUnit(id="KE-GAR", name="Garissa", country="Kenya")
PROV = Provenance(source="HDX/ICPAC EADW CDI", url="https://data.humdata.org/x.tif", retrieved_at=0.0)


def _pipeline(cdi: float):
    sig = HazardSignal(value=cdi, valid_from="2021-05-01")
    trig = evaluate(sig)
    impact = estimate_impact(ADMIN, 841353, {"pastoralist": 0.78, "agro-pastoralist": 0.12, "urban": 0.10},
                             triggered=trig.triggered,
                             sources=[Provenance(source="KNBS 2019 Census", url="https://knbs.or.ke", retrieved_at=0.0)])
    return sig, trig, impact


def test_alert_playbook_ranked_and_actionable():
    _, trig, impact = _pipeline(8)  # Alert
    recs = recommend(trig, impact)
    assert recs[0].rank == 1
    assert recs[0].lead_time_days > 0
    # highest-priority alert action is emergency water trucking
    assert "water trucking" in recs[0].action.lower()
    # ranks are strictly increasing
    assert [r.rank for r in recs] == list(range(1, len(recs) + 1))


def test_warning_playbook_prioritises_early_destocking():
    _, trig, impact = _pipeline(2)  # Warning
    recs = recommend(trig, impact)
    assert "destocking" in recs[0].action.lower()


def test_evidence_chain_has_sources():
    sig, trig, impact = _pipeline(8)
    chain = build_chain(sig, trig, impact, PROV, "Garissa")
    assert len(chain) == 4
    assert all(link.source for link in chain)
    assert "841,353".replace(",", "") in "".join(l.detail for l in chain).replace(",", "")


def test_narrative_is_grounded_no_new_numbers():
    _, trig, impact = _pipeline(8)
    recs = recommend(trig, impact)
    text = compose_ibf_narrative("Garissa", trig, impact, recs)
    context = {"exposed": f"{impact.total_population_exposed:,}", "cdi": 8,
               "leads": " ".join(str(r.lead_time_days) for r in recs)}
    # The composed narrative must not introduce numbers outside the computed facts.
    assert not violates_grounding(text, {**context, "pop": impact.total_population_exposed,
                                         "b": " ".join(f"{b.population}" for b in impact.by_livelihood)})


def test_grounding_guard_flags_invented_number():
    assert violates_grounding("We expect 999999 deaths", {"exposed": "841,353"}) is True
    assert violates_grounding("Exposed: 841,353 people", {"exposed": "841,353"}) is False
