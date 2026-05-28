# Part B — Question 2
# Proposal: 1000 ICP-Qualified Companies in 30 Days

---

## Goal

A verified list of **1000 companies** that pass the Federer Score with evidence-backed scores on all 6 criteria, delivered in 30 calendar days, ready to feed DeepThought's outreach pipeline.

---

## Constraints I'm planning around

| Constraint | Implication |
|------------|-------------|
| **~30% yield** (DT's stated benchmark) | Universe must contain **3,300–4,000 companies** to net 1000 passes |
| **Evidence discipline** — every score must be source-cited | Pure-LLM scoring not enough; need primary-source verification per criterion |
| **One person × 30 days** = ~200 hours of usable time | Per-company budget = 12 minutes average. Rules out pure-manual research; rules in heavy automation + targeted human QA |
| **Tools available** (Claude, Gemini, Copilot, Antigravity, scraping, APIs) | The pipeline should be code-first, not Excel-first |
| **Bad actor profile** — can't trust any single signal | Cross-source validation is mandatory, not optional |

---

## The funnel (target throughput per stage)

```
Stage 0 — Source pull             ~12,000 raw rows (with heavy duplication)
                  ↓ dedup + normalize
Stage 1 — Candidate universe      ~4,000 unique companies
                  ↓ E1+E2 gate (auto)
Stage 2 — Eligible pool           ~2,800
                  ↓ hard auto-disqualifiers (size, PE, group, etc.)
Stage 3 — Scoring pool            ~2,000
                  ↓ AI-assisted C3-C8 pre-scoring + evidence retrieval
Stage 4 — First-pass qualified    ~1,300 with provisional A/B-band
                  ↓ human QA on borderline + low-confidence + sample-audit
Stage 5 — Final verified          1,000 — shipped to DT pipeline
```

Yield checkpoints: 4,000 → 2,800 (70%) → 2,000 (71%) → 1,300 (65%) → 1,000 (77%). Compound yield 25%, slightly tighter than DT's 30% benchmark — chosen deliberately to absorb scoring errors.

---

## Architecture

I treat this as a **data pipeline**, not a research project. Three layers:

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1 — INGESTION                                            │
│  Parsers/scrapers for each source → unified `companies_raw` SQL │
│  table with (name, website, city, source, source_date, raw_blob)│
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2 — ENRICHMENT & GATING                                  │
│  For each company: pull MCA master data, USFDA/CDSCO inspection │
│  records, BSE filings, LinkedIn signals, news, patents.         │
│  Apply E1, E2, hard-disqualifier rules. Output `companies_eligi-│
│  ble` table with full evidence pack as JSON column.             │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 3 — SCORING & QA                                         │
│  Per-company LLM call with structured prompt:                   │
│    {evidence_pack} → {C3..C8 scores + per-criterion citation}   │
│  All borderline (50-70) and all <80%-confidence outputs go to   │
│  human reviewer queue. Sample audit 10% of A-band auto-pass.    │
└─────────────────────────────────────────────────────────────────┘
```

All artefacts live in a single Postgres / DuckDB instance. Every score is reproducible from the evidence pack — so when DT challenges a claim, we can show the exact source URL.

---

## Sourcing — the 12,000 raw rows (Week 1)

| Channel | Expected pull | Why this source |
|---------|---------------|----------------|
| **DSIR R&D-Units list** (downloadable PDF) | ~3,000 | Pre-filter for technical seriousness; near-zero false positives on C3+C4 inferentially |
| **MCA21 NIC-code bulk extracts** for relevant 2-digit codes (20-Chemicals, 21-Pharma, 26-Electronics, 28-Machinery, 32-Other Mfg) filtered to revenue ₹50-500Cr | ~5,000 | Authoritative on size, directors, shareholding |
| **USFDA + EU-GMP + WHO-GMP inspection databases** | ~600 | Hard C7 evidence; near-perfect precision for regulated pharma/devices |
| **CPHI / BioAsia / Aero India / IMTEX / Medical Fair / IMTEX exhibitor lists** (last 2 years) | ~1,500 | C6 growth signal pre-filter |
| **BSE SME + NSE Emerge listed-company directory** (filtered to manufacturers) | ~400 | Authoritative public financials |
| **PLI scheme beneficiary lists** (14 schemes) | ~750 | Hard C5+C6 dual signal |
| **State-level industrial promotion approvals** (TS-iPASS, MAITRI, MIDC, KIADB, GIDC, TIDCO, IIDC, RIICO) | ~1,200 | New facility approvals → real-time C6 |
| **CDSCO manufacturing license database** | ~800 | Pharma/device filter, license-grade signal |
| **DPIIT recognized startup database** filtered to manufacturing | ~500 | Younger-cohort enrichment |
| **Customs export shipment data** (Volza/Datamyne free tier + paid sample) | ~300 | C5 export signal, hard C6 (export growth) |

Total raw: ~14,000. Deduped to **~4,000 unique companies** after fuzzy-match on (name, CIN, website domain).

---

## Enrichment & Gating (Week 2)

For each of the ~4,000, run an enrichment pipeline that pulls:

| Field | Source | Method |
|-------|--------|--------|
| CIN, incorporation date, NIC code, registered office | MCA21 master | API / scrape |
| FY23/FY24 revenue, EBITDA, R&D expense | MCA AOC-4 | XBRL parser |
| Director list with DINs and other directorships | MCA director master | API |
| Shareholding pattern (PE-screen) | MCA AOC-4 / BSE filing | XBRL parser |
| USFDA/CDSCO/EU-GMP status | regulator APIs | scheduled checks |
| LinkedIn employee count, location distribution, IT-role density | LinkedIn Sales Nav API | rate-limited |
| Open job listings | Naukri scraper + LinkedIn jobs | scraper |
| Recent press / news mentions (last 18 months) | Google CSE / NewsAPI | API |
| Patent filings | IP India search | scraper |
| Website tech stack (ERP/CRM mentions on careers page) | direct fetch | regex on careers page |

The output is a **JSON evidence pack** per company. Looks like:

```json
{
  "cin": "U24232TG2003PTC123456",
  "name": "Acme Specialty Synthesis Pvt Ltd",
  "city_of_operations": "Hyderabad",
  "city_evidence": ["mca_registered_office:Hyderabad",
                    "linkedin_hq:Hyderabad",
                    "linkedin_employees_in_hyd_pct:78%"],
  "revenue_band": "Rs.100-300Cr",
  "revenue_evidence": [
    "aoc4_fy23_revenue_inr:182_cr",
    "tofler_fy24_estimate:215_cr"
  ],
  "regulated_market": ["USFDA_VAI_2024", "EU_GMP_2023"],
  "directors": [...],
  "pe_holders_pct": 4.2,
  ...
}
```

E1/E2/auto-disqualifier rules run as deterministic SQL/Python on this evidence pack. **No LLM in the gating path** — these rules are too important to leave fuzzy. Stage 2 → Stage 3 throughput: 2,800 companies survive.

---

## AI-assisted scoring (Week 3 + Week 4 first-half)

For each of the ~2,000 in the scoring pool, one Claude/Gemini call with this structured prompt template:

```
SYSTEM: You are scoring a company against DeepThought's Federer ICP.
You will be given an evidence pack as JSON. Produce a score for each of
6 criteria (C3-C8) with values WEAK, MODERATE, or STRONG, AND a one-line
citation pointing to the specific evidence_pack key that supports that
score. If the evidence is insufficient for a criterion, score it WEAK
and cite "insufficient_evidence". Output strictly as JSON.

USER: { ...evidence_pack... }

OUTPUT SCHEMA:
{
  "C3_differentiated": {"score": "STRONG|MODERATE|WEAK",
                        "citation": "evidence_pack.regulated_market[0]"},
  ...
  "confidence": 0.0-1.0,
  "borderline_concerns": ["..."]
}
```

Why I trust this enough to use at scale:
- **The LLM never invents data** — it only maps evidence_pack fields to score levels. Hallucination surface is small.
- **Confidence + borderline_concerns fields** route uncertain cases to human review automatically.
- **Reproducibility:** same evidence_pack + same model version = same output. Auditable.

Stage 3 → Stage 4 expected throughput: ~1,300 companies score B-band or higher.

---

## Quality control (Week 4 second-half)

Three-tier QA:

**Tier 1 — Mandatory human review**
- All companies with score 50-70 (borderline B/C-band) — about 200 companies
- All companies with confidence <0.8 — about 150
- All companies where `borderline_concerns` is non-empty — about 100

Reviewer (me) reads the evidence pack, optionally pulls fresh info, locks the score. Budget: 8 min/company × 450 companies ≈ 60 hours over 5 days.

**Tier 2 — Random audit on auto-passed A-band**
- 10% sample (~80 companies) reviewed end-to-end. If audit error rate >5%, the entire A-band batch goes back through Tier 1 review.

**Tier 3 — Cross-source contradictions auto-flagged**
- Revenue delta >2x across sources → flag
- City-of-operations claim with only one source → flag
- USFDA-cleared but no GMP certifications listed on website → flag

False-positive controls:
- **PE re-screen** at end of pipeline (since PE deals close mid-month and fresh AOC-4s post during the month)
- **Acquisition watch** — Google Alert + NewsAPI scan for "[company] acquired" / "[company] takeover" run on the final 1,000 list during the last 48 hours of the month
- **Revenue creep** — re-pull FY24 revenue for any company that was right at the Rs.500Cr boundary

---

## Week-by-week plan

### Week 1 — Sourcing & ingestion (Days 1-7)

| Day | Output |
|-----|--------|
| 1 | Pipeline scaffolding (Postgres/DuckDB schema, source-parser stubs, evidence-pack JSON schema) |
| 2-3 | DSIR + MCA-NIC + USFDA + CDSCO parsers running, ~6,000 rows ingested |
| 4-5 | Expo lists + PLI + state portals + customs data parsers, full ~14,000 ingested |
| 6 | Dedup pass; ~4,000 unique companies materialized in `companies_raw` |
| 7 | First-pass review of distribution (city, segment, NIC-code mix) — confirm we have enough volume per target segment; widen sources if any segment is starved |

**Week 1 deliverable:** `companies_raw` table with 4,000 unique candidates and source citations.

### Week 2 — Enrichment & gating (Days 8-14)

| Day | Output |
|-----|--------|
| 8-9 | MCA enrichment running (full director, financials, shareholding pull) |
| 10 | Regulator + LinkedIn enrichment running |
| 11 | News/patent/jobs/website-tech enrichment running |
| 12 | E1/E2/auto-disqualifier rules executed; 2,800 surviving |
| 13 | Manual spot-check of 50 random gate decisions (false-pos / false-neg test); tune rules |
| 14 | Hard-disqualifier rules (size, PE, group, recency) executed; 2,000 in scoring pool |

**Week 2 deliverable:** `companies_eligible` table with evidence packs for 2,000 companies.

### Week 3 — Scoring (Days 15-21)

| Day | Output |
|-----|--------|
| 15 | Scoring prompt finalized; calibration run on 50 known-Federer + 50 known-fail seeds (the 25 from Part A + my fail list of 27); compute confusion matrix; tune prompt until precision ≥90% on calibration set |
| 16-19 | Full scoring pass on 2,000; ~1,300 score B-band or higher |
| 20 | Tier-3 contradiction flags computed; problematic companies re-pulled |
| 21 | Borderline + low-confidence queue (450) frozen for Tier-1 human review |

**Week 3 deliverable:** Auto-scored set with confidence and concern flags.

### Week 4 — QA & delivery (Days 22-30)

| Day | Output |
|-----|--------|
| 22-26 | Tier-1 manual review of 450 companies; ~340 survive |
| 27 | Tier-2 random audit on A-band (80-company sample); accept/reject batch |
| 28 | Final acquisitions/PE/revenue re-screen on top 1,100 candidates |
| 29 | Trim to **1,000**; produce final CSV + per-company evidence JSON + methodology doc |
| 30 | Buffer day — push to DT's pipeline format, sanity-check sample with DT lead |

**Week 4 deliverable:** 1,000 verified Federer-fit companies, each with a full evidence pack.

---

## Team & costs (if asked)

The plan above is sized for **one operator (me) + AI tools**. If DT wants to compress to 2 weeks, the same architecture runs in half the time with one more analyst doing manual QA in parallel.

Estimated tool costs for the month:
- LinkedIn Sales Nav: ~Rs.7,000
- Anthropic Claude API (~2,000 scoring calls × 10K tokens avg): ~Rs.6,000
- Google Search API + NewsAPI: ~Rs.3,000
- Volza/Datamyne sample: ~Rs.5,000 (or free tier)
- Tofler/Zauba premium: ~Rs.4,000
- **Total: ~Rs.25,000** (well under any reasonable internship budget)

MCA bulk-data subscription is the only big-ticket item (~Rs.50K/yr) — but Tofler/Zauba derivative APIs cover most use-cases at lower cost for the first month.

---

## Risks and how I'd handle them

| Risk | Mitigation |
|------|------------|
| LLM scoring drifts when model is updated mid-month | Lock model version (e.g., `claude-3-5-sonnet-20241022`) for entire run; re-calibrate against seed set if forced to upgrade |
| MCA / source APIs go down | Build all parsers as idempotent retries; cache aggressively; have ≥2 sources for every critical field |
| Sourcing universe is too narrow for some segments | Day 7 review checkpoint specifically catches this; can pivot to add expo lists or customs data |
| QA reviewer (me) fatigues at scale | Strict 8-min-per-company timer; break ties toward "REJECT" rather than "PASS" — bias toward precision |
| DT's Federer definition shifts during the month | Lock criteria + scoring rubric on Day 1; if DT updates mid-month, run re-scoring delta only on borderline (50-70) cases — don't redo the whole pipeline |
| Found 1,000 but they cluster too narrowly (e.g., 800 in pharma, 200 elsewhere) | Reserve last 100 slots for diversity quota across DT's basket A/B/C; can drop low-band passes to make room |

---

## What I'd ship at month-end

1. **`final_1000.csv`** — DT's exact required format (same columns as Part A)
2. **`evidence_packs/`** — one JSON per company with all source citations
3. **`pipeline_code/`** — the full ingestion + enrichment + scoring repo, runnable from scratch by next intern
4. **`methodology.md`** — what I sourced, what I dropped and why, calibration metrics
5. **`failed_5000.csv`** — every company we investigated and rejected, with reason — so DT doesn't waste cycles re-discovering them in the next batch

The pipeline is designed to be **rerun monthly** with marginal effort — the second 1000 takes maybe 12 days because the parsers, schema, and prompts are all stable. The third onwards: one analyst-week per 1000.

---

*This proposal optimizes for: (1) **evidence per claim** — every score is auditable, (2) **reproducibility** — the pipeline isn't trapped in my head, (3) **tail-quality** — the 1000th company on the list is only marginally weaker than the 100th, because the pipeline doesn't degrade with volume.*
