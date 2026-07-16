# 158. Static carrier schedule ablation pilot

## 목적

119번에서 사전등록한 “왜 30–34 kHz linear 20개인가?” 질문의 Stage 0 pre-screen을 실행한다.
58번의 400/600 m carrier-bias 곡선 12기하를 사용해 fixed32와 7개 schedule의 평균 편향 상쇄,
tail과 sequence lag-1 proxy를 비교한다.

## 중요

- 이 단계는 **carrier-sensitivity development pre-screen**이다.
- 여기서 고른 schedule은 독립 seed 검증 전까지 원고 본체에 반영하지 않는다.
- canonical `linear20_30_34` schedule과 기존 논문 수치를 변경하지 않는다.
- wide 28–36 kHz 결과는 simulation-only이며 실제 transducer bandwidth를 보장하지 않는다.
- UKF와 위치 RMSE를 실행하지 않았으므로 localization 성능 claim을 만들 수 없다.

## 실행

```powershell
python "158. Static carrier schedule ablation pilot\test_schedules.py"
python "158. Static carrier schedule ablation pilot\run_stage0_schedule_prescreen.py"
```

## 후보

- fixed32 baseline.
- linear20 30–34 kHz.
- narrow linear20 31–33 kHz.
- wide linear20 28–36 kHz.
- four-carrier cycle.
- two-extreme alternating.
- seeded random permutation of the canonical 20 carriers.
- fixed3-hop1 sparse schedule.

## Stage 0 판정

- 후보: seeded random, canonical linear, four-carrier cycle, fixed3-hop1.
- 보류/기각: narrow linear는 sequence |lag-1| 기준 미통과, two-extreme은 완전 교대 상관으로 기각.
- 평가 불가: wide 28–36 kHz는 58번 source grid 밖이므로 외삽하지 않음.
- 다음 Stage 1 우선순위: random → canonical linear → four-carrier. fixed3-hop1은 저비용 보조 후보.

## 시행착오

첫 smoke 실행에서 61번 pipeline을 복사할 때 `measurement.py`와 `peak_measurement.py`가 공통으로
의존하는 `estimators.py`를 누락해 `ModuleNotFoundError`가 발생했다. 실행 전 의존성 감사를 다시
수행해 해당 모듈을 추가했다. 알고리즘 결과가 나온 뒤의 선택적 수정은 없었으며 schedule 정의와 seed는
변경하지 않았다.

두 번째 smoke 실행에서는 82번 runner에서 기억한 `geometric_measurement` 이름을 사용했지만,
복사한 61번 pipeline의 실제 API는 동일 계산의 `ideal_measurement`임을 확인했다. import와 호출
이름만 원본 API에 맞췄다.

schedule 단위 테스트에서는 `fixed3_hop1`의 5개 hop에
`linspace(30,34,5)`를 사용하면 가운데 ping이 32 kHz가 되어 실제 hop fraction이 4/20으로
줄어드는 것을 발견했다. intended 5/20을 지키도록 32 kHz를 제외한 고정 배열
`[30,31,33,34,30]` kHz로 사전 수정했다. 이 수정도 결과 실행 전에 완료했다.

full UKF pilot의 첫 기하가 5분 이상 걸려 8기하×8 schedule은 40분 이상으로 추정됐다. 119번의
사전등록 순서(Stage 0 pre-screen → Stage 1 UKF)에 맞춰 결과 생성 전에 full run을 중단하고, 58번의
400/600 m carrier-bias curve 12기하로 Stage 0를 수행했다. 전환 후 schedule 단위가 Hz에서 kHz로
바뀌었는데 test 기대값이 Hz로 남아 한 차례 실패했고, kHz 기준으로 수정했다.
