"""Hazard service — derives the real per-county CDI class from ICPAC EADW GeoTIFFs.

Flow (all real data):
  1. Ask HDX for the latest available CDI dataset (most recent year), pick its most
     recent dekadal GeoTIFF resource.
  2. Download + cache the GeoTIFF once.
  3. Sample the CDI class at each county centroid with rasterio.

Provenance (dataset name, resource file, retrieval time) is attached to every value.
"""
from __future__ import annotations

import time
from pathlib import Path

import httpx

from app.config import settings
from app.connectors.base import CACHE_DIR
from app.connectors.hdx import hdx_client
from app.domain.models import HazardSignal, Provenance

RASTER_DIR = CACHE_DIR / "rasters"
RASTER_DIR.mkdir(exist_ok=True)

CDI_DATASETS = [
    "igad-region-dekadal-combined-drought-indicator-cdi-2024",
    "igad-region-dekadal-combined-drought-indicator-cdi-2021",
    "igad-region-dekadal-combined-drought-indicator-cdi-2020",
]


def _dataset_for_year(year: str) -> str:
    for ds in CDI_DATASETS:
        if ds.endswith(year):
            return ds
    return CDI_DATASETS[0]


async def resource_for(as_of: str | None = None) -> dict:
    """Return the CDI GeoTIFF resource for a given dekad date (YYYY-MM-DD).

    If as_of is None/"latest", returns the most recent available dekad.
    Otherwise returns the resource whose dekad date is closest on/before as_of.
    """
    as_of = as_of or settings.cdi_as_of
    if as_of == "latest":
        return await latest_cdi_resource()

    year = as_of.split("-")[0]
    pkg = await hdx_client.package(_dataset_for_year(year))
    tiffs = [r for r in pkg.data.get("resources", []) if r.get("format") == "GeoTIFF"]
    if not tiffs:
        return await latest_cdi_resource()
    tiffs.sort(key=lambda r: r["name"])

    def date_of(r: dict) -> str:
        return r["name"].replace("eadw-cdi-data-", "").replace(".tif", "")

    on_or_before = [r for r in tiffs if date_of(r) <= as_of]
    chosen = on_or_before[-1] if on_or_before else tiffs[0]
    return {"dataset": _dataset_for_year(year), **chosen}


async def latest_cdi_resource() -> dict:
    """Return the most recent dekadal CDI GeoTIFF resource {name, url, dataset, modified}."""
    for ds in CDI_DATASETS:
        pkg = await hdx_client.package(ds)
        tiffs = [r for r in pkg.data.get("resources", []) if r.get("format") == "GeoTIFF"]
        if not tiffs:
            continue
        # resource names sort chronologically: eadw-cdi-data-YYYY-MM-DD.tif
        tiffs.sort(key=lambda r: r["name"])
        latest = tiffs[-1]
        return {"dataset": ds, **latest}
    raise RuntimeError("No CDI GeoTIFF resource found on HDX")


async def _download(url: str) -> Path:
    fn = RASTER_DIR / url.split("/")[-1]
    if fn.exists() and fn.stat().st_size > 0:
        return fn
    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
        r = await client.get(url)
        r.raise_for_status()
        fn.write_bytes(r.content)
    return fn


def sample_points(raster_path: Path, points: list[tuple[float, float]]) -> list[float]:
    """Sample CDI class values at (lon, lat) points from the GeoTIFF."""
    import rasterio

    with rasterio.open(raster_path) as src:
        vals = [v[0] for v in src.sample(points)]
    return [float(v) for v in vals]


async def county_hazard_signals(
    counties: list[dict], as_of: str | None = None
) -> tuple[dict[str, HazardSignal], Provenance]:
    """Return {county_id: HazardSignal} sampled from the real CDI raster + provenance."""
    res = await resource_for(as_of)
    path = await _download(res["url"])
    pts = [(c["lon"], c["lat"]) for c in counties]
    vals = sample_points(path, pts)

    ts = time.time()
    prov = Provenance(
        source="HDX/ICPAC East Africa Drought Watch — Combined Drought Indicator (CDI)",
        url=res["url"],
        retrieved_at=ts,
        age_seconds=0.0,
        stale=False,
    )
    valid_date = res["name"].replace("eadw-cdi-data-", "").replace(".tif", "")
    signals = {
        c["id"]: HazardSignal(
            indicator="CDI",
            value=v if v == v else 0.0,  # NaN -> 0 (no data => no drought signal)
            valid_from=valid_date,
            valid_to=valid_date,
            unit="class",
            source=prov.source,
        )
        for c, v in zip(counties, vals)
    }
    return signals, prov
