# 160. Four carrier independent static validation

## 사전등록 목적

159번 개발 4기하에서 선택된 `four_carrier_cycle`이 결과를 보지 않은 신규 600 m 정지표적
20기하에서도 재현되는지 검증한다. 기존 논문 schedule인 `linear20_30_34`와 fixed 32 kHz를
동시에 잠가 비교한다.

## 실행 전 동결 사항

- 신규 geometry seed root 1,600,000, ping seed root 1,603,000. 159번 seed와 중복 없음.
- 20 geometry × 20 ping × 3 schedule, 동일 geometry와 ping seed의 paired 설계.
- schedule은 `fixed32`, `linear20_30_34`, `four_carrier_cycle` 세 개뿐이다.
- primary endpoint는 후반 10 ping settled position RMSE.
- 보조 endpoint는 geometry별 settled-error P90과 elevation innovation absolute lag-1이다.
- 후보를 선택한 159번 결과는 이 검증 표본에 포함하지 않는다.

## 동결 판정 규칙

four-carrier가 fixed 대비 독립 재현을 통과하려면 mean/median gain 양수, 개선비율 0.60 이상,
RMSE P90 비악화, one-sided paired Wilcoxon p<0.05, mean absolute lag-1 감소, 발산 0을 모두
만족해야 한다.

four-carrier가 기존 linear보다 우월하다고 하려면 mean/median gain 양수, 개선비율 0.60 이상,
RMSE P90 비악화, one-sided paired Wilcoxon p<0.05, 발산 0을 모두 만족해야 한다. linear 대비
lag-1 감소는 우월성 필수조건으로 두지 않는다. 최종 위치오차가 primary이기 때문이다.

가능한 최종 판정은 다음 세 가지다.

1. `validated_superior_to_fixed_and_linear`
2. `validated_vs_fixed_not_superior_to_linear`
3. `independent_validation_failed`

## 주장 제한

이 검증이 성공해도 canonical 3-path simulation 내부 결과다. 실제 수중 성능, 모든 carrier
bank에 대한 최적성, 이동 표적 이득으로 확장하지 않는다. 원고 자동 수정은 금지하고 결과를
별도 보강 근거로 검토한다.

## 실행

```powershell
python test_protocol.py
python run_independent_schedule_validation.py
```

## 완료 판정

`independent_validation_failed`.

- four-carrier는 fixed 대비 median과 개선비율은 양호했지만 mean −0.354 m, P90 −0.842 m,
  1/20 발산으로 동결 기준을 통과하지 못했다.
- four-carrier는 linear보다 평균 3.127 m 나빴고 superiority p=0.943이었다.
- 기존 linear는 fixed 11.571→8.798 m, 15/20 개선, p=0.001576으로 독립 재현됐다.

따라서 four-carrier를 폐기하고 기존 linear schedule을 유지한다. 결과 상세는
`result_summary.md`와 `results/four_carrier_independent_validation.json`에 있다.
