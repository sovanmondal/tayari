"""LLM provider with a strict grounding contract (FR-4.3).

The narrative/localization layers may ONLY restate numbers computed by the engine.
We enforce this two ways:
  1. Prompt: instruct the model to use only the provided facts.
  2. Post-validation: reject any numeric token in the output that is not present in the
     allowed grounding numbers; on failure, fall back to the deterministic template.

Providers: template (default, no key needed), bedrock, openai. The template provider
is fully functional so the system runs with zero LLM credentials.
"""
from __future__ import annotations

import re

from app.config import settings

_NUM = re.compile(r"\d[\d,\.]*")


def _norm(tok: str) -> str:
    """Normalize a numeric token: drop thousands separators and trailing punctuation."""
    return tok.strip(".,").replace(",", "")


def allowed_numbers(context: dict) -> set[str]:
    """Collect every numeric token that appears in the grounding context values."""
    allowed: set[str] = set()
    for v in context.values():
        for m in _NUM.findall(str(v)):
            allowed.add(_norm(m))
    return allowed


def violates_grounding(text: str, context: dict, only_major: bool = False) -> bool:
    """True if the text introduces a number not present in the grounding context.

    only_major=True checks only 'major' figures (>= 1000) — used for community messages,
    where the critical guarantee is not fabricating population/impact numbers, while
    natural timeframes ("within 2 weeks") are allowed.
    """
    allowed = allowed_numbers(context)
    for tok in _NUM.findall(text):
        n = _norm(tok)
        if n in allowed:
            continue
        if only_major:
            try:
                if float(n) < 1000:
                    continue
            except ValueError:
                continue
        return True
    return False


class LLMProvider:
    def complete(self, system: str, prompt: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class TemplateProvider(LLMProvider):
    """Deterministic — returns the prompt's pre-rendered template body verbatim.

    The caller passes the fully-rendered fallback text as the prompt; this provider
    simply returns it, guaranteeing grounded output with zero external dependencies.
    """

    def complete(self, system: str, prompt: str) -> str:
        return prompt


class BedrockProvider(LLMProvider):  # pragma: no cover - requires AWS creds
    def complete(self, system: str, prompt: str) -> str:
        import json

        import boto3

        client = boto3.client("bedrock-runtime", region_name=settings.aws_region)
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 600,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }
        resp = client.invoke_model(modelId=settings.bedrock_model_id, body=json.dumps(body))
        payload = json.loads(resp["body"].read())
        return payload["content"][0]["text"]


class OpenAIProvider(LLMProvider):  # pragma: no cover - requires API key
    def complete(self, system: str, prompt: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
        )
        return resp.choices[0].message.content or ""


class GroqProvider(LLMProvider):  # pragma: no cover - requires API key
    """Groq via its OpenAI-compatible endpoint (fast, free-tier)."""

    def complete(self, system: str, prompt: str) -> str:
        from openai import OpenAI

        # Tight timeout + no long retries: if Groq is slow, fail fast so the caller
        # falls back to the deterministic grounded template instead of hanging the UI.
        client = OpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
            timeout=12.0,
            max_retries=1,
        )
        resp = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.3,
        )
        return resp.choices[0].message.content or ""


def get_provider() -> LLMProvider:
    p = settings.llm_provider.lower()
    if p == "bedrock":
        return BedrockProvider()
    if p == "groq" and settings.groq_api_key:
        return GroqProvider()
    if p == "openai" and settings.openai_api_key:
        return OpenAIProvider()
    return TemplateProvider()


def grounded_complete(system: str, prompt: str, context: dict, fallback: str,
                      only_major: bool = False) -> str:
    """Run the provider, but return `fallback` if the output breaks the grounding contract."""
    provider = get_provider()
    if isinstance(provider, TemplateProvider):
        return fallback
    try:
        out = provider.complete(system, prompt).strip()
    except Exception:
        return fallback
    if not out or violates_grounding(out, context, only_major=only_major):
        return fallback
    return out
