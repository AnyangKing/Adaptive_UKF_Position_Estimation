# 53. 위치 음속gradient joint UKF

## 목적

방향 A(위치 + 음속 프로파일 joint 추정)의 핵심 방법을 직접 만들어 검증한다. 52번은 단일 ping
관측가능성이 약함을 보였으나, joint 추정의 본질은 소스가 이동하는 다중 ping이다. 상태를
[위치, 속도, gradient] 7차원으로 확장하고 굴절 궤적에서 (1) gradient가 참값으로 식별되는지,
(2) 위치 RMSE가 굴절 무시 baseline 대비 개선되는지 판정한다.

## 방법

- 상태 x=[px,py,pz,vx,vy,vz,g], 7차원 UKF. 관측모델은 ideal_measurement에 굴절 고도각 이동을
  선형근사(el_shift≈K·g·수평거리, K=3.21e-4; 51번서 shift가 g·range에 선형임 확인)로 더한다.
  gradient는 process noise를 작게 줘 거의 상수로 둔다.
- 24개 궤적, 각 상수 gradient(-0.1~+0.1 s⁻¹, 탐지 유리하게 공격적으로 크게)로 소스 이동, 10 ping.
  굴절 채널(2차반사+거친표면+eigenray 굴절)로 관측 합성. baseline은 6차원 UKF(굴절 무시).
- 지표: g_est vs g_true Spearman·RMSE(사전 0 대비), 위치 RMSE baseline vs joint(Wilcoxon). GT는 평가만.
- 실행: `python run_joint.py`, 계약검증 `python test_diagnostic.py`.

## 결과 (2026-07-07)

| 지표 | 값 |
|---|---:|
| g_est vs g_true Spearman | **−0.010** (p=0.96) |
| gradient RMSE — joint | **0.332** |
| gradient RMSE — 사전(0) | 0.053 |
| 위치 RMSE — baseline | 23.37 m |
| 위치 RMSE — joint | 24.17 m |
| 위치 개선 | **−0.80 m** (개선비율 0.42, Wilcoxon p=0.80) |

- **gradient가 식별되지 않는다.** g_est와 g_true는 무상관(ρ=−0.01)이고, joint 추정 RMSE(0.33)가
  아무것도 안 하고 0으로 두는 것(0.053)보다 **오히려 나쁘다.** 필터가 gradient를 잡지 못하고 다른
  모델오차(멀티패스 편향·거친표면)를 gradient 상태로 잘못 흡수해 값이 발산한다.
- **위치도 개선되지 않는다**(오히려 −0.80 m). gradient를 잘못 추정하니 굴절 보정이 도움이 안 된다.
- gradient를 실제보다 **크게(±0.1)** 줘 탐지를 유리하게 했는데도 못 잡았다 → 문제는 효과 크기가
  아니라 gradient 신호가 위치·깊이와 근본적으로 교락돼 10 ping 궤적에서 분리되지 않는다는 것.
  52번의 단일 ping 약한 관측가능성이 10 ping 누적으로도 극복되지 않았다.

## 판정

**기각 (이 joint-UKF 형태).** 10-ping 궤적·선형 굴절모델의 위치+gradient joint UKF는 gradient를
식별하지 못하고 위치도 개선하지 못한다. 52+53으로 이 형태의 방향 A는 성립하지 않는다.

**단, 방향 A 전체가 닫힌 것은 아니다** — 이 특정 형태가 안 된 것이고 아직 안 해본 변형이 있다:
- 더 긴 궤적/큰 기동으로 거리 변화폭을 키워 gradient leverage 증대
- 여러 궤적의 공유 gradient를 배치로 추정(단일 궤적 대신 다중 궤적 정보 결합)
- 필터의 굴절모델을 선형근사 대신 eigenray로(모델 불일치 축소)
- 프로파일을 gradient 하나가 아니라 다른 파라미터/관측식으로

여기서도 안 되면 프로파일 추정은 "외부(CTD)로 프로파일을 알아야 하는 conventional 문제"로 정리하고,
novelty는 또 다른 미탐색 방향으로 옮긴다. **연구 공간을 이 두 결과로 닫지 않는다.**

솔직한 정황: 52(단일 ping 약함)와 53(joint 필터 실패)이 일관되게 gradient 관측가능성이 약함을
가리킨다. 방향 A의 변형을 더 밀지, 다른 novelty 방향으로 전환할지는 이 정황을 근거로 판단할 사안이다.

주의: 24 궤적·10 ping·선형 굴절 근사·gradient 단일 파라미터화다. baseline RMSE 23 m는 공격적 gradient
(±0.1)가 만든 큰 굴절 편향을 굴절 무시 필터가 못 다뤄 커진 것이며, 현실적 작은 gradient에선 더 작다.
편향은 gated SRP 격자(0.2°)로 하한 추정된다.
