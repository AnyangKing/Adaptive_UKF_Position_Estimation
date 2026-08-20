# 208. Manuscript claim consistency audit

## 목적

204번 OOD 결과와 207번 compact table을 반영한 뒤, 한글/영문 원고의 moving-target claim이 서로 충돌하지 않는지 감사했다.

## 감사 기준

1. plain carrier hopping 단독으로 이동 표적 RMSE 개선을 주장하지 않는다.
2. transition-aware soft-R의 이동 표적 claim은 191 structured simulation과 204 OOD simulation으로 제한한다.
3. 실해역, 임의 motion, hardware frequency response 일반화는 주장하지 않는다.
4. 63--67번의 실패 기록은 삭제하지 않고, transition-aware 방법의 필요성으로 연결한다.

## 수정한 부분

- 한글 원고에서 “본 논문의 성능 claim은 정지 장거리, 특히 600 m 조건을 중심으로 제한한다”는 문장이 최신 이동 표적 claim과 충돌할 수 있어 수정했다.
- 수정 후 표현:
  - 정지 표적 성능 claim은 장거리/600 m 중심.
  - 이동 표적 성능 claim은 transition-aware Adaptive-R 검증에만 별도 한정.
- 한글 요약표와 Discussion 문구에 204 OOD 결과를 추가했다.

## 판정

현재 원고의 claim boundary는 다음 상태로 정합적이다.

- static: carrier-agile schedule의 중심 성능 claim.
- plain moving hop: residual decorrelation과 failure boundary.
- transition-aware moving: structured 191 + OOD 204 simulation-level performance claim.
- real-water/arbitrary motion: future work.
