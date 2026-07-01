from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse

from app.core.security import require_analyst
from app.schemas import HealthResponse, Incident, IncidentCreate, IncidentListItem
from app.services.analysis import analyze_incident
from app.storage.sqlite import create_incident, get_incident, list_incidents, save_incident

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="incidentlens")


@router.get(
    "/incidents",
    response_model=list[IncidentListItem],
    tags=["incidents"],
    dependencies=[Depends(require_analyst)],
)
def get_incidents() -> list[IncidentListItem]:
    return [
        IncidentListItem(
            id=incident.id,
            title=incident.title,
            severity=incident.severity,
            created_at=incident.created_at,
            event_count=len(incident.events),
            mitre_count=len(incident.mitre),
        )
        for incident in list_incidents()
    ]


@router.post(
    "/incidents",
    response_model=Incident,
    status_code=201,
    tags=["incidents"],
    dependencies=[Depends(require_analyst)],
)
def post_incident(payload: IncidentCreate) -> Incident:
    incident = create_incident(payload)
    analyzed = analyze_incident(incident)
    save_incident(analyzed)
    return analyzed


@router.get(
    "/incidents/{incident_id}",
    response_model=Incident,
    tags=["incidents"],
    dependencies=[Depends(require_analyst)],
)
def get_incident_by_id(incident_id: str) -> Incident:
    incident = get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post(
    "/incidents/{incident_id}/analyze",
    response_model=Incident,
    tags=["analysis"],
    dependencies=[Depends(require_analyst)],
)
def analyze_existing_incident(incident_id: str) -> Incident:
    incident = get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    analyzed = analyze_incident(incident)
    save_incident(analyzed)
    return analyzed


@router.get(
    "/incidents/{incident_id}/report/{audience}",
    response_class=PlainTextResponse,
    tags=["reports"],
    dependencies=[Depends(require_analyst)],
)
def get_report(incident_id: str, audience: str) -> str:
    incident = get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    if not incident.reports:
        incident = analyze_incident(incident)
        save_incident(incident)
    if audience == "technical":
        return incident.reports.technical
    if audience == "executive":
        return incident.reports.executive
    raise HTTPException(status_code=400, detail="Audience must be technical or executive")
