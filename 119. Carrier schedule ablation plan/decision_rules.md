# Decision rules

## Primary decision for static schedule

Schedule을 채택하려면 아래를 모두 만족해야 한다.

1. mean settled RMSE gain > 0.
2. median gain > 0.
3. improved fraction ≥ 0.60.
4. P90/tail이 fixed보다 악화되지 않음.
5. DOA elevation residual lag-1이 감소.
6. 독립 seed validation에서 같은 방향 재현.

## Strong pass

- mean RMSE reduction ≥ 20%.
- paired p < 0.05.
- median gain도 충분히 양수.
- lag-1 reduction이 명확.
- tail safety 통과.

이 경우 원고 보충자료나 후속 논문에서 schedule design rule로 주장 가능.

## Weak pass

- mean/median gain은 양수지만 p가 약함.
- lag-1은 줄지만 RMSE gain은 작음.

이 경우 “mechanism-supporting schedule candidate”로만 둔다.

## Reject

- mean gain ≤ 0.
- median gain ≤ 0.
- P90/tail 악화.
- lag-1 reduction은 있어도 RMSE tail이 커짐.

특히 moving target에서는 lag-1 whitening만 보고 채택하면 안 된다. 63~67번에서 이미 이 함정을 확인했다.

## Do-not-cross lines

- development seed에서 고른 schedule을 바로 원고 본체 claim으로 쓰지 않는다.
- 0.100 m/s 양성 결과를 continuous quasi-static boundary로 쓰지 않는다.
- moving target schedule은 risk predictor 검증 전에는 performance claim으로 쓰지 않는다.
- 30–34 kHz linear sweep을 “optimal”이라고 부르지 않는다.

## 원고 반영 단계

| 결과 | 원고 반영 |
|---|---|
| ablation 미실행 | “schedule optimization remains future work” |
| static ablation pass | supplementary에 schedule robustness 추가 |
| static+0.005 m/s pass | quasi-static 보조 claim 강화 |
| moving schedule pass | 별도 후속 논문 후보. 현재 원고 본체에 무리하게 통합하지 않음 |
