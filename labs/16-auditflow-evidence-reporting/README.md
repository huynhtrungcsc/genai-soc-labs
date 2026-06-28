# 16 · AuditFlow: Compliance Evidence Generator

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `AuditFlow`
- Lab focus: Compliance Evidence Generator
- Portfolio track: Extended portfolio track
- Domain: Security — Compliance Reporting
- Method: RAG + LLM
- Difficulty level: 2

## Original Brief

### AI Tạo Báo Cáo Tuân Thủ & Bằng Chứng Audit An Ninh Tự Động

Mỗi kỳ audit bảo mật (ISO 27001, SOC 2, PCI-DSS), đội GRC mất hàng tuần thu thập bằng chứng từ nhiều hệ thống, ánh xạ vào yêu cầu kiểm soát, và viết báo cáo — công việc lặp lại mỗi kỳ và dễ sót. Bài toán: AI ánh xạ các kiểm soát kỹ thuật hiện có vào yêu cầu của khung tuân thủ, tự động thu thập và tổ chức bằng chứng (log cấu hình, kết quả quét, chính sách), phát hiện khoảng trống tuân thủ cần khắc phục, và sinh bản nháp báo cáo audit có cấu trúc. Biến công việc giấy tờ thành quy trình liên tục thay vì chạy nước rút mỗi kỳ.

## Reference Stack

OpenAI/Claude, RAG compliance framework, evidence collection API, python-docx, FastAPI

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
16-auditflow-evidence-reporting/
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
