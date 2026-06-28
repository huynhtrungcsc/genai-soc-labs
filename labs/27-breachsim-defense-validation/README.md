# 27 · BreachSim: Defensive Attack Simulation Planner

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `BreachSim`
- Lab focus: Defensive Attack Simulation Planner
- Portfolio track: Extended portfolio track
- Domain: Security — Breach Simulation
- Method: LLM + RAG
- Difficulty level: 2

## Original Brief

### AI Mô Phỏng Kịch Bản Tấn Công & Đánh Giá Khả Năng Phòng Thủ (BAS)

Đội bảo mật đầu tư nhiều công cụ nhưng không chắc chúng có thực sự phát hiện được tấn công không cho đến khi bị tấn công thật — kiểm thử thủ công tốn kém và không thường xuyên. Bài toán: AI giúp thiết kế và mô phỏng các kịch bản tấn công an toàn theo MITRE ATT&CK (trong môi trường được kiểm soát và ủy quyền), đánh giá hệ thống phòng thủ có phát hiện và cảnh báo đúng không, chỉ ra các kỹ thuật tấn công mà tổ chức đang 'mù', diễn giải khoảng trống phòng thủ và đề xuất cải thiện. Lưu ý đạo đức: chỉ mô phỏng trong môi trường được duyệt, không thực hiện tấn công thật.

## Reference Stack

OpenAI/Claude, RAG MITRE ATT&CK, BAS framework (caldera-like), FastAPI, dashboard

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
27-breachsim-defense-validation/
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
