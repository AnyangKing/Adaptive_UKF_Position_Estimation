# 233. Static full range independent validation

## 목적

다른 AI가 지적한 첫 번째 미해결 약점인 **정지 표적 0--1000 m n≥20 최종검증 부족**을 보완했다.

기존 상태는 다음과 같았다.

- 61번: 600 m 정지 헤드라인을 n=20 독립검증으로 지지
- 184번: 0--1000 m 정지 sweep을 수행했지만 거리별 n=6 diagnostic
- 191번 이후: 이동 표적은 0--1000 m에서 훨씬 큰 검증 밀도 확보

따라서 본 폴더는 184번의 low-n trend map을 독립 seed의 거리별 n=20 검증으로 확장했다.

## 프로토콜

- 거리: 0, 100, ..., 1000 m
- 표본 수: 거리별 n=20, 총 220 cases
- 정책:
  - fixed 32 kHz
  - 30--34 kHz carrier hopping
  - transition-aware soft-R
- 기존 183/184의 frozen signal-level observation/filter protocol 유지
- 새 알고리즘, 새 threshold, 새 claim 추가 없음
- seed root는 184와 분리
  - geometry seed root: 2,330,000
  - ping seed root: 2,333,000

## 핵심 결과

전체 220 paired cases:

| 비교 | 평균 이득 | 95% CI | p | improved fraction | tail worsened |
|---|---:|---:|---:|---:|---:|
| hop vs fixed | +2.001 m | [1.286, 2.740] | 5.343e-09 | 0.645 | 0.141 |
| softR vs hop | -0.011 m | [-0.041, 0.011] | 0.5705 | 0.023 | 0.005 |
| softR vs fixed | +1.990 m | [1.275, 2.730] | 5.866e-09 | 0.645 | 0.141 |

정지 표적에서는 transition-aware soft-R가 거의 발화하지 않으므로 hop baseline과 사실상 동일하게 동작했다. 따라서 정지 표적 claim은 **carrier agility 자체의 full-range simulation support**로 쓰는 것이 맞다.

## 거리별 해석

- 0 m는 near-vertical degenerate case이므로 긍정 근거로 쓰지 않는다.
- 100 m는 거의 중립이다.
- 200 m와 500 m는 평균 이득이 음수 또는 거의 0으로, 모든 거리에서 항상 개선된다는 claim을 금지한다.
- 600--1000 m 장거리 구간에서는 평균 이득이 뚜렷하다.
  - 600 m: +2.763 m
  - 700 m: +3.919 m
  - 800 m: +4.146 m
  - 900 m: +6.459 m
  - 1000 m: +3.414 m
- tail worsened fraction은 전체 14.1%이며, 특히 0 m와 1000 m에서 높다. 따라서 평균 개선과 tail risk를 함께 보고해야 한다.

## 논문 반영 방향

허용:

> In a 0--1000 m static simulation validation with 20 independent geometries per distance, carrier hopping reduced mean settled RMSE by 2.00 m relative to fixed-carrier tracking, with the strongest mean gains in the 600--1000 m range.

금지:

- carrier hopping이 모든 거리에서 개선된다.
- 정지 0--1000 m 결과가 실해역 성능을 보장한다.
- 0 m near-vertical case를 일반 short-range 성능 근거로 사용한다.
- tail risk 없이 평균만 보고한다.

## 산출물

- `run_static_full_range_independent_validation.py`
- `static_full_range_independent_validation.json`
- `result_summary.md`

