# 13 · NetBeacon: C2 & Exfiltration Detection

## Status

Scaffolded. This lab currently contains the original project brief and the planned delivery standard. Implementation will be added later.

## Positioning

- Codename: `NetBeacon`
- Lab focus: C2 & Exfiltration Detection
- Portfolio track: Flagship SOC track
- Domain: Security — Network Detection
- Method: ML + LLM
- Difficulty level: 2

## Original Brief

### AI Phân Tích Lưu Lượng Mạng & Phát Hiện C2/Exfiltration

Mã độc sau khi xâm nhập sẽ 'gọi về' máy chủ điều khiển (C2) và tuồn dữ liệu ra ngoài — các kết nối này lẫn trong hàng triệu luồng mạng hợp lệ và khó phát hiện bằng luật cứng. Bài toán: AI phân tích metadata lưu lượng mạng (NetFlow/Zeek log), phát hiện pattern đáng ngờ (beaconing đều đặn ra IP lạ, DNS tunneling, khối lượng tải lên bất thường), chấm điểm rủi ro và diễn giải vì sao một luồng đáng ngờ bằng ngôn ngữ analyst hiểu, gom các kết nối liên quan thành một câu chuyện tấn công, và ưu tiên điều tra. Tập trung metadata để bảo vệ quyền riêng tư nội dung.

## Reference Stack

OpenAI/Claude diễn giải, ML anomaly, Zeek/NetFlow ingestion, FastAPI, dashboard

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
13-netbeacon-c2-exfil-detection/
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
