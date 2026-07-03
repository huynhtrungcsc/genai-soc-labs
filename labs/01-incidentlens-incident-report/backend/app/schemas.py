from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high", "critical"]
IncidentStatus = Literal["new", "triage", "investigating", "contained", "closed"]
TaskStatus = Literal["open", "in_progress", "done", "waived"]


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    severity: Severity = "medium"
    summary: str = Field(default="", max_length=2000)
    raw_logs: str = Field(min_length=5)
    owner: str = Field(default="soc-tier1", max_length=80)
    environment: str = Field(default="production", max_length=80)
    business_impact: str = Field(default="", max_length=1000)
    affected_assets: list[str] = []
    tags: list[str] = []


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus
    note: str = Field(default="", max_length=1000)


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


class DataQualityFinding(BaseModel):
    severity: Literal["info", "warning", "error"]
    field: str
    message: str


class RiskAssessment(BaseModel):
    score: int = Field(ge=0, le=100)
    level: Severity
    drivers: list[str]
    recommended_sla: str


class ResponseTask(BaseModel):
    id: str
    title: str
    owner_role: str
    status: TaskStatus = "open"
    rationale: str
    requires_approval: bool = True


class AuditEvent(BaseModel):
    id: str
    actor: str
    action: str
    target_id: str
    detail: str
    created_at: datetime


class Incident(BaseModel):
    id: str
    title: str
    severity: Severity
    status: IncidentStatus = "new"
    owner: str = "soc-tier1"
    environment: str = "production"
    summary: str
    business_impact: str = ""
    affected_assets: list[str] = []
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime
    raw_logs: str
    events: list[NormalizedEvent] = []
    timeline: list[TimelineStep] = []
    mitre: list[MitreTechnique] = []
    data_quality: list[DataQualityFinding] = []
    risk: RiskAssessment | None = None
    response_tasks: list[ResponseTask] = []
    reports: ReportBundle | None = None


class IncidentListItem(BaseModel):
    id: str
    title: str
    severity: Severity
    status: IncidentStatus
    owner: str
    created_at: datetime
    event_count: int
    mitre_count: int
    risk_score: int | None


class HealthResponse(BaseModel):
    status: str
    service: str
