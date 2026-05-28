# Hand-Drawn Diagram — What to Draw on Paper

**This is the single most important deliverable in your application.** DT explicitly says applications without a hand-drawn diagram in Internshala chat are not reviewed.

The diagram must show your 1000-company-in-30-days plan **visually**. Below is a layout you can copy to paper. **Do not print and trace** — the point is the marks of your hand. Use a black pen, draw freely. Imperfection is the signal.

---

## Page setup

- **Take a plain A4 sheet** (any unruled paper works).
- **Hold it landscape** (long edge horizontal).
- **Use one black pen** (gel pen / ballpoint). Optional: one second color (red or blue) for highlights.
- **Time budget: 12-15 minutes.** Don't make it pretty. Make it thought-through.

---

## What to draw — section by section

### Top of page — Title strip (1 line)

> **1000 Federer-Fit Companies in 30 Days — Pipeline Plan**

Underline once.

### Left third — The Funnel (vertical pyramid)

Draw 5 stacked horizontal bands, widest at top, narrowest at bottom. Inside each, write the count + stage name:

```
┌──────────────────────────────┐
│   12,000 raw rows            │  Sources
├──────────────────────────────┤
│   4,000 deduped universe     │  Stage 1
├──────────────────────────────┤
│   2,000 eligible             │  Stage 2-3 (gates + disqual)
├──────────────────────────────┤
│   1,300 first-pass scored    │  Stage 4 (LLM scoring)
├──────────────────────────────┤
│   1,000 verified ✓           │  Stage 5 (human QA)
└──────────────────────────────┘
```

To the right of each band, write the % yield (e.g., "33%", "70%", "65%", "77%").

### Middle third — The 4-week timeline (horizontal bar)

Draw four boxes side-by-side, labelled **W1 W2 W3 W4** at the top.

In each box, write 3-4 short bullets:

| W1 | W2 | W3 | W4 |
|----|----|----|----|
| - DSIR pull | - MCA enrich | - Calibration | - Tier-1 QA (450) |
| - MCA NIC pull | - LinkedIn data | - Score 2,000 | - Tier-2 audit (80) |
| - USFDA / CDSCO | - Apply E1/E2 | - Conf flags | - PE re-screen |
| - Expo lists | - Hard disqualif | - Borderline queue | - Ship 1,000 |

Below the four boxes, draw a small arrow flowing left → right.

### Right third — Sources fan (radial)

Draw a small circle in the middle labelled **"Universe ~4,000"**.

Around it, draw 8-10 lines radiating outward, each ending in a labelled box for one source. Suggested labels (use abbreviations):

- DSIR R&D list
- MCA NIC 20/21/26
- USFDA / CDSCO
- BSE SME + NSE Emerge
- CPHI / BioAsia / Aero India
- PLI 14 schemes
- TS-iPASS / MAITRI / MIDC
- LinkedIn Sales Nav (snowball)
- Customs (Volza)
- Patent filings (IP India)

Next to each source line, write the rough count (e.g., "DSIR: 3K", "MCA: 5K").

### Bottom-left — Quality controls box

Draw a box. Inside, write:

```
QA TIERS
T1 — Borderline 50-70 (450 cos)
T2 — Random audit A-band (10%)
T3 — Cross-source flags (auto)

PE re-screen on Day 28
Acquisition watch (NewsAPI)
Revenue boundary re-pull
```

### Bottom-middle — The scoring engine

Draw a small rectangle labelled **"AI Scoring"**. Show:
- Arrow IN from the left labelled "Evidence Pack (JSON)"
- Arrow OUT to the right labelled "C3-C8 + confidence + flags"

Below the box, write:

```
Claude / Gemini
Locked model version
Citations mandatory
"Insufficient evidence" → WEAK
```

### Bottom-right — Outputs box

Draw a box. Inside, list the 5 deliverables:

```
DELIVERABLES
1. final_1000.csv
2. evidence_packs/ (JSON)
3. pipeline_code/
4. methodology.md
5. failed_5000.csv
```

