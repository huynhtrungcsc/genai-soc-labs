# 21 · FraudSignal: Transaction Fraud Detection

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `FraudSignal`
- Lab focus: Transaction Fraud Detection
- Portfolio track: Extended portfolio track
- Domain: Security — Fraud Detection
- Method: ML + LLM
- Difficulty level: 2

## Original Brief

### AI Phát Hiện Lừa Đảo & Gian Lận Giao Dịch Cho Hệ Sinh Thái Số

Các nền tảng số trong một hệ sinh thái lớn (ví, mua sắm, đặt xe) đối mặt với gian lận: tài khoản giả, chiếm đoạt tài khoản, giao dịch bất thường, lạm dụng khuyến mãi — luật cứng dễ bị lách và bỏ sót mẫu gian lận mới. Bài toán: AI phân tích hành vi giao dịch và phiên người dùng, phát hiện pattern gian lận (tốc độ bất thường, thiết bị/vị trí bất thường, mạng lưới tài khoản liên kết), chấm điểm rủi ro real-time, diễn giải vì sao một giao dịch bị gắn cờ (để đội risk ra quyết định), và thích nghi với mẫu gian lận mới. Cân bằng giữa chặn gian lận và không làm phiền khách thật.

## Reference Stack

OpenAI/Claude diễn giải, ML (graph + gradient boosting), real-time scoring, FastAPI, dashboard

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
21-fraudsignal-fraud-detection/
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
