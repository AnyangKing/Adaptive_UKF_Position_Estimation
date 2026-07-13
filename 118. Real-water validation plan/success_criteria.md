# Success criteria

## Tier 1: mechanism validation

### Pass

- fixed 32 kHz에서 DOA elevation residual lag-1이 양의 상관을 보임.
- hop 30–34 kHz에서 lag-1이 의미 있게 감소.
- carrier별 residual 평균이 주파수에 따라 변하는 흔적이 있음.

권장 정량 기준:

- mean lag-1 reduction > 0.2 또는 paired test p < 0.05.
- fixed lag-1이 +0.2 이상인 조건에서 hop lag-1이 0 근처 또는 음수로 이동.

### Partial pass

- lag-1 감소는 있으나 RMSE 개선은 없음.
- carrier sensitivity는 보이나 ground truth 불확실도가 커서 RMSE 판단이 어려움.

해석: 논문 기전 보강에는 사용 가능하지만, 성능 claim으로 쓰지 않는다.

### Fail / non-informative

- fixed에서도 residual lag-1이 거의 없음.
- direct gate 내 surface reflection 에너지가 약함.
- 표적/수신기 흔들림이 커서 residual이 환경 잡음에 묻힘.

해석: 방법 실패라고 단정하지 않는다. “이 실험 조건에서는 coherent locked bias가 충분히 형성되지 않음”으로
기록한다.

## Tier 2: static long-range validation

### Pass

- paired RMSE gain이 양수.
- median gain도 양수.
- P90 또는 gross-error tail이 악화되지 않음.
- DOA residual lag-1 reduction이 함께 관측됨.

권장 정량 기준:

- 400/600 m에서 mean RMSE reduction ≥ 10%.
- paired test p < 0.05 또는 n이 작으면 모든/대부분 geometry에서 방향 일관.
- hop divergence/gross-error rate가 fixed보다 커지지 않음.

### Partial pass

- lag-1 whitening은 확인되지만 RMSE gain은 작거나 조건 의존.

해석: 논문 본체 성능 claim보다는 Discussion/Future Work 또는 보충자료로 사용.

### Fail

- hop이 tail을 크게 악화.
- fixed/hop 차이가 환경 drift나 ground-truth 오차보다 작음.
- carrier schedule이 하드웨어 대역폭/송신 출력 차이 때문에 공정 비교가 아님.

## Tier 3: very-slow-drift validation

### Pass

- 0.005 m/s 근처에서 static과 같은 방향의 RMSE gain.
- lag-1 whitening 동반.
- 0.010 m/s 이상 결과는 별도로 보고하되 연속 경계로 확대하지 않음.

### Fail

- 0.005 m/s에서도 tail 악화 또는 RMSE gain 미재현.

해석: 본 논문 claim을 static only로 더 좁히고, quasi-static은 future work로 둔다.

## 논문 claim 업데이트 규칙

| 실험 결과 | 원고 claim |
|---|---|
| Tier 1만 성공 | “real-water mechanism pilot supports residual whitening” 정도로 제한 |
| Tier 1+2 성공 | “real-water static validation” 추가 가능 |
| Tier 1+2+3 성공 | “static and very-slow-drift validation” 강화 가능 |
| Tier 1 실패 | 기존 시뮬레이션 논문 유지, 실험 조건 미형성으로 기록 |
| Tier 2 실패 | 성능 claim은 시뮬레이션으로 유지, field gap을 limitation으로 명시 |
