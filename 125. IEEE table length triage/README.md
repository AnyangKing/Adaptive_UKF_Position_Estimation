# 125. IEEE table length triage

## 목적

124번에서 figure float를 본문 흐름 안으로 이동한 뒤, 이번에는 IEEE 2단 양식에서 가장 큰 분량 리스크인
full-width `table*` 3개를 점검했다.

논문 파일 자체는 로컬 `paper/`에 남기고 Git에는 올리지 않는다. 이 폴더는 판단 근거와 변경 기록만
저장한다.

## 결론

| 표 | 판단 | 조치 |
|---|---|---|
| `tab:priorart` | 본문 유지 | novelty 방어 핵심이라 구조 유지. |
| `tab:results` | 본문 유지, 강하게 압축 | 13개 결과 행을 6개 핵심 행으로 압축. |
| `tab:limitations` | 본문 유지, 편집용 항목 제거 | 5열을 4열로 줄이고 submission-only 항목 제거. |

## 로컬 원고 변경

`paper/manuscript.tex`에서 다음 저위험 조판 패치를 적용했다.

- `tab:results`
  - caption을 짧게 수정.
  - column 수를 6개에서 5개로 축소.
  - `\tabcolsep`을 3.5pt에서 3.0pt로 축소.
  - 행 수를 13개에서 6개로 축소.
  - 정지 600 m, moving RMSE negative, moving whitening positive, adaptive schedule failure,
    quasi-static boundary, long-range floor는 모두 유지.
- `tab:limitations`
  - caption을 짧게 수정.
  - column 수를 5개에서 4개로 축소.
  - submission-only citation styling 행 제거.
  - scientific limitation 중심으로 재정리.

## 중요한 보존 사항

이번 패치는 표 분량을 줄였지만 핵심 claim은 바꾸지 않았다.

- static 600 m: 13.01 m to 8.87 m, $p=0.0008$ 유지.
- moving pooled RMSE gain 없음: $-0.10$ m, $p=0.301$ 유지.
- moving residual whitening: lag-1 $+0.470$ to $-0.208$, $p=5.56\times10^{-10}$ 유지.
- quasi-static continuous boundary: 0.005 m/s 유지.
- sub-meter 600 m claim 금지 근거: CRLB-scale 11.80 m / routed UKF 12.29 m / NLS 13.38 m 유지.

## 다음 작업

다음은 `126. Local LaTeX build approval check`가 좋다.

지금까지 section 구조, figure 위치, table 분량을 모두 로컬 원고에 반영했다. 이제 실제 PDF를 다시 빌드해
페이지 수, overfull/underfull, float-only warning이 얼마나 줄었는지 확인해야 한다. 다만 이전 122번에서
MiKTeX가 사용자 Roaming 디렉터리에 접근해야 해서 sandbox 빌드가 실패했으므로, 이 단계는 사용자 승인 또는
승인된 실행 환경이 필요하다.

