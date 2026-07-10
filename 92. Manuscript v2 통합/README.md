# 92. Manuscript v2 통합

## 목적

89번 Manuscript v1이 남긴 두 구조적 공백 — 표 callout만 있고 본문 없음(#5), 그림이 참조만 되고
캡션/파일 정합이 원고에 없음(#2) — 을 90번(Tables draft)과 91번(Figure file alignment)의 재료로
채워, 표·그림·본문이 한 문서에서 정합하는 **manuscript v2**를 만든다. 91번 README의 "Next action"
(these figures and the 90번 tables → clean manuscript v2) 수행.

## 방법

- 기반: `89/manuscript_draft_v1.md` 전문. 수치·claim 경계는 v1 검증 문안을 그대로 보존.
- 표 통합: 90번 세 표를 `table_insertion_notes.md`의 지시 위치·lead-in·주의사항 그대로 삽입
  (Table 1은 인용 미해결이므로 draft-status 캡션 명시, Table 2는 §7 끝, Table 3는 Discussion).
- 그림 통합: 91번 캡션 6종을 Figure Captions 절로, canonical 파일 경로를 Figure File Manifest
  절로 수록. fig7→fig6 개명 결정 반영. 본문 callout을 미래형→현재형으로 전환(9곳).
- References(placeholder) 절 신설 — 4개 placeholder의 확보 상태(DOI/Xplore ID/잔여 작업) 명기.
- 90번 일관성 체크리스트 6항목을 전수 검사(모두 통과 — `v2_change_log.md`).

## 결과 (2026-07-09)

- `manuscript_draft_v2.md` — Abstract~Conclusion 9개 절 + Table 1·2·3 본문 + Figure Captions +
  Figure File Manifest + References placeholder 상태까지 한 문서로 정합된 v2.
- `v2_change_log.md` — v1 대비 변경 8건, 일관성 체크 6항목 통과, 의도적 미변경 항목, v3/투고 전
  잔여 5건(인용 실서지 치환, §2 코드 대조, 영어 tightening, Fig.5 PNG·Fig.1 폴리싱, 저널 포맷).

## 판정

**통합 완료(논문조립).** v1의 구조적 공백(#2·#5)이 해소되어 원고가 "표·그림 포함 완전 초고" 상태가
됐다. 남은 것은 내용 추가가 아니라 마감 작업이다: (i) 인용 placeholder 실서지 치환(86번 프로토콜,
도서관 IEEE 접속 필요 — 사용자 몫 포함), (ii) §2 구현 세부 코드 대조, (iii) 영어 tightening,
(iv) 그림 마감(Fig.5 PNG, Fig.1 폴리싱), (v) 저널 포맷. **지도교수 보고(축 승인·저널 선택)가
마감 작업들보다 선행되는 것이 안전하다** — `지도교수_보고_요약.md` 준비돼 있음.

다음 폴더 후보: `93. Method 세부 코드 대조`(v3 잔여 ii) 또는 지도교수 피드백 반영 폴더.
