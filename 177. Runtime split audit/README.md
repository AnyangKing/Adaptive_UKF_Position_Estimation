# 177. Runtime split audit

## 목적

피드백 6번(인과성과 실행 가능성)에 맞춰, 채택된 신호 기반 USBL 파이프라인의 시간을 세 단계로 나눠 측정한다.

1. 수신 신호 합성 시간: 시뮬레이션 생성 비용이며 실제 온라인 필터 시간에는 포함하지 않는다.
2. 관측 추출 시간: matched-filter TOA, GCC-PHAT TDOA, gated SRP-PHAT array-level DOA와 신뢰도 지표 계산.
3. Adaptive UKF 갱신 시간: 현재 ping의 관측과 현재/과거 상태만 사용하는 causal predict-update.

이 폴더는 새 알고리즘이나 새 성능 주장을 만들지 않는다. 기존 61번 canonical 코드의 실행 가능성 감사를 위한 보조 측정이다.

## 산출물

- `runtime_split_audit.py`: 61번 채택 코드 위에서 단계별 wall-clock 시간을 측정한다.
- `runtime_split_summary.json`: 측정 환경, seed, 시나리오, 단계별 ms 통계.
- `runtime_split_notes.md`: 결과 해석과 논문 claim boundary.

## 해석 경계

- Python/MiKTeX/Windows 작업환경의 wall-clock 측정이므로 절대 실시간 보장값이 아니다.
- 신호 생성 시간은 시뮬레이션용 비용으로 분리한다.
- 온라인 추정 가능성 판단에는 관측 추출 + UKF 갱신 시간만 사용한다.
- 실험 결과 RMSE나 논문 헤드라인 수치는 변경하지 않는다.
