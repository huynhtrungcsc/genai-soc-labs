# 07 · PlaybookOps: SOAR Response Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `PlaybookOps`
- Lab focus: SOAR Response Assistant
- Portfolio track: Flagship SOC track
- Domain: Security — SOAR
- Method: LLM + Workflow
- Difficulty level: 2

## Original Brief

### AI Sinh & Diễn Giải Playbook Ứng Phó Sự Cố (SOAR Assistant)

Khi sự cố xảy ra, đội SOC cần phản ứng theo playbook nhưng playbook viết tay thường lỗi thời, không bao quát biến thể mới, và analyst tier-1 dưới áp lực dễ làm sai bước. Bài toán: AI nhận loại sự cố và ngữ cảnh, đề xuất các bước ứng phó phù hợp dựa trên playbook tổ chức và best practice, giải thích lý do từng bước (để analyst không làm như robot mà hiểu việc), tự động hóa các tác vụ an toàn (thu thập bằng chứng, làm giàu IOC) và yêu cầu xác nhận con người trước các hành động có tác động (cô lập máy, khóa tài khoản), và ghi lại quy trình để cải thiện playbook. Con người luôn giữ quyền quyết định.

## Reference Stack

OpenAI/Claude, SOAR/EDR API, workflow engine, FastAPI, Next.js

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
07-playbookops-soar-assistant/
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
