# 02 · QueryForge: Natural Language SIEM Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `QueryForge`
- Lab focus: Natural Language SIEM Assistant
- Portfolio track: Flagship SOC track
- Domain: Security — Threat Hunting
- Method: LLM + Text-to-Query
- Difficulty level: 2

## Original Brief

### AI Trợ Lý Truy Vấn Log Bằng Ngôn Ngữ Tự Nhiên — Hỏi SIEM Như Hỏi Người

Threat hunter muốn hỏi 'có máy nào trong dải mạng kế toán kết nối ra IP lạ ở nước ngoài trong 24h qua không' nhưng phải viết query SPL/KQL/Lucene phức tạp — rào cản cú pháp làm chậm điều tra và loại bỏ những người giỏi về bảo mật nhưng không thạo query language. Bài toán: AI chuyển câu hỏi tiếng Việt/Anh thành truy vấn SIEM đúng cú pháp, giải thích query sinh ra để analyst kiểm chứng, chạy và trình bày kết quả dễ đọc, gợi ý các câu hỏi điều tra tiếp theo dựa trên kết quả, và học từ các truy vấn đã dùng. Hạ thấp rào cản threat hunting cho cả đội SOC.

## Reference Stack

OpenAI/Claude, Splunk/Elastic/Sentinel API, text-to-query, FastAPI, Next.js

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
02-queryforge-siem-assistant/
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
