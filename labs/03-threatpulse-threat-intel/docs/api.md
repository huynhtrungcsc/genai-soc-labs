# ThreatPulse API

ThreatPulse exposes a FastAPI JSON API under `/api`.

## Authentication

Use either HTTP Basic authentication or the API key header.

```text
Authorization: Basic analyst:threatpulse-demo
X-API-Key: change-me-in-production
```

## Assets

`POST /api/assets`

```json
{
  "hostname": "vpn-edge-01",
  "owner": "network-security",
  "business_unit": "infrastructure",
  "environment": "production",
  "criticality": 5,
  "technologies": ["Ivanti Connect Secure", "Linux"],
  "internet_exposed": true,
  "data_classification": "internal",
  "tags": ["remote-access", "edge"]
}
```

## Intelligence

`POST /api/intel`

```json
{
  "source": "CISA KEV",
  "title": "Active exploitation reported for Ivanti Connect Secure gateway vulnerability",
  "summary": "Multiple organizations reported exploitation attempts against exposed appliances.",
  "affected_products": ["Ivanti Connect Secure"],
  "industries": ["financial-services"],
  "cves": ["CVE-2025-0282"],
  "iocs": ["198.51.100.77"],
  "mitre_techniques": ["T1190", "T1133"],
  "references": ["https://www.cisa.gov/known-exploited-vulnerabilities-catalog"],
  "observed_exploitation": true,
  "severity": "critical",
  "confidence": "high",
  "source_reliability": "A",
  "published_at": "2026-07-01T09:30:00+00:00"
}
```

The response includes:

- `assessment.relevance_score`
- `assessment.priority`
- `assessment.affected_assets`
- `assessment.recommended_actions`
- `assessment.evidence`
- `assessment.assumptions`

`POST /api/intel/reassess` recalculates all intelligence items against the current asset inventory.

`POST /api/intel/{id}/reassess` recalculates one intelligence item after inventory changes.

## Briefings

`POST /api/briefings/generate`

```json
{
  "audience": "soc",
  "lookback_days": 30,
  "max_items": 5,
  "owner": "threat-intel"
}
```

Supported audiences:

- `soc`
- `executive`
- `patch`

`POST /api/briefings/{id}/approve`

```json
{
  "approver": "soc-manager",
  "note": "Reviewed for daily SOC distribution"
}
```

## Audit

`GET /api/audit` returns all governance events.

`GET /api/audit/{target_id}` returns events for one asset, intelligence item, or briefing.
