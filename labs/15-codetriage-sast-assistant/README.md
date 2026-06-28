# 15 · CodeTriage: SAST Finding Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `CodeTriage`
- Lab focus: SAST Finding Assistant
- Portfolio track: Extended portfolio track
- Domain: Security — Application Security
- Method: LLM + Code Analysis
- Difficulty level: 2

## Original Brief

### AI Hỗ Trợ Đánh Giá Bảo Mật Mã Nguồn (SAST Assistant)

Công cụ quét mã tĩnh (SAST) báo hàng trăm cảnh báo lỗ hổng, nhiều cái là false positive, và developer không hiểu vì sao một đoạn code lại rủi ro nên bỏ qua hoặc sửa sai. Bài toán: AI đọc kết quả SAST cùng đoạn code liên quan, phân loại cảnh báo thật/giả với giải thích, mô tả lỗ hổng bằng ngôn ngữ developer hiểu (vì sao nguy hiểm, kịch bản khai thác), đề xuất bản vá cụ thể đúng ngữ cảnh code, và ưu tiên theo rủi ro thực. Lưu ý đạo đức: chỉ phục vụ phòng thủ, mô tả lỗ hổng để vá chứ không cung cấp công cụ khai thác.

## Reference Stack

OpenAI/Claude, SAST tool integration (Semgrep), tree-sitter, FastAPI, Next.js

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
15-codetriage-sast-assistant/
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
