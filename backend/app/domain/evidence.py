"""Auditable evidence chain (FR-4.2).

Builds the reasoning trail behind a recommendation:
  forecast value -> threshold crossed -> exposed population -> recommended action.
Every link cites its data source. This is what makes the recommendation defensible.
"""
from __future__ import annotations

from app.domain.models import (
    EvidenceLink,
    HazardSignal,
    ImpactEstimate,
    Provenance,
    Trigger,
)


def build_chain(
    signal: HazardSignal,
    trigger: Trigger,
    impact: ImpactEstimate,
    hazard_provenance: Provenance,
    admin_name: str,
) -> list[EvidenceLink]:
    census = next(
        (p.source for p in impact.sources if "census" in p.source.lower() or "KNBS" in p.source),
        "KNBS 2019 Census",
    )
    links = [
        EvidenceLink(
            step="1. Observed hazard",
            detail=(
                f"{admin_name}: Combined Drought Indicator = class {int(round(signal.value))} "
                f"('{trigger.severity.value}') for dekad {signal.valid_from}."
            ),
            source=hazard_provenance.url,
        ),
        EvidenceLink(
            step="2. Threshold crossed",
            detail=trigger.rationale,
            source="Tayari thresholds.yaml (EDO/EADW CDI class legend; trigger = Warning)",
        ),
        EvidenceLink(
            step="3. Population exposed",
            detail=(
                f"{impact.total_population_exposed:,} people in {admin_name} exposed "
                f"(" + ", ".join(
                    f"{b.population:,} {b.livelihood}" for b in impact.by_livelihood
                ) + ")."
                if impact.by_livelihood
                else f"{impact.total_population_exposed:,} people exposed."
            ),
            source=census,
        ),
        EvidenceLink(
            step="4. Action rationale",
            detail=(
                "Trigger reached at Warning/Alert gives lead time to act before livestock "
                "condition and household food security deteriorate — anticipatory action."
            ),
            source="Kenya NDMA EDE framework / FAO & IFRC drought AA protocols",
        ),
    ]
    return links
