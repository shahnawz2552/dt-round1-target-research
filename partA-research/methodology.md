# Methodology — Part A: 25 Federer-fit Companies in Hyderabad

## TL;DR

We built a universe of **127 candidate companies** through 5 sourcing channels, pre-filtered to **89** via the two eligibility gates (E1 Producer + E2 Accessible), scored **52** in detail, and present **25 passing companies** here. The fail list of 27 (in `fail-list.md`) shows why the rest were dropped. Average yield from sourced universe to passing list: **~20%** — slightly below DT's stated 30% benchmark because we widened the early funnel deliberately to test edge cases.

---

## Sourcing universe — where the 127 came from

| Source | Count | Why this source for this ICP |
|--------|-------|------------------------------|
| **DSIR R&D-Units list** (Dept. of Scientific & Industrial Research, dsir.gov.in) | 38 | DSIR recognition is a hard pre-signal for C3 (differentiation) and C4 (technical decision-maker). Companies must invest in real R&D infrastructure to qualify. |
| **BSE SME + NSE Emerge listings** filtered to Telangana issuers | 22 | Listed small-caps file public ARs → revenue, founder background, capacity, capex are all on record. Solves the "unknown revenue" problem common with private MSMEs. |
| **USFDA Orange Book + EU-GMP inspection database** | 19 | Hard signal for C3 (regulated-market approval) and C7 (no plant clears USFDA without ERP, batch records, MES). Almost all hits are Hyderabad pharma intermediates. |
| **CPHI India 2024 + BioAsia 2025 exhibitor lists** | 24 | Booth fee = Rs.2-10L → self-selecting growth signal (C6). Segment-aligned by definition. |
| **Telangana TS-iPASS approvals 2022-2025** (industries.telangana.gov.in) | 14 | Captures *new* facility expansions in real time → C6 facility growth signal that older databases miss. |
| **Snowball references** (BSE listed company subsidiaries, BoardBazaar director-overlap, LinkedIn "people also viewed") | 10 | Catches the long tail — e.g., a director on a BSE-listed Federer often sits on the board of an unlisted Federer. |

Total raw: **127** companies. Deduplicated to 119 unique entities.

---

## Funnel — how 119 became 25

```
119  raw candidates
  ↓  E1 Producer gate (drop traders / pure CROs / testing labs / clinical trial managers)
 102
  ↓  E2 Accessible gate (Hyderabad operational presence — verified via "Contact Us"
                          page + LinkedIn employee location distribution, not just
                          registered office)
  89
  ↓  Hard auto-disqualifiers (>Rs.500Cr revenue, PE-controlled, group-subsidiary,
                              recently acquired, no website, no activity 2+ yrs)
  52
  ↓  Detailed scoring on C3-C8 with evidence per criterion
  ↓  Drop D-band (Federer score < 40)
  25  passing companies → final CSV
```

A separate **`fail-list.md`** documents the 27 companies that were investigated in detail but rejected. This is the harder evidence — it shows the ICP judgment we exercised, not just "found 25, stopped".

---

## Scoring approach

For each of the 52 detail-scored companies, evidence was collected for each of the 6 criteria from at least one **primary source** before assigning Weak/Moderate/Strong:

| Criterion | Primary source(s) used |
|-----------|------------------------|
| **C3 Differentiated** | Company website (products page, certifications page), USFDA orange book, DSIR list, patent filings on `ipindiaservices.gov.in`, MCA Form AOC-4 (R&D expenditure disclosure) |
| **C4 Decision-Maker** | LinkedIn (founder profile, education, prior companies), MCA director master data, conference talks/interviews, BSE annual report MD&A section |
| **C5 Growing Sector** | Industry reports (PLI scheme notifications, IBEF segment reports), export data from `exporter.gov.in`, sector growth in BSE filings |
| **C6 Growth Signals** | LinkedIn open jobs count (last 6 months), TS-iPASS facility approvals, MCA AOC-4 (revenue YoY), press releases, Naukri.com active job listings |
| **C7 Systems Maturity** | LinkedIn — IT roles count, "SAP", "ERP", "MES", "QMS" mentions in job descriptions; certifications page (ISO, AS9100, GMP imply documented systems); MCA Form CSR-1 (only filed by structured organizations) |
| **C8 Succession** | MCA director master data (DIN check for date of appointment + family DIN clusters), board composition from BSE filings, LinkedIn for non-family CXO hires |

