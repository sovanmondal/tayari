"""Message generation + dispatch routes (FR-5)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.data.exposure_ke import county_by_id
from app.domain.impact_model import estimate_impact
from app.domain.models import AdminUnit, Provenance
from app.domain.playbook import recommend
from app.domain.trigger_engine import evaluate
from app.services import ibf_service
from app.services.hazard import county_hazard_signals
from app.services.localization import compose_message
from app.services.sms import dispatch_sms

router = APIRouter(tags=["messages"])


class MessageRequest(BaseModel):
    admin_id: str
    audience: str = "pastoralist"
    language: str = "en"
    channel: str = "sms"
    as_of: str | None = None


class DispatchRequest(MessageRequest):
    to: str | None = None


async def _build_message(req: MessageRequest):
    county = county_by_id(req.admin_id)
    if county is None:
        raise HTTPException(status_code=404, detail=f"Unknown admin unit '{req.admin_id}'")
    signals, _ = await county_hazard_signals([county], req.as_of)
    admin = AdminUnit(id=county["id"], name=county["name"], country=county["country"])
    trig = evaluate(signals[county["id"]])
    impact = estimate_impact(admin, county["population"], county["livelihood"],
                             triggered=trig.triggered,
                             sources=[Provenance(source="KNBS 2019 Census",
                                                 url="https://www.knbs.or.ke/", retrieved_at=0.0)])
    recs = recommend(trig, impact)
    return compose_message(county["name"], county["id"], trig, impact, recs,
                           req.audience, req.language, req.channel)


@router.post("/messages")
async def messages(req: MessageRequest):
    return (await _build_message(req)).model_dump()


@router.post("/dispatch")
async def dispatch(req: DispatchRequest):
    msg = await _build_message(req)
    result = await dispatch_sms(msg, req.to)
    return {"message": msg.model_dump(), "dispatch": result}
