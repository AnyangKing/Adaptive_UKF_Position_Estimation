# 5. Adaptive R 및 gating

## 목적

`4. 신호 관측 UKF`의 고정 R 결과를 보존하고, 동일 원시 신호 관측에서 quality 기반
adaptive R과 block innovation gating의 효과를 비교한다.

## 방법

- GCC-PHAT와 SRP-PHAT 방향의 각거리 불일치가 커질수록 DOA R을 확대
- TOA(1), TDOA(7), DOA(2)를 별도 block으로 나누어 NIS 계산
- 99% chi-square 문턱을 넘으면 `NIS/threshold` 비율로 해당 R block 확대
- 최대 확대율은 100배
- hard rejection 대신 soft gating을 사용해 관측을 완전히 버리지 않음

품질 배율과 innovation 배율은 곱해진다. 이 값은 탐색 단계의 명시적인 휴리스틱이며,
논문용으로 사용하려면 검증 세트에서 고정하고 별도 테스트 세트에서 평가해야 한다.

## 공정한 비교

fixed와 adaptive 필터는 같은 초기상태, Q, 기본 R, 원시 신호 및 추출 관측을 사용한다.
차이는 시점별 R 조정뿐이다.

## 실행

```powershell
python test_adaptive.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

30시점의 동일 신호와 관측을 사용한 비교:

| 필터 | 전체 RMSE | 5시점 이후 RMSE | 마지막 오차 |
|---|---:|---:|---:|
| Fixed R | 3.356 m | 3.209 m | 3.600 m |
| Adaptive R | **3.059 m** | **2.814 m** | **3.406 m** |

수렴 후 RMSE 개선율은 12.30%이다. 평균 GCC-SRP 방향 불일치는 0.737°였다.

99% NIS 기준의 DOA와 TDOA soft gate는 이 궤적에서 한 번도 활성화되지 않았다.
따라서 개선은 NIS 이상치 제거가 아니라 GCC-SRP 불일치에 따른 DOA R 확대에서 왔다.
이는 현재 주오차가 큰 순간 이상치보다 고도각의 작고 지속적인 멀티패스 편향임을
뒷받침한다. 결과를 좋게 만들기 위해 chi-square 문턱을 사후에 낮추지 않는다.

아직 2.8 m 수준이므로 최종 방법으로 확정하지 않는다. 다음 시행착오에서는 고도각
편향을 상태 변수 또는 시간적으로 완만한 nuisance bias로 추정하는 방법을 검토한다.
