"""
DSIR R&D-Recognized Units Parser
---------------------------------
Pulls the DSIR-recognized in-house R&D units list from dsir.gov.in and
filters to the target Hyderabad specialty chemicals + biotech segments.

DSIR recognition is a hard pre-signal for ICP fit:
- Companies must invest in real R&D infrastructure to qualify
- Directly signals C3 (differentiation via R&D) and C4 (technical decision-maker)

Source: https://dsir.gov.in/recognised-rd-unit
"""

from __future__ import annotations
import csv
import re
import sys
import time
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterator

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

DSIR_LIST_URL = "https://dsir.gov.in/recognised-rd-unit"
TARGET_CITIES = {"Hyderabad", "Secunderabad", "Telangana"}
TARGET_KEYWORDS_SEGMENT_A = [
    "specialty chemical",
    "fine chemical",
    "intermediate",
    "active pharmaceutical",
    "api",
    "custom synthesis",
    "biotech",
    "diagnostic",
    "reagent",
    "antibody",
    "vaccine",
    "ferment",
]


@dataclass
class DSIRRow:
    company_name: str
    address: str
    city_extracted: str | None
    state: str | None
    industry: str | None
    recognition_valid_until: str | None
    raw: dict


def fetch_dsir_html(url: str = DSIR_LIST_URL, timeout: int = 30) -> str:
    """Fetch DSIR list HTML. In production, cache locally."""
    headers = {"User-Agent": "DT-research-bot/0.1 (research; contact: research@deepthought.in)"}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_dsir_table(html: str) -> Iterator[DSIRRow]:
    """Yield DSIRRow per recognized unit. Schema as of mid-2025; verify before each run."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": re.compile(r"recogn", re.IGNORECASE)}) or soup.find("table")
    if table is None:
        logger.error("Could not locate DSIR recognized-unit table on page")
        return
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    for row in table.find_all("tr")[1:]:
        cells = [td.get_text(" ", strip=True) for td in row.find_all("td")]
        if not cells:
            continue
        record = dict(zip(headers, cells))
        yield DSIRRow(
            company_name=record.get("Company Name") or record.get("Name") or "",
            address=record.get("Address") or "",
            city_extracted=_extract_city(record.get("Address", "")),
            state=record.get("State"),
            industry=record.get("Industry") or record.get("Sector"),
            recognition_valid_until=record.get("Valid Until") or record.get("Validity"),
            raw=record,
        )


def _extract_city(address: str) -> str | None:
    address_lower = address.lower()
    for city in TARGET_CITIES:
        if city.lower() in address_lower:
            return city
    return None


def filter_for_target_icp(rows: Iterator[DSIRRow]) -> Iterator[DSIRRow]:
    """Filter DSIR rows to target Hyderabad + specialty chem/biotech segments."""
    for row in rows:
        if row.city_extracted is None:
            continue
        haystack = f"{row.industry or ''} {row.raw}".lower()
        if not any(kw in haystack for kw in TARGET_KEYWORDS_SEGMENT_A):
            continue
        yield row


def main(output_csv: Path = Path("dsir_hyderabad_specialty.csv")) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger.info("Fetching DSIR recognized-units list from %s", DSIR_LIST_URL)
    html = fetch_dsir_html()
    time.sleep(1)
    filtered = list(filter_for_target_icp(parse_dsir_table(html)))
    logger.info("Found %d Hyderabad-area specialty chem/biotech candidates", len(filtered))
    with output_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["company_name", "address", "city_extracted", "state", "industry", "recognition_valid_until"],
        )
        writer.writeheader()
        for row in filtered:
            writer.writerow({k: v for k, v in asdict(row).items() if k != "raw"})
    logger.info("Wrote %s", output_csv)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dsir_hyderabad_specialty.csv"))
