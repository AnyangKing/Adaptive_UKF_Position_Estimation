# Runtime split notes

## 핵심 결과

`runtime_split_audit.py`를 2026-08-11 작업환경에서 실행했다. 61번 canonical 신호 기반 파이프라인을 그대로 호출했고, 새 threshold나 새 알고리즘을 도입하지 않았다.

요약값은 `runtime_split_summary.json`에 저장했다.

| stage | n | mean ms | median ms | p90 ms | 해석 |
|---|---:|---:|---:|---:|---|
| signal synthesis | 20 | 37.117 | 38.065 | 47.103 | 시뮬레이션 수신 신호 생성 비용. 실제 온라인 추정 시간에서 분리 |
| measurement extraction | 20 | 213.594 | 206.587 | 356.798 | matched-filter TOA, GCC-PHAT TDOA, gated SRP-PHAT DOA와 신뢰도 추출 |
| UKF update | 16 | 1.525 | 1.416 | 1.615 | 초기화 이후 causal Adaptive UKF predict/update |
| online excluding synthesis | 20 | 214.814 | 208.034 | 358.185 | 관측 추출 + UKF 갱신 |

## 논문에 쓸 수 있는 말

- 현재 구현에서 UKF 갱신 비용은 관측 추출 비용보다 작다.
- 실행 시간 병목은 Adaptive UKF가 아니라 gated SRP-PHAT 기반 array-level DOA/신뢰도 추출 단계다.
- 온라인 결과는 현재 ping의 수신 신호와 과거 필터 상태만 사용한다.

## 논문에 쓰면 안 되는 말

- 이 측정만으로 실시간 임베디드 구현을 보장한다고 쓰면 안 된다.
- Python wall-clock 결과를 하드웨어 독립적인 절대 처리속도로 주장하면 안 된다.
- RMSE, P90, 발산률 등 위치추정 성능 claim을 이 폴더에서 바꾸면 안 된다.

## 피드백 항목 연결

- 6. 인과성과 실행 가능성: 관측 추출과 UKF 갱신 시간을 분리했다.
- 2. 물리적으로 획득 가능한 관측만 사용: 런타임 측정 입력은 신호에서 추출한 TOA/TDOA/DOA와 quality 지표다.
- 10. 논문 주장보다 실험 증거 우선: runtime claim boundary를 별도 명시했다.
