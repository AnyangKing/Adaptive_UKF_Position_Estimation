"""현실 채널의 멀티패스 도착구조에서 blind 신규 feature를 뽑는다.

49번은 채널을 현실화해도 기존 peak_margin 예측신호가 오히려 약해짐을 보였다. 그러나 richer
채널은 관측 가능한 반사 도착구조(직접-반사 상대지연·진폭비·peak 개수/퍼짐)를 더 많이 노출한다.
직접파와 표면/해저 반사의 상대지연은 소스 깊이·grazing angle 기하를 담으므로, 계통 고도각
편향과 물리적으로 연결될 수 있다. 여기서는 GT 없이 매치드필터 도착 peak만으로 이 구조 feature를
계산한다(색인·라벨에 GT 미사용).
"""

from __future__ import annotations

import numpy as np

from config import ChannelConfig
from path_identifiability import observed_peaks


def structure_features(reference_signal, cfg: ChannelConfig) -> dict:
    """기준 센서 신호의 매치드필터 peak들에서 blind 멀티패스 구조 feature."""
    times, strengths = observed_peaks(reference_signal, cfg, maximum=6)
    order = np.argsort(times)              # 시간 오름차순: 첫 도착=직접파
    t = np.asarray(times)[order]
    s = np.asarray(strengths)[order]
    if len(t) < 2:
        return {"first_reflection_delay_us": 0.0, "reflection_amp_ratio": 0.0,
                "peak_count": float(len(t)), "peak_time_spread_us": 0.0,
                "second_reflection_delay_us": 0.0}
    direct_t, direct_s = t[0], s[0] + 1e-12
    return {
        # 직접파 대비 첫 반사 상대지연(µs) — 소스 깊이·grazing 기하 반영
        "first_reflection_delay_us": float((t[1] - direct_t) * 1e6),
        # 첫 반사/직접파 진폭비 — grazing angle·반사강도 반영
        "reflection_amp_ratio": float(s[1] / direct_s),
        # 두 번째 반사(있으면) 상대지연
        "second_reflection_delay_us": float((t[2] - direct_t) * 1e6) if len(t) >= 3 else 0.0,
        # 검출 peak 개수와 시간 퍼짐(µs)
        "peak_count": float(len(t)),
        "peak_time_spread_us": float((t[-1] - t[0]) * 1e6),
    }


FEATURE_NAMES = ("first_reflection_delay_us", "reflection_amp_ratio",
                 "second_reflection_delay_us", "peak_count", "peak_time_spread_us")
