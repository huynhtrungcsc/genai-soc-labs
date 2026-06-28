# 06 · BehaviorSentinel: UEBA Risk Detection

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `BehaviorSentinel`
- Lab focus: UEBA Risk Detection
- Portfolio track: Extended portfolio track
- Domain: Security — Insider Threat
- Method: Anomaly Detection + LLM
- Difficulty level: 2

## Original Brief

### AI Phát Hiện Bất Thường Hành Vi Người Dùng & Tài Khoản (UEBA)

Tài khoản bị chiếm quyền hay nhân viên nội gián thường hành xử khác thường — đăng nhập giờ lạ, truy cập dữ liệu ngoài phận sự, tải về khối lượng bất thường — nhưng các tín hiệu này rải rác trong log và không ai dựng được 'hành vi bình thường' để so. Bài toán: AI học baseline hành vi từng người dùng/tài khoản dịch vụ từ log truy cập, phát hiện lệch chuẩn đáng ngờ (bất khả thi về địa lý, leo thang quyền, truy cập dữ liệu nhạy cảm bất thường), chấm điểm rủi ro và diễn giải bằng ngôn ngữ analyst hiểu được (không chỉ là số), và ưu tiên điều tra. Cân bằng giữa phát hiện và quyền riêng tư nhân viên.

## Reference Stack

OpenAI/Claude diễn giải, anomaly detection time-series, log ingestion, FastAPI, dashboard

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
06-behaviorsentinel-ueba/
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
