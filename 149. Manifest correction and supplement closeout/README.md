# 149. Manifest correction and supplement closeout

## 목적

146번 source-data manifest와 147번 float/structure audit 사이에서 발견된 작은 불일치를 closeout한다.

이 폴더는 이전 numbered folder를 수정하지 않고, 후속 인계자가 최신 기준을 혼동하지 않도록 “정정 메모”를 남기는 역할이다.

## 정정 1 — 표 개수

146번 README에는 “그림 7개와 표 6개”라고 적었지만, 현재 원고의 labeled table은 다음 7개로 보는 것이 맞다.

1. `tab:priorart`
2. `tab:estimators`
3. `tab:routing`
4. `tab:crlb`
5. `tab:results`
6. `tab:quasi`
7. `tab:limitations`

따라서 최신 표현은 다음이 맞다.

> 현재 원고는 그림 7개와 labeled table 7개를 포함한다.

## 정정 2 — two-ray PNG production path

145번은 two-ray claim을 JSON/SVG로 닫았다.

- source JSON: `145. Two-ray mechanism evidence closure/results/two_ray_fit.json`
- source SVG: `145. Two-ray mechanism evidence closure/results/two_ray_fit.svg`

남은 것은 `paper/figures/fig_tworay_fit.png`가 이 SVG/JSON에서 생성된 final render임을 패키징 단계에서 명시하는 것이다.

권장 closeout 방식:

1. 최종 supplement archive에 `two_ray_fit.json`과 `two_ray_fit.svg`를 포함한다.
2. `fig_tworay_fit.png`는 manuscript-rendered figure로 포함한다.
3. supplement README에 다음 문장을 넣는다.

> `fig_tworay_fit.png` is the manuscript PNG rendering of `two_ray_fit.svg`, whose numerical source data are stored in `two_ray_fit.json`.

## 정정 3 — Data Availability patch 반영됨

148번에서 local-only 원고 패치가 적용됐다.

현재 Data Availability는 더 이상 `Figs.~concept--floor` 같은 좁은 range 표현을 쓰지 않고, all figures and numerical tables를 대상으로 한다. 또한 two-ray `delta/R^2` 값이 `two_ray_fit.json`에서 재현된다는 문장이 들어갔다.

## 현재 상태

- 원고 local build: 성공, 12쪽.
- overfull hbox: 0.
- unresolved references/citations: 0.
- 남은 경고: underfull vbox 1개.
- GitHub: numbered folder만 push하는 정책 유지.

## 다음 후보 목표

`150. Final PDF visual spot check after local patch`

148번 패치 이후 생성된 12쪽 PDF를 페이지 단위로 다시 렌더링/육안 QA하여, Data Availability 패치가 마지막 페이지 레이아웃을 망가뜨리지 않았는지 확인한다.
