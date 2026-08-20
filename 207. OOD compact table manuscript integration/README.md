# 207. OOD compact table manuscript integration

## 목적

204번 OOD moving full validation 결과를 원고에서 문단으로만 언급하지 않고, 리뷰어가 바로 확인할 수 있는 compact table로 고정했다.

## 원고 변경

- `paper/manuscript.tex`
  - OOD moving aggregate table 추가: fixed, plain hop, soft-R의 mean RMSE, P90 RMSE, divergence.
  - claim-boundary table에도 OOD moving robustness validation 행 추가.
- `paper/manuscript_ko.tex`
  - 한글 기준 원고에도 동일한 OOD aggregate table 추가.
  - contribution/claim boundary 표에 structured 191과 OOD 204의 역할을 분리해 반영.

## 수치

| policy | mean RMSE | P90 RMSE | divergence |
|---|---:|---:|---:|
| fixed | 10.83 | 22.34 | 0.049 |
| plain hop | 10.69 | 21.61 | 0.057 |
| soft-R | 7.81 | 15.94 | 0.006 |

## 해석

이 표는 transition-aware soft-R의 simulation-level OOD robustness를 보여주는 보강 근거다. 실해역, 임의 motion, hardware frequency response 일반화는 주장하지 않는다.
