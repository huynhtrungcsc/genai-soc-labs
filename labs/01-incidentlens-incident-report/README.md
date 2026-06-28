# 01 · IncidentLens: AI Incident Report Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `IncidentLens`
- Lab focus: AI Incident Report Assistant
- Portfolio track: Flagship SOC track
- Domain: Security — Incident Response
- Method: LLM + RAG
- Difficulty level: 2

## Original Brief

### AI Tóm Tắt & Phân Tích Sự Cố Bảo Mật — Incident Report Tự Động Cho SOC

Sau một sự cố bảo mật, analyst phải tổng hợp log từ chục hệ thống, dựng timeline, viết báo cáo cho quản lý và khách hàng — mất nhiều giờ trong khi đồng hồ đang đếm, và mỗi người viết một kiểu khiến tri thức không tích lũy được. Bài toán: AI đọc log sự cố, dữ liệu điều tra và các alert liên quan, tự dựng timeline tấn công (initial access → lateral movement → impact), ánh xạ lên framework MITRE ATT&CK, sinh báo cáo sự cố chuẩn cho từng đối tượng đọc (kỹ thuật và lãnh đạo), và đề xuất biện pháp khắc phục. Giải phóng analyst khỏi việc viết lách cơ học để tập trung điều tra.

## Reference Stack

OpenAI/Claude, RAG MITRE ATT&CK, log parsing, python-docx, FastAPI, Next.js

## Minimum Acceptance Criteria

Yêu cầu tối thiểu: sản phẩm web/app hoàn chỉnh — deployed online (có URL truy cập), đăng nhập & phân quyền cơ bản, giao diện UI/UX hoàn chỉnh, quản lý user. Không chấp nhận: demo notebook, script CLI, prototype chỉ chạy localhost.

## Planned Product Shape

This lab should eventually become a complete analyst-facing web application with:

- Clean workflow-oriented UI
- Backend API for ingestion, orchestration, and persistence
- Authentication and basic role-based access control
- Sample or synthetic data suitable for public release
- Documented model prompts, retrieval strategy, and limitations
- Evaluation cases for output quality and safety
- Deployment notes and screenshots

## Suggested Future Structure

```text
01-incidentlens-incident-report/
  README.md
  backend/
  frontend/
  sample-data/
  evals/
  docs/
  docker-compose.yml
```

## Responsible Use Notes

This lab is intended for defensive security, authorized operations, and educational use. Do not add real secrets, private customer data, exploit automation, or instructions that enable unauthorized activity.
