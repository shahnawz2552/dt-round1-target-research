# Part B — Question 1: Sourcing Methods Beyond Google
## How to find Federer-fit companies across India at scale

---

The core insight: **Google search optimizes for marketing-active companies, which biases against operator-led specialty manufacturers** — the exact ICP we want. We need sources that index by *operational reality*, not by SEO budget. Below are the channels I would use, organized by signal strength.

---

## Tier 1 — Hard-signal regulatory & government registries (highest precision)

### 1. DSIR (Dept. of Scientific & Industrial Research) Recognized R&D Units list
- **Where:** dsir.gov.in → "Recognised In-house R&D Units"
- **Why for this ICP:** The act of getting DSIR recognition requires evidence of in-house R&D capex, qualified scientific personnel, and an R&D charter. Directly signals **C3 (differentiation via IP/R&D)** and **C4 (technical decision-maker)**. ~3,000+ companies nationally; updated quarterly.
- **Limitation:** Skews older/established. Misses startups <5 years old. Some lapsed recognitions still listed.

### 2. USFDA Orange Book + Establishment Inspection Reports (EIRs)
- **Where:** accessdata.fda.gov + datadashboard.fda.gov/ora
- **Why:** Any Indian site that has cleared a USFDA inspection has — by definition — documented quality systems (C7 Strong) and a regulated product (C3 Strong). The EIR PDFs name the facility, the inspector observations, and the responsible parties.
- **Limitation:** US-export-oriented only. Misses domestic-market specialty chem.

### 3. CDSCO (Central Drugs Standard Control Org) Manufacturing Licenses
- **Where:** cdscoonline.gov.in
- **Why:** Filters by license type — WHO-GMP, EU-GMP, ISO13485, IVD manufacturing. WHO-GMP+ alone is a near-perfect C3+C7 dual signal.
- **Limitation:** Pharma/medical-device only.

### 4. PLI (Production-Linked Incentive) Scheme Beneficiary Lists
- **Where:** scheme-specific portals (PLI-Bulk-Drugs at chemicals.gov.in, PLI-Medical-Devices, PLI-Telecom, PLI-Specialty-Steel, PLI-Drones, etc. — 14 schemes total)
- **Why:** PLI selection requires committed capex, capacity targets, employment commitments. Selected companies are growing **by contract**. C5+C6 dual signal.
- **Limitation:** PLI lists are scheme-specific; have to mine each separately. ~750 selected companies across all schemes.

### 5. State Industrial Promotion Approvals (TS-iPASS, MAITRI Maharashtra, MIDC, KIADB, GIDC, etc.)
- **Where:** state-specific portals (e.g., industries.telangana.gov.in, maitri.maharashtra.gov.in)
- **Why:** Captures *new* facility approvals — the leading indicator for C6 growth signal. Database includes investment quantum, employment, expected commissioning.
- **Limitation:** State-by-state schema differences; need normalized parsing.

### 6. MCA21 Bulk Data + AOC-4 / MGT-7 filings
- **Where:** mca.gov.in (paid bulk-data subscription, ~Rs.50K/yr) or via Tofler/Zauba derivative APIs
- **Why:** Authoritative on revenue band, directors, shareholding pattern (PE-screen), capital structure, R&D expense disclosure. Filterable by NIC (National Industrial Classification) code → can isolate "specialty chemicals" or "biotech reagents" cleanly.
- **Limitation:** AOC-4 lag is 9-15 months; not real-time.

### 7. Patent Office filings (IP India Public Search)
- **Where:** ipindiaservices.gov.in/PublicSearch
- **Why:** Cross-reference applicants in target NIC codes who filed ≥3 patents in the last 5 years → strong C3 signal, almost no false positives.
- **Limitation:** Patent search UX is bad; needs scripting via Selenium / Playwright.

### 8. GST + IEC (Import-Export Code) data
- **Where:** GST public lookup + DGFT IEC database (dgft.gov.in)
- **Why:** Active IEC = company exports. Cross-tabbed with HS code → "exports specialty chemicals" or "exports diagnostic kits". Export activity is a hard C5+C6 signal.
- **Limitation:** GST/IEC don't disclose revenue.

---

## Tier 2 — Industry concentration sources (event-driven)

### 9. Trade expo exhibitor directories
- **Target expos by basket:**
  - Pharma/specialty chem: **CPHI India**, **CPHI Worldwide India pavilion**, **InformEx**, **Pharmac India**
  - Biotech: **BioAsia (Hyderabad, annual)**, **India Biopharma Conclave**
  - Defence/electronics: **Aero India (Bengaluru, biennial)**, **DefExpo**, **ELECRAMA**
  - Medical devices: **Medical Fair India**, **AIMED industry summit**
  - Specialty agri: **Agri Intex**, **India International Seed Trade Conference**
  - Precision engineering: **IMTEX**, **Engimach**
  - Technical textiles: **Techtextil India**, **Garmenttech**
- **Why:** Booth fees of Rs.2-10L pre-filter for **C6 (growth) + financial seriousness**. Exhibitor lists are publicly available (some require email registration).
- **Limitation:** Biases against bootstrapped MSMEs that can't afford booths.

### 10. Industry association member lists
- **Targets:** ABLE-India (biotech), IPA (Indian Pharma Alliance), IDMA (Indian Drug Manufacturers), AIMED (medical devices), ICC (Indian Chemical Council), AICTAS (technical textiles), ISMA (machinery), ACMA (auto components), CITI (cotton textile).
- **Why:** Membership = signals industry seriousness. Many associations publish member directories with city, products, certifications.
- **Limitation:** Membership data is sometimes paywalled or requires association affiliation to access.

