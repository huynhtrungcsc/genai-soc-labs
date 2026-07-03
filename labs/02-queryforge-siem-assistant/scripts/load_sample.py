from app.schemas import QueryRequest
from app.services.executor import execute_against_sample
from app.storage.sqlite import attach_execution, create_query_job, init_db


def main() -> None:
    init_db()
    job = create_query_job(
        QueryRequest(
            question="Có máy nào trong phòng kế toán kết nối ra IP lạ ở nước ngoài trong 24h qua không?",
            dialect="splunk",
            time_range="24h",
            data_source="security_events",
        )
    )
    attach_execution(job, execute_against_sample(job))
    print(f"Loaded sample query: {job.id}")


if __name__ == "__main__":
    main()
