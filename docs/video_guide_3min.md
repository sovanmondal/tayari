# Tayari — 3-Minute Demo Guide (high-impact)

**Record:** http://localhost:5173  ·  **Tool:** `Cmd+Shift+5` (macOS) → Record.
**Target length:** under 3:00. Tight beats long.

---

## PRE-FLIGHT (do this before hitting record — 2 min)
1. Backend + frontend running (`docker compose ps` → 3 up). Dashboard open at localhost:5173.
2. **Pre-warm the dekads you'll show** (cold dekads take ~15s to first-load the satellite raster):
   - Let the page load on **Latest** (calm view).
   - Drag the slider once to **May 2021** and wait until the map lights up + briefing writes.
   - Drag back to **Latest**. Now both are cached and instant on camera.
   - (The 2021 year is being pre-warmed in the background, so any 2021 dekad is fast.)
3. Browser zoom ~110% (`Cmd +`). Turn on Do Not Disturb. Close other tabs.
4. During recording, **release the slider on your target dekad** (don't scrub back and forth).

---

## THE 3-MINUTE SCRIPT

### 0:00–0:25 · Hook + what it is
> "ICPAC forecasts drought. HUSIKA delivers alerts. The missing piece is the decision in
> between — *who's at risk, what to do, and why.* That's **Tayari** — and it runs on real
> ICPAC data."

*(On screen: the dashboard, currently on the Latest dekad — calm.)*

### 0:25–1:00 · Real-time → real drought (the "wow" moment)
> "Live, right now, conditions are normal — the honest real-time picture. Let me scrub to
> the May 2021 Horn of Africa drought."

**Action:** drag the **timeline slider** to **2021-05** and release.
> "Watch — the AI situation briefing writes itself: four counties triggered, **1.88 million
> people exposed**. This is a real LLM reading real data."

*(Map turns red/orange; briefing types in.)*

### 1:00–1:45 · Impact + auditable evidence (the credibility moment)
**Action:** the worst county (**Garissa**) is auto-selected — point to the IBF card.
> "Garissa: Alert level, **841,353 people exposed**, mostly pastoralists — from the real 2019 census."

**Action:** click **"▶ Show evidence chain"** on the top recommendation.
> "Every recommendation is auditable: forecast → threshold crossed → population exposed →
> action. The AI writes the words, but a guard blocks it from inventing any number."

### 1:45–2:30 · Last-mile message (the human payoff)
**Action:** in the Message panel, set audience **Pastoralist**, language **Swahili** → **Preview**.
> "Now the last mile. Same facts, re-authored for the people who must act — low-literacy,
> their language, fits on any basic phone."

**Action:** switch channel to **Voice** (show IVR script) → click **Approve & dispatch**.
> "One click sends it — the exact payload HUSIKA delivers."

### 2:30–3:00 · Close
> "Tayari doesn't replace ICPAC's tools — it completes the stack: real data, auditable
> decisions, last-mile action, reproducible with one command. That's how you turn early
> warning into early action."

*(Optional 2-sec flash: localhost:8000/health showing hdx/stac/geonode = true.)*

---

## ON-SCREEN TEXT OVERLAYS (optional, add in editor)
- 0:05 — "Tayari · Impact-Based Forecasting Co-pilot"
- 0:30 — "100% real ICPAC / HDX data"
- 1:10 — "Auditable evidence — no black box"
- 1:50 — "Local-language, low-literacy, any phone"
- 2:45 — "Completes ICPAC's stack · 29 tests passing"

## DON'Ts
- Don't drag into 2020 dekads on camera (may be cold → 15s wait).
- Don't scrub the slider rapidly; land once and release.
- Don't read the whole evidence chain aloud — just point and say "auditable."
