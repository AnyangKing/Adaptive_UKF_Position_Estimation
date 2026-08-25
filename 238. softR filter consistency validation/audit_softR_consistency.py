"""Basic audit for folder 238 output."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PAYLOAD = HERE / "softR_consistency_validation.json"


def main() -> None:
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    assert payload["config"]["position_nees_dof"] == 3
    assert payload["config"]["total_nis_dof"] == 10
    assert payload["config"]["source_protocol"].startswith("191.")
    rows = payload["trials"]
    assert len(rows) == 11 * 4 * 12 * 3
    for policy in ("fixed_baseline", "hop_baseline", "hop_transition_softR"):
        overall = payload["summary"]["overall"][policy]
        assert overall["n"] == 11 * 4 * 12
        assert overall["mean_position_nees"] is not None
        assert overall["mean_total_nis"] is not None
    assert "post-update NEES diagnostics only" in payload["config"]["truth_usage"]
    print("PASS: 238 softR consistency output is structurally complete.")


if __name__ == "__main__":
    main()

