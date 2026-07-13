# Local patch record

## 대상

로컬 파일:

```text
paper/manuscript.tex
```

주의:

`paper/`는 Git ignored 상태다. 이번 commit/push에는 원고 파일을 포함하지 않는다.

## 변경 요약

### Results table

변경 전:

```text
6 columns
13 data rows
\tabcolsep = 3.5pt
```

변경 후:

```text
5 columns
6 data rows
\tabcolsep = 3.0pt
```

압축 방식:

- static mean/median validation을 한 행으로 통합.
- moving RMSE와 moving whitening은 각각 유지.
- moving adaptive/sparse schedule failure는 한 행 유지.
- quasi-static speed별 세부 행을 하나의 boundary 행으로 통합.
- long-range floor comparison은 유지.

### Limitations table

변경 전:

```text
5 columns
7 data rows
\tabcolsep = 3.5pt
```

변경 후:

```text
4 columns
6 data rows
\tabcolsep = 3.0pt
```

압축 방식:

- “Final citation styling still pending” 행 제거.
- “Paper placement” column 제거.
- 각 follow-up action 문장을 짧게 정리.

## claim safety check

삭제하거나 약화하지 않은 핵심 문장:

- static 600 m 성능 개선.
- moving target RMSE improvement 미주장.
- moving residual whitening mechanism.
- quasi-static 0.005 m/s conservative boundary.
- compact aperture / long-range floor limitation.
- “first frequency hopping”이 아니라 mechanism/transplantation/boundary claim이라는 novelty 방어.

