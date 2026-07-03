from fastapi import APIRouter, Depends, HTTPException

from app.core.security import require_hunter
from app.schemas import (
    HealthResponse,
    QueryJob,
    QueryJobListItem,
    QueryRequest,
    SchemaResponse,
)
from app.services.executor import execute_against_sample
from app.services.schema_catalog import get_schema
from app.storage.sqlite import (
    attach_execution,
    create_query_job,
    get_query_job,
    list_query_jobs,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="queryforge")


@router.get(
    "/schema",
    response_model=SchemaResponse,
    tags=["schema"],
    dependencies=[Depends(require_hunter)],
)
def schema() -> SchemaResponse:
    return get_schema()


@router.get(
    "/queries",
    response_model=list[QueryJobListItem],
    tags=["queries"],
    dependencies=[Depends(require_hunter)],
)
def get_queries() -> list[QueryJobListItem]:
    return [
        QueryJobListItem(
            id=job.id,
            question=job.question,
            dialect=job.dialect,
            time_range=job.time_range,
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
    dependencies=[Depends(require_hunter)],
)
def post_query(payload: QueryRequest) -> QueryJob:
    return create_query_job(payload)


@router.get(
    "/queries/{job_id}",
    response_model=QueryJob,
    tags=["queries"],
    dependencies=[Depends(require_hunter)],
)
def get_query(job_id: str) -> QueryJob:
    job = get_query_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Query job not found")
    return job


@router.post(
    "/queries/{job_id}/execute",
    response_model=QueryJob,
    tags=["execution"],
    dependencies=[Depends(require_hunter)],
)
def execute_query(job_id: str) -> QueryJob:
    job = get_query_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Query job not found")
    return attach_execution(job, execute_against_sample(job))
