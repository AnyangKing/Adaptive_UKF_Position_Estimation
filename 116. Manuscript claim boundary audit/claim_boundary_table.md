# Claim boundary table

## 핵심 판정

| Claim 영역 | 현재 원고 상태 | 판정 | 유지/수정 규칙 |
|---|---|---|---|
| Novelty | “frequency hopping 자체가 아니라 post-gating coherent DOA bias whitening”으로 표현 | 안전 | “first frequency-hopping USBL” 금지 |
| 정지 표적 성능 | 600 m static, fixed 13.01 m → hop 8.87 m, p=0.0008 | 안전 | 모든 거리·모든 조건 개선으로 확장 금지 |
| 준정지 | 0.005 m/s까지만 continuous boundary로 제한 | 안전 | 0.030/0.100 m/s 양성 결과는 geometry-dependent recovery로만 설명 |
| 이동 표적 | lag-1 whitening은 strong, pooled RMSE gain은 not reliable | 안전 | moving target localization improvement claim 금지 |
| 성능 규모 | sub-meter long-range 아님을 명시 | 안전 | “600 m sub-meter” 금지 |
| UKF | tracking backbone으로 설명 | 안전 | adaptive UKF 자체를 주 novelty로 재상승시키지 않기 |
| Frequency schedule | 30–34 kHz frozen, simple, not globally optimized | 안전 | 최적 schedule이라고 주장 금지 |
| 시뮬레이션 한계 | real-water/tank validation 필요 명시 | 안전 | 실해역 검증 완료처럼 쓰지 않기 |
| 선행연구 | radar/FH USBL/Costas/comb 선행 인정 | 안전 | “직접 선행연구 없음”은 “현재 조사 범위에서” 톤 유지 |

## 단어별 위험도

| 표현 | 위험 | 권장 표현 |
|---|---|---|
| first / 최초 | 매우 높음 | “to our knowledge within the surveyed literature”, 또는 아예 회피 |
| prove | 중간~높음 | show, indicate, support, demonstrate |
| validated to 0.1 m/s | 매우 높음 | positive but non-continuous at 0.100 m/s |
| moving-target improvement | 매우 높음 | moving-target residual whitening without reliable RMSE gain |
| removes multipath | 높음 | mitigates one coherent residual component |
| sub-meter | 매우 높음 | meter-scale floor remains due to compact aperture |
| optimal carrier schedule | 높음 | frozen simple schedule / not globally optimized |

## 원고에서 계속 지켜야 할 중심문장

> Carrier-agile pinging whitens a carrier-locked coherent multipath DOA residual in static
> long-range shallow-water USBL tracking. It improves the 600 m static validation case, but moving
> targets and faster quasi-static cases define a boundary rather than a general performance claim.

이 문장이 현재 논문 안전선의 핵심이다.
