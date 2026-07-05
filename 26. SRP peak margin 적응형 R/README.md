# 26. SRP peak margin 적응형 R

## 목적

GCC-SRP 불일치가 작아도 두 추정기가 같은 잘못된 방향에 동의할 수 있다. 5 ms gated SRP
공간 스펙트럼에서 10° 이상 떨어진 1위·2위 peak의 정규화 margin을 계산해 방향 모호성을
추가 quality로 사용할 수 있는지 검증한다.

## 품질지표

`margin = max(0, (best_score - separated_second_score) / abs(best_score))`

같은 main lobe를 두 번째 peak로 세지 않도록 최적 방향에서 10° 이내 후보를 제외한다.
margin이 작으면 서로 떨어진 두 방향 가설의 score가 비슷하다는 의미다.

## 선택과 평가

- validation seed: 261000/263000 계열
- test seed: 262000/264000 계열, 다른 방위·수심
- 거리: 100/200/400/600 m, 각 10 ping
- threshold 후보: validation margin의 25/50 백분위수
- DOA R 확대 후보: 4배/16배
- baseline도 후보에 포함
- 선택점수: 평균 위치 RMSE + 0.25×최악 거리 RMSE + 발산 penalty

Peak margin과 실제 DOA 오차의 Spearman 상관도 함께 기록한다. test 결과로 threshold나
scale을 다시 조정하지 않는다.

## 실행

```powershell
python test_peak_margin.py
python run_validation_test.py
```

## 결과 (2026-07-05)

Validation margin 분포:

- 25백분위: 0.08691
- 50백분위: 0.12860
- margin과 실제 DOA 오차의 Spearman 상관: **+0.4426** (`p=0.00424`)

작은 margin이 큰 오차를 뜻할 것이라는 가설과 달리 양의 상관이 나왔다. 멀티패스가
강한 잘못된 방향 peak를 만들면 2위와의 margin이 크면서도 오차가 커질 수 있다.

Validation은 `q25_x4`를 선택했지만 강건 점수는 baseline 11.30075, 선택안 11.29956으로
차이가 0.011%에 불과했다. 독립 test에서는 모든 거리에서 low-margin 발동률이 0%여서
선택안과 baseline 결과가 완전히 동일했다.

| 거리 | Baseline/선택안 RMSE |
|---:|---:|
| 100 m | 1.116 m |
| 200 m | 13.954 m |
| 400 m | 2.104 m |
| 600 m | 10.375 m |

따라서 단순 1·2위 peak margin 기반 R 조절은 **기각**한다. Peak 높이의 확신도가 경로의
물리적 정당성을 보장하지 않는다. 다음 후보는 UKF 예측 방향과 여러 분리 peak의 각거리,
시간 연속성, 직접파 지연 일관성을 함께 사용하는 다중가설 선택이다.
