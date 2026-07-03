from app.schemas import QueryRequest
from app.services.generator import generate_query


def test_vietnamese_finance_foreign_question_generates_splunk_query() -> None:
    generated = generate_query(
        QueryRequest(
            question=(
                "Có máy nào trong phòng kế toán kết nối ra IP lạ "
                "ở nước ngoài trong 24h qua không?"
            ),
            dialect="splunk",
            time_range="24h",
            data_source="security_events",
        )
    )

    assert "index=security_events" in generated.query
    assert 'country!="VN"' in generated.query
    assert "department=finance" in generated.query
    assert "action IN" in generated.query
    assert generated.risk_level == "low"
    assert generated.next_questions


def test_power_shell_question_generates_sentinel_kql() -> None:
    generated = generate_query(
        QueryRequest(
            question="Find suspicious PowerShell activity in the last hour",
            dialect="sentinel",
            time_range="1h",
            data_source="SecurityEvents",
        )
    )

    assert "SecurityEvents" in generated.query
    assert "ago(1h)" in generated.query
    assert "powershell" in generated.query.lower()


def test_long_range_emits_warning() -> None:
    generated = generate_query(
        QueryRequest(
            question="Show failed login events for the last month",
            dialect="elastic",
            time_range="30d",
            data_source="security-events-*",
        )
    )

    assert any(item.severity == "warning" for item in generated.validations)
    assert generated.requires_review is True
