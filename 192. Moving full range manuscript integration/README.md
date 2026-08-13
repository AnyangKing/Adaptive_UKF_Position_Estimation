# 192. Moving full range manuscript integration

## 목적

191번의 0--1000 m 이동 표적 독립 검증 결과를 한글 기준 원고(`paper/manuscript_ko.tex`)의 주장 구조에 반영했다.

## 핵심 판단

- 기존 원고는 63--67번 단계의 결론인 “이동 표적 pooled RMSE 개선 미재현”을 중심 경계로 두고 있었다.
- 191번 이후에는 이 문장을 그대로 두면 최신 결과와 맞지 않는다.
- 단, “반송파 도약 자체가 이동 표적을 일반적으로 개선한다”는 주장은 여전히 금지된다.
- 새 claim은 “plain hopping은 tail-prone이지만, 관측 가능한 전환 위험을 Adaptive-R에 반영한 transition-aware 규칙은 현재 신호수준 시뮬레이터의 0--1000 m 이동 검증에서 개선됐다”로 제한한다.

## 반영한 원고 변경

- 제목을 정지 표적 중심에서 정지/이동을 모두 포괄하는 표현으로 수정했다.
- 초록에 191번 528 paired cases 결과를 추가했다.
- claim boundary 표에 이동 표적 claim을 새로 정의했다.
- validation summary 표에 plain hopping 이동 실패와 transition-aware 이동 성공을 분리했다.
- 191번 거리별 RMSE 표를 한글 원고에 추가했다.
- Discussion과 결론에서 “이동 RMSE 개선 미재현”을 “plain hopping만의 한계”로 재정의했다.

## Git 규약

`paper/`는 로컬 전용이므로 커밋하지 않는다. 이 폴더에는 원고 변경의 근거와 diff 설명만 남긴다.

