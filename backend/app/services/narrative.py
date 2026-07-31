"""Narrative service (FR-4.3): compose a grounded IBF summary.

Builds a deterministic template narrative from computed facts, then optionally lets an
LLM rephrase it — but only within the grounding contract (no new numbers). The template
is always a valid, fully-grounded output on its own.
"""
from __future__ import annotations

from app.domain.models import ImpactEstimate, Recommendation, Trigger
from app.services.llm import grounded_complete

SYSTEM = (
    "You are an impact-based-forecasting analyst for the IGAD/ICPAC region. "
    "Write a concise, factual advisory for disaster-risk decision-makers. "
    "Use ONLY the facts provided. Do NOT invent any numbers, dates, or place names. "
    "Do not add figures that are not in the facts."
)


def compose_ibf_narrative(
    admin_name: str,
    trigger: Trigger,
    impact: ImpactEstimate,
    top_actions: list[Recommendation],
) -> str:
    livelihood = ", ".join(
        f"{b.population:,} {b.livelihood}" for b in impact.by_livelihood
    ) or "population"
    action_names = "; ".join(f"{r.action} (lead time {r.lead_time_days} days)" for r in top_actions[:3])

    context = {
        "admin": admin_name,
        "cdi_class": int(round(trigger.observed_value)),
        "severity": trigger.severity.value,
        "exposed": f"{impact.total_population_exposed:,}",
        "livelihood": livelihood,
        "valid": "",
        "actions": action_names,
    }

    if trigger.triggered:
        fallback = (
            f"IMPACT-BASED FORECAST — {admin_name}. The Combined Drought Indicator has reached "
            f"class {context['cdi_class']} ('{trigger.severity.value}'), crossing the anticipatory-action "
            f"trigger. An estimated {context['exposed']} people are exposed ({livelihood}). "
            f"Recommended anticipatory actions before impacts escalate: {action_names}. "
            f"Acting now, within the stated lead times, protects livestock assets and household "
            f"food security ahead of the peak."
        )
    else:
        fallback = (
            f"MONITORING — {admin_name}. The Combined Drought Indicator is at class "
            f"{context['cdi_class']} ('{trigger.severity.value}'), below the anticipatory-action trigger. "
            f"No population is classified as exposed yet. Maintain monitoring and keep contingency "
            f"stocks ready; {action_names}."
        )

    prompt = (
        "Rewrite the following advisory in clear plain English for decision-makers, keeping every "
        "number and name exactly as given and adding no new figures:\n\n" + fallback
    )
    return grounded_complete(SYSTEM, prompt, context, fallback)
