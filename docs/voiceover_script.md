# Tayari — Voiceover Script (for ElevenLabs)

**Target length:** ~3:00 · **Recommended voice:** calm, confident, documentary tone
(e.g. "Adam", "Daniel", or "Rachel"). **Stability ~50%, Similarity ~75%, Speed slightly slow.**

---

## PART A — PASTE THIS INTO ELEVENLABS (phonetic, paste-ready)

In the Horn of Africa, the forecast is rarely the problem.

eye-see-pack already predicts drought. And hoo-see-kah already delivers alerts to the last mile.
The missing piece is the decision in between — who is at risk, what action to take, and why.

This is tah-YAH-ree — the anticipatory action co-pilot. And it runs entirely on real data.

Right now, live, conditions here are normal. That's the honest, real-time picture.

But let's go back to the drought of 2021.

Watch the briefing write itself. Four counties have crossed the drought trigger.
More than one point eight million people are now exposed. This is a real AI model, reading real data.

Take Garissa — the worst hit. Over eight hundred and forty thousand people affected, most of them livestock herders.

And here is what makes it trustworthy. Every recommendation is auditable.

The drought reading. The threshold it crossed. The people exposed. And the action to take.
The AI writes the words — but it is blocked from inventing a single number.

Now, the last mile.

One forecast becomes three messages — for the herder, the farmer, and the officer who
must respond. tah-YAH-ree turns the plan into a message anyone can act on. The same real
actions — sell the weak animals now, move the herd to water, vaccinate the breeding stock —
written in plain words, in the community's own language, and short enough for any basic phone.
And for those who cannot read, a spoken version.

Nothing is sent automatically. The officer reviews, and approves. One click hands the
message to the HUSIKA gateway for delivery — with a tracking reference.

Here, we run against a sandbox. Connected to the live HUSIKA server, that same approval
delivers the alert to every phone, for real.

This is early warning, finally turned into early action.

tah-YAH-ree doesn't replace eye-see-pack's tools. It completes the stack.

Real data. Auditable decisions. Action at the last mile.

---

## PART A2 — OPTIONAL 30-SECOND TECHNICAL OUTRO (paste separately if using)

Under the hood, tah-YAH-ree is built for real deployment.

It runs on live open data — eye-see-pack's drought watch, the humanitarian data exchange,
and national census figures — on the same stack eye-see-pack already uses. Twenty-nine
automated tests, and the whole system starts with a single command.

And it's one pipeline. The same engine scales to any hazard, any district, any language —
from drought today, to floods and disease tomorrow.

From forecast, to decision, to action — for every community that's been left waiting.

---

## PART B — VIDEO SYNC SHEET (match footage to the audio)

| VO line (cue) | On-screen action | Approx clock |
|---|---|---|
| "the forecast is rarely the problem" | Dashboard on **Latest** dekad (calm map) | 0:00–0:12 |
| "This is Tayari… real data" | Slow zoom on header / logo | 0:12–0:22 |
| "conditions here are normal" | Point at calm map + "0 triggered" | 0:22–0:30 |
| "go back to the drought of 2021" | **Drag slider → May 2021**, release | 0:30–0:40 |
| "the briefing write itself… 1.8 million" | Briefing types in; map turns red | 0:40–0:58 |
| "Take Garissa — the worst hit" | Garissa auto-selected; IBF card | 0:58–1:12 |
| "Every recommendation is auditable" | **Click "Show evidence chain"** | 1:12–1:25 |
| "reading… threshold… exposed… action" | Scroll the 4 evidence steps slowly | 1:25–1:45 |
| "AI writes the words… blocked from inventing" | Point at narrative + provenance badges | 1:45–1:58 |
| "Now, the last mile" | Open Message panel | 1:58–2:06 |
| "sell the weak animals… move the herd… vaccinate" | audience **Pastoralist**, lang **English** → **Preview** (show the rich message + SMS segments) | 2:06–2:22 |
| "in the community's own language" | switch lang → **Swahili** → Preview (show Swahili text) | 2:22–2:32 |
| "a spoken version for those who cannot read" | switch channel → **Voice**, show IVR script | 2:32–2:40 |
| "The officer reviews, and approves. One click…" | Click **Approve & dispatch** → the green "✓ QUEUED · HUSIKA … · ref TYR-…" appears | 2:40–2:52 |
| "early warning, finally turned into early action" | Wide shot of dashboard | 2:52–3:00 |

## WHAT TO DO / SHOW AT "APPROVE & DISPATCH"
- Before clicking, hover the two buttons so viewers see **Preview** vs **Approve & dispatch** — this
  sells the human-in-the-loop point ("nothing sends until a human approves").
- Click **Approve & dispatch**. A green confirmation appears:
  **"✓ Delivered to gateway — QUEUED · HUSIKA / Africa's Talking (sandbox) · ref TYR-XXXXXXXXXX"**.
- Let that reference sit on screen for ~2 seconds — the reference number makes it feel operational.
- Do NOT claim "the herder just received an SMS" (it's sandbox). Say "handed to the HUSIKA
  gateway for delivery" — accurate and still impressive.

### Optional outro (if using Part A2) — extends to ~3:30
| VO line (cue) | On-screen action | Approx clock |
|---|---|---|
| "built for real deployment" | Show `localhost:8000/docs` (API) or an architecture slide | 3:00–3:08 |
| "live open data… same stack… 29 tests… single command" | Flash `/health` (hdx/stac/geonode = true) + a terminal showing `29 passed` | 3:08–3:20 |
| "one pipeline… any hazard, any district, any language" | Back to dashboard; hover the language/audience switches | 3:20–3:28 |
| "for every community that's been left waiting" | Slow zoom out on the map | 3:28–3:32 |

---

## PRONUNCIATION / TTS TIPS
- **ICPAC** may read as letters. If it sounds wrong, type it as **"eye-see-pack"** in ElevenLabs.
- **HUSIKA** → if odd, type **"hoo-see-kah"**.
- **Tayari** → **"tah-YAH-ree"**.
- Keep the spoken numbers as written ("one point eight million", "eight hundred and forty
  thousand") — do not paste raw digits; TTS reads long digit strings awkwardly.
- The "..." before "into early action" is a deliberate beat — leave it for emphasis.

## WORKFLOW
1. Generate audio from PART A. Listen; regenerate any awkward line individually.
2. Note the real timestamps of each cue in your audio (they'll be close to Part B).
3. Screen-record the dashboard, performing each action to match the audio timing.
4. Lay the VO over the footage; trim to land under 3:00.
