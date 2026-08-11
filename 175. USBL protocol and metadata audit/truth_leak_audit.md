# Truth-leak audit

## 판정 기준

정답 위치는 다음 경우에만 허용한다.

- 수신 신호 합성
- 최종 위치 오차/RMSE/NEES 계산
- offline mechanism diagnosis

정답 위치를 다음에 쓰면 실패이다.

- TOA/TDOA/DOA 추출
- peak margin, GCC-SRP disagreement 등 quality 생성
- adaptive-R routing
- carrier schedule 또는 guard decision
- threshold tuning 후 test claim 유지

## 채택 실험별 감사

| 실험 | 관측 생성 | adaptive decision | truth 사용 | 판정 |
|---|---|---|---|---|
| 43. EKF/UKF/NLS 비교 | 수신 신호에서 TOA/TDOA/DOA 추출 | 없음 또는 고정 R | trajectory 생성, RMSE, NEES | 통과 |
| 44. conditional adaptive-R ablation | 수신 신호 기반 관측 | GCC-SRP disagreement, block/total NIS | trajectory 생성, RMSE, NEES | 통과 |
| 46. large-scale routing validation | 44와 동일 | GCC-SRP disagreement, NIS | trajectory 생성, RMSE, NEES | 통과 |
| 61. static hop validation | matched-filter TOA, GCC-PHAT TDOA, 5 ms gated SRP-PHAT DOA | GCC-SRP disagreement, NIS | signal synthesis, settled RMSE | 통과 |
| 63. moving hop validation | 61과 동일 | GCC-SRP disagreement, NIS | signal synthesis, RMSE, offline elevation residual lag-1 | 통과. lag-1은 기전 진단 |
| 82. quasi-static boundary | 61과 동일 | GCC-SRP disagreement, NIS | signal synthesis, RMSE, offline lag-1 | 통과. continuous boundary는 0.005 m/s까지만 |
| 160. four-carrier independent validation | 61과 동일 | GCC-SRP disagreement, NIS | signal synthesis, settled RMSE/P90/lag diagnosis | 통과. four-carrier는 실패 |
| 161. sparse-tail diagnostic | 160 결과를 본 뒤 선택한 post-hoc geometry 재생 | 성능 claim 없음 | mechanism diagnosis | 통과. 일반화 claim 금지 |
| 162. TOA guard pilot | post-hoc selected geometry | observed carrier change + TOA jump + NIS/disagreement | pilot 평가 | 통과. 독립검증 전 claim 금지 |

## 주의점

63번과 82번의 lag-1 residual은 `ideal_measurement(pos, cfg)`를 사용해 offline으로 계산한 mechanism metric이다. 이 값은 adaptive decision에 들어가지 않으므로 정답 누설은 아니다. 단, 논문에서는 위치 성능 claim이 아니라 residual-time-structure evidence로만 써야 한다.

## 다음 실험 README에 넣을 문장

```text
Truth usage: ground truth is used only for signal synthesis, final error metrics, and explicitly marked offline diagnostics. It is not used for measurement extraction, quality computation, adaptive-R decisions, carrier schedule decisions, or guard decisions.
```

