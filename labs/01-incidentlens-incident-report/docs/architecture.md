# IncidentLens Architecture

IncidentLens is intentionally compact: one FastAPI service, one SQLite database, and one static frontend served by the API.

```text
Browser
  -> FastAPI static frontend
  -> FastAPI JSON API
  -> SQLite persistence
  -> Parser, timeline, MITRE, report services
```

## Data Flow

1. Analyst creates an incident with raw logs.
2. The parser normalizes JSONL or text logs into security events.
3. Timeline rules group events into attack phases.
4. MITRE rules map observations to ATT&CK techniques.
5. Report generation creates technical and executive Markdown reports.
6. The UI renders metrics, timeline, mapping, and reports.

## Extension Points

- Replace deterministic report generation with an LLM provider.
- Add MITRE ATT&CK retrieval from a local knowledge base.
- Add PostgreSQL for multi-user deployments.
- Add SSO or OIDC for enterprise authentication.
- Add DOCX/PDF export for incident distribution.
