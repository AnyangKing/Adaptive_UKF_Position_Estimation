# 126. Local LaTeX build approval check

## 목적

123--125번에서 적용한 IEEE 조판 패치가 실제 PDF 빌드에서 어떻게 반영되는지 확인했다.

확인 대상:

- 7장 section 구조
- figure float 재배치
- full-width table 축약
- PDF page count
- LaTeX warning
- unresolved reference/citation 여부

## 빌드 결과

최종 빌드 성공.

```text
Output written on manuscript.pdf (7 pages, 1708038 bytes).
```

최신 파일 시각:

```text
manuscript.tex  2026-07-13 13:48:54
manuscript.pdf  2026-07-13 13:55:53
manuscript.log  2026-07-13 13:55:53
```

## 경고 요약

최종 로그 기준:

| 항목 | 결과 |
|---|---:|
| PDF page count | 7 pages |
| unresolved citation/reference | 0 |
| rerun needed | 0 |
| float-only warning | 0 |
| Overfull hbox | 1 |
| Underfull hbox | 1 |

남은 warning:

```text
Overfull \hbox (3.29744pt too wide) in paragraph at lines 140--140
Underfull \hbox (badness 1742) in paragraph at lines 319--325
```

## 판단

이번 빌드로 123--125번 조판 패치가 성공적으로 반영된 것으로 본다.

- 기존에 문제였던 후반부 figure 몰림/float-only warning은 해소됐다.
- 7쪽 분량은 유지됐다.
- reference/citation 정합성은 깨지지 않았다.
- 남은 overfull/underfull은 심각한 수준이 아니며 다음 미세조정에서 처리 가능하다.

## 다음 작업

다음은 `127. Minor overfull underfull cleanup`이 적절하다.

- Overfull line 140은 prior-art table 마지막 column의 `TOA/TDOA/DOA-` 줄바꿈 문제다.
- Underfull line 319--325는 Frequency-Agile Transmission Schedule subsection 첫 문단의 줄 조정 문제다.
- claim이나 수치는 건드리지 않고 hyphenation/wording만 다듬으면 된다.

