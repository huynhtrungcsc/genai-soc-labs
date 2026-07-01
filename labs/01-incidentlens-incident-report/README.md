<div align="center">

# IncidentLens

AI-ready incident report assistant for SOC investigation workflows.

[![Python](https://img.shields.io/badge/Python-3.11%2B-1f2937.svg)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-0f766e.svg)](backend/app/main.py)
[![Storage](https://img.shields.io/badge/Storage-SQLite-334155.svg)](backend/app/storage/sqlite.py)
[![MITRE](https://img.shields.io/badge/MITRE-ATT%26CK-b91c1c.svg)](docs/architecture.md)

[Quick Start](#quick-start) · [Features](#features) · [Architecture](docs/architecture.md) · [API](docs/api.md) · [Evaluation](docs/evaluation.md)

</div>

---

## Overview

IncidentLens turns raw incident logs into a structured SOC investigation package:

- normalized security events
- attack timeline
- MITRE ATT&CK mapping
- technical incident report
- executive incident brief

This first version is deterministic and runs without an external LLM key. That keeps the lab reproducible for reviewers while preserving clean extension points for OpenAI, Claude, RAG, DOCX/PDF export, and enterprise auth later.

## Features

- Browser UI served by FastAPI
- HTTP Basic demo authentication
- JSONL and text log parsing
- SQLite persistence
- Timeline reconstruction by attack phase
- MITRE ATT&CK rule mapping
- Technical and executive Markdown reports
- Synthetic sample incident
- Pytest coverage for parser, analysis, and API workflow
- Dockerfile and Docker Compose support

## Quick Start

```bash
cd labs/01-incidentlens-incident-report
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make dev
```

Open:

```text
http://localhost:8001
```

Demo credentials:

```text
analyst / incidentlens-demo
```

API docs:

```text
http://localhost:8001/docs
```

## Docker

```bash
docker compose up --build
```

Docker is optional. The local Python path above is the fastest way to run the lab.

## Test

```bash
make test
make lint
```

## Repository Structure

```text
01-incidentlens-incident-report/
  backend/
    app/
      api/
      core/
      services/
      storage/
      main.py
  frontend/
    index.html
    styles.css
    app.js
  sample-data/
    incidents/
      acme-ransomware/
  docs/
  tests/
  Dockerfile
  docker-compose.yml
  pyproject.toml
```

## Workflow

1. The analyst creates an incident and pastes raw logs.
2. IncidentLens normalizes log lines into events.
3. Timeline rules group events into SOC investigation phases.
4. MITRE rules map evidence to ATT&CK techniques.
5. Reports separate technical detail from executive communication.

## API Summary

- `GET /api/health`
- `GET /api/incidents`
- `POST /api/incidents`
- `GET /api/incidents/{incident_id}`
- `POST /api/incidents/{incident_id}/analyze`
- `GET /api/incidents/{incident_id}/report/technical`
- `GET /api/incidents/{incident_id}/report/executive`

All incident endpoints require demo analyst credentials.

## Original Brief

### AI Tóm Tắt & Phân Tích Sự Cố Bảo Mật — Incident Report Tự Động Cho SOC

Sau một sự cố bảo mật, analyst phải tổng hợp log từ chục hệ thống, dựng timeline, viết báo cáo cho quản lý và khách hàng — mất nhiều giờ trong khi đồng hồ đang đếm, và mỗi người viết một kiểu khiến tri thức không tích lũy được. Bài toán: AI đọc log sự cố, dữ liệu điều tra và các alert liên quan, tự dựng timeline tấn công (initial access → lateral movement → impact), ánh xạ lên framework MITRE ATT&CK, sinh báo cáo sự cố chuẩn cho từng đối tượng đọc (kỹ thuật và lãnh đạo), và đề xuất biện pháp khắc phục. Giải phóng analyst khỏi việc viết lách cơ học để tập trung điều tra.

## Reference Stack

OpenAI/Claude, RAG MITRE ATT&CK, log parsing, python-docx, FastAPI, Next.js

This implementation starts with FastAPI, SQLite, deterministic analysis, and a static analyst UI. It is designed to accept LLM/RAG and export modules in later iterations without changing the core workflow.

## Security Notes

- Use synthetic or sanitized logs only.
- Do not commit real credentials, tokens, customer logs, or incident data.
- Treat model output as analyst support, not final truth.
- Keep human approval for containment, account lockout, firewall changes, or other disruptive actions.

## Roadmap

- Add OpenAI/Claude report generation with strict evidence grounding.
- Add local MITRE ATT&CK RAG.
- Add DOCX/PDF export.
- Add PostgreSQL and production auth.
- Add richer log adapters for Windows, EDR, firewall, Zeek, and SIEM exports.
