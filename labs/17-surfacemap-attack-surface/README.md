# 17 · SurfaceMap: Attack Surface Management AI

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `SurfaceMap`
- Lab focus: Attack Surface Management AI
- Portfolio track: Extended portfolio track
- Domain: Security — ASM
- Method: LLM + Recon
- Difficulty level: 2

## Original Brief

### AI Đánh Giá Bề Mặt Tấn Công Từ Bên Ngoài (Attack Surface Management)

Tổ chức không biết hết những gì mình đang phơi ra internet — subdomain bị quên, cổng mở không cần thiết, dịch vụ cũ chưa vá — và kẻ tấn công thì lập bản đồ này trước. Bài toán: AI liên tục khám phá tài sản số hướng internet của tổ chức từ nguồn công khai (DNS, chứng chỉ, dữ liệu công khai), phát hiện dịch vụ phơi nhiễm rủi ro (panel quản trị lộ, phần mềm lỗi thời, cấu hình sai), đánh giá mức nguy hiểm và diễn giải, ưu tiên xử lý, và theo dõi thay đổi bề mặt tấn công theo thời gian. Lưu ý đạo đức: chỉ trinh sát thụ động trên tài sản của chính tổ chức, không tấn công.

## Reference Stack

OpenAI/Claude, OSINT/DNS recon, certificate transparency, FastAPI, dashboard

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
17-surfacemap-attack-surface/
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
