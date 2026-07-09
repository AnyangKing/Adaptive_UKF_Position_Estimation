# Figure manifest

## Fig. 1: system and mechanism concept

- Files:
  - `figures/fig1_system_concept.svg`
  - `figures/fig1_system_concept.png`
- Source: `72. Fig1 시스템 개념도/figures/fig1_system_concept.*`
- Purpose: compact USBL array, direct path, in-gate surface reflection, fixed-carrier phase locking, carrier-agile phase rotation.
- Manuscript section: Introduction / System model / Mechanism.
- Current issue: concept figure is usable as a first draft but may need final visual polish.

## Fig. 2: carrier-sensitive bias

- Files:
  - `figures/fig2_frequency_agile_bias.svg`
  - `figures/fig2_frequency_agile_bias.png`
- Source: `70. 논문 그림 1차 생성/figures/fig2_frequency_agile_bias.*`
- Purpose: show that the elevation-bias term changes with carrier frequency and becomes strongly reduced at long range under carrier agility.
- Manuscript section: Mechanism.
- Key numbers from source summary:
  - 600 m fixed median absolute elevation bias: 0.632 deg.
  - 600 m hop-average median absolute elevation bias: 0.053 deg.
  - 600 m reduction: about 91.6%.

## Fig. 3: static 600 m paired RMSE

- Files:
  - `figures/fig3_static_600m_paired_rmse.svg`
  - `figures/fig3_static_600m_paired_rmse.png`
- Source: `70. 논문 그림 1차 생성/figures/fig3_static_600m_paired_rmse.*`
- Purpose: main static validation figure.
- Manuscript section: Results / static validation.
- Key numbers:
  - n = 20.
  - fixed mean RMSE = 13.01 m.
  - hop mean RMSE = 8.87 m.
  - mean improvement = +4.14 m.
  - p = 0.0008.

## Fig. 4: moving-target whitening boundary

- Files:
  - `figures/fig4_moving_whitening_lag1.svg`
  - `figures/fig4_moving_whitening_lag1.png`
- Source: `70. 논문 그림 1차 생성/figures/fig4_moving_whitening_lag1.*`
- Purpose: show that carrier agility whitens moving residuals even though moving RMSE gain is not reliable.
- Manuscript section: Results / moving boundary.
- Key numbers:
  - n = 64.
  - fixed lag-1 = +0.470.
  - hop lag-1 = -0.208.
  - whitening p = 5.56e-10.
  - pooled moving RMSE gain = -0.10 m, p = 0.301.

## Fig. 5: quasi-static speed boundary

- Files:
  - `figures/fig5_quasi_static_speed_boundary.svg`
- Source: `82. 준정지 속도 경계 검증 실행/results/quasi_static_speed_boundary.svg`
- Purpose: show that quasi-static performance is non-monotonic and that the continuous validated boundary is 0.005 m/s.
- Manuscript section: Results / quasi-static boundary.
- Current issue:
  - SVG is available.
  - PNG is not yet generated in the project folder. If the Word workflow requires raster images, convert this SVG later.

## Fig. 6: CRLB / aperture floor

- Files:
  - `figures/fig6_crlb_floor.svg`
  - `figures/fig6_crlb_floor.png`
- Source: `70. 논문 그림 1차 생성/figures/fig7_crlb_floor.*`
- Purpose: explain why sub-meter 600 m performance is not expected under compact-aperture conditions.
- Manuscript section: Discussion.
- Key numbers:
  - 600 m empirical CRLB-scale value = 11.80 m.
  - routed UKF = 12.29 m.
  - NLS = 13.38 m.
  - routing bias floor vs empirical reference = 3.45 m.

