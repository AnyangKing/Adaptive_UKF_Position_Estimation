# 185. Direct path only carrier agility control

## 목적

리뷰 지적 9번에 대한 첫 통제 실험이다.

Carrier agility의 성능 차이가 정말 in-gate coherent multipath phase rotation에서 오는지 보려면, multipath를 제거한 direct-only 채널에서 fixed carrier와 carrier-agile schedule을 비교해야 한다.

## 설계

- distances: 600, 800, 1000 m
- geometries per distance: 8
- target: static source
- channel:
  - `include_multipath=False`
  - `include_noise=True`
- comparison:
  - fixed 32 kHz
  - linear20 30--34 kHz
- paired design:
  - 같은 geometry/environment/ping seed
  - schedule만 변경

## 기대되는 해석

- direct-only에서 hop 이득이 사라지면, 기존 이득이 multipath coherent phase와 관련된다는 설명이 강화된다.
- direct-only에서도 큰 이득이 나오면, carrier-dependent SNR/array response/SRP behavior 등 다른 요인을 분리해야 한다.

## claim boundary

- 이 실험은 통제 실험이다.
- 성능 향상 claim이 아니라 mechanism attribution 검증이다.
- direct-only는 실제 얕은바다 채널이 아니라 원인 분해용 counterfactual이다.
