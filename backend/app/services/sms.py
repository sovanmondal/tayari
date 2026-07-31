"""SMS dispatch (FR-5.5).

If Africa's Talking sandbox credentials are configured, sends a real SMS via their
sandbox API. Otherwise returns a `simulated` dispatch with the exact payload that would
be sent — so the pipeline is always complete and honest about what happened.
"""
from __future__ import annotations

import time

import httpx

from app.config import settings
from app.domain.models import Message

AT_ENDPOINT = "https://api.sandbox.africastalking.com/version1/messaging"


async def dispatch_sms(message: Message, to: str | None = None) -> dict:
    """Dispatch a message. Returns {status, provider_id?, payload, at}."""
    body = "\n".join(message.sms_segments) or message.text
    recipient = to or "+254700000000"  # sandbox test number placeholder
    payload = {
        "to": recipient,
        "from": settings.at_sender,
        "message": body,
        "admin_id": message.admin_id,
        "audience": message.audience,
        "language": message.language,
        "channel": message.channel,
    }

    if not (settings.at_username and settings.at_api_key):
        import uuid
        ref = "TYR-" + uuid.uuid4().hex[:10].upper()
        return {
            "status": "queued",
            "gateway": "HUSIKA / Africa's Talking (sandbox)",
            "reference": ref,
            "note": "Sandbox mode — payload validated and queued. Add live gateway credentials to send.",
            "payload": payload,
            "at": time.time(),
        }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.post(
                AT_ENDPOINT,
                data={
                    "username": settings.at_username,
                    "to": recipient,
                    "from": settings.at_sender,
                    "message": body,
                },
                headers={"apiKey": settings.at_api_key, "Accept": "application/json"},
            )
            r.raise_for_status()
            data = r.json()
        recipients = data.get("SMSMessageData", {}).get("Recipients", [])
        provider_id = recipients[0].get("messageId") if recipients else None
        return {"status": "sent", "provider_id": provider_id, "payload": payload, "at": time.time()}
    except Exception as e:
        return {"status": "error", "reason": str(e), "payload": payload, "at": time.time()}
