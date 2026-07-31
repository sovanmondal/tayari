"""Localization & last-mile message generator (FR-5).

Produces audience-specific, multilingual, low-literacy-friendly messages with SMS
segmentation and a voice/IVR script — the HUSIKA-compatible content payload.

Audiences: drm_officer (technical), pastoralist, farmer.
Languages:  en (English), sw (Swahili). Extensible via TEMPLATES.

Messages are grounded: numbers come only from the computed impact/trigger. The optional
LLM pass may only rephrase within the grounding contract (see services/llm.py).
"""
from __future__ import annotations

from app.domain.models import ImpactEstimate, Message, Recommendation, Trigger
from app.services.llm import grounded_complete

SMS_SEGMENT_LEN = 160

# Human-readable severity per language.
SEVERITY_WORD = {
    "en": {"warning": "Warning", "alert": "ALERT", "watch": "Watch", "none": "Normal"},
    "sw": {"warning": "Tahadhari", "alert": "HATARI", "watch": "Angalizo", "none": "Kawaida"},
}


def _segment_sms(text: str) -> list[str]:
    words = text.split()
    segments, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > SMS_SEGMENT_LEN:
            segments.append(cur.strip())
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        segments.append(cur.strip())
    return segments


def _compose_text(
    audience: str, language: str, admin_name: str, trigger: Trigger,
    impact: ImpactEstimate, top_action: Recommendation | None,
) -> str:
    sev = SEVERITY_WORD.get(language, SEVERITY_WORD["en"]).get(trigger.severity.value, trigger.severity.value)
    action = top_action.action if top_action else ""
    lead = top_action.lead_time_days if top_action else 0
    exposed = f"{impact.total_population_exposed:,}"

    if language == "sw":
        if audience == "pastoralist":
            return (
                f"{sev}: Ukame unakuja {admin_name}. Maji na malisho yatapungua. "
                f"Uza mifugo dhaifu sasa, weka akiba ya maji na malisho. Tenda ndani ya siku {lead}."
            )
        if audience == "farmer":
            return (
                f"{sev}: Ukame unakuja {admin_name}. Panda mbegu zinazostahimili ukame, "
                f"hifadhi maji na chakula. Tenda mapema ndani ya siku {lead}."
            )
        return (  # drm_officer
            f"{sev} — {admin_name}: Kiashiria cha Ukame (CDI) daraja {int(round(trigger.observed_value))}. "
            f"Watu {exposed} wako hatarini. Hatua ya mapema: {action} (siku {lead})."
        )

    # English
    if audience == "pastoralist":
        return (
            f"{sev}: Drought is coming to {admin_name}. Water and pasture will run short. "
            f"Sell weak animals now and store water and feed. Act within {lead} days."
        )
    if audience == "farmer":
        return (
            f"{sev}: Drought is coming to {admin_name}. Plant drought-tolerant seed and "
            f"store water and food now. Act early, within {lead} days."
        )
    return (  # drm_officer
        f"{sev} — {admin_name}: Combined Drought Indicator class {int(round(trigger.observed_value))}. "
        f"{exposed} people exposed. Priority anticipatory action: {action} (lead time {lead} days)."
    )


def _voice_script(text: str, language: str) -> str:
    lead_in = {
        "en": "This is an early warning message from the county disaster team. ",
        "sw": "Huu ni ujumbe wa tahadhari ya mapema kutoka kwa timu ya maafa ya kaunti. ",
    }.get(language, "")
    repeat = {"en": " I repeat. ", "sw": " Narudia. "}.get(language, " ")
    return f"{lead_in}{text}{repeat}{text}"


def compose_message(
    admin_name: str,
    admin_id: str,
    trigger: Trigger,
    impact: ImpactEstimate,
    recommendations: list[Recommendation],
    audience: str = "pastoralist",
    language: str = "en",
    channel: str = "sms",
    valid_until: str | None = None,
) -> Message:
    top = recommendations[0] if recommendations else None
    # Deterministic fallback (always valid, grounded) if the LLM is unavailable/off-contract.
    fallback = _compose_text(audience, language, admin_name, trigger, impact, top)

    top_actions = recommendations[:3]
    actions_str = "; ".join(
        f"{r.action} (within {r.lead_time_days} days)" for r in top_actions
    ) or "follow official guidance"
    livelihood = ", ".join(
        f"{b.population:,} {b.livelihood}" for b in impact.by_livelihood
    ) or "residents"

    lang_name = {"en": "English", "sw": "Swahili"}.get(language, language)
    audience_desc = {
        "pastoralist": "a pastoralist livestock herder in a remote rural area",
        "farmer": "a smallholder farmer",
        "drm_officer": "a county disaster-management officer",
    }.get(audience, "a community member")

    # Numbers the LLM is allowed to use verbatim (major-number guard blocks fake populations).
    context = {
        "exposed": f"{impact.total_population_exposed:,}",
        "cdi": int(round(trigger.observed_value)),
        "leads": " ".join(str(r.lead_time_days) for r in top_actions),
    }

    if audience == "drm_officer":
        system = (
            f"You are ICPAC's disaster-management briefing officer. Write a concise, professional "
            f"drought early-action alert in {lang_name} for {audience_desc}. State the situation and "
            f"the priority actions with their lead times, drawn ONLY from the provided action list. "
            f"3-4 sentences. Do NOT invent population figures or place names."
        )
    else:
        system = (
            f"You are ICPAC's community early-warning officer. Write a clear, practical drought "
            f"warning in {lang_name} for {audience_desc}. Explain simply what is happening and give "
            f"the specific, concrete actions to take — drawn ONLY from the provided action list, "
            f"reworded into plain everyday language a low-literacy reader understands (e.g. 'sell "
            f"weak animals at the market now', 'move your herd to the water points', 'vaccinate your "
            f"breeding animals'). 3-5 short sentences, warm and direct. For any timeframe use only the "
            f"day counts given. Do NOT invent population numbers or place names."
        )

    prompt = (
        f"Location: {admin_name}. Drought level: {trigger.severity.value} "
        f"(Combined Drought Indicator class {context['cdi']}). "
        f"People exposed: {context['exposed']} ({livelihood}). "
        f"Official recommended actions, in priority order: {actions_str}. "
        f"Write the message in {lang_name} now. Start with the alert level word."
    )

    text = grounded_complete(system, prompt, context, fallback, only_major=True)

    return Message(
        audience=audience,
        language=language,
        channel=channel,
        admin_id=admin_id,
        text=text,
        sms_segments=_segment_sms(text),
        voice_script=_voice_script(text, language),
        valid_until=valid_until,
    )
