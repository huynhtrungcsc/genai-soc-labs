# QueryForge Architecture

QueryForge is a compact SIEM query assistant with one FastAPI service, one SQLite database, one static frontend, and a deterministic query generation engine.

```text
Browser
  -> FastAPI static frontend
  -> FastAPI JSON API
  -> Query generator
  -> Sample execution engine
  -> SQLite query history
```

## Data Flow

1. Hunter submits a natural language question.
2. Intent detection extracts the likely hunt objective.
3. Query rendering emits SPL, Sentinel KQL, or Elastic KQL.
4. Validation adds assumptions, warnings, and review notes.
5. Risk/cost estimation identifies broad or expensive hunts.
6. Approval gates execution.
7. Local execution filters synthetic events for an end-to-end demo.
8. Query history and audit events are stored for reuse and later improvement.

## Extension Points

- Add LLM provider behind the same `generate_query` contract.
- Replace synthetic execution with Splunk, Sentinel, or Elastic adapters.
- Import real schema catalogs from SIEM field discovery.
- Add role-based access and saved team hunt libraries.
- Add evaluation reports for query correctness and analyst usefulness.
- Add change control integration for production SIEM execution.

## Design Priorities

- Generated queries must be explainable.
- The app must separate assumptions from confirmed facts.
- Broad queries should emit cost and scope warnings.
- No production secrets or real customer data should be committed.
