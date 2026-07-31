# Solution Details (≈250 words)

**How it works.** Tayari runs a five-stage pipeline on real data:

1. **Ingest (real, verified live).** Connectors pull the ICPAC East Africa Drought Watch
   **Combined Drought Indicator** dekadal GeoTIFFs from HDX (CKAN API), the ICPAC **STAC
   IBF catalog**, and the **GeoNode geoportal** (1,096 layers). A cache layer timestamps
   every response and falls back to last-known data if a source is down — never to
   fabricated values.
2. **Trigger.** A deterministic engine samples the CDI raster per district and maps the
   EDO/EADW class (0–9) to a severity (Watch/Warning/Alert), firing anticipatory action at
   the Warning threshold. No LLM touches this logic.
3. **Impact.** Using geopandas, it intersects the hazard footprint with real **KNBS 2019
   census** exposure to estimate affected population, broken down by livelihood
   (pastoralist, agro-pastoralist, farmer).
4. **Recommend + explain.** It returns ranked actions (lead time, cost band, responsible
   actor) from a real drought AA playbook, each with an **auditable evidence chain**. An
   LLM composes the narrative under a strict grounding contract — a numeric-hallucination
   guard rejects any figure not computed by the engine, with a deterministic template
   fallback so it runs with zero API keys.
5. **Localize + dispatch.** It generates audience- and language-specific last-mile
   messages (SMS segments + voice script), HUSIKA-compatible, dispatchable via Africa's
   Talking.

**Stack:** FastAPI + PostGIS + geopandas/rasterio; React + TypeScript + MapLibre; Docker
Compose. **Tested:** 29 automated tests, including live-endpoint integration.
**Scalable:** one pipeline generalises across hazards, districts, and languages.
