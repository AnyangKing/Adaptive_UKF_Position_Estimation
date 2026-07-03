# 10. SRP-PHAT 관측 UKF

## 목적

약 200 m 독립-noise 궤적에서 지배적인 횡방향 오차를 줄이기 위해 UKF의 DOA 관측을
GCC-PHAT 최소제곱에서 꼬리오차가 작았던 3D SRP-PHAT로 바꾼다.

## 공정 비교 조합

1. GCC DOA + strongest TOA: 8번/9번 기준
2. SRP DOA + strongest TOA: DOA만 변경
3. SRP DOA + tracked TOA: 방향과 방사거리 개선 결합

모든 조합은 같은 원시 신호, TDOA, Q, 기본 R, adaptive R 규칙과 초기 공분산을 쓴다.
SRP 관측에서도 GCC-SRP 불일치는 quality 지표로 유지한다.

## 계산량

SRP는 2° 전역 3D 격자와 0.2° 국소 격자를 탐색하므로 GCC 최소제곱보다 비싸다.
신호 관측 추출 시간과 UKF update 시간을 분리해 기록한다.

## 실행

```powershell
python test_srp_ukf.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

| 조합 | 5시점 이후 RMSE | 방사 RMSE | 횡방향 RMSE | 최대오차 |
|---|---:|---:|---:|---:|
| GCC + strongest | 13.384 m | 1.638 m | 13.284 m | 24.776 m |
| SRP + strongest | **8.284 m** | 1.189 m | **8.198 m** | **12.912 m** |
| SRP + tracked | 9.789 m | **0.597 m** | 9.770 m | 13.450 m |

SRP+strongest는 기존 기준 대비 수렴 후 위치 RMSE를 38.11% 줄였다. SRP 관측으로
횡방향 오차가 크게 감소했으며 현재 200 m 독립-noise 조건의 최선 조합이다.

tracked TOA는 방사오차를 추가로 절반 줄였지만 횡방향 오차와 전체 RMSE를 악화시켰다.
UKF가 강하게 결합된 중복 관측의 cross covariance를 완전히 모델링하지 못해 정확한
거리관측이 편향된 방향관측과 충돌하기 때문이다. 따라서 현재는 SRP+strongest를 채택하고
tracked TOA는 향후 관측 decorrelation 또는 분리 update 실험에 남긴다.

평균 신호 관측 추출 시간은 ping당 677.4 ms, UKF update는 약 1.9 ms였다. 병목은 UKF가
아니라 SRP 3D 격자 탐색이다. 1 Hz ping에서는 근실시간이지만 더 높은 갱신율에는 이전
방향 주변 국소탐색 또는 GPU/vector cache 최적화가 필요하다.