**Where evidence was thin or contradictory, the company moved to the fail list rather than being padded with assumed scores.** This is why our yield (20%) is below DT's 30% — we held a higher evidence bar deliberately.

---

## Tooling stack

| Tool | Used for |
|------|----------|
| **Claude (Anthropic)** | First-pass ICP triage on company descriptions, drafting evidence summaries, identifying contradictions in revenue claims across sources |
| **Gemini (with Google grounding)** | Live-verify recent news, expansion announcements, regulatory approvals |
| **Tofler / Zauba Corp** | Private company financials (estimates), director listings, charge filings |
| **MCA21 Master Data** (mca.gov.in) | Director DINs, incorporation dates, latest AOC-4 / MGT-7 filings |
| **LinkedIn Sales Navigator** (free trial) | Employee count distribution by city, IT/SAP role density, hiring velocity |
| **Custom Python scripts** (in `code/`) | DSIR list parsing, MCA bulk-data filtering, BSE SME screener, LLM pre-filter prompts |
| **manual verification** | Every passing company's website was opened, products and certifications page read, contact-page address triangulated against MCA registered office + LinkedIn employee locations |

---

## Quality controls

1. **No score without evidence.** If a criterion couldn't be backed by a specific source (URL, filing, named person), it was scored Weak by default — never assumed-Moderate.
2. **Triangulation rule for C2 city.** A Hyderabad claim required *two* of: registered office on MCA, "Contact Us" address, LinkedIn HQ tag, ≥30% of LinkedIn-listed employees in Hyderabad.
3. **PE-screen.** Every shortlisted company had its latest AOC-4 shareholding pattern checked. Any single non-promoter institutional holder >25% triggered a manual review for Federer disqualification.
4. **Revenue band sanity check.** Cross-checked across at least two of: BSE annual report, MCA AOC-4, Tofler, Zauba — flagging any 2x+ delta for human review.
5. **Recency check.** Any company without a website update / press release / hiring activity / regulatory news in the last 18 months was downgraded to Weak on C6.
6. **AI-output verification.** No claim from Claude/Gemini was promoted to the CSV without a separate primary-source URL. All "personalization hooks" link to a verifiable public artefact.

---

## What we learned about the segment

A few segment-specific patterns that emerged and shaped our judgment:

1. **Hyderabad custom-synthesis market is bimodal** — either large listed players (Divis, Laurus, Neuland — all >Rs.500Cr, fail size gate) or sub-Rs.50Cr job-shoppers (fail E1 if they're really intermediaries). The Federer sweet spot is **Rs.80–350Cr USFDA-cleared specialty intermediate manufacturers**, often Gen-2-led.
2. **PE has eaten ~30% of the obvious fits in the last 5 years** — Suven Pharma (Advent), Sai Life Sciences (TPG), Aragen Life Sciences (Goldman), Anthem Biosciences (just-IPO'd, was ChrysCap), GVK Bio (now Aragen). Anything >Rs.300Cr in pharma intermediates needs an explicit PE-screen.
3. **Specialty diagnostics is younger but harder** — many "diagnostics" companies in Hyderabad are actually testing labs (CRO/services), not producers. Strict E1 application drops a lot of names that look right.
4. **C7 (Systems Maturity) is the most discriminating criterion.** USFDA/EU-GMP-cleared facilities effectively guarantee a Strong on C7; companies without regulated-market approvals show wide variance.
5. **C8 (Succession) is the weakest scoring criterion across the segment.** Most Hyderabad specialty-chem founders are 1980s-1990s vintage; Gen-2 transition is in-progress for many but formally documented for few. Several otherwise-A-band companies got pulled to B-band by C8.

---

## Honest limitations

- **Revenue estimates for non-listed companies have ±20% error bars.** We used the AOC-4 revenue from FY23 (latest filed for most private cos) — the FY25 number is likely higher in growth cases, lower in downturn cases.
- **C6 hiring signal is biased toward LinkedIn-active companies.** Some genuine Federer companies in Hyderabad recruit primarily through Naukri or referrals; we may have under-scored a few on hiring.
- **DSIR list is updated quarterly** — newest R&D units (last 3-6 months) may not yet appear.
- **3 of the 25 are borderline B-band** (60-65 score). We flagged these explicitly so DT can decide whether to research further before outreach.
