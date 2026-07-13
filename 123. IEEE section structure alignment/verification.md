# Verification

## Static LaTeX structure check

`paper/manuscript.tex`에서 확인된 heading 구조:

```text
62  \section{Introduction}
78  \section{Related Work and Problem Statement}
143 \section{System Model and UKF Fusion}
208 \subsection{Implementation parameters}
226 \section{Proposed Carrier-Agile Whitening Method}
228 \subsection{Post-Gating DOA Bias Floor}
248 \subsection{Carrier-Sensitive Coherent Interference Mechanism}
285 \subsection{Carrier-Agile Transmission Schedule}
300 \section{Experimental Validation and Applicability Boundary}
302 \subsection{Static Long-Range Validation}
324 \subsection{Whitening Evidence and Motion Boundary}
412 \section{Discussion}
475 \section{Conclusion}
```

## Counts

| 항목 | 개수 |
|---|---:|
| primary `\section{}` | 7 |
| `\subsection{}` | 6 |
| `table*` | 3 |
| figure | 6 |
| back-matter `\section*{}` | 6 |

## Build status

이번 작업은 section 구조 조정이다. 최신 PDF 빌드는 아직 완료하지 않았다.

이전 122번에서 확인한 것처럼 sandboxed PowerShell에서는 MiKTeX가 사용자 Roaming 디렉터리에 접근하려다
권한 문제로 실패했다. 최신 PDF 확인은 사용자 승인 후 별도 단계에서 수행한다.

## Git policy

`paper/`는 Git ignored 상태다. 이번 commit/push 대상은 이 123번 기록 폴더만이다.

