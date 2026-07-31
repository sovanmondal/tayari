"""ICPAC GeoNode Geoportal connector — real geospatial layers (1096 resources).

Verified live: /api/v2/resources/ returns layers incl. exposure/livelihood data
(e.g. Livestock ownership). `alternate` gives the GeoServer layer name for WMS.
"""
from __future__ import annotations

from urllib.parse import quote

from app.config import settings
from app.connectors.base import Fetched, HttpCachedClient

# ICPAC GeoServer WMS endpoint (derived from geoportal host)
GEOSERVER_WMS = "https://geoportal.icpac.net/geoserver/wms"


class GeoNodeClient:
    def __init__(self) -> None:
        self._c = HttpCachedClient("geonode")

    async def resources(self, search: str = "", page_size: int = 20) -> Fetched:
        url = f"{settings.geonode_base}/resources/?page_size={page_size}"
        if search:
            url += f"&search={quote(search)}&search_fields=title&search_fields=abstract"
        fetched = await self._c.get(url)
        data = fetched.data
        fetched.data = {
            "total": data.get("total"),
            "resources": [self._slim(r) for r in data.get("resources", [])],
        }
        return fetched

    @staticmethod
    def _slim(r: dict) -> dict:
        return {
            "pk": r.get("pk"),
            "title": r.get("title"),
            "resource_type": r.get("resource_type"),
            "alternate": r.get("alternate"),
            "category": r.get("category"),
            "bbox": r.get("ll_bbox_polygon"),
            "detail_url": r.get("detail_url"),
            "thumbnail_url": r.get("thumbnail_url"),
            "last_updated": r.get("last_updated"),
        }

    @staticmethod
    def wms_url(alternate: str, bbox: str = "21,-12,52,23", width: int = 768) -> str:
        """Build a WMS GetMap URL for a layer (EPSG:4326, lon/lat bbox minx,miny,maxx,maxy)."""
        return (
            f"{GEOSERVER_WMS}?service=WMS&version=1.1.0&request=GetMap"
            f"&layers={quote(alternate)}&bbox={bbox}&width={width}&height={width}"
            f"&srs=EPSG:4326&format=image/png&transparent=true"
        )


geonode_client = GeoNodeClient()
