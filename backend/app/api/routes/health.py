"""Health endpoint — verifies real upstream data sources are reachable (FR-1)."""
from __future__ import annotations

import httpx
from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


async def _ping(url: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url)
            return r.status_code == 200
    except Exception:
        return False


@router.get("/health")
async def health() -> dict:
    hdx = f"{settings.hdx_base}/package_search?q=organization:{settings.hdx_org}&rows=1"
    stac = f"{settings.stac_base}/drought/dr_catalog.json"
    geonode = f"{settings.geonode_base}/resources/?page_size=1"

    upstreams = {
        "hdx": await _ping(hdx),
        "stac": await _ping(stac),
        "geonode": await _ping(geonode),
    }
    return {"status": "ok" if all(upstreams.values()) else "degraded", "upstreams": upstreams}
