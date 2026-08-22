from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
EN = PAPER / "manuscript.tex"
KO = PAPER / "manuscript_ko.tex"
FIGDIR = PAPER / "figures"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def abstract_tokens(tex: str) -> int:
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
    if not m:
        return -1
    body = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", m.group(1))
    body = re.sub(r"[^A-Za-z0-9가-힣%<>=.–—+\-/]+", " ", body)
    return len([t for t in body.split() if t])


def included_figures(tex: str) -> list[str]:
    names = []
    for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        raw = m.group(1)
        name = Path(raw).name
        names.append(name)
    return names


def figure_exists(name: str) -> bool:
    stem = Path(name).stem
    if Path(name).suffix:
        return (FIGDIR / name).exists() or (PAPER / name).exists()
    return (FIGDIR / f"{stem}.pdf").exists() or (FIGDIR / f"{stem}.png").exists()


def required_strings(tex: str) -> list[tuple[str, bool]]:
    checks = [
        ("600 m static fixed mean 13.01", "13.01" in tex),
        ("600 m static agile mean 8.87", "8.87" in tex),
        ("static p=0.0008", "0.0008" in tex),
        ("0--1000 moving range", "0--1000" in tex),
        ("moving soft-R gain vs hop 3.95", "3.95" in tex),
        ("moving soft-R gain vs fixed 4.80", "4.80" in tex),
        ("OOD paired cases 528", "528" in tex and "OOD" in tex),
        ("real-water limitation stated", "real-water" in tex),
        ("arbitrary-motion limitation stated", "arbitrary-motion" in tex),
        ("not first frequency hopping", "not the first" in tex and "frequency" in tex),
    ]
    return checks


def forbidden_claims(tex: str) -> list[str]:
    patterns = [
        r"first\s+frequency\s+hopping\s+USBL",
        r"first\s+use\s+of\s+frequency\s+hopping\s+in\s+USBL",
        r"arbitrary-motion\s+performance",
        r"real-water\s+performance\s+is\s+validated",
        r"sub-meter\s+long-range\s+performance",
    ]
    hits = []
    for pat in patterns:
        for match in re.finditer(pat, tex, flags=re.I):
            context = tex[max(0, match.start() - 80) : min(len(tex), match.end() + 80)].lower()
            negated = any(
                cue in context
                for cue in [
                    "not the",
                    "does not",
                    "not support",
                    "not expected",
                    "avoid",
                    "no ",
                    "nor does",
                    "explains why",
                    "would weaken",
                    "forbid",
                ]
            )
            if not negated:
                hits.append(pat)
    return hits


def log_clean(path: Path) -> list[str]:
    if not path.exists():
        return [f"missing log: {path.name}"]
    text = read(path)
    bad = []
    for pat in [r"^!", r"Undefined", r"Citation .* undefined", r"Reference .* undefined", r"Overfull \\hbox", r"hyperref Warning"]:
        if re.search(pat, text, flags=re.M):
            bad.append(pat)
    return bad


def main() -> None:
    en = read(EN)
    ko = read(KO)
    lines = []
    failures = []

    en_abs = abstract_tokens(en)
    ko_abs = abstract_tokens(ko)
    lines.append(f"- English abstract tokens: {en_abs}")
    lines.append(f"- Korean abstract space tokens: {ko_abs}")
    if not (0 < en_abs <= 200):
        failures.append(f"English abstract length out of bound: {en_abs}")
    if not (0 < ko_abs <= 200):
        failures.append(f"Korean abstract length out of bound: {ko_abs}")

    for label, ok in required_strings(en):
        lines.append(f"- Required claim marker [{label}]: {'OK' if ok else 'MISSING'}")
        if not ok:
            failures.append(f"Missing required marker: {label}")

    forbidden = forbidden_claims(en)
    lines.append(f"- Forbidden-claim pattern hits: {len(forbidden)}")
    if forbidden:
        failures.extend(f"Forbidden claim pattern hit: {x}" for x in forbidden)

    figs = sorted(set(included_figures(en) + included_figures(ko)))
    lines.append(f"- Included figure references: {len(figs)}")
    for fig in figs:
        ok = figure_exists(fig)
        lines.append(f"  - {fig}: {'OK' if ok else 'MISSING'}")
        if not ok:
            failures.append(f"Missing figure file: {fig}")

    for log in [PAPER / "manuscript.log", PAPER / "manuscript_ko.log"]:
        bad = log_clean(log)
        lines.append(f"- Log scan {log.name}: {'OK' if not bad else ', '.join(bad)}")
        failures.extend(f"{log.name}: {x}" for x in bad)

    status = "PASS" if not failures else "FAIL"
    report = ["# Manuscript non-administrative consistency audit", "", f"Status: **{status}**", "", "## Checks", ""]
    report.extend(lines)
    report.extend(["", "## Failures", ""])
    report.extend([f"- {f}" for f in failures] or ["- None"])
    out = Path(__file__).resolve().parent / "consistency_audit_report.md"
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(status)
    print(out)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
