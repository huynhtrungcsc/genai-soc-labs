<div align="center">

# QueryForge

Natural language SIEM query assistant for SOC threat hunting workflows.

[![Python](https://img.shields.io/badge/Python-3.11%2B-1f2937.svg)](pyproject.toml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-1d4ed8.svg)](backend/app/main.py)
[![Dialects](https://img.shields.io/badge/SIEM-SPL%20%7C%20KQL%20%7C%20Elastic-334155.svg)](docs/api.md)
[![Storage](https://img.shields.io/badge/Storage-SQLite-0f766e.svg)](backend/app/storage/sqlite.py)

[Quick Start](#quick-start) · [Features](#features) · [Architecture](docs/architecture.md) · [API](docs/api.md) · [Evaluation](docs/evaluation.md)

</div>

---

## Overview

QueryForge converts natural language threat hunting questions into SIEM-ready queries. It supports Splunk SPL, Microsoft Sentinel KQL, and Elastic KQL, then explains the generated query so an analyst can verify field logic before execution.

This first implementation is deterministic and enterprise-practical: it includes authentication, persistence, query history, validation warnings, sample execution, documentation, and tests. It does not require an external LLM key, but the architecture is ready for an LLM/RAG query planner later.

## Features

- Browser UI served by FastAPI
- HTTP Basic demo authentication
- API key authentication for service-to-service integration
- Natural language question intake in Vietnamese or English
- SPL, Sentinel KQL, and Elastic KQL rendering
- Query explanation, assumptions, and validation warnings
- Query governance with draft, approved, and executed states
- Risk level and estimated SIEM execution cost
- Approval gate before execution
- Audit trail for create, approve, and execute actions
- Suggested follow-up hunts
- SQLite query history
- Local execution against synthetic normalized SOC events
- API docs and schema catalog
- Pytest coverage for generator, executor, and API workflow
- Dockerfile and Docker Compose support

## Quick Start

```bash
cd labs/02-queryforge-siem-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make dev
```

Open:

```text
http://localhost:8002
```

Demo credentials:

```text
hunter / queryforge-demo
```

API docs:

```text
http://localhost:8002/docs
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
02-queryforge-siem-assistant/
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
    events/
  docs/
  tests/
  Dockerfile
  docker-compose.yml
  pyproject.toml
```

## Workflow

1. A hunter asks a question such as: “Trong 24h qua, có máy nào trong phòng kế toán kết nối ra IP lạ ở nước ngoài không?”
2. QueryForge detects hunt intent, target SIEM dialect, time range, and business context.
3. It generates a SIEM query and explains every major clause.
4. It estimates risk/cost and warns when assumptions need analyst review.
5. A reviewer approves the query before execution.
6. It executes against synthetic normalized SOC events to demonstrate the full workflow.
7. It stores query history and audit events for reuse and improvement.

## API Summary

- `GET /api/health`
- `GET /api/ready`
- `GET /api/schema`
- `GET /api/queries`
- `POST /api/queries`
- `GET /api/queries/{job_id}`
- `POST /api/queries/{job_id}/approve`
- `POST /api/queries/{job_id}/execute`
- `GET /api/queries/{job_id}/audit`

All query endpoints require demo hunter credentials or the `X-API-Key` header.

## Original Brief

### AI Trợ Lý Truy Vấn Log Bằng Ngôn Ngữ Tự Nhiên — Hỏi SIEM Như Hỏi Người

Threat hunter muốn hỏi 'có máy nào trong dải mạng kế toán kết nối ra IP lạ ở nước ngoài trong 24h qua không' nhưng phải viết query SPL/KQL/Lucene phức tạp — rào cản cú pháp làm chậm điều tra và loại bỏ những người giỏi về bảo mật nhưng không thạo query language. Bài toán: AI chuyển câu hỏi tiếng Việt/Anh thành truy vấn SIEM đúng cú pháp, giải thích query sinh ra để analyst kiểm chứng, chạy và trình bày kết quả dễ đọc, gợi ý các câu hỏi điều tra tiếp theo dựa trên kết quả, và học từ các truy vấn đã dùng. Hạ thấp rào cản threat hunting cho cả đội SOC.

## Reference Stack

OpenAI/Claude, Splunk/Elastic/Sentinel API, text-to-query, FastAPI, Next.js

This implementation starts with FastAPI, SQLite, deterministic query generation, and a static analyst UI. It is designed so real SIEM connectors and LLM/RAG planning can be added without changing the core workflow.

## Security Notes

- Treat generated queries as analyst drafts, not final truth.
- Validate field names and index/table names before running against production SIEM.
- Avoid broad time ranges during incident response unless cost and performance are understood.
- Do not commit real SIEM credentials, API tokens, customer logs, or private detections.

## Roadmap

- Add OpenAI/Claude provider with strict schema-grounded query generation.
- Add real Splunk, Microsoft Sentinel, and Elastic connector interfaces.
- Add saved hunt packs and approval workflow.
- Add user roles and team-level query library.
- Add field mapping import from customer SIEM schema exports.