### 11. State biotech / MSME cluster portals
- **Targets:** Genome Valley (Hyderabad), Chakan/Talegaon (Pune), Pithampur (Indore), Hosur (Bengaluru-Tamil Nadu border), TICEL (Chennai biotech), Ankleshwar/Vapi (Gujarat chem clusters).
- **Why:** Cluster authorities maintain tenant directories — these are pre-segmented Federer pools.
- **Limitation:** Quality of public data varies by state.

---

## Tier 3 — People-graph and inference sources (high creativity, harder to scale)

### 12. LinkedIn Sales Navigator — reverse pivot from known Federer companies
- **Why:** Employees who left Granules / Divis / Bharat Biotech often joined or founded Federer-band companies. Pivot from "second-degree connections of known-Federer execs" surfaces the long tail.
- **Method:** Use Sales Navigator's "people also viewed" + Boolean search filters (location + industry + headcount 50-500 + "founder/MD/CEO" + "ex-[BigCo]").
- **Limitation:** Sales Nav is paid (~Rs.7K/mo); rate-limited.

### 13. MCA director DIN cross-reference
- **Why:** Directors on Federer boards often sit on 2-3 more boards. Pulling director-DIN graph from MCA reveals adjacent unlisted companies. Especially powerful for finding **subsidiaries that aren't tagged as such** in marketing.
- **Method:** Scrape DIN data, build a director-company bipartite graph, walk 2 hops from known-Federer seeds.
- **Limitation:** Director overlap doesn't guarantee similar companies — needs filtering.

### 14. Job-board reverse search (Naukri, LinkedIn Jobs)
- **Method:** Boolean search for "SAP S/4HANA" + "manufacturing" + "Hyderabad" with employer-size filter 50-500 → directly surfaces companies that have invested in ERP (C7 Strong) and are hiring (C6 signal).
- **Why:** Companies investing in SAP at this revenue band are statistically rare and Federer-aligned.
- **Limitation:** Misses companies on Tally/Oracle NetSuite/local ERPs.

### 15. Government tender award data
- **Where:** eprocure.gov.in, GeM (Government e-Marketplace) winner lists, defence tender awards (DPP).
- **Why:** Companies that win Indian Navy / ISRO / DRDO / Indian Railways / state PSU tenders for specialty products are nearly always Federer-fit (defence vendor empanelment requires technical & systems maturity).
- **Limitation:** Defence vendors often don't market — names show up only on tender award PDFs.

### 16. R&D tax-incentive disclosure in audited financials
- **Why:** Section 35(2AB) weighted deduction (DSIR-linked) shows up in MCA AOC-4 as "R&D expense"  >2% of revenue. Filter MCA NIC-code-based extracts on this ratio → finds companies investing meaningfully in R&D.
- **Limitation:** AOC-4 schema can be inconsistent for unlisted entities.

---

## Tier 4 — Unconventional / creative sources

### 17. Pollution Control Board "Consent to Operate" filings
- **Where:** state PCB websites (TGSPCB, GPCB, MPCB)
- **Why:** Mandatory for any manufacturing facility. Filings disclose plant capacity, products, raw materials. **Strongest E1 evidence available** — proves the company is a real producer, not a trader.
- **Limitation:** UX is poor; many states keep these as scanned PDFs.

### 18. Bank-loan publication notices (Form CHG-1 charge filings)
- **Where:** MCA charges database
- **Why:** Term-loan filings name "purpose of loan" — "expansion of facility", "machinery import", etc. Direct C6 facility signal, often months before press releases.
- **Limitation:** Requires charge-data API access.

### 19. Customs export shipment data (Volza, Datamyne, Importgenius)
- **Why:** Disclose actual shipment-level exports — frequency, destination, HS code. Strongest C5 (export tailwind) and C6 (growing exports) signal possible.
- **Limitation:** Paid databases (~Rs.40K-1L/yr), but free trial often sufficient for sample lookups.

### 20. PhD thesis acknowledgments + academic-industry collaboration databases
- **Where:** Shodhganga (shodhganga.inflibnet.ac.in), DBT-funded project lists, BIRAC grant recipients
- **Why:** Companies that sponsor PhD work or partner on DBT/BIRAC grants are R&D-active and academia-connected — strong C3+C4 inference.
- **Limitation:** Smaller volume; useful as enrichment, not primary funnel.

### 21. Founder podcast / YouTube interview index
- **Method:** Search "[NIC-code keyword] founder interview" on YouTube + podcast platforms (3one4 Capital, The Ken, Founder Thesis, Maed in India).
- **Why:** A founder who has done a 60-min interview signals confidence, communication ability, and willingness to be public — useful proxy for Federer cultural fit. Also exposes operational details rarely on websites.
- **Limitation:** Discovery-only, can't enumerate.

---

## How these stack together for production sourcing

A realistic production funnel uses **DSIR + MCA-NIC + USFDA/CDSCO + Expo lists + TS-iPASS** as the primary universe builders (Tier 1+2), then **LinkedIn Sales Nav + director-DIN-graph + job-board reverse search** as enrichment for the long tail (Tier 3), and **PCB filings + customs data + charge filings** as evidence-deepening for the final QA pass (Tier 4).

This is the architecture I propose to scale to 1000 companies in the proposal in Q2.

---

*Limitation common to all of the above: each source has its own access friction. The compounding value isn't in any single source — it's in **deduplication + cross-validation across 5+ sources**, which is what kills the false-positive rate that pure-Google sourcing produces.*
