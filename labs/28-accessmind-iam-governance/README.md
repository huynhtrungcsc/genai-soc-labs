# 28 · AccessMind: IAM Governance Reviewer

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `AccessMind`
- Lab focus: IAM Governance Reviewer
- Portfolio track: Extended portfolio track
- Domain: Security — Identity Governance
- Method: LLM + Analytics
- Difficulty level: 2

## Original Brief

### AI Trợ Lý Quản Lý Quyền Truy Cập & Rà Soát Định Kỳ (IAM Governance)

Theo thời gian, nhân viên tích lũy quyền truy cập từ các vai trò cũ (privilege creep), tài khoản người đã nghỉ không được khóa, quyền cấp ngoại lệ bị quên — tạo ra rủi ro lớn mà việc rà soát quyền định kỳ thì thủ công và ai cũng 'duyệt hết cho nhanh'. Bài toán: AI phân tích quyền truy cập toàn tổ chức, phát hiện quyền dư thừa/bất thường (truy cập không khớp vai trò, tài khoản orphan, quyền quá mức), đề xuất thu hồi theo nguyên tắc least-privilege với giải thích, hỗ trợ rà soát định kỳ bằng cách làm nổi bật cái đáng nghi thay vì bắt duyệt mọi thứ, và phát hiện xung đột phân quyền (SoD). Giảm bề mặt tấn công từ bên trong.

## Reference Stack

OpenAI/Claude, IAM/AD API, access analytics, FastAPI, Next.js

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
28-accessmind-iam-governance/
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
