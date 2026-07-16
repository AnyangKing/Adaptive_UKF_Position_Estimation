# Supplement archive layout v2

```text
supplement_carrier_agile_usbl/
  README.md
  data/
    crlb.json
    agility.json
    static_hop_validation.json
    moving_validation.json
    quasi_static_boundary.json
    quasi_static_trials.csv
    method_facts.json
    two_ray_fit.json
  code/
    45_crlb_floor/
    58_carrier_sensitivity/
    61_static_validation/
    63_moving_boundary/
    82_quasi_static_boundary/
    93_method_audit/
    145_two_ray_closure/
  figures/
    fig1_system_concept.png
    fig2_frequency_agile_bias.png
    fig3_static_600m_paired_rmse.png
    fig4_moving_whitening_lag1.png
    fig5_quasi_static_speed_boundary.png
    fig6_crlb_floor.png
    fig_tworay_fit.png
    two_ray_fit.svg
  figure_scripts/
    make_fig1_polished.py
    generate_core_figures.py
    generate_fig5_png.py
    reproduce_tworay_fit.py
  docs/
    claim_to_artifact_matrix.md
    figure_source_manifest.md
    table_source_manifest.md
    submission_package_policy.md
    current_submission_state.md
```

## 설계 원칙

1. archive 경로는 영문 ASCII 이름으로 고정한다.
2. source 경로는 현재 번호 폴더를 가리키며 SHA256으로 내용 변경을 검출한다.
3. 각 실험의 공통 모듈을 해당 실험 코드 폴더에 함께 둬 단독 실행 가능성을 보존한다.
4. 원고 파일과 보충자료는 분리한다.
5. 공개 정책이 확정되기 전에는 실제 파일 수집이나 ZIP 생성을 하지 않는다.
