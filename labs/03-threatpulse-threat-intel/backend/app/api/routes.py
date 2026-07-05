from fastapi import APIRouter, Depends, HTTPException

from app.core.security import require_analyst
from app.schemas import (
    ApprovalRequest,
    AssetRecord,
    AssetRequest,
    AuditEvent,
    Briefing,
    BriefingRequest,
    HealthResponse,
    IntelListItem,
    IntelRecord,
    IntelRequest,
    OrganizationProfile,
)
from app.storage.sqlite import (
    approve_briefing,
    bulk_create_assets,
    create_asset,
    create_briefing,
    create_intel_item,
    export_snapshot,
    get_asset,
    get_briefing,
    get_intel_item,
    list_assets,
    list_audit_events,
    list_briefings,
    list_intel_items,
    reassess_all_intel,
    reassess_intel_item,
    record_audit,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="threatpulse")


@router.get("/ready", response_model=HealthResponse, tags=["system"])
def ready() -> HealthResponse:
    list_assets()
    list_intel_items()
    return HealthResponse(status="ready", service="threatpulse")


@router.get("/organization/profile", response_model=OrganizationProfile, tags=["organization"])
def organization_profile(_: str = Depends(require_analyst)) -> OrganizationProfile:
    return OrganizationProfile(
        crown_jewels=["internet banking", "identity platform", "payment processing"],
    )


@router.get("/assets", response_model=list[AssetRecord], tags=["assets"])
def get_assets(_: str = Depends(require_analyst)) -> list[AssetRecord]:
    return list_assets()


@router.post("/assets", response_model=AssetRecord, status_code=201, tags=["assets"])
def post_asset(payload: AssetRequest, actor: str = Depends(require_analyst)) -> AssetRecord:
    asset = create_asset(payload)
    record_audit(actor, "asset.created", asset.id, f"Registered asset {asset.hostname}")
    return asset


@router.post("/assets/bulk", response_model=list[AssetRecord], status_code=201, tags=["assets"])
def post_assets_bulk(
    payload: list[AssetRequest],
    actor: str = Depends(require_analyst),
) -> list[AssetRecord]:
    assets = bulk_create_assets(payload)
    record_audit(actor, "asset.bulk_created", "assets", f"Registered {len(assets)} assets")
    return assets


@router.get("/assets/{asset_id}", response_model=AssetRecord, tags=["assets"])
def get_asset_by_id(asset_id: str, _: str = Depends(require_analyst)) -> AssetRecord:
    asset = get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.get("/intel", response_model=list[IntelListItem], tags=["intelligence"])
def get_intel(_: str = Depends(require_analyst)) -> list[IntelListItem]:
    return [
        IntelListItem(
            id=item.id,
            title=item.title,
            source=item.source,
            severity=item.severity,
            priority=item.assessment.priority,
            relevance_score=item.assessment.relevance_score,
            affected_asset_count=len(item.assessment.affected_assets),
            observed_exploitation=item.observed_exploitation,
            published_at=item.published_at,
            created_at=item.created_at,
        )
        for item in list_intel_items()
    ]


@router.post("/intel", response_model=IntelRecord, status_code=201, tags=["intelligence"])
def post_intel(payload: IntelRequest, actor: str = Depends(require_analyst)) -> IntelRecord:
    item = create_intel_item(payload)
    record_audit(
        actor,
        "intel.ingested",
        item.id,
        f"Ingested {item.source} item with {item.assessment.priority} priority",
    )
    return item


@router.get("/intel/{item_id}", response_model=IntelRecord, tags=["intelligence"])
def get_intel_by_id(item_id: str, _: str = Depends(require_analyst)) -> IntelRecord:
    item = get_intel_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Threat intelligence item not found")
    return item


@router.post("/intel/reassess", response_model=list[IntelRecord], tags=["intelligence"])
def post_intel_reassess(actor: str = Depends(require_analyst)) -> list[IntelRecord]:
    items = reassess_all_intel()
    record_audit(actor, "intel.reassessed", "intel", f"Reassessed {len(items)} items")
    return items


@router.post("/intel/{item_id}/reassess", response_model=IntelRecord, tags=["intelligence"])
def post_intel_reassess_by_id(
    item_id: str,
    actor: str = Depends(require_analyst),
) -> IntelRecord:
    item = get_intel_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Threat intelligence item not found")
    reassessed = reassess_intel_item(item)
    record_audit(
        actor,
        "intel.reassessed",
        item_id,
        f"Reassessed {item.title} as {reassessed.assessment.priority} priority",
    )
    return reassessed


@router.post("/briefings/generate", response_model=Briefing, status_code=201, tags=["briefings"])
def post_briefing(payload: BriefingRequest, actor: str = Depends(require_analyst)) -> Briefing:
    briefing = create_briefing(payload)
    record_audit(
        actor,
        "briefing.generated",
        briefing.id,
        f"Generated {briefing.audience} briefing with {len(briefing.sections)} sections",
    )
    return briefing


@router.get("/briefings", response_model=list[Briefing], tags=["briefings"])
def get_briefings(_: str = Depends(require_analyst)) -> list[Briefing]:
    return list_briefings()


@router.get("/briefings/{briefing_id}", response_model=Briefing, tags=["briefings"])
def get_briefing_by_id(briefing_id: str, _: str = Depends(require_analyst)) -> Briefing:
    briefing = get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing not found")
    return briefing


@router.post("/briefings/{briefing_id}/approve", response_model=Briefing, tags=["governance"])
def approve_briefing_by_id(
    briefing_id: str,
    payload: ApprovalRequest,
    actor: str = Depends(require_analyst),
) -> Briefing:
    briefing = get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing not found")
    approved = approve_briefing(briefing, payload.approver)
    record_audit(
        actor,
        "briefing.approved",
        briefing_id,
        f"Approved by {payload.approver}. {payload.note}".strip(),
    )
    return approved


@router.get("/audit", response_model=list[AuditEvent], tags=["audit"])
def get_audit(_: str = Depends(require_analyst)) -> list[AuditEvent]:
    return list_audit_events()


@router.get("/audit/{target_id}", response_model=list[AuditEvent], tags=["audit"])
def get_audit_for_target(target_id: str, _: str = Depends(require_analyst)) -> list[AuditEvent]:
    return list_audit_events(target_id)


@router.get("/export", response_model=dict[str, object], tags=["governance"])
def get_export(_: str = Depends(require_analyst)) -> dict[str, object]:
    return export_snapshot()
