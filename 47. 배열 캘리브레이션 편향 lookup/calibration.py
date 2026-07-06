"""관측 방위-고도로 색인한 고도각 편향 캘리브레이션 lookup (non-blind).

42번은 계통 고도각 편향이 소스 방위가 아니라 8센서 배열 기하에 결정론적으로 고정됨(array-intrinsic)을
보였다. 따라서 편향은 배열-상대 도래각(방위·고도)의 함수다. 39~41의 실패한 blind 신호(peak_margin)와
달리, 여기서는 관측 도래각을 색인으로 편향을 예측한다. 37번 B에서 편향이 매끄러운 저차 함수가
아니었으므로 국소 kNN 평균으로 비모수 근사한다.

validation ping에서 (측정 az, 측정 el, el_bias=측정-참)를 모아 lookup을 만들고, test에서 측정
도래각으로 편향을 예측해 관측 고도각에서 뺀다. GT는 편향 label 산출(calibration residual)에만 쓴다.
색인은 런타임에 이용 가능한 '측정' 도래각이다.
"""

from __future__ import annotations

import numpy as np

from measurement import ideal_measurement

MAX_CORRECTION_RAD = np.radians(4.0)


def _wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


class ElevationBiasLookup:
    """(측정 az, 측정 el) → 고도각 편향의 kNN 국소평균 예측기."""

    def __init__(self, azimuths, elevations, biases, k=15):
        self.az = np.asarray(azimuths, float)
        self.el = np.asarray(elevations, float)
        self.bias = np.asarray(biases, float)
        self.k = int(min(k, len(self.bias)))

    @classmethod
    def fit(cls, records, cfg, k=15):
        az, el, bias = [], [], []
        for rec in records:
            for i in range(len(rec["truth"])):
                z = rec["observations"][i]
                true_el = float(ideal_measurement(rec["truth"][i], cfg)[9])
                az.append(float(z[8])); el.append(float(z[9]))
                bias.append(float(z[9] - true_el))
        return cls(az, el, bias, k=k)

    def predict(self, measured_az, measured_el):
        # 배열 대칭(90°/180°)을 고려하지 않고 원 도래각으로 색인한다(측정 az가 곧 배열-상대 방위).
        d_az = _wrap(self.az - measured_az)
        d_el = self.el - measured_el
        dist2 = d_az ** 2 + d_el ** 2
        idx = np.argpartition(dist2, self.k - 1)[:self.k]
        value = float(np.mean(self.bias[idx]))
        return float(np.clip(value, -MAX_CORRECTION_RAD, MAX_CORRECTION_RAD))


def corrected_observations(record, lookup: ElevationBiasLookup) -> np.ndarray:
    z = record["observations"].copy()
    for k in range(z.shape[0]):
        z[k, 9] -= lookup.predict(z[k, 8], z[k, 9])
    return z
