# 29 · IoTWatch: IoT/OT Security Monitoring AI

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `IoTWatch`
- Lab focus: IoT/OT Security Monitoring AI
- Portfolio track: Extended portfolio track
- Domain: Security — IoT/OT Security
- Method: ML + LLM
- Difficulty level: 2

## Original Brief

### AI Giám Sát An Ninh Cho Hệ Thống IoT & OT Trong Đô Thị Thông Minh

Hệ sinh thái đô thị thông minh và tòa nhà thông minh (camera, cảm biến, hệ thống điều khiển) dùng vô số thiết bị IoT/OT vốn yếu bảo mật và khó vá — một thiết bị bị chiếm có thể thành bàn đạp tấn công cả hạ tầng. Bài toán: AI giám sát hành vi mạng của thiết bị IoT/OT, học baseline hoạt động bình thường của từng loại thiết bị, phát hiện bất thường (thiết bị giao tiếp với đích lạ, firmware bất thường, lưu lượng tăng đột biến), cảnh báo nguy cơ thiết bị bị xâm nhập, và diễn giải rủi ро trong ngữ cảnh hạ tầng. Đặc biệt phù hợp các tổ hợp bất động sản và đô thị quy mô lớn có hàng nghìn thiết bị kết nối.

## Reference Stack

OpenAI/Claude diễn giải, ML anomaly, IoT/OT protocol parsing, FastAPI, dashboard

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
29-iotwatch-iot-ot-security/
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
