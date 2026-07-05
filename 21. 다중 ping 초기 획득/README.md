# 21. 다중 ping 초기 획득

## 목적

장거리에서 첫 SRP 방향오차가 초기 위치오차로 증폭되는 문제를 줄인다. 첫 1/3/5 ping의
SRP 단위방향을 구면평균하고 마지막 획득 ping의 TOA 거리로 초기 위치를 만든 뒤 UKF를
시작한다.

## 공정 비교

- validation seed: 211000 계열
- test seed: 212000 계열, 다른 방위·수심
- 거리: 100/200/400/600 m, 각 12 ping
- 후보: 1/3/5 ping
- 공통 평가 시작: step 6, 모든 후보가 이미 시작된 이후
- validation score: mean RMSE + 0.25×worst RMSE + divergence penalty
- 필터: 19번의 5° 조건부 라우팅 고정

방위각을 산술평균하지 않고 3차원 단위벡터를 평균해 ±π wrap 문제를 피한다. 다중 ping은
초기 정확도와 교환하여 2~4 ping의 출력 지연을 만든다. test 결과로 ping 수를 바꾸지 않는다.

## 실행

```powershell
python test_initialization.py
python run_validation_test.py
```

## 최초 결과 (2026-07-03)

validation 강건 점수는 3 ping을 선택했다.

- 1 ping: 23.614
- 3 ping: **23.029**
- 5 ping: 23.061

독립 test의 공통 step 6 이후 RMSE:

| 거리 | 1 ping | 선택된 3 ping |
|---:|---:|---:|
| 100 m | **0.625 m** | 0.676 m |
| 200 m | 11.545 m | **11.501 m** |
| 400 m | 19.432 m | **19.191 m** |
| 600 m | **15.672 m** | 15.726 m |

거리 평균은 11.818 m에서 11.773 m로 약 0.38% 개선됐을 뿐이며 2-ping 출력 지연이
생긴다. 100/600 m는 소폭 악화됐다. SRP 오차가 독립 zero-mean jitter라면 평균 효과가
커야 하지만 실제로는 지속 멀티패스 bias가 지배해 구면평균으로 제거되지 않았다.

따라서 3-ping 초기화는 채택하지 않고 1-ping 실시간 초기화를 유지한다. 다음 단계는
평균이 아니라 직접파 도착 구간만 잘라 SRP에 넣는 time-gated DOA를 검토한다.
