# Tayari — Requirements Specification

**Tayari** ("ready / prepared", Swahili) is the operational reasoning layer between ICPAC's
climate forecasts and the last-mile delivery of action. It converts **real** ICPAC forecast,
threshold, and exposure data into district-level **Impact-Based Forecasts (IBF)**, **auditable
anticipatory-action (AA) recommendations**, and **localized, ready-to-send last-mile messages**.

Tayari does not compete with ICPAC's tools — it completes the stack:
`Forecast (cGAN/SEWAA/Hazards Watch)` → **`Tayari (decision + reasoning)`** → `HUSIKA (delivery)`.

---

## 1. Problem Statement (grounded in ICPAC's own findings)

From ICPAC/IGAD's E4DRR workshop material, the unsolved gaps are:
- EWS is based on **deterministic** forecasts; decision-makers need **probabilistic impact** forecasts.
- **Poor use of systematic tools** for optimizing risk/decision analysis with local knowledge.
- **"Long pending operationalization of Impact-Based Forecasting."**

The forecast exists. Delivery (HUSIKA) exists. The missing middle is the **auditable decision layer**
that turns a forecast into *who is impacted, what action to trigger, and why* — today done manually,
district by district, which does not scale.

## 2. Scope

### In scope
- Ingesting **real** ICPAC/humanitarian data (HDX CKAN, STAC IBF catalog, GeoNode Geoportal).
- Deterministic trigger engine (threshold / return-period crossing) per admin unit.
- Impact model (hazard × exposure → impacted population/livelihood per district).
- Anticipatory-action playbook with ranked actions (lead time, cost, responsible actor).
- Auditable evidence chain for every recommendation.
- LLM-composed narrative + localized last-mile messages, strictly grounded on computed numbers.
- React dashboard (map, district drill-down, IBF card, AA recommendations, message preview, approve/dispatch).

### Out of scope (explicit boundaries)
- Building new forecast models (we consume ICPAC's).
- Production integration with HUSIKA's SMS gateway (no credentials) — we emit the HUSIKA-compatible
  payload and optionally send via Africa's Talking **sandbox** to prove real delivery.
- Retraining the cGAN or hazard models.

## 3. Personas
- **P1 — National/District DRM officer:** decides whether to trigger anticipatory action; needs evidence.
- **P2 — Humanitarian/UN partner:** needs impact estimates + cost to release AA financing.
- **P3 — Community last-mile actor (pastoralist / farmer):** needs a plain, localized, actionable message.

## 4. Functional Requirements (EARS)

### FR-1 Real-data ingestion
- **FR-1.1** The system SHALL retrieve hazard/exposure/impact datasets from the HDX CKAN API for the
  ICPAC/IGAD organization.
- **FR-1.2** The system SHALL retrieve the ICPAC STAC IBF catalog (drought + flood) and enumerate its
  collections (observations, ensemble predictions, hazard model, impact model, verification, risk knowledge).
- **FR-1.3** The system SHALL retrieve geospatial layers from the GeoNode Geoportal `/api/v2/resources/` API.
- **FR-1.4** WHEN an upstream source is unreachable, the system SHALL serve the last successfully cached
  response and mark the data provenance as `stale` with its timestamp. It SHALL NOT fabricate values.
- **FR-1.5** The system SHALL record, for every datum used in a recommendation, its source URL, dataset id,
  and retrieval timestamp (provenance).

### FR-2 Trigger engine
- **FR-2.1** The system SHALL evaluate, per admin unit, whether a hazard indicator crosses its configured
  threshold / return period, producing a boolean `triggered` and a `severity` band.
- **FR-2.2** The trigger logic SHALL be deterministic and unit-testable, with NO LLM involvement.
- **FR-2.3** The system SHALL expose the threshold, the observed/forecast value, and the exceedance margin
  used for each trigger decision.

### FR-3 Impact model
- **FR-3.1** The system SHALL compute impacted population per admin unit by intersecting the hazard
  footprint with exposure layers (population, livelihood) using geospatial joins on real admin boundaries.
- **FR-3.2** The system SHALL break down impact by livelihood group (e.g., pastoralist, farmer) where the
  exposure data supports it.
- **FR-3.3** Every impact number SHALL be traceable to its source dataset and computation inputs.

### FR-4 Anticipatory-action playbook + reasoning
- **FR-4.1** WHEN a trigger fires for an admin unit, the system SHALL return a ranked list of anticipatory
  actions, each with lead time, indicative cost, and responsible actor.
- **FR-4.2** Each recommendation SHALL include an **auditable evidence chain**: forecast value → threshold
  crossed → historical analogue (if any) → exposed population.
- **FR-4.3** The LLM narrative SHALL only restate numbers computed by the engine; it SHALL NOT introduce
  new quantitative claims. Numbers SHALL be injected as structured context, not generated.
- **FR-4.4** IF no trigger fires, the system SHALL return a "monitor" state with the current distance to threshold.

### FR-5 Localization & last-mile messaging
- **FR-5.1** The system SHALL generate audience-specific messages for P1 (technical), P3-pastoralist,
  and P3-farmer.
- **FR-5.2** The system SHALL generate messages in at least English + one regional language (e.g., Swahili),
  extensible to others.
- **FR-5.3** The system SHALL produce a low-literacy / SMS-length (≤160 char segment) variant and a
  voice/IVR-ready script variant.
- **FR-5.4** The message payload SHALL be structured for HUSIKA-style consumption (audience, language,
  channel, admin unit, action, valid-until).
- **FR-5.5** WHERE Africa's Talking sandbox credentials are configured, the system SHALL actually dispatch
  an SMS on approval; otherwise it SHALL return the payload and mark dispatch as `simulated`.

### FR-6 Dashboard
- **FR-6.1** The system SHALL render a MapLibre map of the region with admin units colored by IBF severity.
- **FR-6.2** WHEN a user selects an admin unit, the system SHALL show the IBF card (impact estimate,
  severity, provenance), the ranked AA recommendations with evidence, and the community message preview.
- **FR-6.3** The system SHALL provide an "approve & dispatch" action that triggers FR-5.5.
- **FR-6.4** The UI SHALL visibly display data provenance and freshness for every figure shown.

## 5. Non-Functional Requirements
- **NFR-1 Real data only.** No mock/fabricated values in any served figure. Cache is real, timestamped.
- **NFR-2 Reproducible.** `docker compose up` brings up backend + frontend + PostGIS with one command.
- **NFR-3 Auditability.** Every recommendation is explainable and traceable to source data.
- **NFR-4 Performance.** A district IBF query returns < 3 s on warm cache.
- **NFR-5 Resilience.** Upstream failure degrades to cached/stale, never to fabricated data or a crash.
- **NFR-6 Security.** No secrets in repo; API keys via env; endpoints validate input; CORS locked to frontend origin.
- **NFR-7 Tested.** Trigger engine + impact model + connectors have automated tests; connector tests hit real endpoints.
- **NFR-8 Attribution.** All ICPAC/IGAD/HDX sources are credited per hackathon rules.

## 6. Acceptance (definition of done for the build)
- Real HDX + STAC + GeoNode data flows into a computed IBF for a real district.
- A trigger fires deterministically and produces a ranked, evidence-backed AA recommendation.
- A localized SMS-length + voice message is generated and (sandbox) dispatchable.
- The dashboard shows map → district → IBF → actions → message → approve, end-to-end, on real data.
- `docker compose up` reproduces the full stack; tests pass.
