"""거리적응 고도각 편향 보정 모델들.

39번은 el_bias ≈ a + b·peak_margin의 거리무관(global) 보정이 병목 600 m에서 -6.6% 개선했으나
중거리(200/400 m)를 소폭 과보정해 전체 이득이 상쇄됐다. 38번에서 거리별 slope가 달랐으므로,
관측 가능한 TOA 거리(z[0])를 써서 보정을 거리에 적응시킨다. 셋을 비교한다.

- global   : 39번과 동일. a + b·margin, 전 거리 적용 (대조).
- gated    : 장거리(관측 거리 >= gate) ping에서만 계수를 적합하고 그 구간에만 적용. 중거리
             과보정 자체를 피한다.
- interaction: [1, margin, r, margin·r]로 적합해 보정 기울기를 거리의 연속 함수로 만든다.

계수는 모두 validation ping에서만 적합한다(GT는 el_bias= 측정 - 참 계산에만). 예측 편향은
과보정 폭주를 막기 위해 ±3°로 클립한다. 거리 정규화는 r_norm = 관측거리/600.
"""

from __future__ import annotations

import numpy as np

MAX_CORRECTION_RAD = np.radians(3.0)
RANGE_NORM_M = 600.0
GATE_RANGE_M = 300.0


def _pings(records):
    """validation 궤적들을 ping 단위 (margin, observed_range, el_bias)로 편다."""
    margins, ranges, biases = [], [], []
    for rec in records:
        true_el = rec["true_elevation_rad"]
        obs = rec["observations"]
        for k in range(len(true_el)):
            margins.append(float(rec["qualities"][k]["peak_margin"]))
            ranges.append(float(obs[k, 0]))          # 관측 TOA 거리 (m)
            biases.append(float(obs[k, 9] - true_el[k]))
    return np.asarray(margins), np.asarray(ranges), np.asarray(biases)


def fit_global(records) -> dict:
    m, _, y = _pings(records)
    design = np.column_stack([np.ones_like(m), m])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return {"kind": "global", "beta": beta.tolist()}


def fit_gated(records) -> dict:
    m, r, y = _pings(records)
    mask = r >= GATE_RANGE_M
    if mask.sum() < 3:
        return {"kind": "gated", "beta": [0.0, 0.0], "gate_m": GATE_RANGE_M}
    design = np.column_stack([np.ones(mask.sum()), m[mask]])
    beta, *_ = np.linalg.lstsq(design, y[mask], rcond=None)
    return {"kind": "gated", "beta": beta.tolist(), "gate_m": GATE_RANGE_M}


def fit_interaction(records) -> dict:
    m, r, y = _pings(records)
    rn = r / RANGE_NORM_M
    design = np.column_stack([np.ones_like(m), m, rn, m * rn])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return {"kind": "interaction", "beta": beta.tolist()}


def _predict(correction, peak_margin, observed_range_m):
    kind = correction["kind"]; beta = correction["beta"]
    if kind == "global":
        value = beta[0] + beta[1] * peak_margin
    elif kind == "gated":
        if observed_range_m < correction["gate_m"]:
            return 0.0
        value = beta[0] + beta[1] * peak_margin
    elif kind == "interaction":
        rn = observed_range_m / RANGE_NORM_M
        value = beta[0] + beta[1] * peak_margin + beta[2] * rn + beta[3] * peak_margin * rn
    else:
        raise ValueError(kind)
    return float(np.clip(value, -MAX_CORRECTION_RAD, MAX_CORRECTION_RAD))


def corrected_observations(record, correction) -> np.ndarray:
    z = record["observations"].copy()
    for k in range(z.shape[0]):
        z[k, 9] -= _predict(correction, record["qualities"][k]["peak_margin"], z[k, 0])
    return z


FITTERS = {"global": fit_global, "gated": fit_gated, "interaction": fit_interaction}
