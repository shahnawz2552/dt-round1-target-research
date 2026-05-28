"""
MCA21 / Tofler Enrichment
-------------------------
For each candidate company, pull from MCA / Tofler:
- CIN, NIC code, incorporation date, registered office
- Latest AOC-4 revenue, EBITDA, R&D expense
- Director list with DINs and other directorships  -> for director-graph PE re-screen
- Shareholding pattern (PE-screen)

Production notes:
- MCA bulk-data subscription costs ~Rs.50K/yr; Tofler/Zauba derivative APIs are
  cheaper and sufficient for the first 1000-company pass.
- Always retry idempotently and cache responses to a local DB.
- Schema is normalized to a single JSON evidence_pack per company.
"""

from __future__ import annotations
import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)

TOFLER_API_BASE = os.environ.get("TOFLER_API_BASE", "https://api.tofler.in/v2")
TOFLER_API_KEY = os.environ.get("TOFLER_API_KEY", "")


@dataclass
class CompanyEvidencePack:
    company_name: str
    cin: str | None = None
    nic_code: str | None = None
    incorporation_date: str | None = None
    registered_office: dict | None = None
    fy23_revenue_inr_cr: float | None = None
    fy24_revenue_inr_cr: float | None = None
    fy25_revenue_inr_cr: float | None = None
    rnd_expense_pct_revenue: float | None = None
    directors: list[dict] = field(default_factory=list)
    promoter_pct: float | None = None
    institutional_pct: float | None = None
    pe_holders: list[dict] = field(default_factory=list)
    charges_filed_last_24mo: list[dict] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)


class TollerClient:
    """Wraps Tofler API or equivalent. Replace with mca21 client in production."""

    def __init__(self, api_key: str = TOFLER_API_KEY, base_url: str = TOFLER_API_BASE):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def lookup_by_name(self, name: str) -> dict[str, Any] | None:
        try:
            r = self.session.get(f"{self.base_url}/company/search", params={"q": name}, timeout=15)
            r.raise_for_status()
            results = r.json().get("results", [])
            return results[0] if results else None
        except requests.RequestException as exc:
            logger.warning("Tofler search failed for %s: %s", name, exc)
            return None

    def get_company_detail(self, cin: str) -> dict[str, Any] | None:
        try:
            r = self.session.get(f"{self.base_url}/company/{cin}", timeout=20)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as exc:
            logger.warning("Tofler detail failed for %s: %s", cin, exc)
            return None


def detect_pe_control(shareholding_pattern: list[dict]) -> tuple[float, list[dict]]:
    """Detect PE / institutional control. Returns (institutional_pct, pe_holders)."""
    pe_keywords = ["capital", "fund", "holdings", "partners", "advent", "carlyle", "kkr",
                   "blackstone", "tpg", "pag", "warburg", "chryscapital", "samara",
                   "everstone", "general atlantic", "goldman", "quadria", "avendus"]
    pe_holders, total_inst_pct = [], 0.0
    for holder in shareholding_pattern or []:
        name = (holder.get("name") or "").lower()
        pct = float(holder.get("pct") or 0)
        if any(kw in name for kw in pe_keywords):
            pe_holders.append(holder)
        if holder.get("category") in {"FII", "FPI", "PE", "Mutual Fund", "Insurance"}:
            total_inst_pct += pct
    return total_inst_pct, pe_holders


def detect_size_disqualifier(latest_revenue_cr: float | None) -> bool:
    return latest_revenue_cr is not None and latest_revenue_cr > 500.0


def detect_subsidiary_disqualifier(directors: list[dict], parent_holdings: list[dict] | None) -> bool:
    """Crude heuristic: if any single shareholder holds >50% and is not a person, flag."""
    if not parent_holdings:
        return False
    for holder in parent_holdings:
        if holder.get("pct", 0) > 50 and holder.get("type") in {"Body Corporate", "Foreign Company"}:
            return True
    return False


def enrich(name: str, client: TollerClient) -> CompanyEvidencePack:
    pack = CompanyEvidencePack(company_name=name)
    summary = client.lookup_by_name(name)
    if summary is None:
        pack.flags.append("not_found_in_mca")
        return pack
    pack.cin = summary.get("cin")
    pack.sources.append(f"tofler:{pack.cin}")
    detail = client.get_company_detail(pack.cin) if pack.cin else None
    if detail is None:
        pack.flags.append("mca_detail_unavailable")
        return pack
    pack.nic_code = detail.get("nic_code")
    pack.incorporation_date = detail.get("incorporation_date")
    pack.registered_office = detail.get("registered_office")
    fin = detail.get("financials") or {}
    pack.fy23_revenue_inr_cr = fin.get("FY23", {}).get("revenue_cr")
    pack.fy24_revenue_inr_cr = fin.get("FY24", {}).get("revenue_cr")
    pack.fy25_revenue_inr_cr = fin.get("FY25", {}).get("revenue_cr")
    if pack.fy24_revenue_inr_cr:
        rnd = fin.get("FY24", {}).get("rnd_expense_cr") or 0
        if pack.fy24_revenue_inr_cr > 0:
            pack.rnd_expense_pct_revenue = round(100 * rnd / pack.fy24_revenue_inr_cr, 2)
    pack.directors = detail.get("directors", [])
    pack.charges_filed_last_24mo = detail.get("charges_recent", [])
    inst_pct, pe_holders = detect_pe_control(detail.get("shareholding_pattern", []))
    pack.institutional_pct = inst_pct
    pack.pe_holders = pe_holders
    if detect_size_disqualifier(pack.fy25_revenue_inr_cr or pack.fy24_revenue_inr_cr):
        pack.flags.append("size_over_500cr")
    if detect_subsidiary_disqualifier(pack.directors, detail.get("shareholding_pattern", [])):
        pack.flags.append("subsidiary_pattern_detected")
    if pe_holders:
        pack.flags.append("pe_holders_present")
    return pack


def main(input_csv: Path, output_jsonl: Path) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    client = TollerClient()
    with input_csv.open() as fh, output_jsonl.open("w") as out:
        for line in fh:
            name = line.strip().split(",")[0]
            if not name or name.lower() == "company_name":
                continue
            logger.info("Enriching %s", name)
            pack = enrich(name, client)
            out.write(json.dumps(pack.__dict__, default=str) + "\n")
            time.sleep(0.5)


if __name__ == "__main__":
    import sys
    main(Path(sys.argv[1]), Path(sys.argv[2]))
