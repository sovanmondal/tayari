"""District, IBF, recommendations, and provenance routes."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.services import ibf_service

router = APIRouter(tags=["ibf"])


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
