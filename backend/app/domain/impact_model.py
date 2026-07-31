"""Impact model (FR-3): hazard footprint x exposure -> impacted population per admin unit.

Two real, defensible computations:
  1. area_weighted_exposed(): geopandas overlay of a hazard polygon with exposure (admin)
     polygons, apportioning population by intersected area fraction.
  2. zonal_cdi(): rasterio zonal mean of the real CDI GeoTIFF over an admin geometry
     (used to derive the per-admin hazard class that the trigger engine consumes).

Every number is traceable to its source (FR-3.3). No fabricated values.
"""
from __future__ import annotations

from app.domain.models import (
    AdminUnit,
    ExposureBreakdown,
    ImpactEstimate,
    Provenance,
)


def estimate_impact(
    admin: AdminUnit,
    total_population: int,
    livelihood_shares: dict[str, float],
    triggered: bool,
    sources: list[Provenance] | None = None,
) -> ImpactEstimate:
    """Compute impacted population for a single admin unit.

    If the unit's hazard has crossed its trigger, the exposed population is the unit's
    population apportioned across livelihood groups by their real shares. If not
    triggered, exposed population is 0 (monitor state).
    """
    exposed = total_population if triggered else 0
    breakdown: list[ExposureBreakdown] = []
    if exposed:
        # Ensure shares sum consistently; apportion to integer counts.
        allotted = 0
        items = list(livelihood_shares.items())
        for i, (name, share) in enumerate(items):
            if i == len(items) - 1:
                pop = exposed - allotted  # last group absorbs rounding remainder
            else:
                pop = round(exposed * share)
                allotted += pop
            breakdown.append(ExposureBreakdown(livelihood=name, population=max(pop, 0)))

    return ImpactEstimate(
        admin_id=admin.id,
        total_population_exposed=exposed,
        by_livelihood=breakdown,
        method=(
            "Population exposed = admin population where CDI >= trigger (Warning), "
            "apportioned to livelihood groups by their real population shares."
        ),
        sources=sources or [],
    )


def area_weighted_exposed(hazard_geojson: dict, exposure_features: list[dict]) -> int:
    """Geopandas overlay: apportion exposure population by fraction of area inside hazard.

    hazard_geojson: a single Polygon/MultiPolygon (the hazard footprint, EPSG:4326).
    exposure_features: list of {"population": int, "geometry": <geojson geometry>}.
    Returns total exposed population (area-weighted).
    """
    import geopandas as gpd
    from shapely.geometry import shape

    hazard = gpd.GeoDataFrame(geometry=[shape(hazard_geojson)], crs="EPSG:4326")
    rows = [
        {"population": int(f["population"]), "geometry": shape(f["geometry"])}
        for f in exposure_features
    ]
    exposure = gpd.GeoDataFrame(rows, crs="EPSG:4326")

    # Use an equal-area projection for correct area ratios (Africa Albers ~ ESRI:102022).
    ea = "+proj=aea +lat_1=20 +lat_2=-23 +lat_0=0 +lon_0=25 +datum=WGS84 +units=m"
    exp_ea = exposure.to_crs(ea)
    haz_ea = hazard.to_crs(ea)
    exp_ea["full_area"] = exp_ea.geometry.area

    inter = gpd.overlay(exp_ea, haz_ea, how="intersection")
    if inter.empty:
        return 0
    inter["frac"] = inter.geometry.area / inter["full_area"]
    inter["exposed"] = (inter["population"] * inter["frac"]).round()
    return int(inter["exposed"].sum())


def zonal_cdi(raster_path: str, geometry_geojson: dict) -> float:
    """Real zonal mean of a CDI GeoTIFF over an admin geometry (rasterio + numpy)."""
    import numpy as np
    import rasterio
    from rasterio.mask import mask

    with rasterio.open(raster_path) as src:
        out, _ = mask(src, [geometry_geojson], crop=True, nodata=src.nodata)
        arr = out[0].astype("float64")
        if src.nodata is not None:
            arr = np.where(arr == src.nodata, np.nan, arr)
        val = np.nanmean(arr)
    return float(val)
