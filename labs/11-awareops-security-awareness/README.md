# 11 · AwareOps: Security Awareness & Phishing Simulation

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `AwareOps`
- Lab focus: Security Awareness & Phishing Simulation
- Portfolio track: Extended portfolio track
- Domain: Security — Security Awareness
- Method: LLM + Personalization
- Difficulty level: 2

## Original Brief

### AI Đào Tạo Nhận Thức An Ninh Cá Nhân Hóa & Mô Phỏng Phishing

Đào tạo an ninh cho nhân viên hiện là video một chiều xem cho có, ai cũng học cùng nội dung bất kể vai trò hay điểm yếu — kết quả là tỷ lệ click phishing không giảm. Bài toán: AI sinh nội dung đào tạo cá nhân hóa theo vai trò và mức rủi ro từng nhân viên, tạo mô phỏng phishing thực tế theo ngữ cảnh VN (giả mạo ngân hàng, nội bộ, đối tác), phân tích ai dễ mắc lỗi gì để nhắm đào tạo đúng điểm yếu, và đo lường cải thiện theo thời gian. Biến đào tạo từ thủ tục thành thay đổi hành vi thực sự. Lưu ý đạo đức: mô phỏng chỉ phục vụ huấn luyện nội bộ có sự đồng thuận của tổ chức.

## Reference Stack

OpenAI/Claude, phishing simulation framework, LMS integration, FastAPI, Next.js

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
11-awareops-security-awareness/
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
