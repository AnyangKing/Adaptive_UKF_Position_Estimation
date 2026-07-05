"""송신시각과 Ground Truth 없이 사전 위치로 multipath peak의 경로를 연관한다."""

from itertools import permutations
import numpy as np

from channel import paths_for_sensor
from config import usb_array_global_m


PATH_NAMES = ("direct", "surface", "bottom")


def predicted_relative_delays(position, sensor, cfg):
    paths = paths_for_sensor(np.asarray(position), np.asarray(sensor), cfg)
    delays = np.array([path.delay_s for path in paths])
    return delays - delays[0]


def associate_peak_times(peak_times, peak_strengths, predicted_position, sensor, cfg,
                         timing_std_s=2.0e-4, strength_weight=0.15):
    """공통 송신시각을 소거한 상대지연 residual의 최소비용 3경로 할당."""
    times = np.asarray(peak_times); strengths = np.asarray(peak_strengths)
    expected = predicted_relative_delays(predicted_position, sensor, cfg)
    if len(times) < 3:
        raise ValueError("at least three peaks are required")
    best = None
    for indices in permutations(range(len(times)), 3):
        observed = times[list(indices)] - times[indices[0]]
        timing_cost = float(np.sum(((observed[1:] - expected[1:]) / timing_std_s) ** 2))
        # 아주 약한 잡음 peak를 택하는 것만 억제하며 물리 지연이 주 비용이다.
        amplitude_cost = float(strength_weight * np.sum(-np.log(np.clip(strengths[list(indices)], 1e-6, 1.0))))
        cost = timing_cost + amplitude_cost
        if best is None or cost < best[0]: best = (cost, indices, timing_cost, amplitude_cost)
    cost, indices, timing_cost, amplitude_cost = best
    residual = (times[list(indices)] - times[indices[0]]) - expected
    return {"indices": tuple(int(i) for i in indices), "times_s": times[list(indices)],
            "cost": float(cost), "timing_cost": float(timing_cost),
            "amplitude_cost": float(amplitude_cost), "relative_residual_s": residual}


def associate_array(records, predicted_position, cfg):
    sensors = usb_array_global_m(cfg.receiver_depth_m)
    return [associate_peak_times(record["peak_times_s"], record["peak_strengths"],
                                 predicted_position, sensor, cfg)
            for record, sensor in zip(records, sensors)]
