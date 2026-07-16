# Delta from folder 120 supplement dry run

## What changed since 120

120번 `Supplement archive dry run`은 당시 그림 패키지를 Fig.1--6 중심으로 정리했다.

현재 원고는 다음 변화가 있다.

1. `fig_tworay_fit.png`가 추가되어 그림이 7개가 됐다.
2. two-ray mechanism 수치(`delta=1.34/1.87 ms`, `R²=0.99/0.75`)가 원고에서 더 중요해졌다.
3. 144번 traceability audit에서 이 수치의 직접 근거가 약점으로 지적됐다.
4. 145번에서 해당 약점을 닫는 재현 스크립트, JSON, SVG가 생성·커밋됐다.

## Update required to supplement package

Add to `supplement_carrier_agile_usbl/` draft layout:

```text
results/
  two_ray_fit.json
figures/
  fig_tworay_fit.png
  two_ray_fit.svg
figure_scripts/
  reproduce_tworay_fit.py
```

Source folder:

```text
145. Two-ray mechanism evidence closure/
```

## Updated figure list

Old 120 list:

- Fig.1 system concept
- Fig.2 carrier sensitivity
- Fig.3 static validation
- Fig.4 moving whitening
- Fig.5 quasi-static boundary
- Fig.6 CRLB floor

New 136 list:

- Fig.1 system concept
- Fig.2 carrier sensitivity
- Fig.3 static validation
- Fig.4 moving whitening
- Fig.5 quasi-static boundary
- Fig.6 CRLB floor
- Fig.7/two-ray mechanism fit (`fig_tworay_fit.png`; exact numbering depends on final manuscript float order)

## Policy unchanged

The raw manuscript source/PDF remains excluded from GitHub unless the user explicitly requests otherwise. The supplement package can later include figures and source-data as a separate archive/DOI package, not as part of the normal numbered-folder GitHub workflow.
