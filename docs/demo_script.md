# Demo Video Script (≤ 5 minutes)

**Goal:** show the missing middle — forecast → decision → action — working on real data.

---

### 0:00–0:35 · The problem (hook)
> "In the Horn of Africa, the forecast usually isn't the problem. ICPAC already produces
> excellent drought forecasts. HUSIKA already delivers alerts to the last mile. But the
> step in between — deciding *who is at risk, what action to trigger, and why* — is still
> done by hand, district by district. ICPAC calls it the unsolved operationalization of
> Impact-Based Forecasting. That's the gap Tayari fills."

Show the slide: `Forecast → [Tayari] → HUSIKA`.

### 0:35–1:10 · What it is
> "Tayari is the reasoning layer between the forecast and the delivery pipe. It runs
> entirely on real ICPAC and humanitarian open data — no mock data anywhere."

Run `docker compose up`; open `http://localhost:8000/health` → show `hdx/stac/geonode: true`.

### 1:10–2:15 · The map + real hazard
Open the dashboard. Point to the map of Kenya's ASAL counties for the **May 2021** dekad.
> "These colours are the real Combined Drought Indicator from ICPAC's East Africa Drought
> Watch, sampled per county. Garissa and Isiolo are in Alert, Marsabit in Warning."

Click **Garissa**.

### 2:15–3:20 · IBF + auditable reasoning
Show the IBF card: CDI class 8, **841,353 people exposed**, livelihood breakdown.
> "Tayari intersects the hazard with the 2019 census to estimate who's affected."

Expand the top recommendation's **evidence chain**.
> "Every recommendation is auditable: forecast value → threshold crossed → population
> exposed → action. The narrative is AI-generated but grounded — a guard blocks any number
> the engine didn't compute."

### 3:20–4:20 · Last-mile message
Open the Message panel. Switch audience to **Pastoralist**, language to **Swahili**.
> "Now the last mile. Same facts, re-authored for the people who must act — low-literacy,
> in their language, SMS-length, with a voice/IVR script."

Click **Approve & dispatch** → show dispatch status (Africa's Talking).

### 4:20–5:00 · Close
> "Tayari doesn't replace ICPAC's tools — it completes the stack. Real data, auditable
> decisions, last-mile action, reproducible with one command. That's how we turn early
> warning into early action."

Show: GitHub repo + `29 tests passing`.
