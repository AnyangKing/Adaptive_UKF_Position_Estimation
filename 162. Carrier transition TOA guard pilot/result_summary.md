# 162 결과 요약

## 개발 결과

161번에서 선택한 post-hoc 3기하에 carrier-transition-aware TOA guard를 적용했다.

| schedule | 기존 mean RMSE (m) | guard mean RMSE (m) | divergence 기존→guard | guard 횟수 |
|---|---:|---:|---:|---:|
| fixed32 | 9.487 | 9.487 | 0→0 | 0 |
| linear20 | 6.608 | 6.607 | 0→0 | 1 |
| four-carrier cycle | **23.198** | **8.273** | **1→0** | 9 |

catastrophic geometry 2의 four-carrier RMSE는 53.001→8.224 m(−84.5%)로 줄었고, 50 m
초과 발산이 사라졌다. guard는 161번에서 확인한 raw TOA branch 전환 ping
`[1, 4, 5, 8, 9, 12, 13, 16, 17]`에서 정확히 작동했다.

geometry 5와 19는 0.5 m 초과 carrier-transition range jump가 없어 four-carrier guard가 한 번도
작동하지 않았고 결과가 기존과 동일했다. fixed는 carrier가 바뀌지 않아 전 기하에서 bit-identical
결과를 유지했다. linear는 geometry 2의 단 한 번 전환만 격리했으며 3기하 평균은
6.607863→6.606709 m로 사실상 보존됐다. 필터 예외는 전부 0이다.

## 판정

동결한 개발 기준 5개를 모두 통과해 `advance_to_independent_validation`이다. 다만 이 방법과
0.5 m threshold는 160/161 실패를 본 뒤 만들었고 동일 3기하에서 시험했다. 따라서 현재 결과는
알고리즘 동작 확인일 뿐 성능·일반화·노벨티 claim이 아니다.

## 새 알고리즘 방향

이 방법은 carrier change와 TOA continuity break를 공동 조건으로 사용해 **절대 TOA 한 블록만
격리하면서 TDOA·DOA update를 유지**한다. 기존 adaptive-R의 일반 NIS cap이 반복 branch switch를
막지 못했던 빈틈을 carrier schedule 정보로 보완한다.

다음 재개 작업은 163번 완전 신규 seed 독립검증이다. 0.5 m threshold와 1e12 m² isolation을
그대로 잠그고, 최소 20개 신규 정지 기하에서 fixed baseline, linear baseline/guard,
four-carrier baseline/guard를 paired 비교해야 한다. 사용자의 중단 지시에 따라 163번은 아직
생성·실행하지 않았다.
