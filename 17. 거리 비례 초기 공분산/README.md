# 17. 거리 비례 초기 공분산

## 목적

각도오차의 Cartesian 위치영향은 거리에 비례하지만 기존 초기 P는 모든 거리에서 위치
표준편차 8 m인 등방성 행렬이었다. 잘못된 장거리 초기 방향을 과신하지 않도록 구면
불확실성을 Cartesian 공분산으로 변환한다.

## 모델

초기 시선 단위벡터를 `u`, 거리 `r`이라 하면

`P_pos = sigma_r² uuᵀ + (r sigma_theta)² (I - uuᵀ)`

- radial std: 3 m
- angular std: 5°
- tangential std: `max(1 m, r×5°)`
- velocity std: 1.5 m/s

5°는 16번 validation에서 최악 거리 DOA RMSE가 약 5.52°였다는 근거로 보수적으로
고정했다. 이번 test 결과로 다시 조정하지 않는다.

## 비교

- fixed: 기존 위치 std 8 m 등방성
- geometry: 거리비례 이방성
- 신규 seed 170000 계열, 100/200/400/600 m 각 15 ping
- 원시 SRP 사용, Q/R/adaptive 규칙 동일

## 실행

```powershell
python test_covariance.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

| 거리 | Fixed P0 RMSE | Geometry P0 RMSE | 변화 |
|---:|---:|---:|---:|
| 100 m | 2.022 m | 2.018 m | +0.15% |
| 200 m | **36.559 m** | 49.234 m | -34.67% |
| 400 m | **26.182 m** | 26.228 m | -0.18% |
| 600 m | 21.249 m | **21.046 m** | +0.96% |

거리비례 P0는 유의미한 개선이 없고 200 m에서는 크게 악화돼 채택하지 않는다. 200 m
궤적은 두 방법 모두 초기오차 5.19 m에서 시작했지만 최종 53~62 m까지 발산했다. 초기
방향 불확실성을 더 크게 두는 것만으로는 시간 중간의 잘못된 방향관측을 해결할 수 없고,
오히려 초기에 해당 관측을 더 강하게 받아들여 악화될 수 있다.

따라서 기존 fixed P0를 유지한다. 다음 단계는 같은 200 m seed에서 SRP 방향의 시점별
오차와 jump를 진단하고, 물리적 최대 각속도 기반 causal outlier gate를 검토한다.
