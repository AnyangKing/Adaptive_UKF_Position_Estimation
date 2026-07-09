# 85. Manuscript draft v0

## 목적

84번 skeleton을 실제로 이어지는 논문 초안 형태로 변환한다.

이 폴더는 최종 투고 원고가 아니라 `v0 narrative draft`다. 즉, 각 절의 논리 흐름과 핵심 문장이 연결되도록 만든 첫 번째 전체 원고다. 세부 citation, 수식 정제, 그림 번호, journal style formatting은 이후 단계에서 다듬는다.

## 포함 파일

- `manuscript_draft_v0.md`: 9개 절 전체 원고 초안
- `revision_tasks.md`: v0에서 v1로 갈 때 필요한 수정 작업
- `claim_consistency_check.md`: 초록·본문·결론의 claim 일관성 점검

## 반영한 고정 원칙

- 본체 claim은 static long-range shallow-water USBL이다.
- quasi-static은 0.005 m/s very slow drift까지만 제한한다.
- moving target은 residual whitening은 말하되 RMSE improvement claim은 하지 않는다.
- frequency hopping 자체의 최초성은 주장하지 않는다.
- novelty는 post-gating coherent multipath DOA bias whitening + TOA/TDOA/DOA-UKF validation + applicability boundary다.

## 다음 단계

86번에서는 Introduction 또는 Related Work를 citation-ready 수준으로 더 정제하는 것이 좋다. 특히 exact citation audit이 필요하다.
