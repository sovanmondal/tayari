"""Regional situation briefing (AI-era auto-summary).

Aggregates the per-district IBF bundle into region-wide numbers, then composes a briefing.
Uses the real LLM when a provider is configured (Bedrock/OpenAI); otherwise a deterministic
grounded template. Either way, numbers come only from the computed data (grounding contract).
"""
from __future__ import annotations

from app.config import settings
from app.domain.trigger_engine import class_info
from app.services import ibf_service
from app.services.llm import grounded_complete

SYSTEM = (
    "You are ICPAC's regional drought situation analyst. Write a punchy 3-4 sentence "
    "situation briefing for decision-makers. Use ONLY the facts provided; invent no "
    "numbers or place names."
)


async def regional_briefing(as_of: str | None = None) -> dict:
    as_of = as_of or settings.cdi_as_of
    bundle = await ibf_service._compute(as_of)

    triggered = [b for b in bundle.values() if b["trigger"].triggered]
    total_exposed = sum(b["impact"].total_population_exposed for b in triggered)
    dekad = next(iter(bundle.values()))["signal"].valid_from if bundle else as_of

    worst = None
    if triggered:
        worst = max(triggered, key=lambda b: (b["trigger"].severity.rank,
                                              b["impact"].total_population_exposed))
    worst_name = worst["county"]["name"] if worst else None
    top_action = worst["recommendations"][0].action if worst and worst["recommendations"] else ""

    stats = {
        "as_of": dekad,
        "counties_total": len(bundle),
        "counties_triggered": len(triggered),
        "total_exposed": total_exposed,
        "worst_county": worst_name,
        "worst_severity": worst["trigger"].severity.value if worst else "none",
        "top_action": top_action,
        "triggered_names": [b["county"]["name"] for b in triggered],
    }

    if triggered:
        names = ", ".join(stats["triggered_names"])
        fallback = (
            f"SITUATION BRIEFING — dekad {dekad}. {len(triggered)} of {len(bundle)} monitored "
            f"counties have crossed the drought anticipatory-action trigger: {names}. "
            f"An estimated {total_exposed:,} people are exposed across these counties. "
            f"{worst_name} is worst-hit ('{stats['worst_severity']}'); priority action: {top_action}. "
            f"Act now within the stated lead times to protect livestock and food security."
        )
    else:
        fallback = (
            f"SITUATION BRIEFING — dekad {dekad}. None of the {len(bundle)} monitored counties "
            f"have crossed the drought anticipatory-action trigger. Conditions are within normal "
            f"range; maintain routine monitoring."
        )

    context = {
        "triggered": len(triggered), "total": len(bundle),
        "exposed": f"{total_exposed:,}", "action": top_action,
    }
    text = grounded_complete(
        SYSTEM,
        "Rewrite this as a crisp regional briefing, same numbers and names, no new figures:\n\n"
        + fallback,
        context, fallback,
    )
    llm_used = settings.llm_provider.lower() in ("bedrock", "groq", "openai")
    return {"stats": stats, "text": text, "llm": settings.llm_provider if llm_used else "template"}
