# Figure source-data manifest

범위: 144--146번 시점의 `paper/manuscript.tex`, `paper/figures/`.

`paper/` 자체는 GitHub에 올리지 않는다. 이 문서는 제출 패키지를 만들 때 어떤 numbered folder와 결과 파일을 연결해야 하는지 기록한다.

## Figure mapping

| Figure file | Manuscript label | 내용 | Primary source folder | Source data | Figure script / artifact | Status |
|---|---|---|---|---|---|---|
| `fig1_system_concept.png` | `fig:concept` | carrier-agile whitening 개념도 | `101. Fig1 visual polish` | conceptual; no numeric data | `101. Fig1 visual polish/make_fig1_polished.py` | traced |
| `fig6_crlb_floor.png` | `fig:floor` | compact-aperture long-range floor / CRLB comparison | `45. CRLB 이론하한 대비 효율` | `45.../results/crlb.json` | `70. 논문 그림 1차 생성/generate_core_figures.py` | traced |
| `fig_tworay_fit.png` | `fig:tworay` | 400/600 m representative two-ray fit | `145. Two-ray mechanism evidence closure` | `145.../results/two_ray_fit.json`; `145.../results/two_ray_fit.svg` | `145.../reproduce_tworay_fit.py` plus manuscript PNG conversion path | **newly closed** |
| `fig2_frequency_agile_bias.png` | `fig:bias` | carrier sensitivity / 32 kHz vs 30--34 kHz bias collapse | `58. 반송파 미세도약 코히어런트 편향 진단` | `58.../results/agility.json` | `70. 논문 그림 1차 생성/generate_core_figures.py` | traced |
| `fig3_static_600m_paired_rmse.png` | `fig:static` | independent static 600 m validation | `61. 정지표적 도약 대규모 독립검증` | `61.../results/static_hop_validation.json` | `70. 논문 그림 1차 생성/generate_core_figures.py` | traced |
| `fig4_moving_whitening_lag1.png` | `fig:moving` | moving residual whitening and RMSE boundary | `63. 이동표적 도약 대규모검증 백색화 확인` | `63.../results/moving_validation.json` | `70. 논문 그림 1차 생성/generate_core_figures.py` | traced |
| `fig5_quasi_static_speed_boundary.png` | `fig:quasi` | quasi-static speed sweep / validated boundary | `82. 준정지 속도 경계 검증 실행`, `95. Fig5 PNG and submission packaging` | `82.../results/quasi_static_boundary.json`; `82.../results/quasi_static_trials.csv` | `95. Fig5 PNG and submission packaging/generate_fig5_png.py` | traced |

## Current source-file hashes

These hashes were computed locally on 2026-07-16 for reproducibility/package checking. Paths are project-root relative.

| Role | Path | Bytes | SHA256 |
|---|---|---:|---|
| Fig.1 generator | `101. Fig1 visual polish/make_fig1_polished.py` | 7962 | `A4987DCDB300BC2980BF3B424772C06AB050C99BD670CA7F7CB53B5DABE706FD` |
| Fig.2/3/4/6 generator | `70. 논문 그림 1차 생성/generate_core_figures.py` | 9684 | `81862384AFA33737869B8CC722488B1EB95897D63AF96293B3FC1A84D84BE212` |
| Fig.5 generator | `95. Fig5 PNG and submission packaging/generate_fig5_png.py` | 2722 | `35DB8A798A844CC912E6B058B284F08DE5ADF784E7A257A388DCDE5E151CB877` |
| Fig.2 data | `58. 반송파 미세도약 코히어런트 편향 진단/results/agility.json` | 25317 | `6ECD4375FF29165EE2A2B13D51B7FA64BBC3E82933D4FF3BC7B5B79042FF0D3B` |
| Fig.3 data | `61. 정지표적 도약 대규모 독립검증/results/static_hop_validation.json` | 23910 | `7D85E90F406CB082D7F40E53E806DE1AFC647289B48D0B63AC2BD55CD7A5E8D1` |
| Fig.4 data | `63. 이동표적 도약 대규모검증 백색화 확인/results/moving_validation.json` | 19714 | `2CC68FF4A5E0F1237216345B340442525CB28D9E85A11A1B6E8F45C85A27002D` |
| Fig.5 data | `82. 준정지 속도 경계 검증 실행/results/quasi_static_boundary.json` | 86775 | `4D15F10F0F1743F27A29A392A73512958FC9ADD31270995F4B552A5E47EBB06B` |
| Fig.5 trial data | `82. 준정지 속도 경계 검증 실행/results/quasi_static_trials.csv` | 25109 | `74A2E908E8CCCCE2A49B76ADFCA05D6308035110334536EC382D73BEE05ED4E2` |
| Fig.6 data | `45. CRLB 이론하한 대비 효율/results/crlb.json` | 15318 | `E0390800601613B4274F5EC36A6B38EAA90CC9E290BE84DB9E2C8FCCB11BFCD7` |
| Fig. two-ray closure JSON | `145. Two-ray mechanism evidence closure/results/two_ray_fit.json` | 5820 | `47087B3B1A67FEB2EEEE74A6C087AA35EED1A6C34CEA1410DE951788D950BB7C` |
| Fig. two-ray closure SVG | `145. Two-ray mechanism evidence closure/results/two_ray_fit.svg` | 4434 | `03AE73C7CF83F3E1A64852FA410C0ECDF0DC7BDB07651DF1FF6CAA81AAB450E1` |
| Method facts | `93. Method 세부 코드 대조/results/method_facts.json` | 2180 | `9D8BCB9C5F45C82C0440DCFFD205B71F03FADDC792FED59B9F8F0B2B7BD3A250` |

## Open action

`fig_tworay_fit.png` in `paper/figures/` should eventually be regenerated directly from 135's SVG/JSON or have a small conversion note. The claim itself is now traceable; only the final PNG production path remains to be formalized if the journal requires exact figure-generation scripts.
