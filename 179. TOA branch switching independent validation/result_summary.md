# 179 result summary

## 판정

`CarrierTransitionTOAGuardUKF`는 독립 static seed에서 일반적인 tail guard로 검증되지 않았다.

## 핵심 수치

| schedule | mean gain vs baseline (m) | CI95 (m) | p | improved fraction | tail worsened fraction |
|---|---:|---:|---:|---:|---:|
| fixed32 | 0.000 | [0.000, 0.000] | 1.000 | 0.000 | 0.000 |
| linear20_30_34 | -0.019 | [-0.057, 0.000] | 0.841 | 0.000 | 0.000 |
| four_carrier_cycle | -0.086 | [-0.257, 0.000] | 0.841 | 0.000 | 0.050 |

## 해석

- 162번 post-hoc pilot의 TOA guard는 독립 seed에서 재현되지 않았다.
- fixed32에서는 carrier transition이 없으므로 guard가 작동하지 않는 것이 정상이다.
- linear20과 four-carrier에서는 guard trigger가 일부 있었지만, 평균적으로 baseline을 개선하지 못했다.
- 따라서 이 guard를 논문 방법 또는 성능 claim으로 승격하면 안 된다.

## 다음 결정

180번에서는 hard TOA isolation을 그대로 밀지 않는다. 대신 carrier transition + observed range jump + NIS를 이용한 soft covariance routing 후보를 개발표본에서만 시험한다.

성공하더라도 180은 development candidate이며, 독립검증 전까지 논문 claim 금지다.
