# 167.5 Korean caption pass minor corrections

## 목적

167번 감사 후 리뷰어 관점에서 지적된 3건 중 원고 수정이 필요한 1건을 반영하고, 나머지 2건은
167 폴더 이력을 흐리지 않으면서 다음 세션 지침으로 남긴다.

새 실험도, 새 수치도, 새 주장도 없다. 문서 정합성과 표현 강도만 손본다.

## 지적 3건과 처리 방식

| # | 위치 | 지적 | 처리 |
|---|---|---|---|
| 1 | `paper/manuscript_ko.tex` line 155 (`fig:floor` 캡션) | "이 잔여 성분이 ... DOA bias floor에 해당한다"가 CRLB gap 전체를 이 성분과 등치시키는 단정적 표현 | **원고 수정**: "시사한다"로 완화 + gap 구성에 대한 미주장 문장 추가 |
| 2 | 167 폴더 `caption_changes.md` line 157 "새 수치 없음" 표현 | 캡션에 등장한 `20개 독립 seed`, `132 paired trials` 등은 본문 그 자리엔 없었고 원천 폴더에서 확인된 값이라 표현이 부정확 | 167 이력 보존 위해 파일은 안 건드림. 대신 이 폴더에 정확한 표현 지침 남김 |
| 3 | 167 폴더 `README.md` line 14 "캡션 6원칙" | `caption_policy.md`에는 7개 항목 → 숫자 불일치 | 167 이력 보존 위해 파일은 안 건드림. 다음 세션이 7원칙으로 통일하도록 지침 남김 |

## 산출물

- `caption_correction_changes.md` — 3건 각각의 before/after 또는 지침 문안
- `README.md` — 이 문서

## Fig. floor 캡션 개정 요지

리뷰어 지적: CRLB와 UKF RMSE 사이 gap이 **전부** post-gating coherent multipath DOA bias라고
읽힐 위험. 실제로 45번 원천에서도 잔여 ≈ 3.45 m가 이 성분의 존재를 확증하는 것이지 gap 전체가
이 성분만이라는 주장은 아니다.

수정 요점:
- "이 잔여 성분이 ... floor에 해당한다" → "이 gap은 floor가 장거리 오차에 기여함을 시사한다"
- 미주장 문장 추가: "gap 전체가 이 성분만으로 구성된다는 주장의 근거로는 사용되지 않는다"

이 수정은 정책 5번(claim boundary 초과 금지)에 더 잘 맞게 강도를 낮춘 것이다. 새 수치 추가는
없다.

## 왜 167 폴더를 소급 수정하지 않는가

- 167은 이미 커밋·푸시 완료 상태. 소급 수정은 이력을 흐리게 만든다.
- 대신 167.5에 지침을 남겨, 다음 유사 문서(캡션 감사표·정책 요약)가 이 지침을 기준으로 작성되게
  한다.

## 검증

- 정책 6항목(사실은 7원칙) 전수 만족.
- 새 수치·새 주장 0건. 라벨·본문·수식·다른 캡션 변경 0건.
- 원천 대조: 45번(routed UKF 600 m 12.29 m vs 경험적 CRLB 11.80 m, 잔여 ≈ 3.45 m) 정합.
- 166 boundary 부분집합 유지.

## GitHub 규약 준수

- `paper/manuscript_ko.tex` 수정은 로컬에만 적용, GitHub 커밋 대상 아님.
- 이 numbered folder(`167.5 Korean caption pass minor corrections/`)만 stage하여 커밋.
- `git add .` 금지, 폴더 경로 명시.

## 다음 후보

167에서 제안한 168 후보 3가지 유효:

1. **168. Korean abstract and introduction tightening** — 리스크 가장 낮음, 자연스러운 다음 단계
2. **168. Korean discussion and conclusion tightening** — 얼마나 잠글지 사용자 판단 필요
3. **168. Korean-to-English caption port dry run** — 한글 원고 안정 확인 후

167에서 제 판단은 1번이었고, 지금도 그대로 유효.
