# 234. Moving tail case decomposition

## 목적

다른 AI가 지적한 세 번째 미해결 약점인 **191번 이동 표적 tail case 분해 부족**을 보완했다.

191번은 0--1000 m 이동 표적 528 paired cases에서 transition-aware soft-R가 평균 RMSE를 크게 낮춘다는 강한 결과를 냈다. 그러나 softR vs fixed 기준으로도 tail worsened fraction이 13.1% 남아 있었고, 이 tail이 어느 거리/운동 조건에 몰렸는지 분해가 부족했다.

## 분석 방법

- 새 시뮬레이션은 수행하지 않았다.
- 191번의 `moving_full_range_independent_validation.json`을 재분석했다.
- paired gain 기준:
  - `hop_gain_vs_fixed = fixed RMSE - hop RMSE`
  - `softR_gain_vs_fixed = fixed RMSE - softR RMSE`
  - `softR_gain_vs_hop = hop RMSE - softR RMSE`
- tail worsened 정의:
  - paired gain < -1.0 m
  - 즉 target policy가 reference보다 1 m 이상 나쁜 경우

## 전체 결과 재확인

| 비교 | mean gain | tail worsened |
|---|---:|---:|
| hop vs fixed | +0.849 m | 0.214 |
| softR vs hop | +3.948 m | 0.028 |
| softR vs fixed | +4.797 m | 0.131 |

softR는 plain hopping 대비 tail을 21.4%에서 2.8%로 크게 낮췄다.  
하지만 fixed 대비로는 13.1% tail이 남아 있으므로, “tail-free” 또는 “항상 개선” claim은 금지한다.

## 거리별 tail 분포

softR vs fixed tail worsened fraction:

- 0 m: 0.083
- 100 m: 0.021
- 200 m: 0.042
- 300 m: 0.062
- 400 m: 0.062
- 500 m: 0.188
- 600 m: 0.229
- 700 m: 0.229
- 800 m: 0.167
- 900 m: 0.167
- 1000 m: 0.188

tail은 주로 500--1000 m 장거리 쪽에 남는다. 특히 600--700 m에서 fraction이 가장 높았다.  
다만 거리 평균 gain은 대부분 양수이므로, tail이 평균 성능 개선을 부정하지는 않는다.

## 운동 조건별 tail 분포

softR vs fixed tail worsened fraction:

- radial_0.05: 0.098
- radial_1.0: 0.136
- tangential_1.0: 0.106
- tang_1.0_vz: 0.182

가장 취약한 조건은 tangential motion과 vertical component가 섞인 `tang_1.0_vz`였다.  
이는 63--67번에서 관찰된 moving geometry tail risk와 같은 방향이다.

## 대표 tail 집중 셀

가장 높은 softR vs fixed tail fraction을 보인 셀:

- 700 m / radial_1.0: 0.417
- 900 m / tang_1.0_vz: 0.333
- 600 m / radial_0.05: 0.333
- 1000 m / tangential_1.0: 0.333
- 600 m / tang_1.0_vz: 0.333

## 논문 반영 방향

허용:

> Transition-aware soft-R substantially reduces the plain-hopping tail, but residual softR-vs-fixed tail cases remain and concentrate in specific long-range/motion cells.

금지:

- softR가 tail을 제거했다.
- softR가 모든 이동 조건에서 fixed보다 항상 좋다.
- arbitrary moving target 일반화.

## 후속 연구 연결

남은 tail은 후속 연구의 좋은 출발점이다.

- tangential+vertical motion guard
- radial transition guard
- carrier schedule risk prediction
- online tail-risk classifier

이번 논문에서는 이들을 future work로 두고, 현재 claim은 simulation-level structured/OOD moving validation 안에서만 유지한다.

## 산출물

- `analyze_moving_tail_cases.py`
- `moving_tail_decomposition.json`
- `result_summary.md`

