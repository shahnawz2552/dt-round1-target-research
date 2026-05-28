"""
LLM-Assisted ICP Scoring (C3 - C8)
-----------------------------------
Takes enriched evidence-pack JSON and asks Claude / Gemini to score each
company on the 6 Federer criteria with mandatory citations to the evidence pack.

Why we trust LLM scoring at scale:
1. The LLM never invents data. It only maps evidence-pack fields -> score levels.
2. Confidence + borderline_concerns fields route uncertain cases to human review.
3. Reproducibility: same evidence_pack + same model version => same output.
"""

from __future__ import annotations
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import anthropic

logger = logging.getLogger(__name__)

MODEL_VERSION = "claude-3-5-sonnet-20241022"  # Lock to specific version for reproducibility

SYSTEM_PROMPT = """\
You are scoring a company against DeepThought's Federer ICP. You will be given an
evidence pack as JSON. Your job is to score each of 6 criteria (C3 to C8) with
WEAK / MODERATE / STRONG, citing the specific evidence_pack key that supports each
score. If evidence is insufficient for a criterion, score it WEAK and cite
"insufficient_evidence". Do not invent facts.

OUTPUT STRICTLY AS JSON in this schema:
{
  "C3_differentiated": {"score": "STRONG|MODERATE|WEAK",
                        "weight": 20,
                        "citation": "evidence_pack.<field_path>",
                        "reasoning_one_line": "<=1 line"},
  "C4_decision_maker": {...weight: 15...},
  "C5_growing_sector": {...weight: 15...},
  "C6_growth_signals": {...weight: 15...},
  "C7_systems_maturity": {...weight: 20...},
  "C8_succession": {...weight: 15...},
  "federer_score_total": <int 0-100>,
  "score_band": "A|B|C|D",
  "confidence": <float 0.0-1.0>,
  "borderline_concerns": ["..."]
}

Score-to-points mapping: STRONG=full weight, MODERATE=half weight, WEAK=0
Bands: A>=80, B 60-79, C 40-59, D<40

Auto-disqualifiers (return federer_score_total=0 and score_band="D" if any are true):
- size_over_500cr in flags
- subsidiary_pattern_detected in flags
- pe_holders_present in flags AND institutional_pct > 25
- E1 producer fail or E2 accessibility fail
"""


def build_user_prompt(evidence_pack: dict[str, Any]) -> str:
    return (
        "Score this company against the Federer ICP.\n"
        "EVIDENCE PACK:\n"
        f"{json.dumps(evidence_pack, indent=2, default=str)}\n"
    )


def score_one(client: anthropic.Anthropic, evidence_pack: dict[str, Any]) -> dict[str, Any]:
    response = client.messages.create(
        model=MODEL_VERSION,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(evidence_pack)}],
    )
    text = response.content[0].text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Salvage: extract first JSON object found
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


def needs_human_review(score: dict[str, Any]) -> bool:
    if score.get("confidence", 0) < 0.8:
        return True
    if score.get("borderline_concerns"):
        return True
    if 50 <= score.get("federer_score_total", 0) <= 70:
        return True
    return False


def main(input_jsonl: Path, output_jsonl: Path) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Set ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    auto_pass, hr_queue = [], []
    with input_jsonl.open() as fh, output_jsonl.open("w") as out:
        for line in fh:
            pack = json.loads(line)
            try:
                score = score_one(client, pack)
            except Exception as exc:
                logger.error("scoring failed for %s: %s", pack.get("company_name"), exc)
                score = {"federer_score_total": 0, "score_band": "ERR",
                         "confidence": 0.0, "borderline_concerns": [str(exc)]}
            record = {"company_name": pack.get("company_name"), "score": score, "evidence_pack": pack}
            out.write(json.dumps(record, default=str) + "\n")
            (hr_queue if needs_human_review(score) else auto_pass).append(record)
    logger.info("Auto-pass: %d, Human-review queue: %d", len(auto_pass), len(hr_queue))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
