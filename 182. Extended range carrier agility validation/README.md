# 182. Extended range carrier agility validation

## 목적

기존 61번의 100--600 m 결과는 이전 프로젝트 유산에 가까웠다. 이 폴더는 600 m를 넘어 800 m와 1000 m에서 carrier-agile pinging의 효과가 유지되는지 독립 seed로 확인한다.

## 설계

- target: static source
- distances: 800 m, 1000 m
- geometries per distance: 12
- steps: 20
- settled window: last 10 pings
- comparison:
  - fixed 32 kHz
  - linear20 carrier agility, 30--34 kHz
- paired design:
  - 같은 geometry, environment, ping seed를 fixed/agile에 입력

## 판정

주요 지표:

- mean/median settled RMSE
- P90 settled error
- divergence rate
- paired gain, CI95, Wilcoxon one-sided p

## claim boundary

- 이 폴더는 800/1000 m simulation extension이다.
- real-water 1 km 성능 claim으로 쓰지 않는다.
- 1000 m에서 이득이 나와도 “완벽 억제”라고 쓰지 않는다.
- SNR, gate, TOA branch switching, array aperture 한계 때문에 악화될 수 있음을 함께 기록한다.
