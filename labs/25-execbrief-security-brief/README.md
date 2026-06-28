# 25 · ExecBrief: Executive Security Reporting AI

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `ExecBrief`
- Lab focus: Executive Security Reporting AI
- Portfolio track: Extended portfolio track
- Domain: Security — Executive Reporting
- Method: LLM + Analytics
- Difficulty level: 2

## Original Brief

### AI Tổng Hợp & Cảnh Báo An Ninh Cho Lãnh Đạo (Executive Security Brief)

Lãnh đạo cần hiểu tư thế an ninh của tổ chức để ra quyết định đầu tư nhưng nhận về toàn báo cáo kỹ thuật đầy thuật ngữ không thể tiêu hóa, dẫn đến đầu tư an ninh dựa trên cảm tính hoặc sau khi đã bị tấn công. Bài toán: AI tổng hợp dữ liệu từ các hệ thống bảo mật thành bản tin ngắn gọn cho lãnh đạo: rủi ro lớn nhất hiện tại, xu hướng theo thời gian, so sánh với chuẩn ngành, và khuyến nghị đầu tư ưu tiên — tất cả bằng ngôn ngữ kinh doanh kèm liên hệ tác động tài chính/uy tín. Biến dữ liệu kỹ thuật thành insight ra quyết định cho cấp lãnh đạo.

## Reference Stack

OpenAI/Claude, data aggregation, BI visualization, FastAPI, Next.js

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
25-execbrief-security-brief/
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
