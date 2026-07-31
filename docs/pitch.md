# Tayari — Submission Pitch

## One-liner
**ICPAC predicts the drought. HUSIKA delivers the alert. Tayari is the brain in between —
it decides who to protect, what to do, and proves why — turning a forecast into action
before people are harmed.**

## Elevator pitch (30 seconds)
In the Horn of Africa the forecast is rarely the problem — ICPAC already produces
world-class drought forecasts, and HUSIKA already reaches the last mile. The missing piece
is the decision in between: *who exactly is at risk, what action to trigger, and why.*
Today that's done by hand, district by district. Tayari automates it. On real ICPAC and
census data, it converts a drought forecast into a district-level impact estimate, a ranked
set of anticipatory actions with an auditable evidence trail, and a ready-to-send message
in local languages — the exact content HUSIKA delivers. It doesn't compete with ICPAC's
tools; it completes the stack.

## The problem (judges' "last-mile gap")
Early warnings fail not at prediction but at translation into action: forecasts are
technical, don't say who's affected or what to do, aren't in local languages, and the
decision work doesn't scale. ICPAC itself calls this the "unsolved operationalization of
Impact-Based Forecasting."

## What Tayari does
1. Reads the **real** Combined Drought Indicator (ICPAC East Africa Drought Watch).
2. Detects, per district, when it crosses the anticipatory-action trigger.
3. Estimates **who is affected** (real census, by livelihood).
4. Recommends **ranked actions** (Kenya NDMA / FAO / IFRC protocols) with lead times, cost,
   and responsible actor — each with an **auditable evidence chain**.
5. Writes the **last-mile message** — audience- and language-specific, SMS + voice — and
   dispatches it.

## Why it wins
- **Innovation:** solves ICPAC's own stated unsolved problem, not a HUSIKA rebuild.
- **Impact:** anticipatory action saves lives and money (every $1 early ≈ $3–7 saved).
- **Technical quality:** 100% real open data, auditable, 29 automated tests, one-command deploy.
- **UX:** map → district → decision → message, designed for low-literacy last-mile users.
- **Scalability:** one pipeline generalises across hazards, districts, and languages.

## Proof
Runs on real HDX / ICPAC STAC / GeoNode data + KNBS 2019 census; built on ICPAC's own
stack (FastAPI, PostGIS, React); reproducible with `docker compose up`.
