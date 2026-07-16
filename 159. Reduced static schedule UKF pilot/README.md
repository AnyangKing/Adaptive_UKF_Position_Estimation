# 159. Reduced static schedule UKF pilot

## 목적

158번 Stage 0에서 살아남은 `linear20_30_34`, `random20_30_34_seeded`,
`four_carrier_cycle`을 실제 신호 합성→TOA/TDOA/DOA 추출→adaptive-R UKF 전체 경로로
비교한다. 158번은 편향 곡선 사전선별일 뿐 위치 RMSE를 입증하지 않았으므로, 이 폴더가
그 전달 가능성을 확인하는 첫 단계다.

## 범위와 주장 제한

- 600 m 정지 표적, 신규 개발 seed 4기하, 각 20 ping.
- fixed 32 kHz와 세 후보를 같은 기하·같은 ping noise seed로 paired 비교한다.
- 후반 10 ping settled RMSE, settled-error P90, elevation innovation lag-1을 본다.
- 계산비용을 통제하기 위한 **development pilot**이며, n=4 결과로 최적 schedule이나 논문
  성능을 주장하지 않는다.
- 통과 후보가 생겨도 별도 폴더의 잠긴 신규 seed 독립검증 전에는 채택하지 않는다.

## 사전 판정 규칙

후보는 mean/median gain 양수, 4기하 중 2개 이상 개선, 평균 P90 비악화, fixed보다 낮은
평균 absolute lag-1, 발산 0을 모두 만족할 때만 독립검증 대상으로 전진한다. 이 규칙은
소표본에서 유의성을 가장하지 않기 위한 screening 규칙이다.

## 시행착오 계승

158번에서 8 schedule×8 geometry의 전면 UKF 실행은 첫 기하만 5분 이상 걸려 결과가 나오기
전에 중단했다. 159번은 Stage 0 통과 후보만 남기고 기하를 병렬화했다. 중단된 158번 실행의
부분 결과는 없으며 후보 선택에도 쓰지 않았다.

## 실행

```powershell
python test_protocol.py
python run_reduced_schedule_pilot.py
```

실행 후 결과와 판정은 `result_summary.md` 및
`results/reduced_static_schedule_pilot.json`에 기록한다.

## 완료 결과

세 후보가 모두 사전 screening 기준을 통과했다. four-carrier cycle이 개발 4기하에서 fixed
9.321 m 대비 4.109 m로 가장 낮았고 4/4 기하에서 개선했다. random은 lag-1이 가장 낮았지만
RMSE는 linear보다 높아 whitening과 localization accuracy가 동일 목적함수가 아님을 확인했다.

판정은 **four-carrier와 기존 linear를 160번 독립 seed 검증으로 전진**이다. 이 결과는 후보
선별용이며 원고 claim에는 사용하지 않는다.
