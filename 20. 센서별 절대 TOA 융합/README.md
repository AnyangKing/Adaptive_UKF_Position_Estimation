# 20. 센서별 절대 TOA 융합

## 목적

기준 TOA 1개와 GCC-TDOA 7개 대신 센서별 absolute TOA 거리 8개를 직접 UKF에 넣는다.
GCC-TDOA의 잘못된 peak와 공유 기준센서 상관을 피하고 9번에서 확인한 tracked TOA의
거리정확도를 활용한다.

## 관측

- baseline: `[range0, GCC TDOA ranges(7), SRP azimuth, elevation]`
- absolute strongest: `[absolute ranges(8), SRP angles(2)]`
- absolute tracked: 이전 ping 주변 peak를 추적한 absolute ranges 8개 + SRP angles

absolute TOA는 송신시각과 수신시계가 동기화됐다는 강한 가정이 필요하다. 기본 R은 센서
range std 0.03 m와 DOA std 2°의 대각행렬이며 range/DOA block NIS soft gating을 쓴다.
센서별 TOA 오차의 경험적 cross covariance는 아직 포함하지 않았다.

신규 seed 200000 계열의 100/200/400/600 m 궤적에서 현재 최선인 19번 조건부 TDOA와
비교하며 결과로 R을 다시 맞추지 않는다.

## 실행

```powershell
python test_absolute.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

| 거리 | 조건부 TDOA | Absolute strongest | Absolute tracked |
|---:|---:|---:|---:|
| 100 m | **1.629 m** | 1.636 m | 1.636 m |
| 200 m | 5.865 m | **5.853 m** | **5.853 m** |
| 400 m | 28.097 m | 27.745 m | **27.504 m** |
| 600 m | 25.485 m | 25.533 m | **24.203 m** |

absolute tracked는 400 m에서 2.1%, 600 m에서 5.0% 개선했지만 100/200 m는 사실상
동일했다. 모든 구조의 초기오차가 같고 이후 차이도 작아 장거리 병목은 거리관측이 아니라
SRP 방향 초기화임을 다시 확인했다.

absolute TOA 8개는 송수신 동기화라는 강한 가정과 센서간 오차 cross covariance 모델이
추가로 필요하므로 이 정도 개선으로 기준 구조를 교체하지 않는다. 조건부 TDOA 구조를
유지하고, 다음에는 첫 여러 ping의 SRP 방향을 causal하게 평균해 초기 방향 분산을 줄이는
다중 ping 초기 획득을 비교한다.
