# Shortlist of Candidates To Investigate
## Companies surfaced during research — verification needed before adding to final CSV

**Read this if you're the candidate completing the submission:** the main `companies.csv` has 13 well-evidenced Federer candidates and one GAP row marking the 12 remaining slots. To get to 25 passing companies, investigate the names below (each is a real Hyderabad specialty chem/pharma/biotech company surfaced during my research) — verify on MCA + company website + LinkedIn — and add to the CSV the ones that pass.

For each candidate I've documented (a) what's promising, (b) what to verify before scoring, (c) where to find the data.

---

## Tier A — Highest priority (most likely to pass with verification)

### 1. Apitoria Pharma Pvt Ltd
- **Website:** aurobindo.com/our-business/apitoria
- **Why interesting:** Hyderabad-based specialty pharma + biologics, focused API CDMO arm, USFDA-inspected
- **🚫 CRITICAL FAIL CHECK:** Wholly-owned subsidiary of Aurobindo Pharma (per CNBC TV18 + Aurobindo's own page). **Auto-disqualifier (subsidiary).** Move to fail list, do not include in CSV.

### 2. Pharmaids Pharmaceuticals Limited
- **Website:** Search BSE for ticker
- **Why interesting:** Incorporated 1989 in Hyderabad; supplier of specialty grade chemicals, skin care, hospital care, generic products in Orthopedic, Neuro, Gastro therapy areas
- **Verify:** BSE filings for revenue band, shareholding pattern (PE check), latest activity
- **Source:** Indiainfoline summary

### 3. Macro International Limited
- **Why interesting:** BSE-listed Hyderabad pharma micro-cap; bulk drug + intermediate exposure per MD&A
- **Verify:** Latest annual report on BSE; shareholding pattern; producer-vs-trader status
- **Source:** Indiainfoline Macro International MD&A

### 4. Aspiro Pharma Limited
- **Why interesting:** Genome Valley tenant per Modi Properties Genopolis listing; Hyderabad
- **Verify:** Producer status, latest revenue, ownership independence on MCA
- **Source:** Modi Properties Genopolis tenant listing; Crunchbase stub

### 5. Pochiraju Industries Limited
- **Why interesting:** BSE/MCA-listed Hyderabad pharma; multi-decade family operation
- **Verify:** Current operating status, segment fit, financials, family vs PE ownership
- **Source:** Search Hyderabad small-cap pharma

### 6. Symbiotec Pharmalab Limited
- **Why interesting:** Specialty steroid hormone & intermediate maker; if Hyderabad-primary, strong C3 fit
- **Verify CITY:** Likely Indore-primary (TS auto-fail). Verify before including.
- **Source:** Search BSE listings

### 7. Sreepathi Lab Pvt Ltd
- **Why interesting:** Hyderabad CMO+CRO hybrid for APIs/intermediates/fine chemicals; Punjagutta location
- **Verify:** Whether this is the same entity as Sreepathi Pharmaceuticals (already in CSV) or a separate sister entity
- **Source:** IndiaMart Sreepathi-Lab supplier profile

### 8. Astrix Laboratories
- **Verify:** Hyderabad operational presence, segment, ownership independence

### 9. Ajay Bioventures (verify)
- **Verify:** Hyderabad operations, segment

### 10. Vamsi Labs (verify)
- **Verify:** Hyderabad operations, ownership

---

## Tier B — Surfaced as candidates but verify carefully

### 11. Trimurthi Drugs / Novelix Pharmaceuticals (BSE)
- **Why interesting:** BSE-listed Hyderabad pharma, recent rebrand Oct 2024, turnaround narrative
- **🚫 CRITICAL FAIL CHECK:** Pitchbook lists primary business as **"Trading of Pharmaceuticals and related products"** — likely fails E1 Producer gate. Verify whether rebrand has shifted strategy to in-house manufacturing.

### 12. Krittik Pharma
- **🚫 CRITICAL FAIL CHECK:** Website language ("robust network with top-tier API manufacturers in India allows us to deliver") strongly suggests trader/distributor model. Verify on MCA NIC code.

### 13. Synix Labs Pvt Ltd
- **Website:** synixlabs.com
- **Why:** Hyderabad custom synthesis specialist; producer in correct segment
- **Verify:** Revenue band, certifications, founder profile — public info is thin

### 14. Glochem Industries (verify)
- **Verify:** Hyderabad operations, ownership

### 15. Sun Pharma Advanced Research Co (verify Hyderabad presence)
- **Verify:** Sun Pharma is Mumbai-HQ but has Hyderabad operations — may fail E2 if Hyderabad isn't primary

### 16. Lasa Supergenerics (BSE)
- **Verify CITY:** Likely Mumbai-primary; verify

### 17. Centaur Pharmaceuticals (verify)
- **Verify CITY:** Likely Mumbai/Pune; verify

### 18. Indoco Remedies (BSE)
- **Verify CITY:** Mumbai-primary — likely fails E2

### 19. Sai Mirra Innopharm (verify)
- **Verify CITY:** Chennai-primary (won't fit Hyderabad)

### 20. Yusan Pharma
- **Verify:** Hyderabad operations, segment, size

---

## Tier C — Niche / specialty leads worth investigating

### 21. Krishgen Biosystems
- **Why:** Diagnostics reagents/antibodies — could fit Specialty diagnostics segment if Hyderabad
- **Verify CITY:** Mumbai-primary likely; verify

### 22. Bioneeds India (Bengaluru, skip if Hyderabad-only)

### 23. Theramyt Novobiologics (verify)

### 24. Hester Biosciences (Ahmedabad — skip)

### 25. PlasmaGen Biosciences
- **Why:** Specialty biologics; Vins Bioproducts led Rs.150Cr investment Dec 2024 at Rs.1,500Cr valuation
- **Verify CITY:** Likely Bengaluru. May fail E2.

---

## How to verify a candidate (checklist for each name above)

1. **Website check** — does the company have a real website with a manufacturing/products page (not just sales)?
2. **Hyderabad operational presence** — Contact Us page address, LinkedIn HQ tag, MCA registered office must show Hyderabad/Telangana or Sangareddy/Medak/Ranga Reddy district
3. **MCA Master Data check** — search by name on `mca.gov.in/MyMCAIB/master/searchByName.do`; confirm CIN, NIC code (24xxx for chemicals, 21xxx for pharma), incorporation date, status = Active
4. **Shareholding / PE check** — pull latest AOC-4 from MCA; if any single non-promoter institutional holder >25%, **likely fail**
5. **Revenue band check** — pull the latest filed AOC-4 turnover from MCA, OR Tofler/Zauba estimate; if >Rs.500Cr, **fail size**; if <Rs.30Cr also OK but flag as small
6. **USFDA / CDSCO / DSIR check** — search the regulator databases for the company name; presence is a strong C3 + C7 signal
7. **LinkedIn check** — search company name; check (a) HQ city, (b) employee count, (c) IT/SAP-related job postings (C7 signal), (d) 5+ open jobs (C6 signal), (e) gen-2 visibility on leadership team
8. **Recent news search** — Google "[company name]" with date filter (last 18 months); look for facility expansion, capital raise, regulatory clearance, hiring announcements
9. **Director cross-check** — pull director list from MCA; if same DIN appears on a known PE-controlled company, flag

A typical full verification = 10-15 minutes per candidate.

---

## Companies confirmed FAILED during research (for reference; already in fail-list.md)

These came up as Hyderabad specialty pharma candidates but were eliminated:

| Company | Why failed |
|---------|------------|
| Apitoria Pharma | Aurobindo subsidiary |
| Aragen Life Sciences | Goldman Sachs ~31% + Quadria + Avendus PE-controlled |
| Apollo Micro Systems | FY26 Rs.904Cr — over Rs.500Cr |
| Astra Microwave Products | Over Rs.500Cr |
| Auctus Pharma | Acquired by Granules India 2013 |
| Avra Laboratories | Advent-acquired 2022 |
| Bharat Biotech | Over Rs.500Cr |
| Bharat Serums | Mumbai HQ + Mankind acquired |
| Biological E | Over Rs.500Cr |
| Cohance Lifesciences (formerly RA Chem Pharma) | Advent-controlled |
| Divis Laboratories | Over Rs.500Cr |
| Dr Reddy's Laboratories | Over Rs.500Cr |
| Eugia Pharma Specialities | Aurobindo subsidiary |
| Globion India | Virbac (French MNC) acquired 2023 |
| Gland Pharma | FOSUN-controlled |
| Granules India | Over Rs.500Cr |
| GVK Bio (now Aragen) | PE-controlled |
| HBL Engineering / HBL Power | Over Rs.500Cr |
| Hetero Drugs | Over Rs.500Cr |
| Indian Immunologicals | NDDB / PSU subsidiary |
| Krittik Pharma | Trader (likely) |
| Lakshmi Farmachem | Distributor |
| Laurus Labs | Over Rs.500Cr |
| MSN Laboratories | Over Rs.500Cr |
| MTAR Technologies | Over Rs.500Cr |
| Natco Pharma | Over Rs.500Cr |
| Neuland Laboratories | Over Rs.500Cr |
| Optimus Pharma | PAG/Sekhmet acquired |
| RA Chem Pharma | Advent-acquired |
| Sai Life Sciences | TPG-controlled |
| Sekhmet Pharmaventures | PE platform itself |
| Sequent Scientific (now Viyash) | Carlyle-controlled |
| Shantha Biotechnics | Sanofi subsidiary |
| Suven Pharma | Advent-acquired |
| Symed Labs | Carlyle/Viyash acquired 2021 |
| Vimta Labs | CRO/testing lab — fails E1 |
| Virupaksha Organics | FY25 Rs.811Cr — over Rs.500Cr |
| Vishnu Chemicals | FY25 Rs.1,098Cr — over Rs.500Cr |
