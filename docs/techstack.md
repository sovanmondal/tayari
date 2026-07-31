# Tech Stack

## Backend
- **Python 3.11 + FastAPI** — REST API (mirrors ICPAC's own `fast-cgan` service)
- **PostgreSQL 16 + PostGIS 3** — geospatial persistence
- **geopandas / shapely** — area-weighted hazard × exposure intersection
- **rasterio + numpy** — zonal sampling of the real CDI GeoTIFFs
- **Pydantic v2 / pydantic-settings** — typed models, env-driven config
- **httpx + tenacity** — async upstream calls with retry + timestamped cache

## Reasoning
- **Deterministic trigger engine** — CDI class → severity → trigger (no LLM, fully tested)
- **Anticipatory-action playbook** — YAML rules from Kenya NDMA EDE, FAO, IFRC/WFP protocols
- **Auditable evidence chain** — forecast → threshold → exposure → action, each source-cited
- **LLM layer** — provider-agnostic (Amazon Bedrock / OpenAI / deterministic template),
  with a numeric-hallucination guard enforcing a strict grounding contract

## Frontend
- **React 18 + TypeScript + Vite**
- **MapLibre GL** — severity choropleth of districts, click-to-drill-down
- **TanStack Query** — data fetching/caching
- **TailwindCSS** — UI

## Delivery / Ops
- **Docker Compose** — one-command full stack (db + backend + frontend)
- **Africa's Talking** — real SMS dispatch (sandbox), simulated when no credentials

## Real data sources (all verified live)
| Source | API | Used for |
|---|---|---|
| ICPAC East Africa Drought Watch — Combined Drought Indicator | HDX CKAN (`data.humdata.org/api/3`) | Drought hazard signal (dekadal GeoTIFFs) |
| ICPAC STAC IBF catalog | GitHub raw (STAC 1.1.0) | Impact-based-forecasting catalog structure |
| ICPAC GeoNode Geoportal | `geoportal.icpac.net/api/v2` | 1,096 geospatial layers + WMS/WFS |
| Kenya KNBS 2019 Census | Official statistics | Population / livelihood exposure |
| Kenya NDMA / FAO / IFRC | Published protocols | Anticipatory-action playbook |

## Testing
- 29 automated tests: unit (trigger, impact, playbook, grounding, localization),
  deterministic API integration, and live-endpoint connector tests.

## Attribution
Open data and open-source methodology from ICPAC/IGAD, the Humanitarian Data Exchange
(HDX), the Copernicus EDO CDI methodology, and the GeoNode project.
