"""Basic audit for folder 239 output."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PAYLOAD = HERE / "axis_wise_validation.json"


def main() -> None:
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    assert payload["config"]["stage"] == "axis_wise_error_decomposition_validation"
    assert payload["config"]["settle_start"] == 10
    rows = payload["trials"]
    assert len(rows) == 11 * 4 * 12 * 3
    required = {
        "horizontal_rmse_m",
        "vertical_rmse_m",
        "radial_rmse_m",
        "cross_range_rmse_m",
        "step_axis_errors",
    }
    for row in rows:
        assert required.issubset(row)
    for policy in ("fixed_baseline", "hop_baseline", "hop_transition_softR"):
        assert payload["summary"]["overall"][policy]["n"] == 11 * 4 * 12
    assert "post-update error decomposition only" in payload["config"]["truth_usage"]
    print("PASS: 239 axis-wise validation output is structurally complete.")


if __name__ == "__main__":
    main()

