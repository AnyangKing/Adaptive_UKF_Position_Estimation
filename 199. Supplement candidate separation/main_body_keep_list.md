# Main-body keep list

## 반드시 본문에 남길 항목

### 1. Related-work positioning table

현재 원고의 related-work table은 단순 참고문헌 목록이 아니라 novelty 방어 장치다.

남겨야 하는 이유:

- TOA/TDOA/DOA + Kalman/UKF 자체는 이미 존재한다는 점을 정직하게 인정한다.
- frequency agility/pulse-to-pulse agility가 레이더 glint 문헌에 있다는 점도 숨기지 않는다.
- 본 논문의 기여가 “최초 발명”이 아니라 “얕은 수중 compact USBL에서의 물리 기전·관측 설계·적용 경계 규명”이라는 것을 초반에 고정한다.

### 2. Concept/mechanism figure

기전 그림은 본 논문의 중심축이다.

남겨야 하는 이유:

- 리뷰어가 “그냥 알려진 기법 조합 아닌가?”라고 물을 때, 수중 two-ray coherent bias와 작은 배열의 결합 문제를 직관적으로 보여준다.
- 결과표만으로는 왜 주파수 도약이 정지/준정지에서 통하고 이동에서 깨지는지 설명하기 어렵다.

### 3. Static 600 m validation

정지 표적 검증은 frequency agility의 가장 깨끗한 positive result다.

남겨야 하는 이유:

- 본 논문의 출발 기여인 coherent bias decorrelation이 실제 RMSE 감소로 이어진다는 핵심 증거다.
- 이동 표적 결과만 남기면 “왜 주파수 도약을 쓰는가?”가 약해진다.

### 4. Moving 0--1000 m validation

191번 결과는 현재 원고에서 가장 최신이고, 사용자가 원하는 이동 표적 방향으로 논문을 다시 살려주는 핵심 결과다.

남겨야 하는 이유:

- 600 m 유산을 넘어 0--1000 m 전 범위에서 검증했다.
- plain hopping의 한계와 transition-aware soft-R의 필요성을 동시에 보여준다.
- “실패하다가 성공하는 논문” 구조에서 성공 쪽의 중심 증거다.

### 5. Limitations table

한계표는 약점이 아니라 방어 장치다.

남겨야 하는 이유:

- 실제 수조/호수/해상 실험 전 단계라는 점을 정직하게 제한한다.
- simulation-only, channel realism, OOD motion, real-time implementation 같은 리뷰어 공격점을 먼저 정리한다.

## 가능하면 본문에 유지할 항목

- estimator baseline table: NLS/EKF/plain UKF/proposed 비교의 공정성을 보여준다.
- adaptive-R routing ablation table: 제안법의 구성요소가 무엇인지 보여준다.
- quasi-static speed sweep figure/table: 정지와 이동 사이의 경계 설명에 유용하다.

다만 쪽수 제한이 강하면 quasi-static 상세 표는 보충자료 후보로 보낼 수 있다.
