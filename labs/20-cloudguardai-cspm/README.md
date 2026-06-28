# 20 · CloudGuardAI: CSPM Risk Advisor

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `CloudGuardAI`
- Lab focus: CSPM Risk Advisor
- Portfolio track: Extended portfolio track
- Domain: Security — Cloud Security
- Method: LLM + Analytics
- Difficulty level: 2

## Original Brief

### AI Săn Lỗ Hổng Cấu Hình Cloud (CSPM) & Diễn Giải Rủi Ro

Hạ tầng cloud (AWS/GCP/Azure) có hàng nghìn cấu hình, một S3 bucket để public hay một security group mở 0.0.0.0/0 là đủ gây rò rỉ — nhưng đội vận hành không theo kịp tốc độ thay đổi và công cụ CSPM phun ra quá nhiều finding. Bài toán: AI phân tích cấu hình cloud, phát hiện sai cấu hình rủi ro (lưu trữ public, quyền IAM quá rộng, mã hóa thiếu, logging tắt), giải thích kịch bản tấn công cụ thể cho mỗi finding, ưu tiên theo mức phơi nhiễm và độ nhạy dữ liệu, sinh hướng dẫn khắc phục (kèm IaC nếu có), và theo dõi tư thế bảo mật cloud theo thời gian.

## Reference Stack

OpenAI/Claude, cloud API (AWS/GCP/Azure), CSPM rules, FastAPI, dashboard

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
20-cloudguardai-cspm/
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
