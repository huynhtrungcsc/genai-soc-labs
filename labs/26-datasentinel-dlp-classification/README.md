# 26 · DataSentinel: Data Classification & DLP Assistant

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `DataSentinel`
- Lab focus: Data Classification & DLP Assistant
- Portfolio track: Extended portfolio track
- Domain: Security — Data Protection
- Method: LLM + Classification
- Difficulty level: 2

## Original Brief

### AI Phân Loại & Bảo Vệ Dữ Liệu Nhạy Cảm (Data Classification & DLP)

Tổ chức không biết dữ liệu nhạy cảm (thông tin khách hàng, tài chính, bí mật kinh doanh) đang nằm ở đâu trong hàng triệu file rải khắp file server, cloud drive, email — nên không thể bảo vệ cái mình không biết tồn tại, và rò rỉ xảy ra từ những kho dữ liệu bị quên. Bài toán: AI quét và phân loại dữ liệu theo mức nhạy cảm (PII, tài chính, bí mật), phát hiện dữ liệu nhạy cảm lưu sai chỗ hoặc chia sẻ quá rộng, đề xuất biện pháp bảo vệ (mã hóa, hạn chế quyền), giám sát luồng dữ liệu nhạy cảm rời tổ chức, và cảnh báo nguy cơ rò rỉ. Tập trung nhận diện PII tiếng Việt (CCCD, số tài khoản, địa chỉ).

## Reference Stack

OpenAI/Claude, PII detection (tiếng Việt), data scanning, FastAPI, dashboard

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
26-datasentinel-dlp-classification/
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
