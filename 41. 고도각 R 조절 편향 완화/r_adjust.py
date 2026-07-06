"""고도각 관측의 계통 편향을 '차감' 대신 'R 팽창'으로 완화한다.

39·40번은 peak_margin으로 예측한 고도각 편향을 관측 평균에서 빼는 방식이 대규모에서 실용
이득이 없고 발산까지 낸 것을 보였다. 41번은 같은 예측 편향을 관측 평균이 아니라 관측 분산에
더한다: R[el] += (예측편향)^2. 계통 편향을 '지우려' 하지 않고 '못 믿을 관측'으로 down-weight해
편향이 상태로 새는 것을 줄이는, 차감보다 안전한(발산 위험 없는) 대안이다.

예측 편향은 validation ping에서 el_bias ≈ a + b·peak_margin으로 적합한다(GT는 el_bias 산출에만).
채택 알고리즘의 조건부 adaptive-R 라우팅 위에 얹어, baseline과 라우팅·초기화·관측이 동일하고
고도각 R만 추가로 팽창한다.
"""

from __future__ import annotations

import numpy as np

from conditional_adaptive import ConditionalAdaptiveRUKF

MAX_ADD_RAD = np.radians(4.0)   # 분산 추가의 표준편차 상한 (과도 down-weight 방지)


def fit_bias_model(records) -> dict:
    """validation ping의 (peak_margin, el_bias)로 a + b·peak_margin을 최소제곱 적합."""
    margins, biases = [], []
    for rec in records:
        true_el = rec["true_elevation_rad"]
        obs = rec["observations"]
        for k in range(len(true_el)):
            margins.append(float(rec["qualities"][k]["peak_margin"]))
            biases.append(float(obs[k, 9] - true_el[k]))
    margins = np.asarray(margins); biases = np.asarray(biases)
    design = np.column_stack([np.ones_like(margins), margins])
    beta, *_ = np.linalg.lstsq(design, biases, rcond=None)
    return {"intercept_rad": float(beta[0]), "slope_rad_per_margin": float(beta[1])}


def predicted_bias_rad(peak_margin: float, model: dict) -> float:
    value = model["intercept_rad"] + model["slope_rad_per_margin"] * peak_margin
    return float(np.clip(value, -MAX_ADD_RAD, MAX_ADD_RAD))


class ElevationRInflateUKF(ConditionalAdaptiveRUKF):
    """채택 조건부 adaptive-R 라우팅에 고도각 R 팽창을 추가한 변형.

    부모 step의 라우팅·NIS 스케일을 그대로 재현하고, 마지막에 고도각 R에
    gain·(예측편향)^2을 더한 뒤 update한다. gain=0이면 baseline과 동일하다.
    """

    def __init__(self, ukf, threshold_deg, bias_model, gain: float = 1.0):
        super().__init__(ukf, threshold_deg)
        self.bias_model = bias_model
        self.gain = float(gain)

    def step(self, observation, quality):
        self.ukf.predict()
        R = self.base_R.copy()
        disagreement = quality["doa_disagreement_deg"]
        scale = min(100.0, 1.0 + (disagreement / 2.0) ** 2)
        routed = disagreement > self.threshold
        if routed:
            R[1:8, 1:8] *= scale
        else:
            R[8:10, 8:10] *= scale
        _, _, predicted, _, S = self.ukf.measurement_statistics(R)
        residual = self.ukf._z_residual(np.asarray(observation).copy(), predicted)
        for indices, limit in ((slice(0, 1), 6.63), (slice(1, 8), 18.48), (slice(8, 10), 9.21)):
            nis = self._nis(residual, S, indices)
            R[indices, indices] *= min(100.0, max(1.0, nis / limit))
        # 고도각(z[9]) R에 예측 편향 분산을 추가한다.
        bias = predicted_bias_rad(quality["peak_margin"], self.bias_model)
        R[9, 9] += self.gain * bias ** 2
        self.ukf.update(observation, R)
        self.history.append({"disagreement_deg": disagreement, "routed": routed,
                             "el_r_add_rad2": float(self.gain * bias ** 2)})
        return self.ukf.x.copy()
