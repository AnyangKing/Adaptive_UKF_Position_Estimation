# Build commands

## Attempt 1: latexmk

명령:

```powershell
latexmk -pdf -interaction=nonstopmode manuscript.tex
```

결과:

```text
MiKTeX could not find the script engine 'perl' which is required to execute 'latexmk'.
```

해석:

`latexmk` 자체는 편리하지만 현재 Windows/MiKTeX 환경에서는 Perl script engine이 없어 실패한다.

## Attempt 2: direct MiKTeX toolchain

명령:

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

결과:

```text
pdflatex: success
bibtex: success
pdflatex: success
pdflatex: success
```

최종 산출:

```text
manuscript.pdf
7 pages
1708038 bytes
```

## 향후 빌드 규칙

이 로컬 환경에서는 당분간 `latexmk` 대신 아래 수동 빌드 체인을 사용한다.

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

단, `paper/`는 Git ignored 상태이므로 PDF와 aux/log 산출물은 GitHub에 올리지 않는다.

