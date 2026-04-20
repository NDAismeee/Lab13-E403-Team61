# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 
- [REPO_URL]: 
- [MEMBERS]:
  - Member A: [Hieu] | Role: Logging & PII
  - Member B: [Vinh] | Role: Tracing & Enrichment
  - Member C: [Dung] | Role: SLO & Alerts
  - Member D: [Hai] | Role: Load Test 
  - Member E: [Duc Anh] | Role: Demo & Dashboard

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Day13/Lab13-Observability/screenshot/EVIDENCE_CORRELATION_ID_SCREENSHOT.png]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Day13/Lab13-Observability/screenshot/EVIDENCE_PII_REDACTION_SCREENSHOT.png]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)

### Kịch bản 1: RAG phản hồi chậm
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Độ trễ (Latency) tăng đột biến từ ~150ms lên hơn 13.000ms (13 giây).
- [ROOT_CAUSE_PROVED_BY]: Dòng log ghi nhận Correlation ID `req-8efb98a5` với `latency_ms` là 10624.0ms và `req-ef5b87d7` là 13277.8ms.
- [FIX_ACTION]: Tắt cờ sự cố rag_slow bằng lệnh scripts/inject_incident.py --disable.
- [PREVENTIVE_MEASURE]: Thiết lập SLO cho độ trễ P95 và cấu hình cảnh báo (alerts) khi việc truy xuất RAG vượt quá 2000ms.

### Kịch bản 2: Lỗi hệ thống (Tool Failure)
- [SCENARIO_NAME]: tool_fail
- [SYMPTOMS_OBSERVED]: 100% yêu cầu trả về lỗi HTTP 500 (Internal Server Error).
- [ROOT_CAUSE_PROVED_BY]: Log ghi nhận event "request_failed" (Mã lỗi 500) với Correlation ID trả về là `None` do lỗi ngắt mạch xử lý.
- [FIX_ACTION]: Tắt cờ sự cố tool_fail bằng lệnh scripts/inject_incident.py --disable.
- [PREVENTIVE_MEASURE]: Triển khai cơ chế Circuit Breaker (ngắt mạch) hoặc Fallback (dự phòng) để tránh gây sập toàn bộ hệ thống.

---

## 5. Individual Contributions & Evidence

### Hieu
- [TASKS_COMPLETED]:
  - Cấu hình logging chuẩn JSON cho toàn bộ app.
  - Enrich log với các trường context: correlation_id, user_id_hash, session_id, feature, model, env...
  - Triển khai và tích hợp PII scrubber để tự động ẩn thông tin nhạy cảm (email, số điện thoại, CCCD, thẻ tín dụng, passport, địa chỉ...).
  - Đảm bảo mọi log đều được enrich và scrub đúng, pass validate_logs.py.
- [EVIDENCE_LINK]: https://github.com/VinUni-AI20k/Lab13-Observability/commit/26195f4c93f0b409b1198cb2a5a46953ce26130e

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: Thực hiện load test (cơ bản và song song), giả lập các sự cố hiệu năng và hệ thống (rag_slow, tool_fail), xác nhận phục hồi hệ thống và cung cấp dữ liệu log cho việc xây dựng dashboard.
- [EVIDENCE_LINK]: Thực thi trực tiếp các script scripts/load_test.py và scripts/inject_incident.py trên máy cục bộ.

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
