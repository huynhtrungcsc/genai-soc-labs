# 05 · HardeningPilot: CIS/ISO Security Advisor

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `HardeningPilot`
- Lab focus: CIS/ISO Security Advisor
- Portfolio track: Extended portfolio track
- Domain: Security — Compliance & Hardening
- Method: RAG + LLM
- Difficulty level: 2

## Original Brief

### AI Cố Vấn Cấu Hình & Hardening Bảo Mật Theo Chuẩn (CIS/ISO 27001)

Đội vận hành phải hardening hàng trăm máy chủ, cloud account, thiết bị mạng theo CIS Benchmark / ISO 27001 — tài liệu chuẩn dày hàng trăm trang, kiểm tra thủ công từng mục là không khả thi nên cấu hình sai sót để hở cửa cho tấn công. Bài toán: AI đọc cấu hình hệ thống (file config, output lệnh, cloud policy), đối chiếu với chuẩn bảo mật áp dụng, chỉ ra điểm chưa tuân thủ kèm giải thích rủi ro và mức ưu tiên, sinh hướng dẫn khắc phục cụ thể cho từng nền tảng, và tạo báo cáo tuân thủ cho audit. Biến tài liệu chuẩn khô khan thành hành động cụ thể.

## Reference Stack

OpenAI/Claude, RAG CIS/ISO benchmark, config parsing, FastAPI, Next.js

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
05-hardeningpilot-compliance-advisor/
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
