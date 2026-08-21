# Figure overlap fix QA

## 확인 방법

`paper/figures/*.png`를 직접 열어 눈으로 확인하고, `paper/manuscript.tex`를 `pdflatex` 2회로 빌드했다.

## 수정 전 주요 문제

| Figure | 문제 |
| --- | --- |
| Fig.1 | path label, gate label, beacon label, bottom claim 문장이 선/도형과 겹치거나 잘림 |
| Fig.2 | legend와 `-35%` 라벨 겹침 |
| Fig.3 | annotation box와 legend가 데이터 영역을 과도하게 점유 |
| Fig.4 | annotation box가 boxplot/paired lines를 덮음 |
| Fig.5 | check/cross marker가 과대하고 축에 가까움 |
| Fig.6 | legend/annotation이 너무 커서 slide-like |
| Fig.7 | legend가 과대하고 플롯 공간을 많이 차지 |
| Fig. two-ray | legend가 curve/scatter 위를 덮음 |

## 수정 후 판단

| Figure | 수정 후 상태 |
| --- | --- |
| Fig.1 | 큰 겹침 제거. beacon/UKF 박스 위치 미세조정 완료 |
| Fig.2 | legend와 percentage label 겹침 제거 |
| Fig.3 | annotation/legend 축소로 데이터 가림 완화 |
| Fig.4 | 긴 annotation 제거, 짧은 lag-1 note로 대체 |
| Fig.5 | marker 크기와 y-limit 조정 |
| Fig.6 | legend/annotation 축소 |
| Fig.7 | legend 축소 및 annotation 유지 |
| Fig. two-ray | legend를 figure-level top legend로 이동해 데이터 가림 제거 |

## 빌드 결과

- `paper/manuscript.pdf`
- 15 pages
- PDF/vector figures inserted
- fatal error 없음
- undefined citation/reference 없음
- overfull hbox 없음
- 남은 경고는 `Underfull \vbox`뿐

## 남은 주의점

현재 이미지는 원고를 읽고 판단할 수 있는 수준까지 정리됐다.

다만 최종 투고 전에는 실제 PDF 페이지에서 column width로 보이는 크기를 기준으로 한 번 더 육안 QA가 필요하다. 특히 Fig.1은 two-column overview로 유지할지, single-column simplified schematic으로 줄일지 page budget과 함께 결정한다.
