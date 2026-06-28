# 12 · LeakWatch: Data Leak Monitoring Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `LeakWatch`
- Lab focus: Data Leak Monitoring Assistant
- Portfolio track: Extended portfolio track
- Domain: Security — Data Leak Monitoring
- Method: LLM + Monitoring
- Difficulty level: 2

## Original Brief

### AI Giám Sát Rò Rỉ Dữ Liệu & Thông Tin Đăng Nhập Trên Web/Dark Web

Thông tin đăng nhập của nhân viên hoặc dữ liệu khách hàng tổ chức bị rao bán trên các diễn đàn rò rỉ mà đội bảo mật không biết cho đến khi bị tấn công bằng chính credential đó. Bài toán: AI giám sát các nguồn công khai về rò rỉ dữ liệu (paste site, kho leak public, diễn đàn), phát hiện email/domain/thương hiệu tổ chức xuất hiện trong các vụ rò rỉ, đánh giá mức độ nghiêm trọng và độ mới, cảnh báo sớm để buộc đổi mật khẩu/khóa tài khoản, và theo dõi mức phơi nhiễm theo thời gian. Lưu ý đạo đức: chỉ truy cập nguồn hợp pháp, không hướng dẫn truy cập nội dung phi pháp.

## Reference Stack

OpenAI/Claude, breach data API (HaveIBeenPwned-like), monitoring, FastAPI, Next.js

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
12-leakwatch-data-leak-monitoring/
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
