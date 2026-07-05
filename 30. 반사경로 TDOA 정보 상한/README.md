# 30. 반사경로 TDOA 정보 상한

## 목적

경로연관이 완벽하다는 oracle 조건에서 direct-surface, direct-bottom 상대 TDOA가 기존
TOA·센서간 TDOA·DOA UKF에 실제 위치정보를 더하는지 확인한다. 이는 soft path association
필터 개발 전의 정보 상한 실험이다.

## 방법

- 기존 10차원 관측 유지: 절대 TOA 1, 센서간 TDOA 7, SRP DOA 2
- 반사경로 TDOA 후보: 기준센서 2개 또는 8센서 16개
- matched-filter peak의 경로 이름은 평가용 실제 지연으로 oracle 연관
- 측정분산은 validation residual에서만 교정하고 test에는 고정
- 기존 GCC-SRP 조건부 라우팅과 경로 관측 NIS 완화 적용
- validation/test 각각 거리당 4개 독립 10-ping 궤적

## 결과 (2026-07-05)

Validation 평균 RMSE:

| 거리 | 기존 관측 | 기준센서 경로 2개 | 전체 경로 16개 |
|---:|---:|---:|---:|
| 100 m | 1.354 | 1.167 | 1.173 |
| 200 m | 2.421 | 2.287 | 2.279 |
| 400 m | 10.567 | 13.821 | 17.660 |
| 600 m | 9.170 | 4.808 | 4.807 |

강건 점수는 기존 8.520, 기준센서 8.976, 전체 10.895로 validation이 기존 관측(`none`)을
선택했다. 따라서 독립 test에는 선택된 기존 관측만 적용했으며 test 결과를 이용해 경로 설정을
재선택하지 않았다.

## 판정

반사경로 TDOA를 표준 단일-Gaussian UKF 관측으로 직접 쌓는 방법은 **기각**한다. 장거리
600m에서 큰 정보이득이 확인됐지만 400m의 일부 궤적에서 잘못된 모드로 강하게 이동했다.
Oracle 연관에서도 발생했으므로 핵심 문제는 경로 이름 오류만이 아니라 반사 지연 likelihood의
비선형성·다봉성과 중복 관측의 과신이다.

다음 단계에서는 반사 관측을 하나의 Gaussian residual로 압축하지 않고, 가능한 경로·상태 모드의
likelihood를 유지한 뒤 기존 TOA/TDOA/DOA 칼만 posterior와 확률적으로 결합한다.
