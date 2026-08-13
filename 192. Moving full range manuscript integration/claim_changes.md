# Claim changes after 191

## 이전 claim

| 항목 | 이전 원고 상태 |
|---|---|
| 정지 표적 | 600 m에서 carrier-agile schedule이 fixed 대비 RMSE를 낮춤 |
| 이동 표적 | lag-1 residual correlation은 낮아졌지만 pooled RMSE gain은 미재현 |
| 방법 기여 | 정지/준정지 장거리 USBL에서 coherent DOA bias 시간상관 완화 |

## 191 이후 허용 claim

| 항목 | 최신 허용 claim |
|---|---|
| 정지 표적 | 기존 claim 유지: 600 m fixed 13.01 m → agile 8.87 m, p=0.0008 |
| plain hopping 이동 표적 | 기존 실패 claim 유지: plain hopping만으로는 이동 표적 일반 성능 개선을 주장하지 않는다 |
| transition-aware 이동 표적 | 0--1000 m, 528 paired cases에서 frozen transition-aware Adaptive-R이 plain hopping 대비 +3.95 m, fixed 대비 +4.80 m 개선 |
| 기여 정의 | carrier-agile transmission과 runtime-observable transition-risk Adaptive-R을 결합한 관측-필터 설계 |

## 계속 금지되는 claim

- 실해역에서 검증됐다는 표현
- 모든 수중 환경 또는 모든 이동 궤적에서 성능 개선된다는 표현
- frequency hopping 자체를 최초 발명했다는 표현
- plain hopping 결과를 transition-aware 결과처럼 서술하는 표현
- 162번 post-hoc pilot을 독립 성능 검증처럼 사용하는 표현

## 리뷰어 방어 논리

63--67번은 “plain hopping 또는 단순 schedule 분기만으로 이동 표적 RMSE가 보편 개선된다”는 주장을 부정했다.  
191번은 “반송파 전환이 만드는 위험을 실제 관측 기반 Adaptive-R로 흡수하면, 현재 시뮬레이터의 0--1000 m 이동 표적 범위에서 tail을 줄이며 RMSE를 개선할 수 있다”는 더 좁은 주장을 지지한다.

