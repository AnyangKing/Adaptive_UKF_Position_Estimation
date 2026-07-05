# 36. 물리 feature 관측오차 예측력 진단

## 목적

31~35번에서 물리 경로 일관성으로 관측 신뢰도를 조절하는 필터가 모두 기각됐다. 공통 원인은
물리 residual score가 실제 관측오차와 분리되지 않는다는 것이었다. 필터를 더 복잡하게 만들기
전에, contamination likelihood에 넣을 후보 feature가 실제 DOA 관측오차를 예측하는 정보력을
가지는지 GT를 label로만 써서 먼저 독립 진단한다.

## 방법

- 거리 100/200/400/600 m, 거리당 60개 독립 정지 장면 (SNR 10/20/30, 반사계수·방위·수심 분리)
- 각 장면에서 신규 feature(경로배정 residual score, cubature 경로 주변화 evidence)와 기존
  feature(GCC-SRP 불일치, gated SRP peak margin, 최소 peak 품질)를 계산
- feature는 Ground Truth를 쓰지 않고 prior 위치로만 계산하며, prior 오차 0 m(정보 상한)와
  5 m(수렴 후 현실)를 모두 시험
- 실제 DOA 오차는 측정 방향과 GT 방향의 각도차로 정의하고, 상위 25% 오차를 이상 관측 label로 둠
- 지표: feature→label ROC AUC, feature와 DOA 오차의 Spearman 상관, validation에서 최고 AUC
  feature와 Youden 문턱을 골라 독립 test 정밀도/재현율로 일반화 확인
- validation/test seed 완전 분리, test 결과로 feature나 문턱을 재선택하지 않음

## 결과 (2026-07-05)

DOA 오차는 전 거리에서 작았다. test 중앙값 0.92°, P90 1.73°, 절대 5° 초과 비율 0%.

Test AUC와 DOA 오차 Spearman (prior 0 m, prior 5 m 동일 경향):

| feature | 종류 | test AUC | Spearman ρ | p |
|---|---|---:|---:|---:|
| path_residual_score | 신규 | 0.448 | -0.039 | 0.54 |
| neg_path_evidence | 신규 | 0.510 | -0.065 | 0.32 |
| doa_disagreement_deg | 기존 | 0.601 | 0.198 | 0.002 |
| peak_margin | 기존 | 0.573 | 0.045 | 0.49 |
| neg_min_peak_quality | 기존 | 0.506 | -0.002 | 0.98 |

- 신규 물리 feature `path_residual_score`는 validation AUC 0.607이었지만 독립 test 0.448로
  일반화에 실패했고 거리별 test AUC도 0.39~0.48로 우연 이하였다.
- prior 오차를 0 m로 줘도 신규 feature AUC가 개선되지 않아, 문제는 prior 부정확이 아니라
  feature 자체의 정보 부재다.
- 유일하게 유의한 feature는 기존 GCC-SRP 불일치(test AUC 0.601, ρ=0.198, p=0.002)였으나,
  거리별로 100 m 0.95, 200/400/600 m 0.57~0.58로 정작 병목인 장거리에서 약했다.
- validation 선택 feature(불일치) 문턱을 test에 적용한 정밀도는 0.31(기저율 0.25)로 이상 관측
  게이트로 쓰기에 약했다.

## 판정

물리 경로 일관성 feature가 실제 DOA 관측오차를 예측한다는 전제는 **성립하지 않는다(진단)**.
신규 residual score·경로 evidence는 oracle prior에서도 test AUC가 우연 수준이며 일반화하지 않아,
31~35번 계열이 왜 실패했는지 정량적으로 확인해 준다. 또한 DOA 오차 자체가 5° 미만으로 작고
거리 전반에 걸쳐 작은 편향으로 나타나므로, 게이팅할 이상 관측 집단이 존재하지 않는다. 장거리
병목은 검출 가능한 per-ping 오염이 아니라 기하학적으로 증폭되는 계통적 각도 편향이다.

가이드라인의 "예측력이 확인된 feature만 contamination likelihood에 포함한다"는 조건을 어떤
물리 feature도 통과하지 못했다. 따라서 per-ping 잠재 신뢰도 필터를 더 만들지 않는다. 다음
단계는 (a) 작은 계통적 DOA 편향과 거리 기하가 위치오차를 만드는 구조를 직접 모델링하거나,
(b) 유일하게 약한 신호였던 GCC-SRP 불일치가 그나마 유효한 근/중거리에 한정해 재검토하는
것이다. 신규성 주장은 이 진단 결과를 반영해 per-ping 신뢰도 추론에서 계통 편향 보정 쪽으로
재정의를 검토한다.
