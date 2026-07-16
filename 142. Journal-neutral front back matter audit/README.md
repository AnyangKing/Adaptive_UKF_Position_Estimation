# 142. Journal-neutral front back matter audit

## 목적

로컬 `paper/manuscript.tex`의 front/back matter를 점검하여, 아직 확정되지 않은 특정 저널명과 제출 문구를
IEEE 공용 journal-format 표현으로 정리했다.

저자명, 소속, funding, data availability 같은 실제 author decision 항목은 지어내지 않고 placeholder로
보존했다.

## 적용한 변경

특정 저널 문구 제거:

- `IEEE Journal of Oceanic Engineering`
- `IEEE JOE`
- `IEEE JOURNAL OF OCEANIC ENGINEERING (SUBMISSION DRAFT)`

대체 문구:

- `Target journal not finalized; keep IEEEtran journal format until author decision.`
- `Manuscript prepared in IEEEtran journal format.`
- `IEEE JOURNAL FORMAT (SUBMISSION DRAFT)`
- `target journal's no-funding statement`
- `generic IEEE journal conventions`

## 보존한 placeholder

다음 항목은 사용자/교수님/공저자 결정이 필요하므로 유지했다.

- author names
- affiliations
- corresponding author e-mail
- funding source or no-funding statement
- supplementary/data repository URL, DOI, or access policy
- acknowledgment text

## 빌드 결과

```text
Output written on manuscript.pdf (12 pages, 1929319 bytes).
```

남은 warning:

```text
Underfull \vbox (badness 10000) has occurred while \output is active []
```

해석:

- unresolved citation/reference 없음.
- overfull/underfull hbox 없음.
- 남은 것은 page-balancing 성격의 vbox warning 1개뿐.

## 판단

현재 원고는 특정 저널명에 묶이지 않은 IEEE journal-format draft가 되었다.

다음 단계는 `143. Professor-facing manuscript package note`가 좋다. 교수님께 보여줄 때 어떤 부분이
확정/미확정인지 한 장짜리 설명 메모를 만들면, 보고할 때 훨씬 덜 흔들린다.
