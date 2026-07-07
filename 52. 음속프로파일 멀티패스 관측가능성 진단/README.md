# 52. 음속프로파일 멀티패스 관측가능성 진단

## 목적

방향 A(위치 + 음속 프로파일 joint 추정)의 전제를 먼저 진단한다. 원래 "물리 경로 일관성" 아이디어를
반증된 per-ping 신뢰도 추론이 아니라 '환경(음속 프로파일)을 멀티패스로 추정'하는 쪽으로 재조준한
것이다. 그 성립 조건: 관측 가능한 양만으로 음속 gradient를 복원할 수 있는가(관측가능성)를 GT를
label로만 써서 확인한다.

## 방법

- N=240 장면. 소스 위치(거리 100~600 m, 방위·깊이)와 음속 gradient(-0.12~+0.12 s⁻¹)를 **서로 독립**
  으로 랜덤 생성. 독립이므로 관측→gradient 예측력이 있으면 위치 교락이 아니라 gradient 자체의 signature다.
- blind 관측 벡터(위치 GT 미사용): TOA 거리 z[0], DOA 고도, 멀티패스 도착지연(직접-반사 1·2차, peak
  퍼짐), GCC-SRP 불일치, peak margin.
- 지표: 관측→gradient ridge 회귀의 out-of-sample R²(무작위 50:50 split 200회 분포)와 feature별 Spearman.
- 실행: `python run_observability.py`, 계약검증 `python test_diagnostic.py`.

## 결과 (2026-07-07)

| 지표 | 값 |
|---|---:|
| gradient 복원 out-of-sample R² (중앙값) | **−0.049** |
| R² CI90 | [−0.201, +0.023] |
| P(R²>0) | 0.15 |

feature → gradient Spearman: doa_elevation ρ=+0.197 (p=0.002), second_reflection_delay ρ=−0.133
(p=0.040), 나머지 무의미.

- **단일 ping 관측만으로는 음속 gradient가 복원되지 않는다**(out-of-sample R² 음수 = 평균 예측보다
  못함). gradient는 elevation에 약한 흔적을 남기지만(ρ=0.20) 이는 소스 깊이·기하와 교락돼 단일 ping
  에서는 분리되지 않는다.

## 판정

**진단 (단일 ping 프로파일 관측가능성 약함).** 방향 A의 순진한 형태 — 한 ping의 관측으로 프로파일을
blind 복원 — 는 성립하지 않는다. gradient의 관측 signature가 약하고 기하와 교락된다.

**단, 방향 A가 닫힌 것은 아니다.** 이 테스트는 **단일 ping**만 본 것이고, joint 추정의 본질은 소스가
이동하는 **다중 ping**이다. gradient는 한 궤적 내내 **상수**인데 위치(거리)는 변한다. 51번에서 gradient가
거리의존 편향을 만든다(관측거리↔편향 ρ=−0.40)고 확인했으므로, **궤적에서 거리가 변할 때 나타나는
편향 패턴으로 상수 gradient를 분리·식별**하는 것은 근본적으로 다른(그리고 아직 안 해본) 테스트다.
이것이 실제 joint 필터가 프로파일을 추정하는 방식이며, 다음 진단 후보다:
- (다음 후보) 다중 ping 궤적에서 상수 gradient의 시간적 식별가능성: 여러 ping의 거리-편향 패턴이
  gradient를 유일하게 결정하는지, 관측 Fisher 정보로 gradient가 identifiable한지.
- 그 밖에도 프로파일을 여러 파라미터로 확장하거나, 반사경로 도착각을 직접파와 대비하는 등 미탐색
  형태가 남아 있다. (연구 공간을 단일 ping 결과로 닫지 않는다.)

여기서 다중 ping 식별성도 약하면, 프로파일-aware 방향은 "프로파일을 외부(CTD)로 알아야 하는 conventional
보정"으로 정리하고, novelty 탐색은 또 다른 미탐색 방향으로 옮긴다.

주의: N=240 단일 ping, gradient 선형 프로파일 단일 파라미터화다. 회귀 파이프라인은 합성 신호에서 R²
복원·null 케이스로 검증했다(테스트 통과). 편향은 gated SRP 격자(0.2°)로 하한 추정된다.
