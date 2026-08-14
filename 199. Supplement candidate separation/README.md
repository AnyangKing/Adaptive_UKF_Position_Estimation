# 199. Supplement candidate separation

## 목적

191번 이동 표적 full-range 결과를 반영한 뒤, 원고의 본문 그림·표와 보충자료 후보를 분리했다.

이번 단계에서는 실제 원고에서 내용을 삭제하거나 이동하지 않았다. 아직 최종 저널/쪽수/보충자료 허용 범위가 확정되지 않았기 때문이다. 대신 나중에 분량을 줄여야 할 때 어떤 순서로 덜어낼지 결정표를 만들었다.

## 결론

현재 원고의 핵심 논리에는 다음 네 덩어리가 본문에 남아야 한다.

1. 관련연구 대비 위치: “기존 TOA/TDOA/DOA+Kalman류”와 “주파수 다양성/레이더 glint” 사이에서 본 논문의 자리를 설명한다.
2. 물리 기전: 얕은 수중 two-ray/표면반사가 compact USBL DOA bias를 시간상관 있게 만든다는 근거.
3. 정지/준정지 검증: frequency agility가 효과를 보이는 영역과 사라지는 경계를 보여준다.
4. 이동 full-range 검증: plain hopping의 tail 위험과 transition-aware soft-R 회복을 함께 보여준다.

쪽수 압박이 오면 상세 ablation·요약표·보조 진단부터 보충자료로 보내는 것이 안전하다.

## 산출물

- `main_body_keep_list.md`: 본문에 남겨야 할 항목
- `supplement_candidate_map.md`: 보충자료 후보와 이동 우선순위
- `cut_strategy.md`: 13쪽 원고를 줄여야 할 때의 단계별 전략

## Git 규칙

원고 파일(`paper/`)은 로컬 전용으로 유지한다. GitHub에는 이 199번 폴더만 올린다.
