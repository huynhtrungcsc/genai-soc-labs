from app.schemas import GeneratedQuery, QueryRequest, ValidationMessage
from app.services.intent import Intent, department_filter, detect_intents


def generate_query(payload: QueryRequest) -> GeneratedQuery:
    intents = detect_intents(payload.question)
    department = department_filter(payload.question)
    validations = _validate(payload, intents)
    query = _render_query(payload, intents, department)
    return GeneratedQuery(
        dialect=payload.dialect,
        query=query,
        explanation=_explain(payload, intents, department),
        assumptions=_assumptions(payload, department),
        validations=validations,
        next_questions=_next_questions(intents),
        risk_level=_risk_level(payload, len(intents)),
        estimated_cost=_estimated_cost(payload, len(intents)),
        requires_review=_requires_review(payload, len(intents)),
    )


def _render_query(payload: QueryRequest, intents: list[Intent], department: str | None) -> str:
    if payload.dialect == "splunk":
        return _render_spl(payload, intents, department)
    if payload.dialect == "sentinel":
        return _render_kql(payload, intents, department)
    return _render_elastic(payload, intents, department)


def _render_spl(payload: QueryRequest, intents: list[Intent], department: str | None) -> str:
    conditions = _spl_conditions(intents, department)
    return (
        f"index={payload.data_source} earliest=-{payload.time_range} "
        f"| search {' AND '.join(conditions)} "
        "| stats count min(timestamp) as first_seen max(timestamp) as last_seen "
        "by host user src_ip dst_ip country action severity "
        "| sort - count"
    )


def _render_kql(payload: QueryRequest, intents: list[Intent], department: str | None) -> str:
    conditions = _kql_conditions(intents, department)
    return "\n".join(
        [
            payload.data_source,
            f"| where timestamp >= ago({_kql_time(payload.time_range)})",
            f"| where {' and '.join(conditions)}",
            "| summarize count(), first_seen=min(timestamp), last_seen=max(timestamp) "
            "by host, user, src_ip, dst_ip, country, action, severity",
            "| order by count_ desc",
        ]
    )


def _render_elastic(payload: QueryRequest, intents: list[Intent], department: str | None) -> str:
    conditions = _elastic_conditions(intents, department)
    return " and ".join([f"@timestamp >= now-{payload.time_range}", *conditions])


def _spl_conditions(intents: list[Intent], department: str | None) -> list[str]:
    actions = ",".join(f'"{term}"' for intent in intents for term in intent.action_terms)
    conditions = [f"action IN ({actions})"]
    if any(intent.name == "foreign_outbound" for intent in intents):
        conditions.append('country!="VN"')
    if department:
        conditions.append(f"department={department}")
    return conditions


def _kql_conditions(intents: list[Intent], department: str | None) -> list[str]:
    actions = ", ".join(f'"{term}"' for intent in intents for term in intent.action_terms)
    conditions = [f"action in ({actions})"]
    if any(intent.name == "foreign_outbound" for intent in intents):
        conditions.append('country != "VN"')
    if department:
        conditions.append(f'department == "{department}"')
    return conditions


def _elastic_conditions(intents: list[Intent], department: str | None) -> list[str]:
    action_terms = " or ".join(
        f'action:"{term}"' for intent in intents for term in intent.action_terms
    )
    conditions = [f"({action_terms})"]
    if any(intent.name == "foreign_outbound" for intent in intents):
        conditions.append('not country:"VN"')
    if department:
        conditions.append(f'department:"{department}"')
    return conditions


def _validate(payload: QueryRequest, intents: list[Intent]) -> list[ValidationMessage]:
    messages = [
        ValidationMessage(
            severity="info",
            message=(
                "Generated query is a draft. Review field names before running "
                "in production SIEM."
            ),
        )
    ]
    if payload.time_range in {"7d", "30d"}:
        messages.append(
            ValidationMessage(
                severity="warning",
                message="Long time range may be expensive. Consider narrowing scope during triage.",
            )
        )
    if payload.max_rows > 1000:
        messages.append(
            ValidationMessage(
                severity="warning",
                message="Large result limit may expose too much data. Confirm business need.",
            )
        )
    if len(intents) > 2:
        messages.append(
            ValidationMessage(
                severity="warning",
                message="Multiple intents were detected. Validate boolean logic before execution.",
            )
        )
    return messages


def _explain(payload: QueryRequest, intents: list[Intent], department: str | None) -> list[str]:
    lines = [
        f"Targets the {payload.data_source} data source for the last {payload.time_range}.",
        *[intent.explanation for intent in intents],
    ]
    if department:
        lines.append(
            f"Limits results to the {department} department based on the question context."
        )
    lines.append(
        "Aggregates by host, user, source IP, destination IP, country, action, and severity."
    )
    return lines


def _assumptions(payload: QueryRequest, department: str | None) -> list[str]:
    assumptions = [
        f"`{payload.data_source}` contains normalized fields from the documented schema.",
        "Timestamps are stored in UTC.",
        "Country enrichment is already available on network events.",
    ]
    if department:
        assumptions.append("Department context is available as a normalized field.")
    return assumptions


def _next_questions(intents: list[Intent]) -> list[str]:
    questions: list[str] = []
    for intent in intents:
        questions.extend(intent.next_questions)
    questions.append("Which events should be escalated to an incident case?")
    return list(dict.fromkeys(questions))[:6]


def _kql_time(time_range: str) -> str:
    return {"15m": "15m", "1h": "1h", "24h": "24h", "7d": "7d", "30d": "30d"}[time_range]


def _risk_level(payload: QueryRequest, intent_count: int) -> str:
    if payload.time_range == "30d" or payload.max_rows > 1000 or intent_count > 2:
        return "high"
    if payload.time_range == "7d" or payload.max_rows > 500:
        return "medium"
    return "low"


def _estimated_cost(payload: QueryRequest, intent_count: int) -> str:
    if payload.time_range in {"15m", "1h"} and intent_count <= 1:
        return "low - narrow time window and focused predicate"
    if payload.time_range in {"24h", "7d"}:
        return "medium - validate index/table size before production execution"
    return "high - long lookback window can be expensive in production SIEM"


def _requires_review(payload: QueryRequest, intent_count: int) -> bool:
    return payload.time_range in {"7d", "30d"} or payload.max_rows > 1000 or intent_count > 2
