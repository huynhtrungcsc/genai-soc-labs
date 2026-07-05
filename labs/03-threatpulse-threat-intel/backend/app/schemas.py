from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

Severity = Literal["low", "medium", "high", "critical"]
Confidence = Literal["low", "medium", "high"]
Priority = Literal["low", "medium", "high", "critical"]
Audience = Literal["executive", "soc", "patch"]
BriefingStatus = Literal["draft", "approved"]


class HealthResponse(BaseModel):
    status: str
    service: str


class OrganizationProfile(BaseModel):
    name: str = "Northstar Financial"
    industry: str = "financial-services"
    risk_appetite: str = "low"
    crown_jewels: list[str] = Field(default_factory=list)
    required_briefing_cadence: str = "daily"


class AssetRequest(BaseModel):
    hostname: str = Field(min_length=2, max_length=120)
    owner: str = Field(default="security-operations", max_length=120)
    business_unit: str = Field(default="shared-services", max_length=120)
    environment: str = Field(default="production", max_length=80)
    criticality: int = Field(default=3, ge=1, le=5)
    technologies: list[str] = Field(default_factory=list, max_length=30)
    internet_exposed: bool = False
    data_classification: str = Field(default="internal", max_length=80)
    tags: list[str] = Field(default_factory=list, max_length=30)

    @field_validator("technologies", "tags")
    @classmethod
    def normalize_list(cls, values: list[str]) -> list[str]:
        return sorted({value.strip() for value in values if value.strip()})


class AssetRecord(AssetRequest):
    id: str
    created_at: datetime
    updated_at: datetime


class IntelRequest(BaseModel):
    source: str = Field(min_length=2, max_length=120)
    title: str = Field(min_length=8, max_length=240)
    summary: str = Field(min_length=20, max_length=2000)
    affected_products: list[str] = Field(default_factory=list, max_length=40)
    industries: list[str] = Field(default_factory=list, max_length=20)
    cves: list[str] = Field(default_factory=list, max_length=30)
    iocs: list[str] = Field(default_factory=list, max_length=80)
    mitre_techniques: list[str] = Field(default_factory=list, max_length=30)
    references: list[HttpUrl] = Field(default_factory=list, max_length=20)
    observed_exploitation: bool = False
    severity: Severity = "medium"
    confidence: Confidence = "medium"
    source_reliability: Literal["A", "B", "C", "D"] = "B"
    published_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator(
        "affected_products",
        "industries",
        "cves",
        "iocs",
        "mitre_techniques",
        mode="after",
    )
    @classmethod
    def normalize_values(cls, values: list[str]) -> list[str]:
        return sorted({value.strip() for value in values if value.strip()})


class AffectedAsset(BaseModel):
    asset_id: str
    hostname: str
    matched_technologies: list[str]
    exposure_reasons: list[str]
    risk_score: int = Field(ge=0, le=100)
    priority: Priority
    patch_sla: str
    rationale: str


class IntelAssessment(BaseModel):
    relevance_score: int = Field(ge=0, le=100)
    priority: Priority
    analyst_summary: str
    executive_summary: str
    affected_assets: list[AffectedAsset]
    recommended_actions: list[str]
    evidence: list[str]
    assumptions: list[str]
    tags: list[str]


class IntelRecord(IntelRequest):
    id: str
    assessment: IntelAssessment
    created_at: datetime
    updated_at: datetime


class IntelListItem(BaseModel):
    id: str
    title: str
    source: str
    severity: Severity
    priority: Priority
    relevance_score: int
    affected_asset_count: int
    observed_exploitation: bool
    published_at: datetime
    created_at: datetime


class BriefingRequest(BaseModel):
    audience: Audience = "soc"
    lookback_days: int = Field(default=7, ge=1, le=90)
    max_items: int = Field(default=5, ge=1, le=20)
    owner: str = Field(default="threat-intel", max_length=120)


class BriefingSection(BaseModel):
    intel_id: str
    title: str
    priority: Priority
    summary: str
    affected_assets: list[str]
    evidence: list[str]
    recommended_actions: list[str]


class Briefing(BaseModel):
    id: str
    audience: Audience
    status: BriefingStatus = "draft"
    owner: str
    title: str
    top_priorities: list[str]
    patch_queue: list[str]
    sections: list[BriefingSection]
    limitations: list[str]
    generated_at: datetime
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ApprovalRequest(BaseModel):
    approver: str = Field(min_length=2, max_length=120)
    note: str = Field(default="", max_length=1000)


class AuditEvent(BaseModel):
    id: str
    actor: str
    action: str
    target_id: str
    detail: str
    created_at: datetime
