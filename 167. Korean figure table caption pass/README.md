# 167. Korean figure table caption pass

## 목적

한글 기준 원고(`paper/manuscript_ko.tex`)의 그림/표 캡션 10개를 감사·개정해, 캡션이
stand-alone으로 읽혔을 때에도 "무엇을 주장하고 무엇을 주장하지 않는지" 스스로 선언하게 만든다.
166번 claim audit이 정한 boundary를 캡션 층에서도 지키는 단계다.

이번 폴더는 새 실험이 아니라 원고 정합성 개선이다. `paper/`는 로컬 전용이며 GitHub에는
이 numbered folder만 올린다.

## 산출물

- `caption_policy.md` — 캡션 6원칙 (stand-alone / 주장+미주장 / post-hoc 명시 / 새 수치 금지 /
  boundary 초과 금지 / anti-campaigning)
- `caption_claim_audit_table.md` — 10개 캡션의 근거 폴더·리스크·개정 여부 표
- `caption_changes.md` — 10개 캡션 각각의 before/after diff와 개정 이유
- `README.md` — 이 문서

## 감사 결과 요약

| 캡션 | 개정 등급 | 핵심 이유 |
|---|---|---|
| tab:claims | minor | 다른 캡션의 anchor임을 명시 |
| fig:system | minor | 정량 근거 오독 차단 |
| **fig:floor** | 개정 | 원본이 자평만 있고 그림 내용 설명 부재 → CRLB 비교·잔여 3.45 m급 gap 서술, sub-meter 미주장 |
| **fig:tworay** | 개정 | 기하-fixed prediction임을 명시, 근사 미주장 |
| **fig:bias** | 개정 | 자평 축소, "위치 RMSE 근거 아님" 명시 |
| **tab:validation** | 개정 | 행별 지위 차이(성능/기전/경계/floor) 잠금 |
| **fig:static** | 개정 | 정지 600 m 한정 미주장, 조건 이전 방지 |
| fig:moving | minor | mechanism evidence 전용 못박기 |
| fig:quasistatic | minor | 82번 원천 수치·비단조 해석 확장 |
| tab:limitations | minor | 160/162 지위 재확인 |

## 검증

- 정책 6항목 전수 만족.
- 새 수치·새 주장 추가 0건. 캡션에 등장한 수치는 모두 원고 본문에 이미 존재하는 값의 재확인.
- 라벨·본문·수식·표 body 변경 0건. 캡션 문자열만 수정.
- 원천 근거 대조는 166번 audit table 및 61/63/82/45/58/138/145/160/162번 폴더 결과와 정합.

## GitHub 규약 준수

- `paper/manuscript_ko.tex` 수정은 로컬에서만 적용, GitHub 커밋 대상 아님.
- 이 numbered folder (`167. Korean figure table caption pass/`)만 stage하여 커밋한다.
- `git add .` 금지, 반드시 폴더 경로 명시.

## 다음 후보

캡션 정리가 끝났으니 자연스러운 다음 단계 후보:

1. **168. Korean abstract and introduction tightening** — 초록·서론이 캡션 정책과 정합하는지
   같은 boundary 원칙으로 훑기.
2. **168. Korean discussion and conclusion tightening** — Discussion/Conclusion의 자평·과잉
   일반화 표현 감사.
3. **168. Korean-to-English caption port dry run** — 개정된 한글 캡션을 영어 원고
   `manuscript.tex`에 옮길 때의 매핑 초안 (실제 반영은 별도).

사용자 판단에 따라 선택한다.
