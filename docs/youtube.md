# YouTube — Title & Description

## TITLE (recommended)
Tayari — From Drought Forecast to Last-Mile Action | IGAD Hackathon 2026

**Live video:** https://youtu.be/wGpn9EZxptI

### Alternate titles
- Tayari: The AI Co-pilot that Completes ICPAC's Early-Warning Stack
- Tayari — Impact-Based Forecasting Co-pilot (IGAD Hackathon 2026 Demo)
- Turning Early Warning into Early Action — Tayari | IGAD Hackathon 2026

---

## DESCRIPTION

Tayari is the missing middle of early warning.

In the Horn of Africa, the drought forecast is rarely the problem — ICPAC already predicts
drought, and HUSIKA already delivers alerts to the last mile. The gap is the decision in
between: who is at risk, what action to take, and why. Today that's done by hand, district by
district. Tayari automates it — on 100% real data.

For any district, Tayari:
• Reads the real ICPAC East Africa Drought Watch Combined Drought Indicator
• Detects when a district crosses the anticipatory-action trigger
• Estimates who is affected, by livelihood, using real census exposure
• Recommends ranked anticipatory actions (Kenya NDMA / FAO / IFRC) with an auditable evidence chain
• Writes the last-mile message — for herders, farmers, and officials — in English or Swahili,
  as a low-literacy SMS and a voice/IVR script — then hands it to the HUSIKA gateway

Tayari doesn't replace ICPAC's tools. It completes the stack.

⏱️ Chapters
0:00  The problem — the missing middle
0:30  Real ICPAC drought data, in real time
1:00  Impact-based forecast + auditable evidence chain
1:45  The last mile — one forecast, three audiences (English + Swahili + voice)
2:40  Approve & dispatch to HUSIKA
2:50  From early warning to early action

🧰 Built with
Python · FastAPI · PostGIS · geopandas · rasterio · React · TypeScript · MapLibre · Groq
(Llama-3.3) · Docker · Africa's Talking

📡 Real data sources
ICPAC East Africa Drought Watch (Combined Drought Indicator, via HDX) · Humanitarian Data
Exchange (HDX) · ICPAC GeoNode Geoportal & STAC IBF catalog · Kenya KNBS 2019 Census

✅ Fully operational: runs end-to-end on real open data with one command; 29 automated tests.
🔒 Responsible AI: the LLM writes the narrative and messages but is blocked from inventing any
number, and a human approves before anything is dispatched.

🔗 Links
GitHub: (paste your repo URL here)
Devpost: (paste your project URL here)

Built for the IGAD Hackathon 2026 — "Smarter Early Warning, Stronger Communities."
Data © ICPAC / IGAD, HDX, and the GeoNode project. Built with respect and proper attribution.

#IGADHackathon2026 #ICPAC #EarlyWarning #AnticipatoryAction #DisasterRiskReduction
#ClimateResilience #AI #GIS #HornOfAfrica #Drought
