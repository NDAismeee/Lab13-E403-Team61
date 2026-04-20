# Langfuse Dashboard Runbook (Lab13 Team61)

## Goal

Use **Langfuse custom dashboards** as the Layer-2 dashboard for the lab:

- Latency P50 / P95 / P99
- Traffic
- Error rate with breakdown
- Cost over time
- Tokens in / out
- Quality proxy (score)

Constraints:

- default time range: **Last 1 hour**
- auto refresh: **15s or 30s**
- keep it to **6 panels** on the main dashboard
- use clear units and add a visible threshold/SLO line where possible

## Before you build the dashboard

1. Configure `.env` with:
   - `LANGFUSE_PUBLIC_KEY`
   - `LANGFUSE_SECRET_KEY`
   - `LANGFUSE_BASE_URL` (example: `https://cloud.langfuse.com`)
2. Start the app locally.
3. Generate demo traces:

```bash
python scripts/generate_dashboard_demo.py --traces 14
```

You should see **>= 10 traces** in Langfuse after this.

## Create the dashboard in Langfuse UI

1. Open Langfuse (cloud or your instance).
2. Select your project for this lab.
3. Go to **Dashboards** → **New dashboard**.
4. Name it:

```text
Lab13 Team61 - Layer 2 Dashboard
```

5. Set:
   - Time range: **Last 1 hour**
   - Auto refresh: **15s** (or **30s**)

### Recommended global filters

If you want to avoid noise, set a dashboard-level filter:

- tags contains `lab`

Optionally add:

- metadata `environment` = `dev`

## Panel 1 — Latency P50 / P95 / P99

- Visualization: time series
- Metric: trace (or request) latency
- Show: P50, P95, P99
- Unit: ms
- Threshold line: P95 < 2000ms (example)

## Panel 2 — Traffic

- Visualization: time series
- Measure: trace count over time
- Unit: requests (or req/min)

## Panel 3 — Error rate with breakdown

Option A (preferred if supported):

- Visualization: time series
- Measure: failed trace count
- Breakdown/group by: trace metadata `error_type`

Option B (acceptable):

- failed trace count over time, grouped by `error_type`

Tips:

- You can filter failed traces using Langfuse failure status.
- Failed requests are tagged with `error` by the API layer.

## Panel 4 — Cost over time

- Visualization: time series
- Measure: cost
- Unit: USD
- Optional split: by `model` or `feature` (trace metadata)

## Panel 5 — Tokens in / out

- Visualization: stacked time series (or 2-series time series)
- Measure: generation token usage
- Series: input tokens and output tokens
- Unit: tokens

## Panel 6 — Quality proxy

- Visualization: time series
- Data source: scores
- Score name: `quality_score`
- Aggregation: average over time
- Unit: 0.0–1.0
- Threshold line: 0.7 (example)

Optional variations:

- Add another score panel for `retrieval_hit` (avg over time)
- Compare quality during incidents by filtering on metadata:
  - `incident_rag_slow` / `incident_tool_fail` / `incident_cost_spike`

## Evidence / screenshots checklist

Capture these for grading evidence:

1. Trace list showing **>= 10 traces**
2. One full trace waterfall showing retrieval + generation
3. Dashboard screenshot with all **6 panels** visible
4. Error scenario evidence (after `tool_fail`)
5. Slow scenario evidence (after `rag_slow`)
6. Logs screenshot showing `correlation_id` in `data/logs.jsonl`
7. Logs screenshot showing PII redaction (e.g., an email becomes `[REDACTED_EMAIL]`)

