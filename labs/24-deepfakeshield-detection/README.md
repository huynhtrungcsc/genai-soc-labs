# 24 · DeepfakeShield: Synthetic Media Detection

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `DeepfakeShield`
- Lab focus: Synthetic Media Detection
- Portfolio track: Extended portfolio track
- Domain: Security — Deepfake Detection
- Method: Vision/Audio + LLM
- Difficulty level: 2

## Original Brief

### AI Phát Hiện Deepfake & Nội Dung Giả Mạo Trong Xác Thực

Quy trình eKYC và xác thực bằng khuôn mặt/giọng nói đối mặt với mối đe dọa mới: deepfake và giọng nói tổng hợp dùng để vượt xác thực và lừa đảo. Bài toán: AI phân tích hình ảnh/video/âm thanh trong luồng xác thực để phát hiện dấu hiệu giả mạo (bất thường ánh sáng, chuyển động không tự nhiên, artifact tổng hợp, dấu hiệu phát lại), chấm điểm độ tin cậy là người thật, diễn giải dấu hiệu nghi ngờ cho đội risk, và cảnh báo các vụ tấn công mạo danh. Lưu ý đạo đức: chỉ phục vụ phòng chống lừa đảo, xử lý dữ liệu sinh trắc tuân thủ quyền riêng tư.

## Reference Stack

Vision/audio model, deepfake detection, OpenAI/Claude diễn giải, FastAPI, dashboard

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
24-deepfakeshield-detection/
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
