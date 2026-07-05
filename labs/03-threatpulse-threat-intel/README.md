# ThreatPulse

AI-ready threat intelligence briefing platform for SOC, vulnerability management, and patch teams.

ThreatPulse ingests threat intelligence, maps it to internal assets, calculates relevance and remediation priority, and generates analyst-ready briefings with evidence, assumptions, action items, and approval workflow.

## What This Lab Demonstrates

- Threat intelligence ingestion with normalized CVE, IOC, MITRE, source, and product fields
- Asset-aware relevance scoring based on technology inventory, exposure, criticality, and exploitation status
- Deterministic briefing generation that can later be replaced with RAG/LLM orchestration
- Human approval gate before a briefing is treated as ready
- Basic authentication and API key support
- SQLite persistence, audit trail, sample data, tests, Docker, and local runbook

## Enterprise Workflow

```text
Threat feeds / advisories
        |
        v
Intel ingestion API
        |
        v
Asset exposure matching + relevance scoring
        |
        v
SOC / executive / patch briefing draft
        |
        v
Human review and approval
        |
        v
Patch queue, hunting tasks, and audit record
```

## Quick Start

```bash
cd labs/03-threatpulse-threat-intel
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make seed
make dev
```

Open:

```text
http://localhost:8003
```

Demo credentials:

```text
username: analyst
password: threatpulse-demo
```

API key header:

```text
X-API-Key: change-me-in-production
```

Smoke test while the server is running:

```bash
make smoke
```

## Core Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Service health |
| GET | `/api/ready` | Storage readiness |
| GET | `/api/assets` | List asset inventory |
| POST | `/api/assets` | Register one asset |
| POST | `/api/assets/bulk` | Register multiple assets |
| GET | `/api/intel` | List prioritized intelligence |
| POST | `/api/intel` | Ingest one intelligence item |
| POST | `/api/intel/reassess` | Recalculate relevance after inventory changes |
| POST | `/api/briefings/generate` | Generate SOC, executive, or patch briefing |
| POST | `/api/briefings/{id}/approve` | Approve a briefing |
| GET | `/api/audit` | Review governance events |

## Project Structure

```text
backend/
  app/
    api/
    core/
    services/
    storage/
frontend/
sample-data/
  assets/
  intel/
docs/
tests/
scripts/
```

## Operating Model

ThreatPulse is intentionally deterministic in this lab version. That makes evaluation, testing, and audit behavior reproducible. In a production GenAI build, the deterministic assessment layer should remain the control plane while an LLM/RAG layer drafts richer language with strict evidence citations and human review.

## Security Notes

- Use sanitized or synthetic intelligence and asset data only.
- Do not store secrets, customer logs, private incident data, or exploit instructions.
- Rotate `THREATPULSE_API_KEY` before any non-local deployment.
- Keep human approval for external or executive distribution.

## Documentation

- [API](docs/api.md)
- [Architecture](docs/architecture.md)
- [Evaluation](docs/evaluation.md)
