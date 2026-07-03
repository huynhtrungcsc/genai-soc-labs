from fastapi import APIRouter, Depends, HTTPException

from app.core.security import require_hunter
from app.schemas import (
    ApprovalRequest,
    AuditEvent,
    HealthResponse,
    QueryJob,
    QueryJobListItem,
    QueryRequest,
    SchemaResponse,
)
from app.services.executor import execute_against_sample
from app.services.schema_catalog import get_schema
from app.storage.sqlite import (
    approve_query_job,
    attach_execution,
    create_query_job,
    get_query_job,
    list_audit_events,
    list_query_jobs,
    record_audit,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="queryforge")


@router.get("/ready", response_model=HealthResponse, tags=["system"])
def ready() -> HealthResponse:
    list_query_jobs()
    return HealthResponse(status="ready", service="queryforge")


@router.get(
    "/schema",
    response_model=SchemaResponse,
    tags=["schema"],
)
def schema(_: str = Depends(require_hunter)) -> SchemaResponse:
    return get_schema()


@router.get(
    "/queries",
    response_model=list[QueryJobListItem],
    tags=["queries"],
)
def get_queries(_: str = Depends(require_hunter)) -> list[QueryJobListItem]:
    return [
        QueryJobListItem(
            id=job.id,
            question=job.question,
            dialect=job.dialect,
            time_range=job.time_range,
            status=job.status,
            owner=job.owner,
            row_count=job.execution.row_count if job.execution else None,
            created_at=job.created_at,
        )
        for job in list_query_jobs()
    ]


@router.post(
    "/queries",
    response_model=QueryJob,
    status_code=201,
    tags=["queries"],
)
def post_query(payload: QueryRequest, actor: str = Depends(require_hunter)) -> QueryJob:
    job = create_query_job(payload)
    record_audit(actor, "query.created", job.id, f"Created {job.dialect} query draft")
    return job


@router.get(
    "/queries/{job_id}",
    response_model=QueryJob,
    tags=["queries"],
)
def get_query(job_id: str, _: str = Depends(require_hunter)) -> QueryJob:
    job = get_query_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Query job not found")
    return job


@router.post(
    "/queries/{job_id}/approve",
    response_model=QueryJob,
    tags=["governance"],
)
def approve_query(
    job_id: str,
    payload: ApprovalRequest,
    actor: str = Depends(require_hunter),
) -> QueryJob:
    job = get_query_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Query job not found")
    approved = approve_query_job(job, payload.approver)
    record_audit(
        actor,
        "query.approved",
        job_id,
        f"Approved by `{payload.approver}`. {payload.note}".strip(),
    )
    return approved


@router.post(
    "/queries/{job_id}/execute",
    response_model=QueryJob,
    tags=["execution"],
)
def execute_query(job_id: str, actor: str = Depends(require_hunter)) -> QueryJob:
    job = get_query_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Query job not found")
    if job.status not in {"approved", "executed"}:
        raise HTTPException(status_code=409, detail="Query must be approved before execution")
    executed = attach_execution(job, execute_against_sample(job))
    record_audit(actor, "query.executed", job_id, "Executed against synthetic SOC dataset")
    return executed


@router.get(
    "/queries/{job_id}/audit",
    response_model=list[AuditEvent],
    tags=["audit"],
)
def get_query_audit(job_id: str, _: str = Depends(require_hunter)) -> list[AuditEvent]:
    if not get_query_job(job_id):
        raise HTTPException(status_code=404, detail="Query job not found")
    return list_audit_events(job_id)
