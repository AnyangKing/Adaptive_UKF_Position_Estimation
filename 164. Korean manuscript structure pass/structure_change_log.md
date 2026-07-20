# Structure change log

## 변경 전

163번 한글 원고 v0는 연구 흐름을 설명하는 데에는 충분했지만, 논문 기준본으로 쓰기에는 다음이 부족했다.

- 초록 뒤 핵심어 없음
- 사용자가 읽는 기준본이라는 역할 설명 부족
- claim boundary가 본문 문장에 흩어져 있음
- 그림과 표의 본문 위치가 아직 명확하지 않음
- 실패 실험을 어디에 둘지 명시적 표가 없음

## 변경 후

164번에서 `paper/manuscript_ko.tex`를 v1로 갱신했다.

- `핵심어` 절 추가
- `한글 기준 원고의 역할` 절 추가
- `tab:claims` 추가: 주장 가능/금지 표현을 표로 고정
- `fig:system`, `fig:floor`, `fig:tworay`, `fig:bias`, `fig:static`, `fig:moving`, `fig:quasistatic` callout 배치
- `tab:validation` 추가: static/moving/quasi-static/CRLB 결과 요약
- `tab:limitations` 추가: 실패와 한계 결과의 원고 내 배치 고정

## 영어 원고 반영 시 주의

영어 `paper/manuscript.tex`에 반영할 때는 다음 순서가 안전하다.

1. 한글 원고 v1의 장 흐름을 영어 장 번호와 대조한다.
2. 표 `tab:claims`를 영어 원고의 contribution/limitation 문장과 대조한다.
3. 그림 7개의 순서와 caption을 영어 원고의 기존 Fig.1--6/두-ray 그림 배치와 대조한다.
4. `tab:limitations`의 160--162번 해석을 Discussion 또는 Supplement로만 넣는다.

## 비고

이번 작업은 paper-local edit이므로 GitHub에는 `paper/manuscript_ko.tex`를 올리지 않는다.
커밋 대상은 이 164번 폴더뿐이다.
