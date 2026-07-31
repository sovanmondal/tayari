"""Live integration tests — assert real ICPAC/HDX/GeoNode endpoints return expected shapes.

Run: pytest -m live
These hit the network intentionally (FR-1, NFR-7): we prove the system uses real data.
"""
import pytest

from app.connectors.hdx import hdx_client
from app.connectors.stac import stac_client
from app.connectors.geonode import geonode_client


@pytest.mark.live
async def test_hdx_returns_real_drought_datasets():
    f = await hdx_client.search("drought", rows=5)
    assert f.data["count"] > 0
    names = [d["name"] for d in f.data["datasets"]]
    assert any("drought-indicator" in n for n in names)
    assert f.provenance.source == "hdx"


@pytest.mark.live
async def test_hdx_cdi_package_has_geotiffs():
    p = await hdx_client.package("igad-region-dekadal-combined-drought-indicator-cdi-2024")
    assert p.data["num_resources"] > 0
    formats = {r["format"] for r in p.data["resources"]}
    assert "GeoTIFF" in formats


@pytest.mark.live
async def test_stac_drought_catalog_collections():
    s = await stac_client.catalog("drought")
    assert s.data["id"] == "drought-ibf-catalog"
    titles = [c["title"] for c in s.data["collections"]]
    assert "Impact Model" in titles and "Ensemble Predictions" in titles


@pytest.mark.live
async def test_geonode_exposure_layers():
    g = await geonode_client.resources("livestock", page_size=5)
    assert g.data["total"] > 0
    assert any(r["alternate"] for r in g.data["resources"])
