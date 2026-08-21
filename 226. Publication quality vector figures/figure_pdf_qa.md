# PDF figure QA

## 생성 결과

`make_publication_figures.py` 실행 결과 `paper/figures`에 9개 PDF와 대응 PNG가 생성됐다.

| figure | PDF 생성 | 현재 영문 원고 사용 |
| --- | --- | --- |
| `fig1_system_concept.pdf` | yes | yes |
| `fig2_frequency_agile_bias.pdf` | yes | yes |
| `fig3_static_600m_paired_rmse.pdf` | yes | yes |
| `fig4_moving_whitening_lag1.pdf` | yes | yes |
| `fig5_quasi_static_speed_boundary.pdf` | yes | yes |
| `fig6_crlb_floor.pdf` | yes | yes |
| `fig7_moving_full_range_rmse.pdf` | yes | yes |
| `fig8_moving_full_range_gain_tail.pdf` | yes | not currently included |
| `fig_tworay_fit.pdf` | yes | yes |

## LaTeX include 방식

`paper/manuscript.tex`와 `paper/manuscript_ko.tex`의 그림 include는 `.png` 확장자를 제거한 형태로 로컬 수정했다.

예:

```tex
\includegraphics[width=\columnwidth]{fig2_frequency_agile_bias}
```

이렇게 하면 `pdflatex`가 같은 이름의 PDF를 우선 사용한다.

## 빌드 확인

영문 원고:

- `paper/manuscript.pdf`
- 14 pages
- log에서 `figures/*.pdf` 사용 확인
- fatal error 없음
- undefined citation/reference 없음
- overfull hbox 없음

한글 독해본:

- `paper/manuscript_ko.pdf`
- 16 pages
- log에서 `figures/*.pdf` 사용 확인
- fatal error 없음
- undefined citation/reference 없음
- overfull hbox 없음

한글 독해본은 PDF/vector 그림의 bounding box가 달라지면서 페이지 수가 14쪽에서 16쪽으로 늘었다. 한글본은 독해용이므로 즉시 문제는 아니지만, 사용자가 원하면 별도 작업에서 폭/float 배치를 줄여 다시 14쪽 안팎으로 맞출 수 있다.

## 품질 개선 내용

- PNG-only workflow에서 PDF/vector-first workflow로 변경.
- 대응 PNG는 600 dpi로 생성.
- 색상 팔레트, 선 굵기, marker, grid alpha, legend frame 제거를 통일.
- Matplotlib PDF font embedding을 Type 42로 설정.
- 기존 claim을 바꾸는 새 수치나 새 실험 결과는 추가하지 않음.

## 다음 그림 작업 후보

1. Fig.1은 현재 단일-column에 들어가면 정보량이 많다. 최종 투고 전 `figure*` 또는 단순화된 single-column schematic 중 하나로 결정하면 좋다.
2. Fig.8은 이미 PDF로 생성되어 있으나 현재 영문 원고에는 직접 include되지 않는다. 보충그림 또는 Fig.7과의 통합 여부를 나중에 결정할 수 있다.
3. 최종 저널/template이 확정되면 column width 기준으로 font size와 aspect ratio를 한 번 더 조정한다.
