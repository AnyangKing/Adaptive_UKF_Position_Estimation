"""Diagnostic checks for the Stage-0 pre-screen result."""

from pathlib import Path
import json


def main() -> None:
    path = Path(__file__).resolve().parent / "results" / "stage0_schedule_prescreen.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["config"]["ukf_executed"] is False
    assert payload["config"]["localization_rmse_claim_allowed"] is False
    assert payload["config"]["geometries"] == 12
    summary = payload["summary"]
    candidates = {name for name, item in summary.items() if item["decision"] == "stage0_candidate"}
    assert candidates == {
        "random20_30_34_seeded",
        "linear20_30_34",
        "four_carrier_cycle",
        "fixed3_hop1_static",
    }
    random = summary["random20_30_34_seeded"]
    linear = summary["linear20_30_34"]
    assert abs(random["mean_abs_bias_reduction_deg"] - linear["mean_abs_bias_reduction_deg"]) < 1e-12
    assert random["mean_schedule_abs_lag1"] < linear["mean_schedule_abs_lag1"]
    assert summary["two_extreme_alternating"]["mean_schedule_abs_lag1"] == 1.0
    assert summary["two_extreme_alternating"]["decision"] == "reject_or_defer"
    assert summary["wide_linear20_28_36"]["decision"] == "defer_no_extrapolation"
    print("ok")


if __name__ == "__main__":
    main()
