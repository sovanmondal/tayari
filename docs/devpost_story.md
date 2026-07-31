## 🌍 Inspiration

In the Horn of Africa, the drought forecast is rarely the problem. **ICPAC** already produces
world-class early warnings, and **HUSIKA** already delivers alerts to the last mile. Yet people
and livestock still die in slow-onset droughts that were forecast *months* in advance.

Why? Because of the **missing middle** — the step between a forecast and action. Turning
"below-average rainfall" into *who exactly is at risk, what action to trigger, and why* is still
done manually, district by district, on spreadsheets. It doesn't scale. ICPAC itself names this
the *"long-pending operationalization of Impact-Based Forecasting."*

We built **Tayari** (Swahili for *"ready"*) to be that missing middle.

## 🚀 What it does

Tayari is the operational **decision-and-reasoning layer** between the forecast and the delivery
pipe. For every district it:

1. **Reads real hazard data** — the ICPAC East Africa Drought Watch **Combined Drought Indicator**.
2. **Detects triggers** — deterministically flags districts that cross the anticipatory-action threshold.
3. **Estimates impact** — intersects the hazard with **real census exposure** to count who's affected, by livelihood.
4. **Recommends action** — a ranked anticipatory-action plan (lead time, cost, responsible actor) from Kenya NDMA / FAO / IFRC protocols, each backed by an **auditable evidence chain**: forecast → threshold → exposure → action.
5. **Writes the last-mile message** — one forecast becomes three audiences (pastoralist, farmer, DRM officer), in English or Swahili, as a low-literacy SMS *and* a voice/IVR script — then hands it to the HUSIKA gateway.

**Tayari doesn't replace ICPAC's tools — it completes the stack.**

## 🛠️ How we built it

- **Backend:** Python + **FastAPI**, **PostGIS**, `geopandas`/`shapely` (hazard × exposure intersection), `rasterio` (sampling the real CDI GeoTIFFs) — mirroring ICPAC's own stack.
- **Real data connectors:** HDX CKAN API (CDI rasters, census/exposure), the ICPAC **STAC IBF catalog**, and the **GeoNode geoportal** (1,096 layers). Every figure carries provenance; if a source is down we serve timestamped cache — never fabricated values.
- **Reasoning:** a deterministic trigger engine + anticipatory-action playbook, plus an **LLM (Groq / Llama-3.3)** that writes the human narrative and localized messages under a **strict grounding contract** — a numeric-hallucination guard rejects any number the engine didn't compute, with a deterministic template fallback.
- **Frontend:** **React + TypeScript + MapLibre**, with a real-time dekad timeline, a self-writing "AI situation briefing," and a district drill-down.
- **Delivery:** **Africa's Talking** (SMS + voice), HUSIKA-compatible payload.
- **Ops:** one-command **Docker Compose**; **29 automated tests** including live-endpoint integration.

## 🧗 Challenges we ran into

- **Real data, always.** We refused mock data, so we verified every ICPAC/HDX/GeoNode endpoint was live and reachable before designing around it.
- **Decoding the real CDI.** The rasters store discrete classes 0–9; we mapped them to the authoritative Copernicus/EDO drought-severity legend (Watch/Warning/Alert + recovery), documenting every assumption.
- **Honest "real-time."** The latest dekad showed no active drought — so we made the timeline default to real-time *and* let users scrub to the real **2021 Horn of Africa drought** (4 counties in Alert, **1.88M people exposed**).
- **Grounding the AI.** Getting genuinely useful, multilingual messages out of an LLM *without letting it invent numbers* required a two-tier guard (strict on population figures, relaxed on natural timeframes).
- **Performance.** Cold satellite rasters + eager LLM calls made it sluggish; we added caching, per-dekad locks, request debouncing, and moved the LLM off the hot path.

## 🏆 Accomplishments we're proud of

- A **fully operational**, real-data system — not a mockup — reproducible with `docker compose up`.
- **Auditable AI**: every recommendation is explainable and source-cited; the AI never fabricates a figure.
- **Genuine digital inclusion**: local-language, low-literacy, voice-ready messages for people on basic phones.

## 📚 What we learned

The last-mile gap is a *reasoning and translation* problem, not a forecasting one. And "using AI
responsibly" in a humanitarian context means **grounding it in verifiable data** and keeping a
human in the loop — the officer always approves before anything is dispatched.

## 🔭 What's next

Live HUSIKA integration for real dispatch; extend the same pipeline to **floods and disease**
(the STAC catalog already supports flood IBF); more languages; and probabilistic/ensemble triggers
from ICPAC's cGAN forecasts.

## 🧰 Built with

`python` · `fastapi` · `postgis` · `geopandas` · `rasterio` · `react` · `typescript` · `maplibre` ·
`groq` · `llama-3.3` · `docker` · `africas-talking` · ICPAC Drought Watch · HDX · GeoNode STAC
