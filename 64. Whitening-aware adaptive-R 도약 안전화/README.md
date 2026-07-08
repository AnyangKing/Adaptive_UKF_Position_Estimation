# 64. Whitening-aware adaptive-R 도약 안전화

## 목적

63번에서 frequency hop이 이동 표적의 고도각 오차 자기상관을 강하게 낮춘다는 것은 확인됐다. 하지만 always-on hop은 이동 표적 전체 RMSE를 유의하게 개선하지 못했고, 일부 tangential/vertical 기하에서 outlier 악화를 만들었다.

이번 64번의 목적은 단순한 `whitening-aware adaptive-R` 안전장치로 hop의 백색화 이점은 유지하면서 outlier 악화를 줄일 수 있는지 검증하는 것이다.

## 가설

- H1: hop 관측에서 DOA R을 전체적으로 키우면 이동 표적 outlier가 줄어들 수 있다.
- H2: ping 간 DOA jump가 큰 경우에만 DOA R을 키우면 위험한 hop 관측만 약화할 수 있다.
- H3: innovation/NIS guard를 추가하면 always-on hop의 악화 케이스를 억제할 수 있다.

## 방법

- 거리: 600 m
- 조건: `radial_0.05`, `radial_1.0`, `tangential_1.0`, `tang_1.0_vz`
- 기하 수: 조건당 12개, 총 48개
- 시간 길이: 20 step, 정착 평가는 10 step 이후
- 비교 정책:
  - `fixed`
  - `hop_always`
  - `hop_R4`
  - `hop_R9`
  - `hop_jump1_x16`
  - `hop_jump2_x16`
  - `hop_R4_jump1_x8`
  - `hop_guard4`

각 궤적에서 fixed 관측열과 hop 관측열을 한 번씩 생성하고, 같은 관측열 위에서 여러 필터 정책을 paired 방식으로 비교했다.

## 실행

```powershell
python -m py_compile run_whitening_guard.py whitening_adaptive.py test_diagnostic.py
python test_diagnostic.py
python run_whitening_guard.py
```

결과 파일:

- `results/whitening_guard.json`

## 핵심 결과

전체 평균 RMSE 기준 최선 정책은 `fixed`였다.

| 정책 | 평균 RMSE m | 중앙값 RMSE m | fixed 대비 평균 이득 m | Wilcoxon p | 개선 비율 |
|---|---:|---:|---:|---:|---:|
| fixed | 11.156 | 8.964 | 0.000 | 1.000 | 0.000 |
| hop_always | 11.857 | 8.879 | -0.701 | 0.660 | 0.500 |
| hop_R4 | 11.567 | 9.031 | -0.411 | 0.763 | 0.417 |
| hop_R9 | 12.109 | 9.775 | -0.953 | 0.972 | 0.313 |
| hop_jump1_x16 | 13.190 | 10.125 | -2.035 | 0.964 | 0.417 |
| hop_jump2_x16 | 11.827 | 9.608 | -0.671 | 0.700 | 0.479 |
| hop_R4_jump1_x8 | 13.026 | 10.671 | -1.871 | 0.993 | 0.333 |
| hop_guard4 | 11.857 | 8.879 | -0.701 | 0.660 | 0.500 |

백색화 자체는 다시 재현됐다.

- fixed 고도각 오차 lag-1 자기상관 평균: `+0.458`
- hop 고도각 오차 lag-1 자기상관 평균: `-0.162`
- fixed > hop 검정 p값: `6.06e-08`
- 자기상관 감소 비율: `75%`

하지만 lag 감소량과 hop RMSE 이득의 관계는 사라졌다.

- Spearman ρ: `-0.011`
- p값: `0.941`

즉, hop은 오차를 백색화하지만 단순히 R을 키우거나 jump gate를 거는 것만으로는 위치 RMSE 개선으로 안정적으로 연결되지 않았다.

## 조건별 관찰

- `radial_0.05`: hop_always가 평균 +0.51 m 이득을 보였으나 개선 비율은 50%라 안정적 채택 근거는 약하다.
- `radial_1.0`: `hop_R4`가 평균 +0.79 m 이득을 보였지만 중앙값은 음수이고 개선 비율도 41.7%라 표본 의존 가능성이 크다.
- `tangential_1.0`: hop_always는 중앙값으로는 좋아 보이나 평균은 -2.77 m 악화다. outlier가 결론을 뒤집는 대표 조건이다.
- `tang_1.0_vz`: hop_always 평균은 약간 양수지만 중앙값은 음수다. R 팽창과 jump gate는 대체로 더 나빠졌다.

## 판정

기각.

64번은 “hop 백색화가 거짓”이라는 뜻이 아니다. 오히려 백색화는 63번에 이어 다시 강하게 재현됐다. 기각된 것은 아래의 단순 안전화 방식이다.

- hop 관측의 DOA R을 일괄적으로 키우기
- ping 간 DOA jump가 크면 R을 크게 키우기
- 단순 innovation/NIS guard로 outlier를 잡기

이 방식들은 hop의 백색화 이점을 위치 추정 이득으로 바꾸지 못했고, 일부 조합은 fixed보다 명확히 악화됐다.

## 연구적 의미

중요한 결론은 “백색화만으로는 알고리즘이 완성되지 않는다”는 점이다. hop은 편향의 시간상관 구조를 바꾸는 관측 설계 도구이고, UKF가 그것을 안정적으로 받아들이려면 사후 R 팽창보다 송신 스케줄 자체를 설계해야 할 가능성이 커졌다.

따라서 다음 연구축은 `whitening-aware R inflation`에서 `anchor-hop schedule`로 이동한다.

## 다음 단계

65번 후보:

`65. Anchor-hop schedule 이동표적 안전화`

핵심 아이디어는 fixed 32 kHz를 동역학 안정화 anchor로 유지하고, hop은 매 ping 항상 쓰지 않고 주기적/간헐적 probe로 넣는 것이다.

검증할 정책 예:

- fixed-only
- hop-always
- alternating fixed-hop
- fixed 3회 + hop 1회
- fixed 기반 상태예측 + hop probe의 DOA 가중 제한
- lag 또는 innovation 기반의 sparse hop trigger

성공 기준은 단순 평균 RMSE 개선만이 아니라 다음을 함께 봐야 한다.

- fixed 대비 평균 RMSE 이득
- 중앙값 이득
- outlier/tail 악화 여부
- 고도각 lag-1 자기상관 감소 유지 여부
- 조건별 악화, 특히 `tangential_1.0`, `tang_1.0_vz`
