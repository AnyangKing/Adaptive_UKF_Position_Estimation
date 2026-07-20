# Source trace notes

## 61번 정지 검증

`61. 정지표적 도약 대규모 독립검증/README.md`:

- 600 m fixed mean RMSE 13.01 m
- 600 m hop mean RMSE 8.87 m
- paired improvement +4.137 m, rounded to 4.14 m
- CI [+2.17, +6.05]
- p=0.0008
- median 13.97 → 7.96

원고의 정지 성능 claim과 정합한다.

## 63번 이동 검증

`63. 이동표적 도약 대규모검증 백색화 확인/README.md` 및 레지스트리:

- pooled RMSE gain은 -0.10 m, p=0.301로 기각
- DOA elevation residual lag-1은 fixed +0.470 → hop -0.208
- whitening mechanism은 통과, moving RMSE improvement claim은 금지

원고의 moving boundary 표현과 정합한다.

## 82번 준정지 경계

`82. 준정지 속도 경계 검증 실행/README.md` 및 result_summary:

- 132 paired trials
- fixed mean RMSE 11.98 m
- hop mean RMSE 10.49 m
- +1.49 m gain, p=8.00e-05
- lag-1 +0.220 → -0.100
- continuous quasi-static boundary는 0.005 m/s까지만
- 0.010/0.050은 not supported
- 0.030/0.100 양성은 비단조/기하 의존 회복

원고의 quasi-static 제한 표현과 정합한다.

## 160--162번 schedule/guard

160번:

- four-carrier는 신규 20기하에서 1/20 발산, mean/P90 악화
- linear20은 fixed 11.571 → 8.798 m, p=0.001576으로 재현

161번:

- geometry 2에서 3.557 m TOA branch jump
- four-cycle이 9회 반복 횡단
- total variation 32.013 m
- settled RMSE 53.001 m

162번:

- post-hoc TOA guard pilot
- geometry 2 four-carrier 53.001 → 8.224 m
- 독립검증 전이므로 본문 성능 claim 금지

원고의 limitation/future work 배치와 정합한다.
