# 119. Carrier schedule ablation plan

## 목적

현재 논문은 30–34 kHz 20-ping linear carrier-agile schedule을 **동결된 검증 정책**으로 사용한다. 이
스케줄은 61번 static 600 m에서 강하게 검증되었지만, 리뷰어는 다음 질문을 할 수 있다.

> “왜 하필 30–34 kHz인가? 왜 20개 carrier인가? linear sweep이 최적인가?”

119번은 이 질문에 대비한 **사전등록형 ablation 계획**이다. 새 실험은 실행하지 않는다. 현재 논문 본체의
claim을 바꾸지 않고, 후속 보충실험 또는 future work로 수행할 schedule ablation 설계를 정리한다.

## 결론

현재 원고에서는 30–34 kHz schedule을 “최적”이라고 주장하면 안 된다. 안전한 표현은 다음이다.

> We use a simple frozen 30–34 kHz ping-to-ping schedule to test the mechanism; optimizing the
> carrier schedule is left for ablation and future work.

## 기존 교훈

- 58번: 30–34 kHz 범위에서 long-range carrier sensitivity가 보였고, 400/600 m에서 hop-average bias
  reduction이 컸다.
- 61번: frozen 30–34 kHz schedule이 static 600 m RMSE를 13.01→8.87 m로 줄였다.
- 63번: moving residual lag-1 whitening은 강하지만 pooled RMSE gain은 미재현.
- 65번: sparse/anchor-hop이 pilot에서는 유망했지만,
- 66~67번: moving schedule generalization은 독립 seed에서 약하거나 기각.

따라서 ablation의 1차 대상은 **static/quasi-static schedule design**이고, moving schedule은 보조/future work다.

## 산출물

- `ablation_protocol.md`: 어떤 schedule들을 어떤 순서로 시험할지.
- `candidate_schedules.md`: candidate schedule 정의.
- `decision_rules.md`: 채택/기각 기준.
- `manuscript_positioning.md`: 원고에서 schedule을 어떻게 표현할지.

## 다음

119번 이후 교수님 없이 가능한 다음 작업은 120번 `Supplement archive dry run`이다. 115번에서 재현성
매핑을 끝냈으므로, 실제 보충자료 ZIP 구조를 만들어보는 것이 자연스럽다.
