# Build verification

## Build command

현재 로컬 환경에서는 `latexmk`가 Perl 부재로 실패하므로 수동 `pdflatex` 체인을 사용한다.

이번 129번에서는 `pdflatex`를 두 번 실행해 참조를 안정화했다.

```powershell
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

## Final log extraction

검색 패턴:

```powershell
Select-String -LiteralPath "manuscript.log" -Pattern "Output written|Overfull|Underfull|float-only|undefined|Rerun|Warning|Citation|Reference"
```

최종 중요 출력:

```text
Underfull \vbox (badness 10000) has occurred while \output is active []
Package rerunfilecheck Info: File `manuscript.out' has not changed.
Output written on manuscript.pdf (9 pages, 1725893 bytes).
```

## Interpretation

| 항목 | 결과 |
|---|---:|
| PDF page count | 9 pages |
| unresolved citation/reference | 0 |
| rerun needed | 0 |
| float-only warning | 0 |
| overfull hbox | 0 |
| underfull hbox | 0 |
| underfull vbox | 1 |

남은 `Underfull \vbox`는 page-building/float spacing 성격의 경고다. 문장 overflow나 reference 오류는 아니다.
다음 `130. Expanded manuscript visual QA`에서 실제 페이지 이미지를 보고 조정할지 판단한다.

## File state

```text
manuscript.tex  47,859 bytes
manuscript.pdf  1,725,893 bytes
manuscript.log  23,938 bytes
```

`paper/`는 Git ignored 상태이므로 위 파일들은 GitHub에 올리지 않는다.

