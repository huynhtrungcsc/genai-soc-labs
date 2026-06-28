# 22 · RedReport: Defensive Red Team Reporting Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `RedReport`
- Lab focus: Defensive Red Team Reporting Assistant
- Portfolio track: Extended portfolio track
- Domain: Security — Offensive Security (Defensive Use)
- Method: LLM + RAG
- Difficulty level: 2

## Original Brief

### AI Trợ Lý Red Team — Lập Kế Hoạch Kiểm Thử & Báo Cáo Phòng Thủ

Đội red team/pentest nội bộ tốn nhiều thời gian lập kế hoạch kiểm thử theo phạm vi được duyệt, ghi chép phát hiện, và viết báo cáo với khuyến nghị khắc phục — phần viết lách lấn át thời gian kiểm thử thực. Bài toán: AI hỗ trợ lập kế hoạch kiểm thử có cấu trúc theo phạm vi và mục tiêu được tổ chức phê duyệt (ánh xạ MITRE ATT&CK), tổ chức ghi chép phát hiện trong quá trình, sinh báo cáo pentest chuyên nghiệp với mô tả rủi ro và khuyến nghị vá lỗi ưu tiên. Lưu ý đạo đức: chỉ hỗ trợ kiểm thử có ủy quyền hợp pháp, không sinh mã khai thác hay hướng dẫn tấn công thực tế ngoài phạm vi phòng thủ.

## Reference Stack

OpenAI/Claude, RAG MITRE/OWASP, python-docx, FastAPI, Next.js

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
22-redreport-redteam-reporting/
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
