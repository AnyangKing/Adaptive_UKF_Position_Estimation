# 180. Carrier transition aware Adaptive R moving pilot

## 목적

179번에서 hard TOA isolation guard는 독립 static seed에서 검증되지 않았다. 따라서 이 폴더는 guard를 성능 방법으로 승격하지 않고, 더 약한 형태의 carrier-transition-aware Adaptive-R 후보를 moving target development set에서 시험한다.

핵심 아이디어:

- carrier가 바뀌고
- reference TOA range가 직전 ping 대비 크게 점프하며
- 그 점프가 수신 관측에서 직접 계산 가능할 때

TOA block을 버리는 대신 TOA variance를 부드럽게 키운다. TDOA/DOA와 기존 GCC-SRP disagreement/NIS routing은 유지한다.

## 실험 지위

- stage: development pilot
- moving target 성능 claim 금지
- 독립검증 전까지 논문 본문 성능표에 넣지 않음
- 성공하면 181번 독립검증 후보, 실패하면 transition-aware R도 low-priority future work로 강등

## 비교

- `fixed_baseline`: fixed 32 kHz + 기존 ConditionalAdaptiveRUKF
- `hop_baseline`: 30--34 kHz linear hop + 기존 ConditionalAdaptiveRUKF
- `hop_transition_softR`: 30--34 kHz linear hop + carrier-transition-aware soft TOA variance routing

## 관측 입력

사용 가능한 런타임 지표만 쓴다.

- current/past reference TOA-derived range
- carrier transition flag
- GCC-SRP disagreement
- block NIS

ground truth motion label, true residual, fixed-vs-hop gain은 decision 입력에 쓰지 않는다.
