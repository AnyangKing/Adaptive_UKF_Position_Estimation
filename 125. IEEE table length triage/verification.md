# Verification

## Static checks

실행한 정적 검사:

```powershell
rg -n "begin\{table\*\}|end\{table\*\}|begin\{tabularx\}|end\{tabularx\}|tab:results|tab:limitations|13\.01|0\.005|not first frequency" paper\manuscript.tex
Select-String -LiteralPath "paper\manuscript.tex" -Pattern "\\label\{tab:" | Group-Object Line | Select-Object Count,Name
git status --short --ignored "paper"
```

## 확인 결과

`tabularx` / `table*` 짝:

```text
105:\begin{table*}[!t]
114:\begin{tabularx}{\textwidth}{L c c L c c L}
140:\end{tabularx}
141:\end{table*}

419:\begin{table*}[!t]
426:\begin{tabularx}{\textwidth}{L L L L L}
448:\end{tabularx}
449:\end{table*}

482:\begin{table*}[!t]
488:\begin{tabularx}{\textwidth}{L L L L}
510:\end{tabularx}
511:\end{table*}
```

Table label 중복 없음:

```text
1 \label{tab:priorart}
1 \label{tab:results}
1 \label{tab:limitations}
```

Git ignored 상태:

```text
!! paper/
```

## Build status

이번 단계도 PDF 빌드는 수행하지 않았다. 실제 효과는 다음 빌드에서 page count, overfull/underfull,
float-only warning으로 확인해야 한다.

