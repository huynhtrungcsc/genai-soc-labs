# Architecture

ThreatPulse is built as a small but production-shaped SOC application.

## Components

| Component | Responsibility |
|---|---|
| FastAPI API | Authenticated JSON API for assets, intel, briefings, and audit |
| SQLite storage | Local persistence for demo and portfolio deployment |
| Scoring service | Deterministic asset matching, priority, SLA, and action generation |
| Briefing service | Audience-specific briefing assembly |
| Static frontend | Analyst dashboard for queue review and approval workflow |
| Sample data | Synthetic asset inventory and threat intelligence feed |

## Data Model

```text
AssetRecord
  hostname
  criticality
  technologies
  internet_exposed
  data_classification

IntelRecord
  source
  title
  cves
  iocs
  affected_products
  mitre_techniques
  assessment

Briefing
  audience
  status
  top_priorities
  patch_queue
  sections
```

## Assessment Logic

The scoring service combines:

- Source severity
- Source confidence
- Source reliability
- Observed exploitation
- CVE count
- Product match against asset technologies
- Asset criticality
- Internet exposure
- Sensitive data classification
- Industry relevance

The result is a reproducible `relevance_score`, `priority`, patch SLA, and action list.

## GenAI Extension Point

The lab deliberately keeps the control plane deterministic. A production LLM/RAG layer can be added after scoring:

1. Retrieve source advisories, vendor notes, and internal runbooks.
2. Build a prompt with only selected evidence and asset matches.
3. Generate draft language for each briefing section.
4. Validate citations, facts, and assumptions.
5. Require human approval before distribution.

This keeps AI output constrained by evidence instead of allowing free-form threat claims.
