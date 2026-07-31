# Presentation clips (record separately, cut around the app footage)

Two standalone animated pages — no build, no server. Open in Chrome, press **F11**
(fullscreen), screen-record, then **reload the page** (`Cmd/Ctrl + R`) to re-run from zero.
Tip: hide the mouse cursor while recording.

---

## 1) intro.html  — 3–5 second opener (before the app)
One-shot animation:
- Logo mark pops in → **Tayari** title → "Impact-Based Forecasting Co-pilot"
- Flow chips: **ICPAC forecast → decision → last-mile action**
- Tagline: "Turning early warning into early action."

**Full reveal completes ~4.5s.** Record ~5–6s, then hard-cut to the live app.
No voiceover needed here (or a 2-word "This is Tayari").

---

## 2) technical-outro.html — ~30s, synced to the Part A2 voiceover
Total timeline **~32s** (a progress bar runs along the bottom). Reveals are timed to
the outro narration in `docs/voiceover_script.md` (Part A2):

| VO line | On-screen (auto-timed) | ~clock |
|---|---|---|
| "built for real deployment" | Kicker + title appear | 0–3s |
| "live open data — ICPAC drought watch, HDX, census… same stack… 29 tests… one command" | 3 data sources slide in → flow into the **TAYARI** core → badges (same stack / 29 tests / one command) | 4–8s |
| "it's one pipeline" | Pipeline stages reveal: Ingest→Trigger→Impact→Reason→Localize→Dispatch | 14–18s |
| "scales to any hazard, district, language — drought today, floods and disease tomorrow" | Scalability chips fade in | 20–24s |
| "From forecast, to decision, to action — for every community left waiting" | Closing overlay: "From forecast, to decision, to **action**." | 27–32s |

### Sync method
1. Generate the Part A2 audio in ElevenLabs (~28–32s).
2. Open technical-outro.html fullscreen, start screen-recording, click **Replay** so the
   animation starts from 0.
3. In your editor, lay the audio under the video, nudge so the beats line up (the progress
   bar makes alignment easy). If your VO is a little faster/slower, trim the tail hold.

### Want the timing tweaked?
The reveal times are CSS `animation-delay` values (in seconds) in the file — easy to shift.
Tell Kiro your exact audio length per beat and it can retime it to match precisely.
