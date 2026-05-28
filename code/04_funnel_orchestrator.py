"""
Funnel Orchestrator
-------------------
End-to-end pipeline: source -> dedupe -> gate -> enrich -> score -> QA queue.

In production: scheduled via cron / Airflow / GitHub Actions. Each step is
idempotent so failures resume from the last completed stage.
"""

from __future__ import annotations
import argparse
import logging
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PIPELINE_STAGES = [
    ("01-source-dsir", ["python", "01_dsir_parser.py", "raw/dsir.csv"]),
    # Add: 01b-source-mca-nic, 01c-source-uspharma, 01d-source-cphi-exhibitors, etc.
    ("02-dedupe", ["python", "-m", "dedupe_companies", "raw/", "deduped.csv"]),
    ("03-enrich", ["python", "02_mca_enrichment.py", "deduped.csv", "evidence_packs.jsonl"]),
    ("04-gate-deterministic", ["python", "-m", "gate_e1_e2_disqualifiers",
                              "evidence_packs.jsonl", "scoring_pool.jsonl"]),
    ("05-llm-score", ["python", "03_llm_scoring.py", "scoring_pool.jsonl", "scored.jsonl"]),
    ("06-qa-queue", ["python", "-m", "build_qa_queue", "scored.jsonl",
                    "auto_pass.jsonl", "human_review.jsonl"]),
    ("07-final-csv", ["python", "-m", "render_final_csv",
                     "auto_pass.jsonl", "human_review_resolved.jsonl", "final_1000.csv"]),
]


def run_stage(name: str, cmd: list[str]) -> int:
    logger.info("--- Stage %s ---", name)
    return subprocess.run(cmd, check=False).returncode


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-from", default=PIPELINE_STAGES[0][0])
    parser.add_argument("--end-at", default=PIPELINE_STAGES[-1][0])
    args = parser.parse_args()
    start = next(i for i, s in enumerate(PIPELINE_STAGES) if s[0] == args.start_from)
    end = next(i for i, s in enumerate(PIPELINE_STAGES) if s[0] == args.end_at)
    for name, cmd in PIPELINE_STAGES[start : end + 1]:
        rc = run_stage(name, cmd)
        if rc != 0:
            logger.error("Stage %s failed (exit %d). Aborting.", name, rc)
            sys.exit(rc)


if __name__ == "__main__":
    main()
