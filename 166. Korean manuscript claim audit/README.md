# 166. Korean manuscript claim audit

## 목적

한글 기준 원고 v2(`paper/manuscript_ko.tex`)의 핵심 수치와 claim boundary가 실제 실험 폴더 및
`실험_레지스트리.md`와 일치하는지 감사했다.

이번 단계는 새 실험이 아니라 원고 정합성 점검이다.

## 감사 대상

- 정지 600 m 성능 claim: 61번
- 이동 표적 whitening/boundary claim: 63번
- 준정지 속도 경계 claim: 82번
- Method/프로토콜 기존 코드대조 결과: 93번
- 160--162번 schedule/guard 후속 결과의 배치: 160, 161, 162번

## 결론

수치 불일치 0건.

한글 원고의 headline claim은 기존 실험 레지스트리 및 관련 폴더 README/result summary와 정합했다.
다만 초록과 claim 표의 "정지/준정지" 표현이 넓게 읽힐 수 있어, 82번의 안전선에 맞춰
"정지 및 매우 느린 준정지"로 좁혀 보정했다.

## 보정 내용

`paper/manuscript_ko.tex`에서 다음 표현을 수정했다.

- 초록 결론: `정지 및 준정지 장거리 USBL 조건` → `정지 및 매우 느린 준정지 장거리 USBL 조건`
- claim 표 핵심 방법: `정지/준정지 장거리 USBL` → `정지 및 매우 느린 준정지 장거리 USBL`

`paper/`는 로컬 전용이므로 GitHub에는 올리지 않는다.

## 감사 판정

한글 기준 원고 v2는 minor wording patch 후 claim audit 통과.
다음 단계에서는 그림·표 캡션과 본문 callout의 해석을 더 다듬으면 된다.
