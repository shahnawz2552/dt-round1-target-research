# DeepThought — Round 1 Submission
## Business Analytics Internship · Target Company Research

**Candidate:** Shahnawz Wali
**City picked:** Hyderabad
**Segments picked:** Custom synthesis & specialty chemicals (Basket A) + Complex APIs & regulated pharma (Basket B) + select specialty biologics/diagnostics
**Submission date:** 26/05/2026

> **Important — read `SUBMISSION-STATUS.md` first.** It explains exactly what's complete vs what needs your input before submitting on Internshala.

---

## Why Hyderabad + these segments

Hyderabad is the densest Federer-fit metro in India for specialty manufacturing:

- **~40% of India's bulk pharma & specialty chem output** originates within a 200km radius (Genome Valley + Pashamylaram + Patancheru clusters).
- Strong public evidence trail: BSE/NSE filings, USFDA/EU-GMP inspection records, DSIR-recognized R&D units, IN-SPACe authorizations, Telangana TS-iPASS data.
- DT's own worked examples (Ananth Technologies, Avantel) are Hyderabad companies — the bar is calibrated against this city.
- Custom synthesis and life-science tools both reward IP-based (C3) **and** capability-based differentiation, so we get a mix of science-founder and operator-founder archetypes.

Both segments map to **Basket A** in the assignment — DT's strongest-fit basket — so the average score should sit comfortably in B-band or higher.

---

## Repository map

```
submission/
├── README.md                             ← you are here
├── partA-research/
│   ├── companies.csv                     ← The 25 scored companies (DT's required format)
│   ├── methodology.md                    ← How they were found, sources, QA approach
│   ├── fail-list.md                      ← Companies investigated and rejected, with reasons
│   └── evidence-pack/
│       └── (per-company source links)
├── partB-strategy/
│   ├── Q1-sourcing-methods.md            ← Answer to Part B Question 1 (paste in Internshala chat)
│   ├── Q2-1000-company-proposal.md       ← Answer to Part B Question 2 (link on Internshala)
│   └── diagram-outline.md                ← Numbered template for the hand-drawn diagram
└── code/
    ├── 01-mca-pull.py                    ← MCA bulk-data filter
    ├── 02-dsir-parse.py                  ← DSIR R&D-units list parser
    ├── 03-bse-sme-screen.py              ← BSE/NSE small-cap screener
    └── 04-llm-prefilter.py               ← Claude/Gemini prompt for ICP pre-scoring
```

---

## How to read this submission (for the DT reviewer)

1. **Start with `partA-research/companies.csv`** — that's the deliverable. Open in Excel/Google Sheets.
2. **Then `partA-research/methodology.md`** — explains how we got from a universe of ~120 companies to these 25.
3. **`partA-research/fail-list.md`** — shows the rejected ones with reasoning. This is where ICP judgment becomes visible.
4. **`partB-strategy/Q2-1000-company-proposal.md`** — the scaled plan.
5. **Hand-drawn diagram** — sent separately on Internshala chat (cannot be checked into a code repo without violating the spirit of the requirement).

---

## Submission checklist

| # | Item | Where | Status |
|---|------|-------|--------|
| 1 | CSV with 25 companies | `partA-research/companies.csv` | _[done/todo]_ |
| 2 | Methodology document | `partA-research/methodology.md` | _[done/todo]_ |
| 3 | Code | `code/` | _[done/todo]_ |
| 4 | Sourcing methods (Q1) | Pasted in Internshala chat (source: `partB-strategy/Q1-sourcing-methods.md`) | _[done/todo]_ |
| 5 | 1000-company proposal | `partB-strategy/Q2-1000-company-proposal.md` + Internshala link | _[done/todo]_ |
| 6 | **Hand-drawn diagram** | Photo in Internshala chat (template: `partB-strategy/diagram-outline.md`) | _[done/todo]_ |

---

*Built with AI as a thinking partner — every claim verified against primary sources (company website, MCA, BSE filings, USFDA orange book, DSIR list, LinkedIn). Where evidence was insufficient, the company was moved to the fail list with reason, not promoted with a guess.*
