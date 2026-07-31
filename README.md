# Tayari — Anticipatory Action Co-pilot

**From ICPAC's forecast to the last mile's action.**

Tayari is the operational **reasoning layer** that sits between ICPAC's climate forecasts and
HUSIKA's last-mile delivery. It converts **real** ICPAC + humanitarian data into district-level
**Impact-Based Forecasts**, **auditable anticipatory-action recommendations**, and **localized,
ready-to-send messages** — the missing middle that today is done manually and does not scale.

```
Forecast (ICPAC cGAN / SEWAA / Hazards Watch)
        → Tayari (impact + decision + reasoning + localization)   ← this project
        → HUSIKA (SMS / app / radio delivery)
```

## Real data sources (verified live)
- **HDX CKAN API** — 91 ICPAC/IGAD datasets (exposure, impact, admin boundaries)
- **ICPAC STAC IBF catalog** — drought & flood: observations, ensemble predictions, hazard/impact models
- **GeoNode Geoportal API** — geospatial layers + WMS/WFS

No mock data is served anywhere; unreachable upstreams degrade to timestamped cache (never fabricated).

## Stack
FastAPI · PostGIS · geopandas · React + Vite + MapLibre · Docker Compose · grounded LLM (with
deterministic template fallback) · Africa's Talking (SMS sandbox).

## Run
```bash
cp .env.example .env      # public data sources need no keys; LLM/SMS optional
docker compose up --build
# backend  → http://localhost:8000/docs
# frontend → http://localhost:5173
# health   → http://localhost:8000/health   (shows live upstream status)
```

## Docs
- [`docs/requirements.md`](docs/requirements.md) — EARS acceptance criteria
- [`docs/design.md`](docs/design.md) — architecture, modules, API contracts

## Attribution
Built on open data and open-source methodology from **ICPAC / IGAD** (Hazards Watch, Drought Watch,
STAC IBF catalog, `ibf-thresholds-triggers`), the **Humanitarian Data Exchange (HDX)**, and the
**GeoNode** project. IGAD Hackathon 2026 — *Smarter Early Warning, Stronger Communities*.
