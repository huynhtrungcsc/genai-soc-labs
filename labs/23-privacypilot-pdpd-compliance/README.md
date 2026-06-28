# 23 · PrivacyPilot: Vietnam PDPD Compliance Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `PrivacyPilot`
- Lab focus: Vietnam PDPD Compliance Assistant
- Portfolio track: Extended portfolio track
- Domain: Security — Data Privacy Compliance
- Method: RAG + LLM
- Difficulty level: 2

## Original Brief

### AI Giám Sát Tuân Thủ Nghị Định Bảo Vệ Dữ Liệu Cá Nhân VN (PDPD)

Nghị định 13/2023 về bảo vệ dữ liệu cá nhân buộc doanh nghiệp VN phải kiểm soát thu thập, lưu trữ, chia sẻ dữ liệu cá nhân — nhưng nhiều tổ chức không biết mình đang vi phạm ở đâu vì không có bản đồ luồng dữ liệu. Bài toán: AI giúp lập bản đồ luồng dữ liệu cá nhân trong tổ chức, đối chiếu thực tế xử lý dữ liệu với yêu cầu của Nghị định, phát hiện điểm chưa tuân thủ (thiếu sự đồng ý, lưu trữ quá hạn, chia sẻ trái phép), sinh hồ sơ đánh giá tác động và tài liệu tuân thủ cần thiết, và cảnh báo khi có thay đổi quy định. Biến yêu cầu pháp lý mơ hồ thành checklist hành động.

## Reference Stack

OpenAI/Claude, RAG Nghị định 13/2023, data mapping, FastAPI, Next.js

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
23-privacypilot-pdpd-compliance/
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
