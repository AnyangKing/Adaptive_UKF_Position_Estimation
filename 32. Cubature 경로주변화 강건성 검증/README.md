# 32. Cubature 경로주변화 강건성 검증

## 목적

31번 validation에서 선택한 정책(`timing_std=1 ms`, `temperature=1`)을 변경하지 않고 더 많은
신규 궤적에서 cubature 경로가설 주변화의 재현성을 paired 검증한다.

## 설계

- 완전 신규 seed, 거리당 8개·총 32개 10-ping 궤적
- 동일 신호와 초기값에 baseline/soft update를 paired 적용
- 평균, 개선 궤적 비율, bootstrap 95% CI, 단측 Wilcoxon, 발산률 기록
- 실행 결과를 본 뒤 정책이나 문턱을 재조정하지 않음

## 결과 (2026-07-05)

| 거리 | Baseline 평균 RMSE | Soft 평균 RMSE | 변화 |
|---:|---:|---:|---:|
| 100 m | 1.364 m | 1.244 m | -8.83% |
| 200 m | 3.671 m | 3.377 m | -8.02% |
| 400 m | 6.578 m | 6.874 m | +4.50% |
| 600 m | 5.831 m | 5.905 m | +1.28% |

전체 평균은 4.361→4.350m(-0.25%)였고 개선량 bootstrap 95% CI는
`[-0.751, +0.712]m`, 단측 Wilcoxon `p=0.227`이다. 32개 중 59.4%에서 개선됐지만 통계적
우위를 보이지 않았다.

가장 큰 실패는 400m 한 궤적의 7.51→15.43m 악화였다. 이 궤적은 평균 유효 point 4.84/12,
최대 가중치 0.46, evidence span 8.41로 가장 강한 확신을 보였다. 단순 confidence gate로는
`confidently wrong` 경로 모드를 제거할 수 없다.

## 판정

31번의 예비 개선은 다수 신규 궤적에서 **재현되지 않아 현재 형태를 기각**한다. Soft
marginalization 원리 자체는 100/200m에서 평균 8% 개선을 보였으나, 잘못된 모드가 기존
TOA/TDOA/DOA posterior를 과도하게 이동시키는 tail risk가 남는다.

다음 단계는 evidence confidence 문턱이 아니라, 경로 posterior가 기존 칼만 posterior에서 이동할
수 있는 Mahalanobis 거리를 제한하는 trust-region moment matching이다.
