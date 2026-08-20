# 211. Korean manuscript structure and numbering audit

## 목적

한글 기준 원고의 장 구조, 번호 흐름, 표/그림 배치, 최신 204 OOD 반영 이후의 기여 항목 번호를 감사했다.

## 발견한 문제

204 OOD 결과가 추가되면서 서론의 기여 항목이 늘었지만, 문장은 아직 “네 가지”라고 되어 있었다. 또한 “다섯째”가 두 번 반복되어 장 구조가 어수선하게 읽힐 수 있었다.

## 수정

- `한글 기준 원고 v3` → `v4`
- 날짜를 2026년 8월 20일로 갱신
- “본 논문의 기여는 네 가지” → “여섯 가지”
- 중복된 “다섯째” 중 마지막 항목을 “여섯째”로 수정

## 표/그림 흐름 판정

- Fig. system → floor → two-ray/bias → static → moving boundary → moving full-range/OOD → quasi-static 순서는 논리적으로 유지된다.
- 204 OOD 표는 moving full-range 표 앞에 배치되어 “structured 검증에 과적합된 것인가?”라는 질문을 먼저 방어한다.
- 63 plain hopping failure와 191/204 transition-aware success가 분리되어 있어 claim boundary가 무너지지 않는다.

## GitHub 규약

`paper/` 원고는 local-only다. 이 폴더만 커밋한다.
