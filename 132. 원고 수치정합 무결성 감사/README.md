# 132. 원고 수치정합·무결성 감사

## 목적

저자 검토 전, `paper/manuscript.tex`의 헤드라인 수치가 초록·본문·표·그림캡션·결론에서 서로
일치하는지, claim 경계가 무결한지, draft 잔여물이 없는지 체계적으로 대조했다. 원고 실체는 로컬
`paper/` 전용, 이 폴더는 감사 기록.

## 방법

핵심 수치별로 원고 전체를 grep 추출해 등장 위치를 대조. claim 경계 문구·draft 마커도 전수 확인.
발견 시 `paper/manuscript.tex`에 edit in place로 수정 후 재빌드.

## 결과 (2026-07-13)

### 발견·수정한 불일치 (1건)

- **이동 표적 lag-1 p값 표기 불일치**: 본문(§Whitening)은 `p=5.6×10⁻¹⁰`, Fig.4 캡션·Table II는
  `p=5.56×10⁻¹⁰`. 참값(폴더 63)은 5.56×10⁻¹⁰. → **본문을 5.56로 통일**(세 곳 일치 확인).

### 정합 확인된 수치 (수정 불필요)

- 정지 600 m: 13.01→8.87 m, +4.14 m, −32%, median 13.97→7.96 m, p=0.0008 — 초록·본문·Table II·
  결론 **전부 일치**.
- 이동 pooled: −0.10 m, p=0.301 — 본문·Fig.4·Table II 일치.
- 준정지: 0.005 m/s 경계, 11.98→10.49 m, p=8.00×10⁻⁵ — 초록·본문·Table II·결론 일치.
- CRLB floor: 11.80 / 12.29 / 13.38 / 3.45 m — 본문·Table II 일치.

### claim 경계·draft 마커

- claim 경계 문구(sub-meter 미주장·first-FH 미주장·moving 개선 미주장·does not support 등) 9곳 존재,
  무결.
- draft 마커는 전부 **예정된 human-author placeholder**(저자명 "to be completed", back matter의
  Author Contributions·Funding·Data Availability·Conflicts "decision required"). 스트레이 TODO/XXX/
  FIXME/미해결 [REF] **없음**.

### 재빌드

- `latexmk` → 미해결 인용/참조 0, overfull 0, 9쪽. 수정 반영 정상.

## 판정

**무결성 감사 통과.** 수치 불일치 1건 수정 완료, 나머지 전부 정합, claim 무결. 남은 placeholder는
사람 결정 항목(저자·Funding·저널)뿐 — 원고 자체의 내적 결함은 없다.

## 다음 (판단)

시각 QA(130)·참고문헌(131)·수치정합(132)까지 원고 내적 완성도 점검이 일단락됐다. 원고 본체는
저자 정보/저널만 채우면 되는 상태. 추가 AI작업은 점점 marginal(예: 방법 원전 1~2편 더, 문장 다듬기)
이며, 본질은 사람 결정 영역. 다음 후보: 문장 수준 영문 tightening 또는 여기서 마무리 후 사용자 검토.
