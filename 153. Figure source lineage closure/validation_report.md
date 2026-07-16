# Figure lineage validation report

## 총괄

| 항목 | 결과 |
|---|---:|
| 원고 PNG | 7 |
| byte-identical | 7/7 |
| pixel-identical | 7/7 |
| generator present | 7/7 |
| data source present | 전부 |

## source 연결

| 원고 그림 | reference 또는 재현 출력 | generator |
|---|---|---|
| fig1_system_concept.png | 101 polished PNG | 101 make_fig1_polished.py |
| fig2_frequency_agile_bias.png | 95 packaged PNG | 70 generate_core_figures.py |
| fig3_static_600m_paired_rmse.png | 95 packaged PNG | 70 generate_core_figures.py |
| fig4_moving_whitening_lag1.png | 95 packaged PNG | 70 generate_core_figures.py |
| fig5_quasi_static_speed_boundary.png | 95 packaged PNG | 95 generate_fig5_png.py |
| fig6_crlb_floor.png | 95 packaged PNG | 70 generate_core_figures.py |
| fig_tworay_fit.png | 153 temporary reproduction | 138 generate_tworay_fit_figure.py |

## two-ray 직접 재현

```text
(400, 1): fixed-delta fit R^2 = 0.995
(600, 5): fixed-delta fit R^2 = 0.750
wrote figure_lineage_report.json: 7/7 byte-identical, 7/7 pixel-identical
ok: 7/7 figures have exact pixel lineage
```

원고 PNG와 재현 PNG:

- bytes: 159,608 / 159,608
- SHA256:
  `DE3D71050CA6BF86024604F3F1DC66D259E65B9D6257158076D6D8CE7E4E7C8C`
- dimensions: 1050 × 1320 px
- RGBA mean absolute difference: 0.0

## 결론

147번에서 제기한 two-ray PNG production-path gap은 해소됐다. 실제 생성기는 138번에 있었으며,
현재 원고 그림은 그 생성기의 결정적 출력과 완전히 동일하다. 실제 supplement에는 145번 evidence
generator와 138번 manuscript PNG generator를 모두 포함해야 한다.
