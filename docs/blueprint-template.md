# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Group 25
- [REPO_URL]: https://github.com/NDAismeee/Lab13-E403-Team25.git
- [MEMBERS]:
Member A: [Hieu] | Role: Logging & PII
Member B: [Vinh] | Role: Tracing & Enrichment
Member C: [Dung] | Role: SLO & Alerts
Member D: [Hai] | Role: Load Test
Member E: [Duc Anh] | Role: Demo & Dashboard


---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 227 (estimated from completed requests in `data/logs.jsonl`)
- [PII_LEAKS_FOUND]: 0 (validate_logs.py found no potential PII leaks)

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Day13/Lab13-Observability/evidence/EVIDENCE_CORRELATION_ID_SCREENSHOT.png]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Day13/Lab13-Observability/evidence/EVIDENCE_PII_REDACTION_SCREENSHOT.png]
- [TRACE_WATERFALL_EXPLANATION]: Trace hiển thị rõ ràng mối quan hệ cha-con: `agent-run` bao bọc `retrieval` và `llm-generation`. Cấu trúc này giúp xác định chính xác bước nào trong pipeline gây ra độ trễ hoặc lỗi (ví dụ: phân biệt chậm do truy vấn dữ liệu hay chậm do Model phản hồi).

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [screenshot/vite-dashboard-6-panels-team25.png]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | ~2655ms (last 1h demo window; rag_slow pushes tail latency) |
| Error Rate | < 2% | 28d | ~14.14% (last 1h demo window; tool_fail intentionally triggers 500s) |
| Cost Budget | < $2.5/day | 1d | ~0.304 USD/hour (≈$7.3/day during cost_spike demo period) |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [screenshot/alert-rules-and-runbook-link.png]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#1-high-latency-p95]

---

## 4. Incident Response (Group)

### Kịch bản 1: RAG phản hồi chậm
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Độ trễ (Latency) tăng mạnh (P95 tiến gần/vượt ngưỡng 2000ms) khi có tải và bật kịch bản `rag_slow`.
- [ROOT_CAUSE_PROVED_BY]: Root cause được chứng minh trực tiếp từ code `app/mock_rag.py`: khi `STATE["rag_slow"] == True` thì hàm `retrieve()` `time.sleep(2.5)` làm chậm bước retrieval. Log `response_sent` cũng phản ánh `latency_ms` tăng cao trong thời điểm bật incident.
- [FIX_ACTION]: Tắt cờ sự cố `rag_slow` bằng endpoint điều khiển hoặc script: `python scripts/inject_incident.py --scenario rag_slow --disable`.
- [PREVENTIVE_MEASURE]: Thiết lập SLO cho Latency P95 và cảnh báo P2 khi P95 vượt ngưỡng (ví dụ 2000ms) trong 30 phút; drill-down bằng trace để tách retrieval vs generation; áp dụng giới hạn truy vấn và fallback retrieval.

### Kịch bản 2: Lỗi hệ thống (Tool Failure)
- [SCENARIO_NAME]: tool_fail
- [SYMPTOMS_OBSERVED]: 100% yêu cầu trả về lỗi HTTP 500 (Internal Server Error).
- [ROOT_CAUSE_PROVED_BY]: Root cause nằm ở `app/mock_rag.py`: khi `STATE["tool_fail"] == True` thì `retrieve()` raise `RuntimeError("Vector store timeout")`. Log event `request_failed` ghi rõ `error_type=RuntimeError` và correlation_id của request vẫn được giữ để truy vết.
- [FIX_ACTION]: Tắt cờ sự cố `tool_fail` bằng endpoint điều khiển hoặc script: `python scripts/inject_incident.py --scenario tool_fail --disable`.
- [PREVENTIVE_MEASURE]: Thêm cơ chế fallback/circuit breaker: (1) retry có backoff cho retrieval, (2) fallback trả lời “general answer” khi vector store timeout, (3) tách lỗi tool vs lỗi hệ thống để dashboard có breakdown theo `error_type` và theo incident flag.

---

## 5. Individual Contributions & Evidence

### [DO MINH HIEU]
- [TASKS_COMPLETED]: Cấu hình logging chuẩn JSON cho toàn bộ app.
Enrich log với các trường context: correlation_id, user_id_hash, session_id, feature, model, env...
Triển khai và tích hợp PII scrubber để tự động ẩn thông tin nhạy cảm (email, số điện thoại, CCCD, thẻ tín dụng, passport, địa chỉ...).
Đảm bảo mọi log đều được enrich và scrub đúng, pass validate_logs.py.
- [EVIDENCE_LINK]:(https://github.com/NDAismeee/Lab13-E403-Team25/pull/1)

### [KHUONG QUANG VINH]
- [TASKS_COMPLETED]: Tích hợp Langfuse Tracing vào FastAPI; triển khai nested spans cho Retrieval và Generation để tạo hệ thống phân cấp trace; cấu hình Generation type để theo dõi model và token usage; gắn tags (lab, feature, model) và metadata (correlation_id, doc_count) để làm giàu dữ liệu quan sát.
- [EVIDENCE_LINK]: Modified `app/tracing.py`, `app/agent.py`, `app/mock_rag.py`, `app/mock_llm.py`, and `app/main.py`.

### [NGUYEN TIEN DUNG]
- [TASKS_COMPLETED]: Xác định các chỉ số SLI và thiết lập mục tiêu SLO cho hệ thống (Latency, Error Rate, Cost); Thiết lập các quy tắc cảnh báo (Alert Rules) dựa trên ngưỡng SLO; Xây dựng tài liệu hướng dẫn xử lý sự cố (Runbooks) chi tiết trong `docs/alerts.md`; Liên kết các cảnh báo từ Dashboard tới Runbook.
- [EVIDENCE_LINK]: docs/alerts.md và cấu hình phần [SLO_TABLE] trong báo cáo này.

### [TRAN LONG HAI]
- [TASKS_COMPLETED]: Thực hiện load test (cơ bản và song song), giả lập các sự cố hiệu năng và hệ thống (rag_slow, tool_fail), xác nhận phục hồi hệ thống và cung cấp dữ liệu log cho việc xây dựng dashboard.
- [EVIDENCE_LINK]: Thực thi trực tiếp các script scripts/load_test.py và scripts/inject_incident.py trên máy cục bộ.

### [NGUYEN DUC ANH]
- [TASKS_COMPLETED]: Chuẩn bị demo & dashboard theo đúng spec Layer-2: tạo dashboard chạy trên Langfuse (theo runbook) và thêm dashboard local bằng Vite để visualize 6 panels (Latency P50/P95/P99, Traffic, Error breakdown, Cost, Tokens, Quality). Thêm hướng dẫn thao tác trong `docs/langfuse-dashboard-runbook.md` và script tạo traffic `scripts/generate_dashboard_demo.py` để sinh >=10 traces và đủ tình huống incident (rag_slow/tool_fail/cost_spike) phục vụ chụp evidence.
- [EVIDENCE_LINK]: `frontend-dashboard/` + `docs/langfuse-dashboard-runbook.md` + `scripts/generate_dashboard_demo.py`

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
