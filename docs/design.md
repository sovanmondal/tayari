# Tayari — Design & Architecture

## 1. System overview

```
                ICPAC / Humanitarian OPEN DATA (real, verified live)
   ┌───────────────────────────┬──────────────────────────┬───────────────────────────┐
   │  HDX CKAN API             │  ICPAC STAC IBF catalog   │  GeoNode Geoportal API    │
   │  (exposure, impact,       │  (drought/flood:          │  (/api/v2/resources/,     │
   │   admin boundaries)       │   ensemble, hazard,       │   WMS/WFS layers)         │
   │                           │   impact, verification)   │                           │
   └────────────┬──────────────┴─────────────┬────────────┴──────────────┬────────────┘
                │                             │                           │
        ┌───────▼─────────────────────────────▼───────────────────────────▼────────┐
        │                     CONNECTOR LAYER (httpx + cache + provenance)           │
        │      HdxClient        StacClient        GeoNodeClient                      │
        └───────────────────────────────┬───────────────────────────────────────────┘
                                         │  normalized, provenance-tagged records
        ┌────────────────────────────────▼──────────────────────────────────────────┐
        │                         DOMAIN / REASONING CORE                             │
        │  TriggerEngine  →  ImpactModel  →  AAPlaybook  →  EvidenceChain             │
        │  (deterministic)   (geopandas)     (ranked)       (auditable)               │
        │                                         │                                   │
        │                         Grounding context (numbers only)                    │
        │                                         ▼                                   │
        │                     NarrativeService (LLM, grounded)                        │
        │                     LocalizationService (LLM, grounded)                     │
        └────────────────────────────────┬───────────────────────────────────────────┘
                                          │
                 ┌────────────────────────▼────────────────────────┐
                 │                FastAPI (REST)                    │
                 │  /districts /ibf /recommendations /messages      │
                 │  /dispatch  /provenance  /health                 │
                 └────────────────────────┬────────────────────────┘
                                          │  JSON
                 ┌────────────────────────▼────────────────────────┐
                 │        React + Vite + MapLibre dashboard         │
                 │  Map → District drill-down → IBF card →          │
                 │  AA recommendations (evidence) → Message →       │
                 │  Approve & Dispatch  (Africa's Talking sandbox)  │
                 └──────────────────────────────────────────────────┘

  Persistence: PostgreSQL + PostGIS (admin geometries, exposure, cached datasets, dispatch log)
  Orchestration: docker compose (backend, frontend, db)
```

## 2. Tech stack (mirrors ICPAC repos)
- **Backend:** Python 3.11, FastAPI, Pydantic v2, httpx (async), SQLAlchemy 2 + GeoAlchemy2,
  geopandas / shapely (exposure intersection), tenacity (retry).
- **DB:** PostgreSQL 16 + PostGIS 3.
- **LLM:** provider-agnostic `LLMProvider` interface; default Amazon Bedrock (Anthropic Claude),
  with an OpenAI-compatible fallback and a deterministic template fallback (so the system runs
  even with no LLM key — narrative degrades to templated, numbers unchanged).
- **Frontend:** React 18 + TypeScript + Vite, MapLibre GL JS, TailwindCSS, TanStack Query.
- **SMS:** Africa's Talking SDK (sandbox).
- **Testing:** pytest (+ live-connector marker), vitest for frontend.

## 3. Module design (backend)

```
backend/app/
  main.py                 # FastAPI app, CORS, router registration, startup cache warm
  config.py               # pydantic-settings; env-driven, no secrets in code
  db/                     # engine, session, models (PostGIS geometries), seed
  connectors/
    base.py               # HttpCachedClient: retry, timeout, on-disk/db cache, provenance
    hdx.py                # HdxClient.search(org), package(id), resource_download
    stac.py               # StacClient.catalog(), collection(id), items()
    geonode.py            # GeoNodeClient.resources(), layer_wms_url()
  domain/
    models.py             # AdminUnit, HazardSignal, ExposureLayer, Trigger, ImpactEstimate,
                          #   Recommendation, EvidenceChain, Message  (pydantic)
    trigger_engine.py     # evaluate(admin_unit, signal, threshold) -> Trigger  (pure, tested)
    impact_model.py       # intersect(hazard_geom, exposure) -> ImpactEstimate  (geopandas)
    playbook.py           # AA rules -> ranked Recommendation[] (lead time, cost, actor)
    evidence.py           # build_chain(trigger, impact, analogue) -> EvidenceChain
  services/
    llm.py                # LLMProvider (bedrock|openai|template), strict grounding contract
    narrative.py          # compose IBF narrative from EvidenceChain (numbers injected)
    localization.py       # audience+language+channel message variants
    sms.py                # Africa's Talking sandbox dispatch (or simulated)
    ibf_service.py        # orchestrates connectors->engine->impact->playbook->narrative
  api/routes/
    districts.py ibf.py recommendations.py messages.py dispatch.py provenance.py health.py
  data/
    playbook_drought.yaml # AA playbook (actions, lead time, cost band, actor, trigger link)
    thresholds.yaml       # per-indicator thresholds / return periods (from ibf methodology)
```

