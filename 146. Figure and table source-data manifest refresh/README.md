# 146. Figure and table source-data manifest refresh

## 목적

현재 local `paper/manuscript.tex`는 12쪽 IEEE-neutral draft이며, 그림 7개와 표 6개를 포함한다. 120번 supplement dry run은 당시 Fig.1--6 기준이었고, 이후 `fig_tworay_fit.png`와 145번 two-ray evidence closure가 추가됐다.

이 폴더는 최신 원고 기준으로 그림/표별 source-data와 numbered folder 근거를 다시 정리한다.

## 핵심 업데이트

- Fig. `fig_tworay_fit.png`를 공식 manifest에 추가.
- 145번 `results/two_ray_fit.json` / `two_ray_fit.svg`를 two-ray mechanism source-data로 연결.
- `paper/`는 계속 local-only/ignored로 유지.
- GitHub에는 numbered folder manifest만 올리고, 실제 manuscript source/PDF는 올리지 않는 규약을 재확인.

## 산출물

- `figure_source_manifest.md` — 그림 7개별 source-data/script/folder 매핑
- `table_source_manifest.md` — 표 6개별 근거 폴더 매핑
- `supplement_delta_from_120.md` — 120번 dry-run 대비 변경점
- `submission_package_policy.md` — 무엇을 포함/제외할지에 대한 투고 패키지 정책

## 판정

최신 원고의 핵심 그림/표는 numbered folder와 추적 가능하다. 특히 144번에서 약점으로 잡힌 two-ray fit 수치는 145번으로 닫혔으므로, 이제 supplement manifest에 넣을 수 있다.
