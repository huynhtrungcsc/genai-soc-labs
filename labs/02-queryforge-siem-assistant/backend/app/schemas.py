from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

SiemDialect = Literal["splunk", "sentinel", "elastic"]
TimeRange = Literal["15m", "1h", "24h", "7d", "30d"]
QueryStatus = Literal["draft", "approved", "executed"]
RiskLevel = Literal["low", "medium", "high"]


class QueryRequest(BaseModel):
    question: str = Field(min_length=8, max_length=500)
    dialect: SiemDialect = "splunk"
    time_range: TimeRange = "24h"
    data_source: str = Field(default="security_events", max_length=80)
    owner: str = Field(default="soc-hunter", max_length=80)
    purpose: str = Field(default="threat_hunt", max_length=120)
    max_rows: int = Field(default=100, ge=1, le=10000)


class ApprovalRequest(BaseModel):
    approver: str = Field(min_length=2, max_length=80)
    note: str = Field(default="", max_length=1000)


class ValidationMessage(BaseModel):
    severity: Literal["info", "warning", "error"]
    message: str


class GeneratedQuery(BaseModel):
    dialect: SiemDialect
    query: str
    explanation: list[str]
    assumptions: list[str]
    validations: list[ValidationMessage]
    next_questions: list[str]
    risk_level: RiskLevel
    estimated_cost: str
    requires_review: bool


class ExecutionResult(BaseModel):
    row_count: int
    rows: list[dict[str, str]]
    summary: str


class QueryJob(BaseModel):
    id: str
    question: str
    dialect: SiemDialect
    time_range: TimeRange
    data_source: str
    owner: str
    purpose: str
    max_rows: int
    status: QueryStatus = "draft"
    approved_by: str | None = None
    approved_at: datetime | None = None
    generated: GeneratedQuery
    execution: ExecutionResult | None = None
    created_at: datetime
    updated_at: datetime


class QueryJobListItem(BaseModel):
    id: str
    question: str
    dialect: SiemDialect
    time_range: TimeRange
    status: QueryStatus
    owner: str
    row_count: int | None
    created_at: datetime


class HealthResponse(BaseModel):
    status: str
    service: str


class SchemaField(BaseModel):
    name: str
    type: str
    description: str


class SchemaResponse(BaseModel):
    fields: list[SchemaField]
    supported_dialects: list[SiemDialect]


class AuditEvent(BaseModel):
    id: str
    actor: str
    action: str
    target_id: str
    detail: str
    created_at: datetime
