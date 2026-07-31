"""IBF orchestration service — ties the real pipeline together (design §4).

county_hazard_signals (real CDI raster) -> per county: trigger -> impact -> playbook ->
evidence chain -> grounded narrative. Results are cached per as-of dekad for speed (NFR-4).
"""
from __future__ import annotations

from functools import lru_cache

from app.config import settings
from app.data.exposure_ke import CENSUS_SOURCE, COUNTIES, county_by_id
from app.domain.evidence import build_chain
from app.domain.impact_model import estimate_impact
from app.domain.models import AdminUnit, Provenance
from app.domain.playbook import recommend
from app.domain.trigger_engine import class_info, evaluate
from app.services.hazard import county_hazard_signals
from app.services.narrative import compose_ibf_narrative

_CACHE: dict[str, dict] = {}


def _census_prov() -> Provenance:
    return Provenance(source=CENSUS_SOURCE, url="https://www.knbs.or.ke/", retrieved_at=0.0)


async def _compute(as_of: str) -> dict:
    """Compute the full IBF bundle for all counties for a given dekad. Cached."""
    if as_of in _CACHE:
        return _CACHE[as_of]

    signals, hazard_prov = await county_hazard_signals(COUNTIES, as_of)
    bundle: dict[str, dict] = {}
    for c in COUNTIES:
        admin = AdminUnit(id=c["id"], name=c["name"], country=c["country"])
        sig = signals[c["id"]]
        trig = evaluate(sig)
        impact = estimate_impact(
            admin, c["population"], c["livelihood"],
            triggered=trig.triggered, sources=[_census_prov()],
        )
        recs = recommend(trig, impact)
        chain = build_chain(sig, trig, impact, hazard_prov, c["name"])
        # attach evidence chain to the top recommendation
        if recs:
            recs[0].evidence = chain
        narrative = compose_ibf_narrative(c["name"], trig, impact, recs)
        bundle[c["id"]] = {
            "admin": admin,
            "county": c,
            "signal": sig,
            "trigger": trig,
            "impact": impact,
            "recommendations": recs,
            "evidence": chain,
            "narrative": narrative,
            "hazard_provenance": hazard_prov,
        }
    _CACHE[as_of] = bundle
    return bundle


async def list_districts(as_of: str | None = None) -> list[dict]:
    as_of = as_of or settings.cdi_as_of
    bundle = await _compute(as_of)
    out = []
    for cid, b in bundle.items():
        c, trig = b["county"], b["trigger"]
        out.append({
            "id": cid, "name": c["name"], "country": c["country"],
            "lon": c["lon"], "lat": c["lat"], "population": c["population"],
            "cdi_class": int(round(trig.observed_value)),
            "cdi_label": class_info(trig.observed_value)["name"],
            "severity": trig.severity.value, "triggered": trig.triggered,
            "population_exposed": b["impact"].total_population_exposed,
            "as_of": b["signal"].valid_from,
        })
    return out


async def get_ibf(admin_id: str, as_of: str | None = None) -> dict | None:
    as_of = as_of or settings.cdi_as_of
    if county_by_id(admin_id) is None:
        return None
    b = (await _compute(as_of))[admin_id]
    return {
        "admin": b["admin"].model_dump(),
        "as_of": b["signal"].valid_from,
        "cdi_class": int(round(b["trigger"].observed_value)),
        "cdi_label": class_info(b["trigger"].observed_value)["name"],
        "severity": b["trigger"].severity.value,
        "trigger": b["trigger"].model_dump(),
        "impact": b["impact"].model_dump(),
        "narrative": b["narrative"],
        "provenance": _provenance_list(b),
    }


async def get_recommendations(admin_id: str, as_of: str | None = None) -> list[dict] | None:
    as_of = as_of or settings.cdi_as_of
    if county_by_id(admin_id) is None:
        return None
    b = (await _compute(as_of))[admin_id]
    return [r.model_dump() for r in b["recommendations"]]


def _provenance_list(b: dict) -> list[dict]:
    hp = b["hazard_provenance"]
    return [
        {"source": hp.source, "url": hp.url, "retrieved_at": hp.retrieved_at,
         "stale": hp.stale, "role": "hazard (CDI)"},
        {"source": CENSUS_SOURCE, "url": "https://www.knbs.or.ke/", "role": "exposure (population)"},
        {"source": "Kenya NDMA EDE / FAO / IFRC drought AA protocols", "url": "",
         "role": "anticipatory-action playbook"},
    ]


async def get_provenance(admin_id: str, as_of: str | None = None) -> list[dict] | None:
    as_of = as_of or settings.cdi_as_of
    if county_by_id(admin_id) is None:
        return None
    return _provenance_list((await _compute(as_of))[admin_id])
