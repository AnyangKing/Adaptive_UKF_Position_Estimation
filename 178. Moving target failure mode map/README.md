# 178. Moving target failure mode map

## 목적

정지/준정지에서는 carrier-agile pinging의 이득이 재현되었지만, 이동 표적에서는 residual whitening이 RMSE 개선으로 일반화되지 않았다. 이 폴더는 63--67, 160--162번 결과를 다시 읽어 “이동 표적에서 무엇이 실패했고, 무엇이 아직 살릴 만한가”를 정리한다.

새 성능 실험을 돌리지 않는다. 기존 결과를 재분류해 다음 실험(179, 180)의 방향을 정하는 감사·설계 폴더다.

## 핵심 결론

1. 이동 표적에서는 carrier agility가 DOA residual lag-1을 낮추지만 pooled RMSE 개선은 재현되지 않았다.
2. fixed carrier에서도 표적 운동이 경로 차를 바꾸기 때문에 motion self-whitening이 이미 작동한다.
3. 64--67번의 schedule/risk-aware 계열은 독립 seed에서 안정적 이득을 보이지 못했다.
4. 160--162번이 보여준 tail 원인 중 TOA branch switching은 실제 관측 가능한 reference TOA jump로 감지 가능하다.
5. 따라서 다음 후보는 “도약 스케줄을 더 영리하게 고르는 것”보다 “carrier transition이 관측 추출에 만든 위험을 UKF 관측공분산에 반영하는 것”이 더 타당하다.

## 산출물

- `build_failure_mode_map.py`: 기존 결과 JSON을 읽어 실패 모드 표를 생성한다.
- `failure_mode_map.json`: 기계 판독 가능한 요약.
- `failure_mode_map.md`: 사람이 읽는 실패 지도.
- `next_experiment_decision.md`: 179/180으로 넘어가는 이유와 claim boundary.

## 다음 결정

- 179: 162번 TOA branch switching guard를 post-hoc pilot에서 독립검증으로 승격한다.
- 180: 정지 tail에만 묶인 TOA guard를 moving target에서도 사용할 수 있는 carrier-transition-aware Adaptive-R 후보로 재정의한다.

단, 180은 “성공 주장”이 아니라 개발 후보 검증이다. 독립 seed 통과 전에는 논문 성능 claim으로 쓰지 않는다.
