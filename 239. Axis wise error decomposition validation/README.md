# 239. Axis wise error decomposition validation

## 목적

238번은 transition-aware softR의 NEES/NIS 일관성을 확인했지만, 3D 오차가 수평/수직/radial/cross-range 중 어디에 실리는지는 저장하지 않았다.

이 폴더는 191/238과 같은 이동표적 0--1000 m 독립 검증 프로토콜을 재실행하면서 상태 공간의 축별 오차를 기록한다.

## 기록 지표

- `x_rmse_m`, `y_rmse_m`, `z_rmse_m`
- `horizontal_rmse_m`
- `vertical_rmse_m`
- `radial_rmse_m`
- `cross_range_rmse_m`
- 각 축의 signed bias
- settled 구간은 기존과 동일하게 20 ping 중 후반 10 ping이다.

## 해석 원칙

- 이 결과는 DOA block NIS가 관측 공간에서 보여준 병목을 위치 상태 공간에서 다시 확인하기 위한 진단이다.
- 수평 오차와 수직 오차를 분리해 USBL 관례상 중요한 horizontal localization 성능을 따로 볼 수 있게 한다.
- radial/cross-range 분해는 배열 기준 방사방향/접선방향 오차가 어디에 몰리는지 보기 위한 보조 진단이다.
- 새 알고리즘을 제안하지 않는다.

## 결과 요약

transition-aware softR는 hop baseline 대비 3D RMSE뿐 아니라 수평/수직 오차도 함께 줄였다.

- 3D RMSE: 11.337 m → 7.389 m
- horizontal RMSE: 7.457 m → 4.851 m
- vertical RMSE: 7.442 m → 4.582 m
- radial RMSE: 0.940 m → 0.625 m
- cross-range RMSE: 7.275 m → 4.664 m
- divergence rate: 7.2% → 0.4%

해석상 중요한 점은 오차가 radial 방향보다 cross-range와 vertical 방향에 크게 실린다는 것이다. 이는 소형 USBL 배열의 DOA/고도각 취약성이 위치 오차에서도 드러난다는 기존 기전 해석과 잘 맞는다.

단, 이 결과는 여전히 191/238과 같은 시뮬레이션 프로토콜의 상태공간 진단이다. 실해역 성능이나 arbitrary moving-target 일반화를 주장하지 않는다.
