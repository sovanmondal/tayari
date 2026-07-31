"""HttpCachedClient: retry + timeout + on-disk cache + provenance + stale fallback.

Implements FR-1.4 (serve cached/stale on failure, never fabricate) and FR-1.5 (provenance).
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)


@dataclass
class Provenance:
    source: str
    url: str
    retrieved_at: float
    stale: bool = False

    def as_dict(self) -> dict:
        return {
            "source": self.source,
            "url": self.url,
            "retrieved_at": self.retrieved_at,
            "age_seconds": round(time.time() - self.retrieved_at, 1),
            "stale": self.stale,
        }


@dataclass
class Fetched:
    data: Any
    provenance: Provenance
    meta: dict = field(default_factory=dict)


class HttpCachedClient:
    """Async GET with retry and a timestamped on-disk cache used as stale fallback."""

    def __init__(self, source_name: str) -> None:
        self.source_name = source_name

    def _cache_path(self, url: str) -> Path:
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        return CACHE_DIR / f"{self.source_name}_{key}.json"

    def _write_cache(self, url: str, data: Any) -> float:
        ts = time.time()
        self._cache_path(url).write_text(
            json.dumps({"url": url, "retrieved_at": ts, "data": data})
        )
        return ts

    def _read_cache(self, url: str) -> tuple[Any, float] | None:
        p = self._cache_path(url)
        if not p.exists():
            return None
        try:
            blob = json.loads(p.read_text())
            return blob["data"], blob["retrieved_at"]
        except Exception:
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4))
    async def _get(self, url: str, headers: dict | None = None) -> Any:
        async with httpx.AsyncClient(timeout=settings.request_timeout, follow_redirects=True) as client:
            r = await client.get(url, headers=headers or {"Accept": "application/json"})
            r.raise_for_status()
            # Some sources (e.g. GitHub raw) serve JSON as text/plain — parse regardless.
            try:
                return r.json()
            except Exception:
                import json as _json
                try:
                    return _json.loads(r.text)
                except Exception:
                    return r.text

    async def get(self, url: str, headers: dict | None = None) -> Fetched:
        try:
            data = await self._get(url, headers)
            ts = self._write_cache(url, data)
            return Fetched(data, Provenance(self.source_name, url, ts, stale=False))
        except Exception:
            cached = self._read_cache(url)
            if cached is not None:
                data, ts = cached
                return Fetched(data, Provenance(self.source_name, url, ts, stale=True))
            raise
