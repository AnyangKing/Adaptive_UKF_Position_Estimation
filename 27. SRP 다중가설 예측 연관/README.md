# 27. SRP 다중가설 예측 연관

## 목적

5 ms 직접파 구간 SRP에서 10° 이상 분리된 상위 5개 방향 가설을 보존하고, UKF의 사전
예측 방향과 SRP 상대 점수를 함께 사용하면 멀티패스 peak 선택 오류를 줄일 수 있는지 검증한다.

## 방법

- coarse SRP 격자에서 선택한 peak 주변 10°를 순차 제외해 최대 5개 가설 생성
- 각 가설을 0.2° 격자로 미세 탐색
- validation 후보: 상위 3/5개, 1위 대비 score ratio 0.50/0.75, score penalty 0°/10°
- 비용: `예측 방향과의 각거리 + score_weight × (1 - score_ratio)`
- 기존 5° GCC-SRP 조건부 라우팅과 NIS soft gating은 유지
- validation과 test는 서로 다른 궤적·환경·noise seed 사용

## 실행

```powershell
python test_multihypothesis.py
python run_validation_test.py
```

## 결과 (2026-07-05)

Validation은 baseline(1위 peak 고정)을 선택했다. 모든 다중가설 정책의 switch rate가 0%여서
baseline과 결과가 완전히 같았다.

| 거리 | Validation baseline RMSE | 독립 test baseline/선택 RMSE |
|---:|---:|---:|
| 100 m | 0.784 m | 3.310 m |
| 200 m | 12.718 m | 2.609 m |
| 400 m | 10.952 m | 26.177 m |
| 600 m | 11.867 m | 13.812 m |

후보 coverage를 별도로 확인한 결과 validation과 test의 모든 거리·ping에서 1위 peak 자체가
실제 방향 5° 이내였다. 따라서 상위 2~5위에 더 좋은 peak가 숨어 있지 않았고, UKF도 1위
DOA로 초기화되어 같은 가설을 계속 선택했다.

## 판정

현재 형태의 예측 기반 다중가설 연관은 **기각**한다. 이 실험은 peak switching보다 1위 peak의
잔여 0.5~2° 오차가 장거리 횡방향 오차로 증폭되는 현상이 더 중요한 병목임을 보여준다.
다음 실험은 다중 peak 선택을 더 조정하지 않고 직접파/표면반사의 물리적 도달시간 구조를 이용해
잔여 DOA bias를 줄일 수 있는지 확인한다.
