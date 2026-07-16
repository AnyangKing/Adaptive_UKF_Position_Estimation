# 161 결과 요약

## 핵심 발견

160번 geometry 2의 53 m tail은 raw DOA outlier가 아니라 **carrier-dependent TOA peak/path
switch를 sparse cycle이 반복 재생한 현상**으로 진단됐다.

| geometry 2 | fixed32 | linear20 | four-carrier cycle |
|---|---:|---:|---:|
| settled RMSE (m) | 10.151 | 7.360 | **53.001** |
| raw range-error span (m) | ~0 | 3.557 | 3.557 |
| raw range-error total variation (m) | ~0 | 3.558 | **32.013** |
| adjacent range jump >0.5 m | 0 | 1 | **9** |
| max TOA-block NIS | 0.0005 | 72.18 | **111.69** |
| max raw elevation bias (deg) | 1.029 | 0.771 | 0.771 |

geometry 2에서 30 kHz의 raw range error는 약 0.025 m, 나머지 four-carrier bank의 값은 약
3.582 m였다. cycle은 30 kHz로 돌아올 때마다 이 3.557 m 단차를 왕복해 ping 4/5, 8/9,
12/13, 16/17에서 TOA NIS burst를 반복했다. 위치오차는 후반에 누적되어 ping 16~19에서
50 m를 넘었다. 필터 예외는 없었다.

linear20도 같은 range span을 한 번 통과했지만 carrier를 되돌아가지 않아 큰 단차가 1회뿐이었고,
이후 같은 측정 branch에 머물러 7.36 m로 안정됐다. 즉 **carrier bandwidth 자체가 아니라
path-switch boundary를 반복 횡단하는 schedule topology**가 tail을 만들었다.

## 대조 기하

- geometry 5의 four-carrier 최대 인접 range jump는 0.022 m, geometry 19는 0.000017 m로
  0.5 m 초과 전환이 없었다.
- 따라서 모든 four-carrier 반복이 자동으로 발산하는 것은 아니다. 특정 기하에서 carrier bank가
  TOA peak-selection boundary 양쪽에 걸칠 때 위험하다.
- 세 기하는 결과를 보고 선택했으므로 이 패턴의 발생확률이나 일반화는 주장하지 않는다.

## 연구적 의미

현재 frequency agility는 DOA coherent bias를 백색화하지만, 송신 carrier 변경은 TOA matched-filter
peak 선택도 바꿀 수 있다. 따라서 schedule 설계의 새 안전조건은 다음 두 목적을 함께 만족해야 한다.

1. DOA의 carrier-dependent coherent bias를 평균 상쇄한다.
2. carrier-induced TOA branch switch를 반복적으로 재방문하지 않는다.

이는 기존 linear one-way sweep이 sparse cyclic bank보다 안정적이었던 기전 설명이다. 다음 개발
후보는 carrier 전환 시 TOA continuity를 감시해 반복 branch switch의 range update를 격리하는
**carrier-transition-aware TOA guard**다. 단, 이 진단 표본에서 만든 방법은 반드시 신규 seed에서
독립검증해야 한다.
