"""District, IBF, recommendations, and provenance routes."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.services import ibf_service
from app.services.hazard import list_dekads
from app.services.briefing import regional_briefing

router = APIRouter(tags=["ibf"])


@router.get("/briefing")
async def briefing(as_of: str | None = Query(default=None)):
    """AI-authored regional situation briefing (real LLM when configured)."""
    return await regional_briefing(as_of)


@router.get("/dekads")
async def dekads():
    """List all real available CDI dekad dates (newest first)."""
    d = await list_dekads()
    return {"dekads": d, "latest": d[0] if d else None}


@router.get("/districts")
async def districts(as_of: str | None = Query(default=None)):
    return await ibf_service.list_districts(as_of)


@router.get("/ibf/{admin_id}")
async def ibf(admin_id: str, as_of: str | None = Query(default=None)):
    result = await ibf_service.get_ibf(admin_id, as_of)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown admin unit '{admin_id}'")
    return result


@router.get("/recommendations/{admin_id}")
async def recommendations(admin_id: str, as_of: str | None = Query(default=None)):
    result = await ibf_service.get_recommendations(admin_id, as_of)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown admin unit '{admin_id}'")
    return result


@router.get("/provenance/{admin_id}")
async def provenance(admin_id: str, as_of: str | None = Query(default=None)):
    result = await ibf_service.get_provenance(admin_id, as_of)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Unknown admin unit '{admin_id}'")
    return result
