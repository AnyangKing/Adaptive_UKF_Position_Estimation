# 226. Publication quality vector figures

## 목적

논문 그림을 PNG 중심 산출물에서 PDF/vector 중심 산출물로 재생성했다.

기존 원고의 수치 claim은 바꾸지 않고, 그림의 인쇄 품질과 논문스러운 만듦새를 개선하는 것이 목적이다.

## 산출 원칙

- 모든 그림은 `paper/figures/*.pdf`를 1차 산출물로 만든다.
- 호환성과 빠른 확인을 위해 같은 그림의 `*.png`도 600 dpi로 함께 만든다.
- 원고에서는 확장자를 제거한 `\includegraphics{fig_name}` 형태를 사용하면 LaTeX가 PDF를 우선 사용할 수 있다.
- 색상, 선 굵기, 마커, grid, legend 위치를 통일한다.
- 새 실험, 새 수치, 새 claim은 추가하지 않는다.

## 생성 대상

- `fig1_system_concept`
- `fig2_frequency_agile_bias`
- `fig3_static_600m_paired_rmse`
- `fig4_moving_whitening_lag1`
- `fig5_quasi_static_speed_boundary`
- `fig6_crlb_floor`
- `fig7_moving_full_range_rmse`
- `fig8_moving_full_range_gain_tail`
- `fig_tworay_fit`

## 재현

```powershell
python ".\226. Publication quality vector figures\make_publication_figures.py"
```

스크립트는 결과 JSON/CSV/요약 파일에서 값을 읽어 `paper/figures`에 PDF와 600 dpi PNG를 생성한다.

## 커밋 규칙

이 폴더만 git에 올린다. `paper/`의 PDF/PNG 그림 파일과 원고 include 변경은 로컬 전용으로 유지한다.
