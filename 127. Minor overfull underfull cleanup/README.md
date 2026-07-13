# 127. Minor overfull underfull cleanup

## 목적

126번 빌드에서 남은 hbox warning 2개를 claim-safe 조판 문구 수정으로 제거했다.

대상 warning:

```text
Overfull \hbox (3.29744pt too wide) in paragraph at lines 140--140
Underfull \hbox (badness 1742) in paragraph at lines 319--325
```

## 적용한 로컬 수정

대상 파일:

```text
paper/manuscript.tex
```

수정 내용:

1. Prior-art table의 present-work 행에서 긴 `TOA/TDOA/DOA-UKF fusion` 표현을 `UKF fusion`으로 축약.
2. Carrier-Agile Transmission Schedule subsection 첫 문단을 줄바꿈 친화적인 문장으로 재작성.

두 수정 모두 claim, 수치, 실험 결과를 바꾸지 않는다.

## 빌드 결과

최종 `pdflatex` 빌드 성공.

```text
Output written on manuscript.pdf (7 pages, 1708011 bytes).
```

최종 warning 상태:

| 항목 | 결과 |
|---|---:|
| PDF page count | 7 pages |
| unresolved citation/reference | 0 |
| rerun needed | 0 |
| float-only warning | 0 |
| Overfull hbox | 0 |
| Underfull hbox | 0 |

## 판단

이제 로컬 IEEE PDF는 조판 로그 기준으로 상당히 깨끗한 상태다.

다음은 실제 PDF 시각 QA가 좋다. 로그상 문제는 사라졌지만, 표/그림이 독자 눈에 자연스럽게 배치됐는지는
페이지 이미지를 확인해야 한다.

