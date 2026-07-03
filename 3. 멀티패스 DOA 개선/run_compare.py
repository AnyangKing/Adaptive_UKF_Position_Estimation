"""동일 수신 신호에서 세 DOA 추정법을 비교한다."""

from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from estimators import (
    estimate_array_doa,
    estimate_gcc_phat_doa,
    estimate_srp_phat_doa,
    estimate_toa_matched_filter,
)


def angular_separation_deg(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.degrees(np.arccos(np.clip(a @ b, -1.0, 1.0))))


def run() -> dict[str, float]:
    cfg = ChannelConfig()
    source = np.array([100.0, 20.0, -20.0])
    _, received, _ = synthesize_received(source, cfg)
    toas, _ = estimate_toa_matched_filter(received, cfg)
    _, _, matched_direction = estimate_array_doa(toas, cfg)
    _, _, gcc_direction, _ = estimate_gcc_phat_doa(received, cfg)
    _, _, srp_direction, srp_score = estimate_srp_phat_doa(received, cfg)
    true_direction = source - usb_array_global_m(cfg.receiver_depth_m).mean(axis=0)
    true_direction /= np.linalg.norm(true_direction)
    metrics = {
        "matched_filter_doa_error_deg": angular_separation_deg(matched_direction, true_direction),
        "gcc_phat_doa_error_deg": angular_separation_deg(gcc_direction, true_direction),
        "srp_phat_doa_error_deg": angular_separation_deg(srp_direction, true_direction),
        "srp_peak_score": srp_score,
    }
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    (output / "doa_comparison.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    run()

