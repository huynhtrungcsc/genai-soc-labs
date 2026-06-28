# 19 · SOCMentor: Tier-1 Analyst Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `SOCMentor`
- Lab focus: Tier-1 Analyst Assistant
- Portfolio track: Flagship SOC track
- Domain: Security — SOC Assistant
- Method: RAG + LLM
- Difficulty level: 2

## Original Brief

### AI Trợ Lý SOC Tier-1 — Chatbot Hỏi-Đáp Cảnh Báo & Hướng Dẫn Xử Lý

Analyst tier-1 mới vào, gặp một loại cảnh báo lạ là phải hỏi senior hoặc tra runbook rải rác — thời gian phản ứng chậm và senior bị gián đoạn liên tục bởi câu hỏi lặp. Bài toán: AI trợ lý hiểu ngữ cảnh cảnh báo, giải thích cảnh báo này nghĩa là gì và mức độ nghiêm trọng, hướng dẫn từng bước điều tra dựa trên runbook tổ chức, gợi ý truy vấn để xác minh, biết khi nào cần leo thang lên tier-2 và đóng gói thông tin bàn giao, và ghi nhận câu hỏi chưa trả lời được để bổ sung tri thức. Tăng tốc đào tạo analyst mới và giảm gián đoạn cho senior.

## Reference Stack

OpenAI/Claude, RAG runbook + threat intel, SIEM context API, FastAPI, Next.js

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
19-socmentor-tier1-assistant/
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
