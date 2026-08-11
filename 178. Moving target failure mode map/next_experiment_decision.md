# Next experiment decision

## 결정

다음 실험은 schedule-only moving method가 아니라 carrier transition이 만든 관측 위험을 다룬다.

1. 179번: 162번 TOA branch switching guard를 독립 seed에서 검증한다.
2. 180번: guard 개념을 carrier-transition-aware Adaptive-R 후보로 일반화해 moving target 개발 조건에서 찔러본다.

## 이유

- 63번은 carrier agility가 residual lag-1을 낮춘다는 기전은 보였지만 moving pooled RMSE gain은 보이지 않았다.
- 64--67번은 schedule을 바꾸거나 oracle condition rule을 써도 독립 seed에서 이득이 안정적으로 재현되지 않았다.
- 162번의 TOA branch switching은 ground truth 없이도 reference TOA jump와 carrier transition으로 감지할 수 있다.

## 금지

- 179 또는 180이 독립검증 전이면 논문 성능 claim으로 쓰지 않는다.
- moving target RMSE 개선을 lag-1 whitening만으로 주장하지 않는다.
- oracle condition label 또는 post-hoc geometry 선택을 제안법 입력으로 쓰지 않는다.