### Anywhere — Three callouts (in red/second color, if you have one)

Pick spots in the white space and write these reminders, with an arrow pointing to the relevant section:

1. **"Evidence per claim — no score without source URL"** → point to the AI Scoring box
2. **"30% yield assumption — universe sized for slack"** → point to the Funnel
3. **"Pipeline is rerunnable — month 2 is faster"** → point to the Outputs box

---

## A simple ASCII layout to follow

This is what the page should roughly look like before you draw it (don't trace, just use as guide):

```
+────────────────────────────────────────────────────────────────────+
│   1000 Federer-Fit Companies in 30 Days — Pipeline Plan            │
+────────────────────────────────────────────────────────────────────+
│                                                                    │
│   ╔══════════╗      W1   W2   W3   W4         ⊙ Universe 4K        │
│   ║12K raw   ║     ┌──┐┌──┐┌──┐┌──┐         /│ \ \ \ \             │
│   ╠══════════╣     │  ││  ││  ││  │       DSIR MCA USFDA BSE       │
│   ║4K univ.  ║     │  ││  ││  ││  │            CPHI PLI TS-iPASS   │
│   ╠══════════╣     └──┘└──┘└──┘└──┘            LinkedIn Customs    │
│   ║2K elig.  ║       →    →    →                                   │
│   ╠══════════╣                                                     │
│   ║1.3K scd. ║                                                     │
│   ╠══════════╣      ┌────────────────┐                             │
│   ║1K ✓      ║      │ AI Scoring     │                             │
│   ╚══════════╝      │ Evidence→Score │                             │
│                     └────────────────┘                             │
│                                                                    │
│   ┌────────────┐    Claude / Gemini     ┌─────────────────┐        │
│   │ QA Tiers   │    Citations mand.     │ Deliverables    │        │
│   │ T1 T2 T3   │                        │ 1. CSV          │        │
│   │ PE rescr.  │    ⚠ Evidence!         │ 2. Evidence     │        │
│   │ Acq watch  │                        │ 3. Code         │        │
│   └────────────┘                        │ 4. Methodology  │        │
│                                         │ 5. Failed list  │        │
│                                         └─────────────────┘        │
+────────────────────────────────────────────────────────────────────+
```

---

## What the diagram is signalling to the DT recruiter

The recruiter will spend ~30 seconds on the photo. They are looking for **5 things**:

1. **Funnel logic** — do you understand yield rates and source-sizing?
2. **Time logic** — does each week build on the last, or is it a checklist soup?
3. **Source diversity** — did you go beyond Google? (8-10 named sources is the magic number)
4. **Quality control** — is there an explicit QA layer, or are you handing them garbage?
5. **Hand-drawn-ness** — can they see your pen pressure, your scratchy lines, the moment you re-drew an arrow? That proves you thought, not just typed.

**Things that will get your application rejected even with this diagram:**
- Drawn in Figma / Lucidchart / Whimsical and printed (digital lines have uniform pressure)
- Photo of a screen showing a digital diagram (DT specifies "photo of hand-drawn")
- Just a list of bullet points on paper (must be visual / spatial, not textual)
- Too clean — looks like you traced a printout

**Pro-move:** sign and date it in the bottom-right corner. Costs 2 seconds, makes it feel earned.

---

## Photographing the diagram

- Daylight near a window, or a desk lamp at a 45° angle
- Photo from directly above — not angled
- Full page in frame, plus ~1cm margin
- Phone camera in default mode (not "Document scan" — that processes the image and erases the hand-drawn quality DT is looking for)
- Send the original photo to Internshala — don't compress, don't apply filters

---

## What if you don't have a printer / scanner / good camera?

- Phone photo is fine. JPEG. ~2-4 MB. Internshala accepts this.
- If the photo looks dim, take it again with the phone flash off and a window light source.
- If the page has a tea stain or a coffee mark, leave it. Authenticity helps.
