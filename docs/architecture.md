# Architecture

This repository uses a monorepo layout so the 29 labs share a consistent engineering standard while remaining easy to browse individually.

## Target Pattern

A completed lab should generally contain:

- Frontend: analyst-facing web UI
- Backend: FastAPI or equivalent service layer
- Data adapters: log, feed, file, or API ingestion
- LLM layer: prompt orchestration, tool calling, and guardrails
- Retrieval layer: vector search or structured retrieval when needed
- Evaluation: test cases, golden outputs, and failure analysis
- Deployment: Docker-based local run and hosted demo when appropriate

## Shared Components

The `shared/` directory is reserved for reusable components that multiple labs can adopt later:

- Authentication and role-based access control patterns
- RAG helpers
- Security data parsers
- Evaluation utilities
- UI primitives
- Synthetic dataset generators

## Design Priorities

The labs should prioritize analyst trust:

- Show evidence and source references where possible
- Separate facts from model inference
- Make model uncertainty visible
- Require human approval for disruptive response actions
- Keep sensitive logs and credentials out of public artifacts
