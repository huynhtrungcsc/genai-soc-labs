# 18 · ForensicTrace: Investigation Timeline Builder

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `ForensicTrace`
- Lab focus: Investigation Timeline Builder
- Portfolio track: Flagship SOC track
- Domain: Security — Digital Forensics
- Method: LLM + Correlation
- Difficulty level: 2

## Original Brief

### AI Phân Tích & Tương Quan Log Đa Nguồn Cho Điều Tra Số (Forensics)

Khi điều tra một vụ xâm nhập, chuyên gia forensics phải ghép log từ endpoint, server, mạng, cloud — mỗi cái định dạng và timezone khác nhau — để dựng lại chuyện gì đã xảy ra, một quá trình thủ công kéo dài nhiều ngày. Bài toán: AI chuẩn hóa và tương quan log đa nguồn theo dòng thời gian thống nhất, dựng lại chuỗi sự kiện của cuộc tấn công, làm nổi bật các hành động đáng ngờ và mối liên hệ giữa chúng, sinh narrative điều tra dễ hiểu cho cả kỹ thuật và pháp lý, và xuất bằng chứng có cấu trúc. Rút ngắn thời gian từ 'có sự cố' đến 'hiểu toàn cảnh'.

## Reference Stack

OpenAI/Claude, log normalization, timeline correlation, FastAPI, Next.js

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
18-forensictrace-timeline-builder/
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
