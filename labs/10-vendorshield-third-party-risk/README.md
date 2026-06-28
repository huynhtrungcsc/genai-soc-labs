# 10 · VendorShield: Third-Party Risk Assessor

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `VendorShield`
- Lab focus: Third-Party Risk Assessor
- Portfolio track: Extended portfolio track
- Domain: Security — Third-Party Risk
- Method: RAG + LLM
- Difficulty level: 2

## Original Brief

### AI Đánh Giá Rủi Ro Nhà Cung Cấp & Bên Thứ Ba (Third-Party Risk)

Tổ chức lớn dùng hàng trăm nhà cung cấp, mỗi bên là một cửa ngõ rủi ro (vụ rò rỉ qua bên thứ ba ngày càng phổ biến) — nhưng đánh giá an ninh nhà cung cấp dựa trên bảng câu hỏi dài hàng trăm mục, gửi đi đợi vài tuần, đọc câu trả lời thủ công. Bài toán: AI tự động hóa quy trình: sinh bộ câu hỏi đánh giá phù hợp loại nhà cung cấp và mức truy cập dữ liệu, phân tích câu trả lời và tài liệu chứng minh (chứng chỉ, báo cáo audit), đối chiếu với tín hiệu công khai (lịch sử rò rỉ, bề mặt tấn công lộ ra internet), chấm điểm rủi ro và đề xuất điều khoản/biện pháp giảm thiểu trong hợp đồng.

## Reference Stack

OpenAI/Claude, RAG security questionnaire, OSINT, FastAPI, Next.js

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
10-vendorshield-third-party-risk/
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
