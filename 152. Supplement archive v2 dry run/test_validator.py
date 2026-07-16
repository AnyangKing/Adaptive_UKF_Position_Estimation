"""Diagnostic checks for the folder-152 supplement dry-run validator."""

from __future__ import annotations

import json

import validate_supplement_v2 as validator


def expect_rejected(source: str) -> None:
    try:
        validator.validate_source_policy(source)
    except ValueError:
        return
    raise AssertionError(f"forbidden source was accepted: {source}")


def main() -> None:
    current = validator.build_manifest()
    expected = json.loads(validator.MANIFEST.read_text(encoding="utf-8"))
    assert current == expected
    assert current["artifact_count"] == 90
    assert current["category_counts"] == {
        "code": 65,
        "data": 8,
        "document": 5,
        "figure": 8,
        "figure_script": 4,
    }

    archive_paths = [entry["archive_path"] for entry in current["entries"]]
    assert len(archive_paths) == len(set(archive_paths))
    assert all(not path.startswith("/") for path in archive_paths)

    expect_rejected("paper/manuscript.tex")
    expect_rejected("paper/manuscript.pdf")
    expect_rejected(".claude/private.md")
    expect_rejected("study_exports/note.md")
    expect_rejected("61. 정지표적 도약 대규모 독립검증/__pycache__/channel.pyc")

    validator.validate_source_policy("paper/figures/fig1_system_concept.png")
    validator.validate_source_policy("145. Two-ray mechanism evidence closure/results/two_ray_fit.json")
    print("ok")


if __name__ == "__main__":
    main()
