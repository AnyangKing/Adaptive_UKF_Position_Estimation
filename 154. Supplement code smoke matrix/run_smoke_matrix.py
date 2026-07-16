"""Run the seven core supplement diagnostics and detect output drift."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPORT = HERE / "smoke_matrix_report.json"


CASES = [
    ("45_crlb_floor", "45. CRLB 이론하한 대비 효율/test_diagnostic.py"),
    ("58_carrier_sensitivity", "58. 반송파 미세도약 코히어런트 편향 진단/test_diagnostic.py"),
    ("61_static_validation", "61. 정지표적 도약 대규모 독립검증/test_diagnostic.py"),
    ("63_moving_boundary", "63. 이동표적 도약 대규모검증 백색화 확인/test_diagnostic.py"),
    ("82_quasi_static_boundary", "82. 준정지 속도 경계 검증 실행/test_diagnostic.py"),
    ("93_method_audit", "93. Method 세부 코드 대조/test_diagnostic.py"),
    ("145_two_ray_closure", "145. Two-ray mechanism evidence closure/test_diagnostic.py"),
]


def normalized_lines(text: str) -> list[str]:
    return [line.rstrip() for line in text.replace("\r\n", "\n").split("\n") if line.strip()]


def count_checks(lines: list[str]) -> int:
    explicit = sum(line.startswith("PASS ") for line in lines)
    if explicit:
        return explicit
    if any(line in {"diagnostic tests passed", "ok"} for line in lines):
        return 1
    return 0


def run_case(case: tuple[str, str]) -> dict:
    name, relative = case
    script = ROOT / relative
    if not script.is_file():
        return {
            "name": name,
            "script": relative,
            "returncode": 127,
            "passed": False,
            "check_count": 0,
            "stdout": [],
            "stderr": ["missing diagnostic script"],
        }
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        check=False,
    )
    stdout = normalized_lines(completed.stdout)
    stderr = normalized_lines(completed.stderr)
    return {
        "name": name,
        "script": relative,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "check_count": count_checks(stdout),
        "stdout": stdout,
        "stderr": stderr,
    }


def build_report() -> dict:
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(CASES)) as pool:
        records = list(pool.map(run_case, CASES))
    records.sort(key=lambda item: item["name"])
    return {
        "schema": "supplement-code-smoke-matrix-1",
        "case_count": len(records),
        "passed_count": sum(record["passed"] for record in records),
        "failed_count": sum(not record["passed"] for record in records),
        "check_count": sum(record["check_count"] for record in records),
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    current = build_report()
    if args.write:
        REPORT.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"wrote {REPORT.name}: {current['passed_count']}/{current['case_count']} cases, "
            f"{current['check_count']} checks"
        )
        return 0 if current["failed_count"] == 0 else 1

    if not REPORT.is_file():
        print("missing report; run with --write")
        return 1
    expected = json.loads(REPORT.read_text(encoding="utf-8"))
    if current != expected:
        print("smoke-matrix drift detected")
        return 1
    if current["failed_count"]:
        print(f"failed cases: {current['failed_count']}")
        return 1
    print(f"ok: {current['passed_count']}/{current['case_count']} cases, {current['check_count']} checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
