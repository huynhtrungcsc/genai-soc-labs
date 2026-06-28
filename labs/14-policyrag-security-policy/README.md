# 14 · PolicyRAG: Security Policy Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `PolicyRAG`
- Lab focus: Security Policy Assistant
- Portfolio track: Extended portfolio track
- Domain: Security — Policy Management
- Method: RAG + LLM
- Difficulty level: 2

## Original Brief

### AI Quản Lý & Truy Vấn Chính Sách Bảo Mật Nội Bộ Bằng Ngôn Ngữ Tự Nhiên

Tổ chức có hàng chục tài liệu chính sách an ninh (mật khẩu, truy cập, xử lý dữ liệu, BYOD) nhưng nhân viên không đọc và đội bảo mật mất thời gian trả lời lặp lại 'theo chính sách thì tôi được/không được làm X'. Bài toán: AI trợ lý trả lời câu hỏi về chính sách bảo mật dựa trên tài liệu nội bộ, trích dẫn chính xác điều khoản liên quan, từ chối khi câu hỏi ngoài phạm vi và chuyển cho con người, phát hiện mâu thuẫn giữa các tài liệu chính sách, và đề xuất cập nhật khi có quy định mới (như Nghị định bảo vệ dữ liệu cá nhân VN). Giảm tải đội bảo mật và tăng tuân thủ.

## Reference Stack

OpenAI/Claude, RAG policy docs, citation, FastAPI, Next.js

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
14-policyrag-security-policy/
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
