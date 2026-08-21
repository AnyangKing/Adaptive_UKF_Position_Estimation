from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = (ROOT / "paper" / "manuscript.tex").read_text(encoding="utf-8")


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def require_token(token: str) -> None:
    if token not in MANUSCRIPT:
        raise AssertionError(f"Missing manuscript token: {token}")


def require_close(label: str, actual: float, expected: float, tol: float = 0.005) -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"{label}: {actual} != {expected} within {tol}")


def main() -> None:
    r191 = load_json(
        "191. Moving full range transition aware independent validation/"
        "moving_full_range_independent_validation.json"
    )
    r204 = load_json("204. Overnight OOD validation aggregate result/compact_metrics.json")
    r215 = load_json(
        "215. Hardware frequency response sensitivity/"
        "hardware_response_sensitivity.json"
    )
    r216 = load_json(
        "216. Extended OOD motion family validation/"
        "extended_ood_motion_family_validation.json"
    )

    s191 = r191["summary"]["overall"]
    fixed191 = s191["fixed_baseline"]["mean_rmse_m"]
    hop191 = s191["hop_baseline"]["mean_rmse_m"]
    soft191 = s191["hop_transition_softR"]["mean_rmse_m"]
    require_close("191 softR gain vs hop", hop191 - soft191, 3.95, 0.01)
    require_close("191 softR gain vs fixed", fixed191 - soft191, 4.80, 0.01)
    require_token("528 paired cases")
    require_token("3.95~m")
    require_token("4.80~m")

    s204 = r204["summary"]["overall"]
    require_close("204 fixed mean", s204["fixed_baseline"]["mean_rmse_m"], 10.83, 0.01)
    require_close("204 hop mean", s204["hop_baseline"]["mean_rmse_m"], 10.69, 0.01)
    require_close("204 softR mean", s204["hop_transition_softR"]["mean_rmse_m"], 7.81, 0.01)
    require_close("204 fixed P90", s204["fixed_baseline"]["p90_rmse_m"], 22.34, 0.01)
    require_close("204 hop P90", s204["hop_baseline"]["p90_rmse_m"], 21.61, 0.01)
    require_close("204 softR P90", s204["hop_transition_softR"]["p90_rmse_m"], 15.94, 0.01)
    require_token("7.81~m")
    require_token("10.69~m")
    require_token("10.83~m")
    require_token("15.94~m")
    require_token("22.34/21.61~m")

    by_profile = r215["summary"]["by_profile"]
    for profile in ["flat_reference", "edge_loss_3db", "edge_loss_6db"]:
        value = by_profile[profile]["hop_transition_softR"]["mean_rmse_m"]
        if not (7.67 <= value <= 7.69):
            raise AssertionError(f"215 {profile} softR outside 7.68--7.69 band: {value}")
        if by_profile[profile]["hop_transition_softR"]["n"] != 192:
            raise AssertionError(f"215 {profile} n is not 192")
    require_token("7.68--7.69~m")
    require_token("192 paired cases per profile")

    s216 = r216["summary"]["overall"]
    require_close("216 fixed mean", s216["fixed_baseline"]["mean_rmse_m"], 12.48, 0.01)
    require_close("216 hop mean", s216["hop_baseline"]["mean_rmse_m"], 11.37, 0.01)
    require_close("216 softR mean", s216["hop_transition_softR"]["mean_rmse_m"], 8.13, 0.01)
    if s216["hop_transition_softR"]["n"] != 144:
        raise AssertionError("216 softR n is not 144")
    require_token("8.13~m")
    require_token("12.48/11.37~m")
    require_token("144 additional OOD-family cases")

    for boundary in [
        "not a real-water or arbitrary-motion guarantee",
        "not measured hardware calibration",
        "not arbitrary-motion proof",
    ]:
        require_token(boundary)

    print("PASS: manuscript claim tokens match 191/204/215/216 result JSONs.")


if __name__ == "__main__":
    main()
