# Proposed supplement archive layout

```text
supplement_carrier_agile_usbl/
  README.md
  environment/
    python_version.txt
    package_notes.txt
  data/
    agility.json
    static_hop_validation.json
    moving_validation.json
    quasi_static_boundary.json
    quasi_static_trials.csv
    crlb.json
    method_facts.json
  code/
    45_crlb_floor/
    58_carrier_sensitivity/
    61_static_validation/
    63_moving_boundary/
    82_quasi_static_boundary/
    93_method_audit/
  figures/
    fig1_system_concept.png
    fig2_frequency_agile_bias.png
    fig3_static_600m_paired_rmse.png
    fig4_moving_whitening_lag1.png
    fig5_quasi_static_speed_boundary.png
    fig6_crlb_floor.png
  figure_scripts/
    make_fig1_polished.py
    generate_core_figures.py
    generate_fig5_png.py
  docs/
    claim_to_artifact_matrix.md
    rerun_commands.md
    data_code_availability_statement.md
```

## README에 들어갈 핵심 문장

> This supplement contains simulation scripts, frozen carrier schedules, result JSON/CSV files,
> and figure-generation scripts supporting the manuscript’s static 600 m validation, moving-target
> residual-whitening boundary, quasi-static speed boundary, and compact-aperture floor analysis.

## 재현 순서

1. Python 환경 확인.
2. 각 folder의 `test_diagnostic.py` 실행.
3. 61/63/82 runner 중 필요한 것 재실행.
4. figure scripts 실행.
5. manifest SHA256과 새 결과 비교.

## 공개 정책별 차이

| 정책 | archive 사용 |
|---|---|
| public GitHub + DOI | 이 구조를 release archive로 사용 |
| journal supplementary ZIP | 이 구조를 ZIP으로 제출 |
| data/code on request | 이 구조를 내부 보관하고 요청 시 제공 |

## 주의

논문 파일 `paper/manuscript.tex`는 이 archive의 필수 구성요소가 아니다. 저널 제출본과 supplement는 분리한다.
