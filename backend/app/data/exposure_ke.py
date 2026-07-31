"""Real exposure baseline for Kenya ASAL drought-hotspot counties.

Population: Kenya Population & Housing Census 2019 (KNBS) — official, citable figures.
Livelihood shares: derived from Kenya ASAL classification / KFSSG livelihood zoning
(pastoral / agro-pastoral / marginal-mixed-farming). Values are the dominant-zone
approximations used for exposure apportioning and are documented as such.

Geometry (bbox centroid + envelope) is a lightweight real approximation for map placement;
the seed script (data_prep) can replace these with full geoBoundaries polygons in Docker.

These are the ASAL counties most exposed to drought — the anticipatory-action focus.
"""
from __future__ import annotations

# id, name, population (KNBS 2019), centroid lon/lat, livelihood shares
COUNTIES: list[dict] = [
    {
        "id": "KE-MBT", "name": "Marsabit", "country": "Kenya",
        "population": 459785, "lon": 37.99, "lat": 2.33,
        "livelihood": {"pastoralist": 0.80, "agro-pastoralist": 0.15, "urban": 0.05},
    },
    {
        "id": "KE-TUR", "name": "Turkana", "country": "Kenya",
        "population": 926976, "lon": 35.6, "lat": 3.5,
        "livelihood": {"pastoralist": 0.75, "agro-pastoralist": 0.15, "fisher": 0.05, "urban": 0.05},
    },
    {
        "id": "KE-WAJ", "name": "Wajir", "country": "Kenya",
        "population": 781263, "lon": 40.06, "lat": 1.75,
        "livelihood": {"pastoralist": 0.82, "agro-pastoralist": 0.10, "urban": 0.08},
    },
    {
        "id": "KE-MAN", "name": "Mandera", "country": "Kenya",
        "population": 867457, "lon": 40.95, "lat": 3.6,
        "livelihood": {"pastoralist": 0.70, "agro-pastoralist": 0.22, "urban": 0.08},
    },
    {
        "id": "KE-GAR", "name": "Garissa", "country": "Kenya",
        "population": 841353, "lon": 39.9, "lat": -0.45,
        "livelihood": {"pastoralist": 0.78, "agro-pastoralist": 0.12, "urban": 0.10},
    },
    {
        "id": "KE-ISI", "name": "Isiolo", "country": "Kenya",
        "population": 268002, "lon": 38.5, "lat": 0.85,
        "livelihood": {"pastoralist": 0.80, "agro-pastoralist": 0.12, "urban": 0.08},
    },
    {
        "id": "KE-SAM", "name": "Samburu", "country": "Kenya",
        "population": 310327, "lon": 37.1, "lat": 1.2,
        "livelihood": {"pastoralist": 0.78, "agro-pastoralist": 0.17, "urban": 0.05},
    },
    {
        "id": "KE-TTA", "name": "Tana River", "country": "Kenya",
        "population": 315943, "lon": 39.6, "lat": -1.5,
        "livelihood": {"pastoralist": 0.55, "agro-pastoralist": 0.30, "farmer": 0.10, "urban": 0.05},
    },
]

CENSUS_SOURCE = (
    "Kenya National Bureau of Statistics (KNBS), 2019 Kenya Population and Housing "
    "Census, Volume I. https://www.knbs.or.ke/"
)


def county_by_id(cid: str) -> dict | None:
    return next((c for c in COUNTIES if c["id"] == cid), None)
