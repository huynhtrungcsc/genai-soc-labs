from app.schemas import QueryRequest
from app.services.executor import execute_against_sample
from app.storage.sqlite import approve_query_job, attach_execution, create_query_job, init_db


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
    approved = approve_query_job(job, "sample-loader")
    attach_execution(approved, execute_against_sample(approved))
    print(f"Loaded sample query: {job.id}")


if __name__ == "__main__":
    main()
