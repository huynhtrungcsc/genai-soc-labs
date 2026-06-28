# 03 · ThreatPulse: AI Threat Intelligence Briefing

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `ThreatPulse`
- Lab focus: AI Threat Intelligence Briefing
- Portfolio track: Flagship SOC track
- Domain: Security — Threat Intelligence
- Method: RAG + LLM
- Difficulty level: 2

## Original Brief

### AI Tổng Hợp Threat Intelligence — Từ Hàng Trăm Nguồn Đến Cảnh Báo Liên Quan Đến Tổ Chức

Đội threat intel ngập trong báo cáo CVE, bài blog của hãng bảo mật, feed IOC, cảnh báo của cơ quan nhà nước — đọc hết là bất khả thi, nên lỗ hổng đang bị khai thác ngoài thực địa liên quan đến công nghệ tổ chức đang dùng bị phát hiện muộn. Bài toán: AI thu thập và tổng hợp threat intel đa nguồn, lọc theo tech stack và ngành của tổ chức (chỉ cảnh báo cái thực sự liên quan), tóm tắt mức độ nghiêm trọng và khả năng bị khai thác, ánh xạ CVE với tài sản nội bộ có nguy cơ, và sinh bản tin tình báo hàng ngày kèm khuyến nghị ưu tiên vá lỗi.

## Reference Stack

OpenAI/Claude, RAG threat feed (NVD/CISA/vendor), embeddings, FastAPI, Next.js

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
03-threatpulse-threat-intel/
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
