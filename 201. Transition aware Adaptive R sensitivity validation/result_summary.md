# Transition-aware Adaptive-R sensitivity validation result

## Protocol

- total paired subset cases per variant: 24
- variants: 9
- baselines: fixed and plain-hop results are reused from folder 191 for the same subset keys.
- truth usage: truth is used for signal synthesis and final error computation only.
- claim boundary: first-pass subset sensitivity diagnostic, not a replacement for the 528-case validation.

## Overall sensitivity grid

| variant | threshold | cap | mean RMSE | gain vs hop | p vs hop | tail worse vs hop | gain vs fixed | p vs fixed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| softR_thr0.25_cap25 | 0.25 | 25 | 6.986 | 7.205 | 1.101e-02 | 0.000 | 3.276 | 7.189e-03 |
| softR_thr0.25_cap100 | 0.25 | 100 | 6.979 | 7.212 | 2.194e-02 | 0.000 | 3.283 | 7.189e-03 |
| softR_thr0.25_cap400 | 0.25 | 400 | 7.020 | 7.171 | 2.194e-02 | 0.000 | 3.242 | 7.189e-03 |
| softR_thr0.5_cap25 | 0.50 | 25 | 6.993 | 7.198 | 1.591e-02 | 0.000 | 3.269 | 7.921e-03 |
| softR_thr0.5_cap100 | 0.50 | 100 | 6.986 | 7.205 | 1.591e-02 | 0.000 | 3.276 | 7.921e-03 |
| softR_thr0.5_cap400 | 0.50 | 400 | 7.005 | 7.186 | 1.591e-02 | 0.000 | 3.257 | 7.921e-03 |
| softR_thr1_cap25 | 1.00 | 25 | 7.009 | 7.182 | 4.086e-02 | 0.000 | 3.252 | 7.921e-03 |
| softR_thr1_cap100 | 1.00 | 100 | 6.922 | 7.269 | 4.086e-02 | 0.000 | 3.339 | 7.921e-03 |
| softR_thr1_cap400 | 1.00 | 400 | 6.922 | 7.269 | 4.086e-02 | 0.000 | 3.339 | 7.921e-03 |

## Ranking by gain vs plain hop

| rank | variant | gain vs hop | tail worse vs hop | mean RMSE |
|---:|---|---:|---:|---:|
| 1 | softR_thr1_cap400 | 7.269 | 0.000 | 6.922 |
| 2 | softR_thr1_cap100 | 7.269 | 0.000 | 6.922 |
| 3 | softR_thr0.25_cap100 | 7.212 | 0.000 | 6.979 |
| 4 | softR_thr0.5_cap100 | 7.205 | 0.000 | 6.986 |
| 5 | softR_thr0.25_cap25 | 7.205 | 0.000 | 6.986 |
| 6 | softR_thr0.5_cap25 | 7.198 | 0.000 | 6.993 |
| 7 | softR_thr0.5_cap400 | 7.186 | 0.000 | 7.005 |
| 8 | softR_thr1_cap25 | 7.182 | 0.000 | 7.009 |
| 9 | softR_thr0.25_cap400 | 7.171 | 0.000 | 7.020 |

## Canonical setting

The folder-191 canonical setting is `softR_thr0.5_cap100`. Interpret this folder as a sensitivity check, not as a new parameter search unless a different setting is explicitly revalidated on new seeds.
