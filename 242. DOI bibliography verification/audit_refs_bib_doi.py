from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "paper" / "refs.bib"

EXPECTED_DOIS = {
    "Beaujean2007FrequencyHoppedUSBL": "10.1121/1.2400616",
    "Nhat2022CostasUSBL": "10.1109/IMCOM53663.2022.9721736",
    "Qian2025FrequencyCombIUSBL": "10.1109/JIOT.2025.3564346",
    "Zhang2024DifferentialUSBL": "10.1016/j.oceaneng.2024.117984",
    "Zhang2019USBLCalib": "10.1504/IJSNET.2019.101243",
    "Tong2019USBLError": "10.3390/s19204373",
    "Li2019UnderwaterSRUKF": "10.3390/e21080740",
    "RaviKumar2021HybridUKF": "10.1016/j.ijleo.2020.165813",
    "AlAboosi2016Multipath": "10.11591/ijeecs.v2.i2.pp351-358",
}

EXPECTED_FIELDS = {
    "Zhang2019USBLCalib": {
        "pages": "254--262",
    },
}


def parse_entries(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    pattern = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n@\w+\s*\{|\Z)", re.S)
    for match in pattern.finditer(text):
        entries[match.group(1)] = match.group(2)
    return entries


def field(body: str, name: str) -> str | None:
    match = re.search(rf"\b{name}\s*=\s*[\{{\"]([^}}\"]+)[\}}\"]", body, re.I)
    return match.group(1).strip() if match else None


def main() -> None:
    text = REFS.read_text(encoding="utf-8")
    entries = parse_entries(text)
    missing_doi = [key for key, body in entries.items() if not field(body, "doi")]
    empty_doi = [key for key, body in entries.items() if field(body, "doi") == ""]

    assert len(entries) == 22, f"Expected 22 BibTeX entries, found {len(entries)}"
    assert not missing_doi, f"Entries without DOI: {missing_doi}"
    assert not empty_doi, f"Entries with empty DOI: {empty_doi}"

    for key, expected in EXPECTED_DOIS.items():
        assert key in entries, f"Missing key: {key}"
        got = field(entries[key], "doi")
        assert got is not None
        assert got.lower() == expected.lower(), f"{key}: expected DOI {expected}, got {got}"

    for key, fields in EXPECTED_FIELDS.items():
        assert key in entries, f"Missing key: {key}"
        for name, expected in fields.items():
            got = field(entries[key], name)
            assert got == expected, f"{key}: expected {name}={expected}, got {got}"

    print("PASS: refs.bib has 22 entries, 22 DOI fields, and checked high-risk DOI/page markers.")


if __name__ == "__main__":
    main()
