from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse

from app.core.security import require_analyst
from app.schemas import (
    AuditEvent,
    HealthResponse,
    Incident,
    IncidentCreate,
    IncidentListItem,
    IncidentStatusUpdate,
)
from app.services.analysis import analyze_incident
from app.storage.sqlite import (
    create_incident,
    get_incident,
    list_audit_events,
    list_incidents,
    record_audit,
    save_incident,
    update_incident_status,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="incidentlens")


@router.get("/ready", response_model=HealthResponse, tags=["system"])
def ready() -> HealthResponse:
    list_incidents()
    return HealthResponse(status="ready", service="incidentlens")


@router.get(
    "/incidents",
    response_model=list[IncidentListItem],
    tags=["incidents"],
)
def get_incidents(_: str = Depends(require_analyst)) -> list[IncidentListItem]:
    return [
        IncidentListItem(
            id=incident.id,
            title=incident.title,
            severity=incident.severity,
            status=incident.status,
            owner=incident.owner,
            created_at=incident.created_at,
            event_count=len(incident.events),
            mitre_count=len(incident.mitre),
            risk_score=incident.risk.score if incident.risk else None,
        )
        for incident in list_incidents()
    ]


@router.post(
    "/incidents",
    response_model=Incident,
    status_code=201,
    tags=["incidents"],
)
def post_incident(payload: IncidentCreate, actor: str = Depends(require_analyst)) -> Incident:
    incident = create_incident(payload)
    analyzed = analyze_incident(incident)
    save_incident(analyzed)
    record_audit(actor, "incident.created", analyzed.id, f"Created incident `{analyzed.title}`")
    return analyzed


@router.get(
    "/incidents/{incident_id}",
    response_model=Incident,
    tags=["incidents"],
)
def get_incident_by_id(incident_id: str, _: str = Depends(require_analyst)) -> Incident:
    incident = get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post(
    "/incidents/{incident_id}/analyze",
    response_model=Incident,
    tags=["analysis"],
)
def analyze_existing_incident(incident_id: str, actor: str = Depends(require_analyst)) -> Incident:
    incident = get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    analyzed = analyze_incident(incident)
    save_incident(analyzed)
    record_audit(
        actor,
        "incident.analyzed",
        analyzed.id,
        "Rebuilt timeline, MITRE, risk, and reports",
    )
    return analyzed


@router.patch(
    "/incidents/{incident_id}/status",
    response_model=Incident,
    tags=["incidents"],
)
def patch_incident_status(
    incident_id: str,
    payload: IncidentStatusUpdate,
    actor: str = Depends(require_analyst),
) -> Incident:
    incident = get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    updated = update_incident_status(incident, payload.status)
    record_audit(
        actor,
        "incident.status_changed",
        incident_id,
        f"Status changed to `{payload.status}`. {payload.note}".strip(),
    )
    return updated


@router.get(
    "/incidents/{incident_id}/audit",
    response_model=list[AuditEvent],
    tags=["audit"],
)
def get_incident_audit(
    incident_id: str,
    _: str = Depends(require_analyst),
) -> list[AuditEvent]:
    if not get_incident(incident_id):
        raise HTTPException(status_code=404, detail="Incident not found")
    return list_audit_events(incident_id)


@router.get(
    "/incidents/{incident_id}/report/{audience}",
    response_class=PlainTextResponse,
    tags=["reports"],
)
def get_report(incident_id: str, audience: str, actor: str = Depends(require_analyst)) -> str:
    incident = get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    if not incident.reports:
        incident = analyze_incident(incident)
        save_incident(incident)
    if audience == "technical":
        record_audit(actor, "report.viewed", incident_id, "Technical report viewed")
        return incident.reports.technical
    if audience == "executive":
        record_audit(actor, "report.viewed", incident_id, "Executive report viewed")
        return incident.reports.executive
    raise HTTPException(status_code=400, detail="Audience must be technical or executive")
