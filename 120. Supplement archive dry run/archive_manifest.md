# Supplement archive manifest

## 원칙

- 이 파일은 로컬 파일의 manifest다.
- 원본 결과 JSON/CSV는 이 120번 폴더에 복사하지 않는다.
- GitHub에는 numbered folder인 이 manifest만 올라가며, raw results는 로컬 또는 별도 supplement/DOI archive로 둔다.

## Core result data candidates

| 역할 | 로컬 파일 | bytes | SHA256 |
|---|---|---:|---|
| Fig.2 / carrier sensitivity | `58. 반송파 미세도약 코히어런트 편향 진단/results/agility.json` | 25317 | `6ECD4375FF29165EE2A2B13D51B7FA64BBC3E82933D4FF3BC7B5B79042FF0D3B` |
| Fig.3 / static 600 m validation | `61. 정지표적 도약 대규모 독립검증/results/static_hop_validation.json` | 23910 | `7D85E90F406CB082D7F40E53E806DE1AFC647289B48D0B63AC2BD55CD7A5E8D1` |
| Fig.4 / moving whitening boundary | `63. 이동표적 도약 대규모검증 백색화 확인/results/moving_validation.json` | 19714 | `2CC68FF4A5E0F1237216345B340442525CB28D9E85A11A1B6E8F45C85A27002D` |
| Fig.5 / quasi-static summary | `82. 준정지 속도 경계 검증 실행/results/quasi_static_boundary.json` | 86775 | `4D15F10F0F1743F27A29A392A73512958FC9ADD31270995F4B552A5E47EBB06B` |
| Fig.5 / trial-level data | `82. 준정지 속도 경계 검증 실행/results/quasi_static_trials.csv` | 25109 | `74A2E908E8CCCCE2A49B76ADFCA05D6308035110334536EC382D73BEE05ED4E2` |
| Fig.6 / CRLB floor | `45. CRLB 이론하한 대비 효율/results/crlb.json` | 15318 | `E0390800601613B4274F5EC36A6B38EAA90CC9E290BE84DB9E2C8FCCB11BFCD7` |
| Method constants | `93. Method 세부 코드 대조/results/method_facts.json` | 2180 | `9D8BCB9C5F45C82C0440DCFFD205B71F03FADDC792FED59B9F8F0B2B7BD3A250` |

## Figure/code candidates

| 역할 | 로컬 파일 | bytes | SHA256 |
|---|---|---:|---|
| Figure package manifest | `95. Fig5 PNG and submission packaging/figure_package_manifest.md` | 1333 | `C468C5FE44C22B8F53BB939F6E2F5E631B278536B3F859F22DB512838BEF7EB5` |
| Fig.1 generator | `101. Fig1 visual polish/make_fig1_polished.py` | 7962 | `A4987DCDB300BC2980BF3B424772C06AB050C99BD670CA7F7CB53B5DABE706FD` |
| Fig.2/3/4/6 generator | `70. 논문 그림 1차 생성/generate_core_figures.py` | 9684 | `81862384AFA33737869B8CC722488B1EB95897D63AF96293B3FC1A84D84BE212` |
| Fig.5 generator | `95. Fig5 PNG and submission packaging/generate_fig5_png.py` | 2722 | `35DB8A798A844CC912E6B058B284F08DE5ADF784E7A257A388DCDE5E151CB877` |

## Need to include by folder

For full reproducibility, include each core experiment folder’s `.py` files, not just the runner.
The folders are self-contained and include `channel.py`, `config.py`, `estimators.py`, `measurement.py`,
`peak_measurement.py`, `ukf.py`, `conditional_adaptive.py`, and tests where applicable.

## Do not include by default

- `paper/` unless user explicitly decides to share manuscript source.
- root handoff/operation MD files.
- `study_exports/`.
- `.claude/`.
- `__pycache__/`.
- temporary logs unless required by the journal.
- unrelated exploratory folders not cited by the manuscript.
