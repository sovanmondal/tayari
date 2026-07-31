"""HDX (Humanitarian Data Exchange) CKAN connector — real ICPAC/IGAD datasets.

Verified live: 91 datasets under the IGAD/ICPAC organization, including the
Combined Drought Indicator (CDI) dekadal GeoTIFF series (real drought hazard signal).
"""
from __future__ import annotations

from urllib.parse import quote

from app.config import settings
from app.connectors.base import Fetched, HttpCachedClient


class HdxClient:
    def __init__(self) -> None:
        self._c = HttpCachedClient("hdx")

    async def search(self, query: str = "", rows: int = 20) -> Fetched:
        """Search datasets within the ICPAC/IGAD organization."""
        q = f"organization:{settings.hdx_org}"
        if query:
            q = f"{quote(query)} {q}"
        url = f"{settings.hdx_base}/package_search?q={q}&rows={rows}"
        fetched = await self._c.get(url)
        result = fetched.data.get("result", {})
        fetched.data = {
            "count": result.get("count", 0),
            "datasets": [self._slim(d) for d in result.get("results", [])],
        }
        return fetched

    async def package(self, name: str) -> Fetched:
        """Full dataset detail incl. downloadable resources."""
        url = f"{settings.hdx_base}/package_show?id={quote(name)}"
        fetched = await self._c.get(url)
        fetched.data = self._slim(fetched.data.get("result", {}), full=True)
        return fetched

    @staticmethod
    def _slim(d: dict, full: bool = False) -> dict:
        out = {
            "name": d.get("name"),
            "title": d.get("title"),
            "notes": d.get("notes"),
            "last_modified": d.get("metadata_modified"),
            "num_resources": d.get("num_resources"),
        }
        if full:
            out["resources"] = [
                {
                    "name": r.get("name"),
                    "format": r.get("format"),
                    "url": r.get("url"),
                    "last_modified": r.get("last_modified"),
                }
                for r in d.get("resources", [])
            ]
        return out


hdx_client = HdxClient()
