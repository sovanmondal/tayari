# Project Overview (≈250 words)

**Tayari — the Impact-Based Forecasting Co-pilot**

In the Horn of Africa, the forecast is rarely the problem. ICPAC already produces
world-class drought forecasts, and HUSIKA already delivers alerts to the last mile. The
gap ICPAC itself names as unsolved is the **missing middle**: turning a forecast into a
decision — *who exactly is at risk, what action should be triggered, and why* — is still
done manually, district by district, and it does not scale. This is the "long pending
operationalization of Impact-Based Forecasting."

Tayari fills that gap. It is the operational reasoning layer that sits **between the
forecast and the delivery pipe**. For every district it ingests the **real** Combined
Drought Indicator (ICPAC East Africa Drought Watch, via HDX), crosses it against
published drought triggers, intersects the hazard with **real census exposure** to
estimate who is affected, and returns a ranked list of **anticipatory actions** drawn
from Kenya NDMA, FAO and IFRC protocols — each backed by an **auditable evidence chain**
from forecast value → threshold crossed → population exposed → recommended action.

It then generates the **last-mile message** — audience-specific (pastoralist, farmer,
DRM officer), in English or Swahili, as low-literacy SMS or a voice/IVR script — the exact
content HUSIKA needs, and can dispatch it via a real SMS gateway.

Tayari does not compete with ICPAC's systems; it **completes the stack**. Every number is
traceable to a real source, no figure is fabricated, and it runs on real open data with
one `docker compose up`. It converts early warning into early, accountable action.
