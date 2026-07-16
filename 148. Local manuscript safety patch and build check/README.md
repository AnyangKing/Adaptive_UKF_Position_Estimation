# 148. Local manuscript safety patch and build check

## 목적

147번 감사에서 나온 안전 패치 중 원고 claim을 바꾸지 않는 항목만 `paper/manuscript.tex`에 local-only로 적용하고, LaTeX 빌드를 확인했다.

중요: `paper/`는 GitHub에 올리지 않는다. 이 148번 폴더에는 적용 기록과 빌드 결과만 남긴다.

## 적용한 local-only 원고 패치

`Supplementary Material and Data Availability` 문장을 수정했다.

변경 전 요지:

- figure-generation scripts underlying `Figs.~\ref{fig:concept}--\ref{fig:floor}`

문제:

- label range가 좁게 읽혀 static/moving/quasi/two-ray figure가 빠져 보일 수 있음.

변경 후 요지:

- all figures and numerical tables의 source-data를 제공한다고 표현.
- two-ray fit curves와 `delta/R^2` 값이 supplementary `two_ray_fit.json`에서 재현된다고 명시.

## 빌드 결과

명령:

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
```

결과:

- 빌드 성공.
- PDF: 12 pages.
- 출력 PDF 크기: 1,938,316 bytes.
- Overfull hbox: 0.
- Underfull hbox: 0.
- 남은 경고: `Underfull \vbox (badness 10000)` 1개.
- unresolved reference/citation 없음.

## Git 정책 확인

`git status --short`에서 `paper/`는 표시되지 않았다. 즉 원고 소스/PDF는 계속 ignored/local-only 상태다.

커밋 대상은 148번 기록 폴더만이다.
