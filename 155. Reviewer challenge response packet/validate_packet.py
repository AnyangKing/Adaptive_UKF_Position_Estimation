"""Validate reviewer challenge IDs, statuses, counts, and evidence paths."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MATRIX = HERE / "reviewer_challenge_matrix.json"
ALLOWED = {
    "closed_with_current_evidence",
    "partial_future_ablation",
    "open_requires_field_validation",
    "open_requires_human_policy",
}


def main() -> None:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    challenges = data["challenges"]
    ids = [item["id"] for item in challenges]
    assert len(ids) == len(set(ids)), "duplicate challenge ID"
    assert set(item["status"] for item in challenges) <= ALLOWED
    observed = Counter(item["status"] for item in challenges)
    assert dict(observed) == data["counts"], (observed, data["counts"])

    missing = []
    for item in challenges:
        assert item["safe_position"].strip()
        assert item["must_not_claim"].strip()
        assert item["evidence"]
        for relative in item["evidence"]:
            if not (ROOT / relative).exists():
                missing.append({"id": item["id"], "path": relative})
    assert not missing, missing
    print(f"ok: {len(challenges)} challenges, {sum(observed.values())} classified, 0 missing evidence paths")


if __name__ == "__main__":
    main()
