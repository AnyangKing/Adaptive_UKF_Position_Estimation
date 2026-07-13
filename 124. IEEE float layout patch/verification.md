# Verification

## Commands used

```powershell
rg -n "fig:concept|fig:bias|fig:static|fig:moving|fig:quasi|fig:floor|begin\{figure\}|end\{figure\}|section\{Conclusion\}|section\*\{Supplementary" paper\manuscript.tex
Select-String -LiteralPath "paper\manuscript.tex" -Pattern "\\label\{fig:" | Group-Object Line | Select-Object Count,Name
git status --short --ignored "paper"
```

## Key output

```text
206:Fig.~\ref{fig:concept}.
208:\begin{figure}[!t]
218:\label{fig:concept}

251:Fig.~\ref{fig:floor}
261:\begin{figure}[!t]
268:\label{fig:floor}

297:Fig.~\ref{fig:bias}
308:\begin{figure}[!t]
315:\label{fig:bias}

350:Fig.~\ref{fig:static}
357:\begin{figure}[!t]
363:\label{fig:static}

381:Fig.~\ref{fig:moving}
385:\begin{figure}[!t]
392:\label{fig:moving}

402:Fig.~\ref{fig:quasi}
405:\begin{figure}[!t]
412:\label{fig:quasi}

537:\section{Conclusion}
557:\section*{Supplementary Materials}
```

Label duplication check:

```text
1 \label{fig:concept}
1 \label{fig:floor}
1 \label{fig:bias}
1 \label{fig:static}
1 \label{fig:moving}
1 \label{fig:quasi}
```

Git ignored check:

```text
!! paper/
```

## Build status

최신 PDF 빌드는 아직 수행하지 않았다. 이전 122번에서 MiKTeX가 사용자 Roaming 디렉터리에 접근하려다
권한 문제를 일으켰기 때문에, PDF 빌드는 사용자 승인 후 별도 단계로 진행한다.

