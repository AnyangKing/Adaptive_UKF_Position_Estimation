# Real-water analysis contract

## Tier 1 primary endpoint

- DOA elevation residual lag-1의 paired fixed-minus-hop 감소.
- fixed lag-1이 충분히 양수인 조건에서 hop이 0 또는 음수 방향으로 이동하는지 확인.
- RMSE는 secondary endpoint.

## Tier 2 primary endpoint

- geometry별 settled RMSE paired gain.
- median gain과 P90/gross-error 비악화 동시 확인.
- lag-1 reduction 동반 여부.

## Tier 3 boundary

- 0.005 m/s까지만 preregistered continuous quasi-static 조건.
- 0.010 m/s 이상은 탐색 결과이며 연속 경계 확대에 사용하지 않음.

## 제외 규칙

다음 block은 `exclusion_flag=true`와 사유를 남기고 paired headline 분석에서 제외할 수 있다.

- ground truth interruption 또는 sigma가 예상 gain보다 큼.
- fixed/hop 사이의 큰 환경 변화.
- carrier별 출력 보정 실패.
- clock sync 손실.
- pings < 40 또는 유효 관측률 급락.

제외 기준은 결과를 본 뒤 새로 만들지 않고 현장 로그에서 즉시 기록한다.

## claim update

- Tier 1만 성공: real-water mechanism pilot.
- Tier 1+2 성공: real-water static validation.
- Tier 3까지 성공: static and very-slow-drift validation.
- moving 일반 RMSE claim은 별도 실험 없이는 추가하지 않음.
