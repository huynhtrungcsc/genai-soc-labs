from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

SiemDialect = Literal["splunk", "sentinel", "elastic"]
TimeRange = Literal["15m", "1h", "24h", "7d", "30d"]


class QueryRequest(BaseModel):
    question: str = Field(min_length=8, max_length=500)
    dialect: SiemDialect = "splunk"
    time_range: TimeRange = "24h"
    data_source: str = Field(default="security_events", max_length=80)


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
    generated: GeneratedQuery
    execution: ExecutionResult | None = None
    created_at: datetime
    updated_at: datetime


class QueryJobListItem(BaseModel):
    id: str
    question: str
    dialect: SiemDialect
    time_range: TimeRange
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
