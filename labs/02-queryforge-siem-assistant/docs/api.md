# API

Base URL: `http://localhost:8002/api`

All query endpoints use HTTP Basic authentication. Service integrations may also use the
`X-API-Key` header.

Demo credentials:

```text
hunter / queryforge-demo
```

## Endpoints

- `GET /health`
- `GET /ready`
- `GET /schema`
- `GET /queries`
- `POST /queries`
- `GET /queries/{job_id}`
- `POST /queries/{job_id}/approve`
- `POST /queries/{job_id}/execute`
- `GET /queries/{job_id}/audit`

Interactive OpenAPI docs are available at `/docs`.

## Example Request

```json
{
  "question": "Trong 24h qua, có máy nào trong phòng kế toán kết nối ra IP lạ ở nước ngoài không?",
  "dialect": "splunk",
  "time_range": "24h",
  "data_source": "security_events"
}
```

Supported dialects:

- `splunk`
- `sentinel`
- `elastic`
