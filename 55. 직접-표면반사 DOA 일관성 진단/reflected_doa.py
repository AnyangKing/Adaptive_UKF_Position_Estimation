"""반사경로(표면반사 등 2번째 도착) DOA를 gated SRP로 추출한다.

직접파는 가장 이른 도착, 표면반사는 그 다음 도착으로 배열에 도달한다. 반사파는 소스의 표면
image에서 오므로 직접파와 다른(대개 더 높은) 고도각에서 도착해, 소스 깊이를 독립적으로 제약한다.
채택 관측이 직접파 창만 gating하는 것과 달리, 여기서는 2번째 도착 창을 gating해 반사경로 DOA를
얻는다. "물리 경로 일관성"을 직접-반사 DOA 중복으로 검사하기 위한 관측이다.
"""

from __future__ import annotations

import numpy as np

from config import ChannelConfig
from estimators import estimate_srp_phat_doa
from path_identifiability import observed_peaks


def reflected_arrival_time(reference_signal, cfg: ChannelConfig) -> float:
    """기준 센서 매치드필터 peak 중 2번째로 이른 도착시각(=첫 반사)."""
    times, _ = observed_peaks(reference_signal, cfg, maximum=6)
    t = np.sort(np.asarray(times))
    return float(t[1]) if len(t) >= 2 else float(t[0])


def _crop_around(received, cfg: ChannelConfig, center_s, window_s=0.005, pre_s=0.0001):
    fs = cfg.sample_rate_hz
    start = max(0, int(np.floor((center_s - pre_s) * fs)))
    end = min(received.shape[1], int(np.ceil((center_s + window_s) * fs)))
    if end - start < 32:
        end = min(received.shape[1], start + 32)
    return received[:, start:end]


def reflected_srp_doa(received, cfg: ChannelConfig):
    """2번째 도착(반사) 창을 gating한 SRP-PHAT DOA (azimuth, elevation)."""
    t_ref = reflected_arrival_time(received[0], cfg)
    cropped = _crop_around(received, cfg, t_ref)
    az, el, _, _ = estimate_srp_phat_doa(cropped, cfg)
    return float(az), float(el)
