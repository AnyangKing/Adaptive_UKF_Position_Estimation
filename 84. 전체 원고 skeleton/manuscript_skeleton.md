# Manuscript skeleton

## Working title

Primary candidate:

> Carrier-Agile Whitening of Coherent Multipath DOA Bias in Static Shallow-Water USBL Tracking

Alternative candidate:

> Frequency-Agile Pinging for Whitening Post-Gating Multipath DOA Bias in Long-Range USBL Localization

Avoid titles centered on “moving target localization” because moving-target RMSE improvement is not validated.

## Abstract

Use 83번 Version C as baseline. Shorten only after target journal word limit is known.

Core abstract logic:

1. Compact USBL long-range localization is sensitive to DOA elevation bias.
2. Direct-path gating does not fully remove in-gate surface-reflection leakage.
3. Fixed carrier locks the coherent interference phase.
4. Ping-to-ping carrier agility rotates `phi = 2*pi*f*delta` and whitens residual DOA bias.
5. Static 600 m validation: 13.01 m to 8.87 m, -32%, p = 0.0008.
6. Moving/quasi-static boundary: whitening persists, RMSE gain is not general; continuous quasi-static support only to 0.005 m/s.

## 1. Introduction

### Paragraph 1 — problem context

Open with underwater localization demand: AUV docking, moored beacon tracking, compact USBL on small platforms. Emphasize that compact apertures make angular errors dominate long-range position error.

### Paragraph 2 — why conventional filtering is insufficient

State that TOA/TDOA/DOA-UKF fusion is necessary but not sufficient because the dominant error is not only stochastic measurement noise. In shallow water, coherent multipath can create deterministic or slowly varying DOA bias even after direct-path gating.

### Paragraph 3 — gap in prior work

Acknowledge prior work:

- radar frequency agility/glint decorrelation
- frequency-hopped acoustic modem USBL
- Costas hopping USBL
- underwater frequency diversity / frequency comb / transmitting diversity

Then narrow the gap:

> Existing work does not characterize post-gating carrier-locked coherent multipath DOA bias as a residual entering a TOA/TDOA/DOA-UKF tracking loop, nor does it quantify the static-to-moving applicability boundary of carrier-agile whitening.

### Paragraph 4 — proposed idea

Introduce frequency-agile pinging as transmit-side observation design, not a new receiver estimator. The carrier schedule changes the residual structure before fusion.

### Paragraph 5 — contributions

Use C1--C4:

1. Bias-floor characterization in compact shallow-water USBL.
2. Carrier-sensitive coherent mechanism `phi = 2*pi*f*delta`.
3. Static 600 m validation, -32%, p = 0.0008.
4. Boundary: moving whitening without reliable RMSE gain; quasi-static continuous support only to 0.005 m/s.

## 2. System and signal model

### 2.1 Array and coordinate system

Describe the eight-sensor compact USBL geometry. Give radius/height only if needed:

- radius 0.033 m
- vertical offset 0.079 m
- receiver depth 30 m in the simulation configuration

### 2.2 Channel model

Describe direct path, surface reflection, bottom reflection, white noise, sound speed, and sampling. Keep it concise and refer to simulation code as reproducibility artifact.

### 2.3 Observation vector

Observation:

```text
z = [TOA range, 7 reference TDOA ranges, azimuth, elevation]
```

Estimator state:

```text
x = [px, py, pz, vx, vy, vz]
```

### 2.4 Baseline UKF and adaptive-R routing

Explain conditional adaptive-R as the stable fusion backbone. Do not oversell it as the main novelty. It exists to put frequency-agile observation design in a realistic tracking loop.

## 3. Post-gating DOA bias floor

Purpose: compress pillar A.

### Paragraph plan

1. Even with direct-path gating and adaptive-R UKF, long-range RMSE remains meter-scale.
2. CRLB and estimator comparison show the issue is not simply filter inefficiency.
3. Rotation/bias diagnostics show a systematic elevation component tied to array/multipath geometry.
4. Blind correction routes fail or do not reproduce.

