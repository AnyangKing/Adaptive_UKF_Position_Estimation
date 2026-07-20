# 165. Korean manuscript language tightening

## 목적

164번에서 구조를 잡은 한글 기준 원고를 사용자가 더 쉽게 읽을 수 있도록 문장 밀도를 다듬었다.
이번 단계는 새 연구나 수치 변경이 아니라, 한글 원고의 설명문 톤을 논문 초안 톤으로 정리하는 작업이다.

## 수행 내용

- `paper/manuscript_ko.tex`의 author/version을 `한글 기준 원고 v2`로 갱신했다.
- 초록 문장을 압축하고, 핵심 병목과 제안 방법이 더 빨리 드러나도록 수정했다.
- "한글 기준 원고의 역할" 절을 짧고 명확하게 다듬었다.
- 서론 첫 부분의 반복 표현을 줄였다.
- 초기 가설, 실패 분석, carrier sensitivity 발견 흐름을 더 자연스럽게 연결했다.
- 기여 문단을 간결하게 정리했다.

## 유지한 것

- 핵심 수치 유지: 정지 600 m 13.01 m to 8.87 m, improvement 4.14 m, p=0.0008
- moving target claim 유지: residual whitening only, pooled RMSE gain 미재현
- quasi-static claim 유지: continuous safe boundary 0.005 m/s
- 160--162번 결과 해석 유지: limitation/future work, 본문 성능 claim 금지
- `paper/` 로컬 전용 규칙 유지

## 다음 작업

166번 후보는 `Korean manuscript claim audit`이다.
한글 기준 원고 v2의 모든 핵심 수치와 claim boundary를 기존 실험 폴더/레지스트리와 다시 대조한다.
