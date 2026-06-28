# 04 · PhishGuard: Context-Aware Phishing Detection

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `PhishGuard`
- Lab focus: Context-Aware Phishing Detection
- Portfolio track: Extended portfolio track
- Domain: Security — Email Security
- Method: LLM + Classification
- Difficulty level: 2

## Original Brief

### AI Phát Hiện Email Lừa Đảo & Phishing Nội Bộ Theo Ngữ Cảnh

Nhân viên là tuyến phòng thủ yếu nhất: một email giả mạo CEO yêu cầu chuyển tiền gấp, hay link giả trang đăng nhập nội bộ, vẫn lọt qua bộ lọc spam truyền thống vốn dựa vào blacklist và chữ ký. Phishing nhắm mục tiêu (spear-phishing) ngày càng tinh vi nhờ chính AI. Bài toán: AI phân tích email đến theo ngữ cảnh ngôn ngữ (giọng điệu khẩn cấp bất thường, yêu cầu vượt quy trình, mạo danh nội bộ), kiểm tra dấu hiệu kỹ thuật (domain gần giống, header bất thường, link rút gọn), chấm điểm rủi ro và giải thích vì sao, cảnh báo người nhận trước khi họ click, và báo cáo mẫu phishing mới cho đội bảo mật. Tập trung phishing tiếng Việt và mạo danh thương hiệu nội bộ.

## Reference Stack

OpenAI/Claude, email header analysis, URL reputation, FastAPI, browser/Outlook plugin

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
04-phishguard-phishing-detection/
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
