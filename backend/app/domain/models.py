"""Core domain models (pydantic). Shared across engine, services, and API."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    NONE = "none"
    WATCH = "watch"
    WARNING = "warning"
    ALERT = "alert"

    @property
    def rank(self) -> int:
        return {"none": 0, "watch": 1, "warning": 2, "alert": 3}[self.value]


class Provenance(BaseModel):
    source: str
    url: str
    retrieved_at: float
    age_seconds: float = 0.0
    stale: bool = False


class AdminUnit(BaseModel):
    id: str
    name: str
    country: str
    level: int = 1


class HazardSignal(BaseModel):
    """A single observed/forecast hazard indicator value for an admin unit."""
    indicator: str = "CDI"  # Combined Drought Indicator
    value: float
    valid_from: str | None = None
    valid_to: str | None = None
    unit: str = "class"
    source: str = "HDX/ICPAC EADW CDI"


class Trigger(BaseModel):
    triggered: bool
    severity: Severity
    indicator: str
    observed_value: float
    threshold: float
    exceedance: float = Field(..., description="observed - threshold (>=0 means crossed)")
    distance_to_trigger: float = Field(..., description=">0 means below trigger")
    rationale: str


class ExposureBreakdown(BaseModel):
    livelihood: str
    population: int


class ImpactEstimate(BaseModel):
    admin_id: str
    total_population_exposed: int
    by_livelihood: list[ExposureBreakdown] = []
    method: str
    sources: list[Provenance] = []


class EvidenceLink(BaseModel):
    step: str
    detail: str
    source: str | None = None


class Recommendation(BaseModel):
    rank: int
    action: str
    lead_time_days: int
    cost_band: str
    actor: str
    window: str
    evidence: list[EvidenceLink] = []


class Message(BaseModel):
    audience: str
    language: str
    channel: str
    admin_id: str
    text: str
    sms_segments: list[str] = []
    voice_script: str = ""
    valid_until: str | None = None
