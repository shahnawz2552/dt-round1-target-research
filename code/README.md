# Code

Reproducible pipeline that backs the methodology in `partA-research/methodology.md`.

## Files

| File | Stage | What it does |
|------|-------|--------------|
| `01_dsir_parser.py` | Source ingestion | Pulls DSIR R&D-recognized units list, filters to Hyderabad + specialty chem/biotech NIC codes |
| `02_mca_enrichment.py` | Enrichment | For each candidate, pulls MCA / Tofler data — CIN, financials, directors, shareholding pattern, charge filings |
| `03_llm_scoring.py` | Scoring | Sends evidence pack to Claude with strict JSON schema — scores C3-C8 with mandatory citations |
| `04_funnel_orchestrator.py` | Pipeline | Runs stages 1-7 idempotently; resumable on failure |

## Why these specifically

These are the four leverage points — source ingestion, enrichment, scoring, and orchestration — that turn the manual Part A research process into a 1,000-company / 30-day pipeline. The Part B proposal explains how these four files scale.

## Running locally

```bash
# Install deps
pip install requests beautifulsoup4 anthropic

# Set env vars
export TOFLER_API_KEY=...
export ANTHROPIC_API_KEY=...

# Run end-to-end
python 04_funnel_orchestrator.py
```

## Why not pure manual

For 25 companies (Part A), manual research is faster than building this. We did the actual Part A research manually with Claude-as-thinking-partner. **The code shows what the operationalized version looks like for 1,000+ companies (Part B Q2)** — and demonstrates we know the difference between bench research and production data engineering.
