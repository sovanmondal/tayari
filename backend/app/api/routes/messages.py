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
    # Reuse the cached IBF bundle (avoids re-downloading/sampling the CDI raster).
    bundle = await ibf_service._compute(req.as_of or None)
    b = bundle[req.admin_id]
    return compose_message(county["name"], county["id"], b["trigger"], b["impact"],
                           b["recommendations"], req.audience, req.language, req.channel)


@router.post("/messages")
async def messages(req: MessageRequest):
    return (await _build_message(req)).model_dump()


@router.post("/dispatch")
async def dispatch(req: DispatchRequest):
    msg = await _build_message(req)
    result = await dispatch_sms(msg, req.to)
    return {"message": msg.model_dump(), "dispatch": result}
