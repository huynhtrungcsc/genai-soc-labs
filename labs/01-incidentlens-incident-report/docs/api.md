# API

Base URL: `http://localhost:8001/api`

All incident endpoints use HTTP Basic authentication.

Demo credentials:

```text
analyst / incidentlens-demo
```

## Endpoints

- `GET /health`
- `GET /incidents`
- `POST /incidents`
- `GET /incidents/{incident_id}`
- `POST /incidents/{incident_id}/analyze`
- `GET /incidents/{incident_id}/report/technical`
- `GET /incidents/{incident_id}/report/executive`

Interactive OpenAPI docs are available at `/docs`.
