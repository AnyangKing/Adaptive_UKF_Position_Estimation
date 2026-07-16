"""Diagnostic checks for the folder-157 paired analysis."""

from __future__ import annotations

import analyze_paired_blocks as analysis


def main() -> None:
    report = analysis.analyze(analysis.DEFAULT_INPUT)
    assert report["is_research_evidence"] is False
    assert report["record_statuses"] == ["mock"]
    assert report["session_count"] == 1
    session = report["sessions"][0]
    assert session["included_fixed_blocks"] == 2
    assert session["included_hop_blocks"] == 2
    assert abs(session["fixed_rmse_mean_m"] - 5.15) < 1e-12
    assert abs(session["hop_rmse_mean_m"] - 4.55) < 1e-12
    assert abs(session["rmse_gain_m"] - 0.60) < 1e-12
    assert abs(session["fixed_lag1_mean"] - 0.435) < 1e-12
    assert abs(session["hop_lag1_mean"] - 0.065) < 1e-12
    assert abs(session["lag1_reduction"] - 0.37) < 1e-12
    assert session["decision"] == "DRY_RUN_ONLY_NOT_EVIDENCE"
    print("ok")


if __name__ == "__main__":
    main()
