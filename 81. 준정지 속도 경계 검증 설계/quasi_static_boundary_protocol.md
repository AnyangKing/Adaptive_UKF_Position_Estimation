# Quasi-static speed boundary validation protocol

작성일: 2026-07-09  
상태: 실험 전 사전등록 프로토콜.

## 1. Motivation

The validated positive result of the current paper is static 600 m localization: fixed 32 kHz transmission produced 13.01 m mean settled RMSE, whereas frequency-agile pinging produced 8.87 m. However, the moving-target validation showed residual whitening without reproducible RMSE improvement. The paper therefore uses the phrase “static/quasi-static” cautiously.

To defend this phrase, we need to quantify the transition between the static and moving regimes.

## 2. Physical hypothesis

The carrier-sensitive interference phase is

```text
phi(t) = 2*pi*f*delta(t) + theta_r.
```

For a static target, `delta(t)` is approximately constant. Fixed carrier transmission therefore locks the coherent bias phase, and frequency hopping provides useful phase diversity.

For a moving target, `delta(t)` changes over time. Even under fixed carrier transmission, the phase drifts and creates motion-induced self-whitening. Frequency hopping may still whiten residuals, but the incremental RMSE benefit can disappear.

The quasi-static boundary is the speed range where `delta(t)` changes slowly enough that fixed-carrier bias remains harmful, while frequency hopping still provides additional whitening.

## 3. Experimental design

### Primary setting

- Range: 600 m
- Source types:
  - static: `v = 0`
  - radial slow drift
  - tangential slow drift
- Speeds:
  - `0.000 m/s`
  - `0.005 m/s`
  - `0.010 m/s`
  - `0.030 m/s`
  - `0.050 m/s`
  - `0.100 m/s`
- Carrier policies:
  - fixed 32 kHz
  - frequency-agile 30–34 kHz schedule from 61/63
- Repeats:
  - recommended n = 20 geometry/seed pairs per speed and motion type
  - minimum n = 12 if runtime is high

### Optional secondary setting

- Range: 400 m
- Purpose: check whether the transition appears earlier/later in the intermediate gate regime.

## 4. Metrics

### Performance metrics

- settled RMSE fixed
- settled RMSE hop
- paired gain = fixed RMSE − hop RMSE
- mean gain
- median gain
- improved fraction
- P90 RMSE
- divergence rate

### Mechanism metrics

- DOA/elevation residual lag-1 correlation under fixed
- DOA/elevation residual lag-1 correlation under hop
- lag-1 reduction = fixed lag-1 − hop lag-1
- Spearman correlation between lag-1 reduction and RMSE gain

## 5. Statistical tests

For each speed and motion type:

- paired one-sided Wilcoxon test for RMSE gain > 0
- paired test for lag-1 fixed > lag-1 hop
- bootstrap 95% CI for mean gain

Across speeds:

- identify the largest speed at which mean and median gain remain positive and p < 0.05
- if p is weak but effect direction is positive, report as trend, not validated quasi-static regime

## 6. Decision rules

| Outcome | Interpretation | Manuscript consequence |
|---|---|---|
| gains remain significant up to 0.01 m/s | quasi-static claim supported | keep “static/quasi-static” |
| gains remain significant up to 0.03–0.05 m/s | slow-drift applications supported | mention docking/moored beacon drift more confidently |
| only v=0 works | static only | change title/body to “static targets” |
| lag-1 whitening persists but RMSE gain vanishes | mechanism holds, performance boundary | keep moving boundary interpretation |
| hop worsens tail at low speed | need risk-aware schedule before quasi-static claim | reduce claim and move to future work |

## 7. Implementation notes

- Reuse 61번 static validation pipeline for settled RMSE measurement.
- Reuse 63번 moving validation pipeline for residual lag-1 extraction.
- Do not alter carrier schedule after seeing results.
- Use new independent seeds; do not reuse 61/63 seeds as validation data.
- Store output JSON with per-speed summaries and raw paired trials.
- Generate at least one figure:
  - x-axis: speed
  - y-axis left: mean RMSE gain
  - y-axis right or second panel: lag-1 reduction
  - mark validated / trend / failed regimes.

## 8. Expected manuscript use

If successful, this experiment can strengthen the title and claims:

> static/quasi-static long-range USBL targets

If unsuccessful, it still improves honesty:

> static long-range USBL targets, with quasi-static extension left to future work

Either outcome is useful because it prevents overclaiming.
