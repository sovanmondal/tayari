"""API integration tests via TestClient, with hazard signals stubbed (no network).

Proves the full orchestration + routing works deterministically. Live real-data flow is
covered separately by tests/test_connectors_live.py and the docker e2e.
"""
import pytest
from fastapi.testclient import TestClient

from app.domain.models import HazardSignal, Provenance
import app.services.ibf_service as ibf_service
import app.api.routes.messages as messages_route
from app.main import app

# Fixed, realistic CDI classes for the 2021 drought (mirrors real sampled values).
STUB = {
    "KE-MBT": 2, "KE-TUR": 0, "KE-WAJ": 0, "KE-MAN": 0,
    "KE-GAR": 8, "KE-ISI": 8, "KE-SAM": 2, "KE-TTA": 3,
}


@pytest.fixture(autouse=True)
def _stub_hazard(monkeypatch):
    async def fake_signals(counties, as_of=None):
        prov = Provenance(source="HDX/ICPAC EADW CDI (stub)", url="https://data.humdata.org/x.tif",
                          retrieved_at=0.0)
        sigs = {c["id"]: HazardSignal(value=STUB.get(c["id"], 0), valid_from="2021-05-01")
                for c in counties}
        return sigs, prov

    monkeypatch.setattr(ibf_service, "county_hazard_signals", fake_signals)
    monkeypatch.setattr(messages_route, "county_hazard_signals", fake_signals)
    ibf_service._CACHE.clear()
    yield
    ibf_service._CACHE.clear()


client = TestClient(app)


def test_districts_lists_all_with_triggers():
    r = client.get("/districts")
    assert r.status_code == 200
    d = r.json()
    assert len(d) == 8
    assert sum(1 for x in d if x["triggered"]) == 5  # 5/8 for May 2021 drought


def test_ibf_garissa_alert_and_exposed():
    r = client.get("/ibf/KE-GAR")
    assert r.status_code == 200
    body = r.json()
    assert body["severity"] == "alert"
    assert body["impact"]["total_population_exposed"] == 841353
    assert "Garissa" in body["narrative"] and len(body["narrative"]) > 20
    assert len(body["provenance"]) == 3


def test_recommendations_have_evidence_chain():
    r = client.get("/recommendations/KE-GAR")
    recs = r.json()
    assert recs[0]["rank"] == 1
    assert "water trucking" in recs[0]["action"].lower()
    assert len(recs[0]["evidence"]) == 4


def test_message_and_dispatch_flow():
    m = client.post("/messages", json={"admin_id": "KE-GAR", "audience": "pastoralist", "language": "sw"})
    assert m.status_code == 200
    assert "Ukame" in m.json()["text"]
    d = client.post("/dispatch", json={"admin_id": "KE-GAR", "audience": "pastoralist", "language": "en"})
    assert d.json()["dispatch"]["status"] in ("queued", "sent", "simulated")


def test_unknown_district_404():
    assert client.get("/ibf/XX-ZZZ").status_code == 404


def test_non_triggered_has_no_exposure():
    body = client.get("/ibf/KE-TUR").json()
    assert body["trigger"]["triggered"] is False
    assert body["impact"]["total_population_exposed"] == 0
