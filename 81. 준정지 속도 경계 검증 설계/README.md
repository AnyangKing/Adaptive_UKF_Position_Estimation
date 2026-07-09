# 81. 준정지 속도 경계 검증 설계

## 목적

현재 논문 본체는 “static/quasi-static long-range USBL에서 frequency-agile pinging이 coherent DOA bias를 백색화해 RMSE를 개선한다”는 주장이다.

정지 표적은 61번에서 검증됐고, 일반 이동 표적은 63~67번에서 RMSE 개선이 미재현됐다. 따라서 남은 중요한 경계는 **정지와 이동 사이의 준정지 속도 regime**이다.

이 폴더는 실험 실행 전 사전등록 설계다. 다음 AI가 실험을 수행할 때 조건을 임의로 바꾸지 않도록 기준을 고정한다.

## 핵심 질문

> target speed가 얼마나 작을 때까지 static 600 m에서 관찰된 frequency-agile 이득이 유지되는가?

## 가설

- H1: 속도 0 m/s에서는 61번 결과처럼 hop 이득이 유지된다.
- H2: 매우 느린 속도에서는 fixed carrier에서도 `δ(t)`가 조금 변해 self-whitening이 생기므로 hop 이득이 감소한다.
- H3: 특정 임계 속도 이상에서는 63번 moving 결과처럼 residual whitening은 되지만 RMSE 이득은 재현되지 않는다.

## 권장 실험 조건

| 항목 | 값 |
|---|---|
| 거리 | 600 m 우선, 가능하면 400 m 보조 |
| 속도 | 0, 0.005, 0.01, 0.03, 0.05, 0.10 m/s |
| trajectory | radial slow, tangential slow, optional shallow vertical drift |
| 비교 | fixed 32 kHz vs 30–34 kHz frequency-agile schedule |
| 반복 | 조건당 최소 12~20 geometry/seed |
| 주요 metric | settled RMSE gain, median gain, improved fraction |
| mechanism metric | DOA residual lag-1 correlation fixed vs hop |
| 통계 | paired Wilcoxon one-sided for RMSE gain; paired test for lag-1 reduction |

## 채택 기준

속도 조건 `v`에서 quasi-static 이득을 인정하려면:

1. mean RMSE gain > 0
2. median RMSE gain > 0
3. improved fraction ≥ 0.60
4. Wilcoxon p < 0.05 또는 p가 약하면 “trend only”로 표시
5. lag-1 residual whitening은 fixed > hop 방향으로 재현

위 조건 중 RMSE gain이 없고 lag-1만 줄면, 그 속도는 moving-boundary regime으로 분류한다.

## 결과 해석 기준

- 0~0.01 m/s에서 이득 유지: 논문 제목의 `static/quasi-static` 표현이 강해진다.
- 0 m/s만 이득: 제목/본문에서 `static targets`를 더 강하게 써야 한다.
- 0.03~0.05 m/s까지 이득: 계류 비콘·도킹·저속 드리프트 응용까지 주장 가능.
- 모든 저속에서 미재현: 61번 정지 결과는 유지하되 quasi-static 표현을 future work로 낮춘다.

## 다음 단계

82번에서 실제 실험을 구현한다. 63번 moving validation 코드와 61번 static validation 코드를 재사용하되, 속도 sweep만 새로 둔다. 기존 결과를 덮어쓰지 말고 새 폴더에서 독립 seed로 수행한다.
