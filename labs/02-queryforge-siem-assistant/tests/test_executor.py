from app.schemas import QueryRequest
from app.services.executor import execute_against_sample
from app.storage.sqlite import create_query_job, init_db


def test_execute_against_sample_returns_finance_foreign_rows(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("QUERYFORGE_DATABASE_PATH", str(tmp_path / "queryforge.db"))
    init_db()
    job = create_query_job(
        QueryRequest(
            question="Trong 24h qua, phòng kế toán có kết nối ra IP lạ ở nước ngoài không?",
            dialect="splunk",
            time_range="24h",
            data_source="security_events",
        )
    )

    result = execute_against_sample(job)

    assert result.row_count >= 2
    assert all(row["country"] != "VN" for row in result.rows)
    assert any(row["host"] == "FIN-WS-014" for row in result.rows)
