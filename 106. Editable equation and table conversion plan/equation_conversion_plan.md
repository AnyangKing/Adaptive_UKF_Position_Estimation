# Equation conversion plan

The current manuscript contains 23 fenced `math` blocks. These should be converted into editable equations, not images.

## Equation groups

| Group | Equations | Manuscript role | Conversion priority |
|---|---:|---|---|
| Geometry and observation model | Eq. (1)--(6) | Defines array center, ranges, TOA/TDOA/DOA observation vector | High |
| UKF and adaptive-R model | Eq. (7)--(11) | Defines state, transition, measurement model, adaptive covariance scaling | High |
| Carrier-sensitive coherent mechanism | Eq. (12)--(18) | Defines phase-locking, carrier agility, and motion self-whitening mechanism | Highest |
| Frequency policies | Eq. (19)--(20) | Fixed 32 kHz and 30--34 kHz agile schedule | Medium |
| Validation metrics | Eq. (21)--(23) | Settled RMSE, elevation residual, lag-1 correlation | High |

## Conversion rules

- Use editable equation objects in Word or native LaTeX equations.
- Preserve numbering for equations that are referenced in the text or likely to be discussed by reviewers.
- Do not convert equations to images.
- Keep the adaptive-R expression exactly aligned with the folder-93 code audit:
  - continuous scale `s_k=min(100,1+(g_k/2)^2)`;
  - block-wise NIS inflation;
  - thresholds 6.63, 18.48, 9.21.
- Keep the carrier phase expression visible because it is the mechanism core:
  - `\phi_k(f_k,\delta_k)=2\pi f_k\delta_k+\theta_r`.

## Possible equation-count compression

If the target template is tight:

- Combine DOA azimuth/elevation into one aligned equation.
- Inline fixed/agile frequency policy equations if necessary.
- Keep adaptive-R, phase model, settled RMSE, and lag-1 correlation as display equations.

## Verification after conversion

After conversion, check:

- all 23 math blocks are either converted or intentionally inlined;
- equation numbers are consecutive;
- no equation became a bitmap;
- `f_k`, `\delta_k`, `\phi_k`, `R_k`, and `NIS` notation remains consistent;
- all headline results remain outside equations and unchanged.
