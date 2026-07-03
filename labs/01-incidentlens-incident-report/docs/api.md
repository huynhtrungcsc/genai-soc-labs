# API

Base URL: `http://localhost:8001/api`

All incident endpoints use HTTP Basic authentication. Service integrations may also use
the `X-API-Key` header.

Demo credentials:

```text
analyst / incidentlens-demo
```

## Endpoints

- `GET /health`
- `GET /ready`
- `GET /incidents`
- `POST /incidents`
- `GET /incidents/{incident_id}`
- `POST /incidents/{incident_id}/analyze`
- `PATCH /incidents/{incident_id}/status`
- `GET /incidents/{incident_id}/audit`
- `GET /incidents/{incident_id}/report/technical`
- `GET /incidents/{incident_id}/report/executive`

Interactive OpenAPI docs are available at `/docs`.