### 3.1 Grounding contract (anti-hallucination)
`NarrativeService` and `LocalizationService` receive a **frozen `GroundingContext`**: a dict of
already-computed strings/numbers (impacted_population, severity, threshold, action names, etc.).
The system prompt instructs the LLM to compose prose using ONLY those tokens and to never emit a
number not present in the context. Output is post-validated: any numeric token not in the context
is rejected and the request retried; on repeated failure it falls back to the deterministic template.
This satisfies FR-4.3 / NFR-1.

## 4. Core data flow (district IBF request)
1. `GET /ibf/{admin_id}` → `ibf_service`.
2. Connectors fetch (cached) hazard signal (STAC/GeoNode), exposure (HDX/GeoNode), admin geom (PostGIS/HDX).
3. `trigger_engine.evaluate` → `Trigger` (deterministic).
4. `impact_model.intersect` → `ImpactEstimate` (geopandas spatial join).
5. `playbook.recommend` → ranked `Recommendation[]`.
6. `evidence.build_chain` → `EvidenceChain` per recommendation.
7. `narrative.compose` (grounded LLM) → human IBF summary.
8. Response includes provenance for every figure.

## 5. API contracts (representative)
- `GET /health` → `{status, upstreams:{hdx,stac,geonode}}`
- `GET /districts` → `[{id,name,country,severity,triggered}]` (for map coloring)
- `GET /ibf/{admin_id}` → `{admin, severity, impact:{population,byLivelihood}, trigger, provenance[]}`
- `GET /recommendations/{admin_id}` → `[{action,leadTimeDays,costBand,actor,rank,evidence:{...}}]`
- `POST /messages` `{admin_id, audience, language, channel}` → `{text, smsSegments, voiceScript, payload}`
- `POST /dispatch` `{admin_id, message_id, to?}` → `{status: sent|simulated, providerId?}`
- `GET /provenance/{admin_id}` → source URLs, dataset ids, retrieval timestamps.

## 6. Data model (PostGIS)
- `admin_unit(id, name, country, level, geom(MultiPolygon,4326))`
- `exposure(admin_id, kind, value, source, retrieved_at)`
- `hazard_signal(admin_id, indicator, value, valid_from, valid_to, source, retrieved_at)`
- `dataset_cache(key, url, payload jsonb, retrieved_at, stale bool)`
- `dispatch_log(id, admin_id, message jsonb, status, provider_id, created_at)`

## 7. Frontend structure
```
frontend/src/
  api/client.ts           # typed fetchers (TanStack Query)
  components/MapView.tsx   # MapLibre; severity choropleth; click -> select district
  components/IbfCard.tsx   # impact, severity, provenance badges
  components/Recommendations.tsx  # ranked actions + expandable evidence chain
  components/MessagePanel.tsx     # audience/lang/channel switch, SMS + voice preview, dispatch
  components/ProvenanceBadge.tsx  # source + freshness
  pages/Dashboard.tsx
```

## 8. Resilience & provenance
- `HttpCachedClient` wraps every upstream call: timeout, tenacity retry, writes payload to
  `dataset_cache` with `retrieved_at`. On failure returns cached row flagged `stale=true`.
- The UI renders a provenance badge (source + age + stale flag) beside every number (FR-6.4).

## 9. Security
- Secrets via env only (`.env` git-ignored; `.env.example` committed).
- CORS restricted to the frontend origin.
- Input validation via Pydantic; district ids validated against DB.
- SMS dispatch requires explicit approval action (no auto-send).

## 10. Testing strategy
- `trigger_engine` / `impact_model` / `playbook` / `evidence`: pure unit tests (deterministic).
- Connectors: live integration tests (marked `@pytest.mark.live`) asserting real endpoints return
  expected shapes (HDX package_search, STAC catalog, GeoNode resources).
- Grounding: test that narrative output contains no numeric token absent from the context.
- Frontend: component tests for IbfCard / Recommendations rendering + a smoke e2e.

## 11. Build order (maps to task list)
Scaffold → connectors (live-verified) → trigger engine → impact model → playbook+evidence+narrative
→ localization+SMS → dashboard → e2e verification → submission assets.
