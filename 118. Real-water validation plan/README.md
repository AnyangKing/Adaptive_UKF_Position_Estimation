# 118. Real-water validation plan

## 목적

현재 논문은 시뮬레이션·신호수준 검증으로 충분히 조립되어 있지만, 더 높은 저널이나 교수님 판단에 따라
호수/해상/수조 검증이 필요할 수 있다. 118번은 그때 바로 움직일 수 있도록 **최소 실험 프로토콜**을
설계한 폴더다.

새 실험을 실행하지 않았다. 대신 실제 실험으로 넘어갈 때 무엇을 측정해야 하고, 어떤 결과가 나오면
논문 claim이 강화되거나 약해지는지 사전등록 형태로 정리했다.

## 핵심 전략

실해역 검증은 한 번에 600 m 성능 실험으로 뛰면 위험하다. 먼저 “기전이 실제 물에서도 보이는가”를
확인하고, 그다음 “위치 RMSE가 줄어드는가”를 확인해야 한다.

1. **Tier 1: mechanism validation**
   - 목표: fixed carrier에서 DOA residual lag-1 상관이 생기고, carrier agility가 이를 낮추는지 확인.
   - 장소: 수조, 항만, 짧은 호수 구간 등 가능.
   - 성공 기준: RMSE보다 DOA residual whitening이 우선.

2. **Tier 2: static long-range validation**
   - 목표: 400~600 m 정지 표적에서 fixed 32 kHz 대비 30~34 kHz ping-to-ping schedule의 RMSE 개선 확인.
   - 장소: 호수/해상.
   - 성공 기준: paired RMSE gain + lag-1 whitening 동시 확인.

3. **Tier 3: very-slow-drift validation**
   - 목표: 0.005 m/s 수준의 매우 느린 drift까지 확장 가능한지 확인.
   - 성공 기준: 82번과 동일하게 0.005 m/s까지만 연속 경계로 본다.

## 산출물

- `experiment_protocol.md`: 실험 구성과 절차.
- `success_criteria.md`: 성공/부분성공/실패 판정 기준.
- `measurement_log_template.md`: 현장 기록 템플릿.
- `risk_and_fallback.md`: 실패 가능성과 대체 경로.

## 다음

118번 이후 교수님 없이 더 할 수 있는 후보는 두 가지다.

1. 119번: `Carrier schedule ablation plan` — 30~34 kHz schedule이 임의적이라는 공격에 대비.
2. 120번: `Supplement archive dry run` — 결과 JSON/CSV와 코드만 모아 보충자료 ZIP 구조 설계.

내 판단으로는 119번이 먼저다. 실험을 당장 못 하는 상황에서는 schedule ablation 설계를 해두면 방법론
방어가 더 단단해진다.
