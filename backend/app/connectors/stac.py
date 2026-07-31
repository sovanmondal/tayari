"""ICPAC STAC IBF catalog connector — real E4DRR Impact-Based Forecasting catalog.

Verified live: drought & flood catalogs, each with collections: observations,
ensemble-predictions, hazard-model, impact-model, forecast-verification, risk-knowledge.
"""
from __future__ import annotations

from app.config import settings
from app.connectors.base import Fetched, HttpCachedClient


class StacClient:
    def __init__(self) -> None:
        self._c = HttpCachedClient("stac")

    def _catalog_url(self, hazard: str) -> str:
        code = {"drought": "dr", "flood": "fl"}.get(hazard, "dr")
        return f"{settings.stac_base}/{hazard}/{code}_catalog.json"

    async def catalog(self, hazard: str = "drought") -> Fetched:
        """Root catalog with its child collections."""
        fetched = await self._c.get(self._catalog_url(hazard))
        cat = fetched.data
        fetched.data = {
            "id": cat.get("id"),
            "title": cat.get("title"),
            "description": cat.get("description"),
            "collections": [
                {"title": l.get("title"), "href": l.get("href")}
                for l in cat.get("links", [])
                if l.get("rel") == "child"
            ],
        }
        return fetched

    async def collection(self, hazard: str, path: str) -> Fetched:
        """Fetch a specific collection.json by its relative path from the catalog root."""
        url = f"{settings.stac_base}/{hazard}/{path}"
        fetched = await self._c.get(url)
        col = fetched.data
        fetched.data = {
            "id": col.get("id"),
            "title": col.get("title"),
            "description": col.get("description"),
            "extent": col.get("extent"),
            "children": [
                {"rel": l.get("rel"), "href": l.get("href")}
                for l in col.get("links", [])
                if l.get("rel") in ("child", "item")
            ],
            "assets": col.get("assets", {}),
        }
        return fetched


stac_client = StacClient()
