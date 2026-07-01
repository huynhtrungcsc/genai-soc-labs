from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high", "critical"]


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    severity: Severity = "medium"
    summary: str = Field(default="", max_length=2000)
    raw_logs: str = Field(min_length=5)


class NormalizedEvent(BaseModel):
    timestamp: datetime | None = None
    source: str = "unknown"
    host: str = "unknown"
    user: str = "unknown"
    action: str = "observed"
    src_ip: str | None = None
    dst_ip: str | None = None
    raw_message: str


class TimelineStep(BaseModel):
    phase: str
    timestamp: datetime | None = None
    title: str
    evidence: list[str]
    inference: str
    confidence: float = Field(ge=0, le=1)


class MitreTechnique(BaseModel):
    tactic: str
    technique_id: str
    technique: str
    evidence: list[str]
    confidence: float = Field(ge=0, le=1)


class ReportBundle(BaseModel):
    technical: str
    executive: str


class Incident(BaseModel):
    id: str
    title: str
    severity: Severity
    summary: str
    created_at: datetime
    updated_at: datetime
    raw_logs: str
    events: list[NormalizedEvent] = []
    timeline: list[TimelineStep] = []
    mitre: list[MitreTechnique] = []
    reports: ReportBundle | None = None


class IncidentListItem(BaseModel):
    id: str
    title: str
    severity: Severity
    created_at: datetime
    event_count: int
    mitre_count: int


class HealthResponse(BaseModel):
    status: str
    service: str
