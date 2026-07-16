# 151. BibTeX and reference formatting audit

## 목적

`paper/manuscript.tex`의 citation key와 `paper/refs.bib`의 BibTeX entry를 로컬 기준으로 대조했다.

웹/도서관 원문 검증은 하지 않았다. 이 감사는 현재 파일 내부의 누락, 미사용, 중복, 기본 필드 문제를 확인하는 범위다.

## 요약

- manuscript unique cited keys: 21
- refs.bib entries: 22
- missing BibTeX entries: 0
- duplicate BibTeX keys: 0
- basic required-field gaps: 0
- entries with DOI: 22/22
- unused BibTeX entry: `Delano1953TargetGlint`

## 판정

현재 references는 로컬 정합성 기준으로 안정적이다. LaTeX 빌드에서도 unresolved citation이 없었다.

주의할 점은 하나다. `Delano1953TargetGlint`는 bib에 있지만 원고 본문에서 직접 인용되지 않는다. radar glint 배경을 더 강화하려면 관련 문장에 추가 인용할 수 있고, 분량/간결성이 우선이면 bib에서 제거할 수 있다. 현재 상태로도 빌드 문제는 없다.

## 다음 권장

최종 투고 전에는 목표 저널 스타일에 맞춰 다음을 확인한다.

- article-number형 논문에서 `pages` 필드 사용이 저널 스타일에 맞는지;
- conference title 표기 축약/대문자 보호;
- DOI 표시 여부;
- `Delano1953TargetGlint`를 실제로 인용할지 또는 제거할지.
