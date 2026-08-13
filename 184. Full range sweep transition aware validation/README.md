# 184. Full range sweep transition aware validation

## 목적

사용자 요청에 따라 0--1000 m를 100 m 단위로 훑어 fixed carrier, carrier-agile hop, transition-aware softR의 거리별 성능을 확인한다.

## 설계

- horizontal distances: 0, 100, ..., 1000 m
- geometries per distance: 6
- target: static source
- policies:
  - `fixed_baseline`
  - `hop_baseline`
  - `hop_transition_softR`

## 0 m 해석

0 m는 표적이 배열 중심의 수직선상에 놓이는 near-vertical special case이다. source depth는 12--78 m로 랜덤이므로 센서와 동일 위치가 아니며 직접 range는 존재한다. 일반적인 horizontal long-range claim과는 분리해 해석한다.

## claim boundary

- 이 sweep은 거리별 trend diagnostic이다.
- 거리당 n=6이므로 최종 성능 claim에는 부족하다.
- 강한 claim은 거리별 독립검증으로 다시 확장해야 한다.