Key numbers:

- 600 m empirical CRLB around 11.80 m
- routed UKF around 12.29 m
- residual bias floor around 3.45 m
- near-range best median around 1.2 m, not sub-meter generally

## 4. Carrier-sensitive coherent interference mechanism

Purpose: explain why frequency agility can help.

Core model:

```text
phi(f, delta) = 2*pi*f*delta + theta_r
```

For static targets, `delta` is approximately fixed. A fixed carrier therefore makes a fixed interference phase and a persistent DOA bias. Changing `f` ping by ping rotates the phase and changes the residual sign/magnitude.

This section should connect:

- direct-path gate
- in-gate surface-reflection leakage
- compact aperture angular amplification
- why the method attacks only the carrier-locked component, not all errors

## 5. Frequency-agile whitening method

### 5.1 Carrier schedule

Use the frozen 30--34 kHz 20-ping schedule. State that the schedule was not retuned after validation.

### 5.2 Integration with TOA/TDOA/DOA-UKF

No receiver architecture change is required in the simulation. The method changes the measurement residual structure before UKF fusion.

### 5.3 Expected effect

For static targets:

- fixed carrier: bias is temporally correlated
- agile carrier: residual becomes temporally less correlated

For moving targets:

- fixed carrier already experiences motion-induced phase drift
- extra agility may whiten residuals but not guarantee RMSE gain

## 6. Static validation

This is the strongest results section.

Primary result:

- fixed 32 kHz 600 m: 13.01 m mean settled RMSE
- frequency-agile: 8.87 m
- improvement: -32%, paired +4.14 m, p = 0.0008
- median: 13.97 m to 7.96 m

Make the claim strong but bounded:

> The result validates carrier-agile whitening for static long-range USBL under this channel and array model.

Avoid:

> The method achieves sub-meter long-range localization.

## 7. Whitening evidence and applicability boundary

### 7.1 Moving-target whitening

Use 63번:

- lag-1 residual correlation fixed +0.470
- hop -0.208
- p = 5.6e-10

Then immediately state:

- pooled moving RMSE gain: -0.10 m
- p = 0.301

Interpretation: mechanism holds, performance gain is not general.

### 7.2 Quasi-static speed sweep

Use 82번:

- overall 82 sweep: 11.98 m to 10.49 m, p = 8.00e-05
- continuous validated speed: 0.005 m/s
- not supported: 0.010 and 0.050 m/s
- later positive: 0.030 and 0.100 m/s, interpreted as non-monotonic geometry-dependent recoveries

Safe sentence:

> The slow-drift sweep supports a very limited quasi-static extension, but not a monotonic speed threshold up to 0.100 m/s.

## 8. Discussion

### 8.1 What frequency agility does and does not do

It reduces a carrier-locked coherent bias component. It does not change aperture, array geometry, or all multipath limitations.

### 8.2 Relation to prior work

Explicitly distinguish from:

- radar glint/frequency agility
- frequency-hopped USBL modem positioning
- Costas hopping USBL
- frequency-comb iUSBL
- MIMO sonar transmitting diversity smoothing

### 8.3 Deployment implications

Static/moored/very slow drift use cases are plausible. General moving AUV target tracking requires motion/geometry-aware schedule logic.

### 8.4 Limitations

- simulation-based
- compact array
- shallow-water channel assumptions
- exact citation audit still needed
- schedule not optimized beyond frozen 30--34 kHz sweep

## 9. Conclusion

Conclusion should be short and bounded:

1. Post-gating coherent multipath DOA bias can dominate compact USBL long-range localization.
2. Carrier agility whitens a carrier-locked component of that bias.
3. Static 600 m validation shows reproducible RMSE reduction.
4. Moving and quasi-static tests define the boundary rather than proving a general moving-target method.

Final sentence candidate:

> The result is a bounded observation-design method for static long-range shallow-water USBL localization, and a starting point for future motion- and geometry-aware carrier scheduling.
