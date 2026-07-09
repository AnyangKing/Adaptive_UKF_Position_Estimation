# 87. Method equations integration

## 목적

85번 원고 v0의 약한 부분인 System/Method 수식 밀도를 보강한다.

이번 폴더는 원고 본문에 바로 삽입 가능한 수식 블록, notation table, 절별 삽입 계획을 제공한다. 최종 수식 번호와 LaTeX 스타일은 target journal template에 맞춰 이후 조정한다.

## 포함 파일

- `method_equations_v1.md`: observation model, UKF state model, carrier-agile mechanism 수식 초안
- `notation_table.md`: 주요 기호 정의
- `manuscript_insertion_plan.md`: 85번 원고 v0의 어느 위치에 어떤 수식을 삽입할지
- `equation_claim_check.md`: 수식이 과장 claim을 만들지 않는지 점검

## 핵심 방향

수식은 “새로운 복잡한 필터”를 강조하지 않는다. 오히려 다음을 명확히 한다.

1. TOA/TDOA/DOA 관측 구조
2. UKF는 표준 추적 backbone
3. novelty는 carrier schedule이 residual phase를 바꾼다는 observation-design 측면
4. moving target에서는 `delta(t)`가 변해 self-whitening이 생길 수 있음

## 다음 단계

88번에서는 85번 원고 v0에 figure/table references를 삽입하거나, Introduction/Related Work를 citation placeholder-safe 상태로 더 다듬는 것이 좋다.
