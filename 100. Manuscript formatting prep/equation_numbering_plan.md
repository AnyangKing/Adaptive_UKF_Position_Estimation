# Equation numbering plan

This plan maps every math block in `manuscript_clean_source.md` to a stable equation number for later Word or LaTeX conversion.

## Primary equation sequence

| Eq. | Manuscript location | Content | Conversion note |
|---:|---|---|---|
| (1) | Section 2 | Array center `\bar{s}` | Keep as display equation. |
| (2) | Section 2 | Source-to-sensor range `\rho_{i,k}` | Keep as display equation. |
| (3) | Section 2 | Observation vector `z_k` | This is central: one TOA range, seven TDOA differences, two DOA angles. |
| (4) | Section 2 | Ideal TOA/TDOA range terms | Keep index range `i=1,\ldots,7`. |
| (5) | Section 2 | Azimuth `\alpha_k` | Can be grouped with Eq. (6) if the journal prefers fewer equations. |
| (6) | Section 2 | Elevation `\epsilon_k` | Can be grouped with Eq. (5). |
| (7) | Section 2 | UKF state vector | Avoid using the same symbol `x_k` for state and coordinate in final typesetting if the editor requests stricter notation. |
| (8) | Section 2 | Constant-velocity transition | Include process noise definition in prose if page space is tight. |
| (9) | Section 2 | Measurement model | Short equation; may be inline in a compressed version. |
| (10) | Section 2 | Adaptive-R graded scale `s_k` | Important because folder 93 found the original draft had oversimplified this rule. |
| (11) | Section 2 | Block-wise NIS covariance inflation | Keep degrees of freedom and thresholds in prose immediately after the equation. |
| (12) | Section 4 | Carrier-dependent interference phase | Mechanism core. Must remain visible in the final manuscript. |
| (13) | Section 4 | Static fixed-carrier condition | Can be combined with Eq. (14) in one aligned block. |
| (14) | Section 4 | Fixed-carrier locked phase | Mechanism explanation. |
| (15) | Section 4 | Agile carrier set | Can be combined with Eq. (16). |
| (16) | Section 4 | Agile carrier phase variation | Mechanism explanation. |
| (17) | Section 4 | Motion-varying path difference | Boundary explanation for moving targets. |
| (18) | Section 4 | Motion-induced fixed-carrier phase variation | Supports self-whitening interpretation. |
| (19) | Section 5 | Fixed 32 kHz baseline | Could be inline if equation count must be reduced. |
| (20) | Section 5 | 30--34 kHz agile policy | Could be inline if equation count must be reduced. |
| (21) | Section 6 | Settled RMSE | Performance metric; keep as display. |
| (22) | Section 7 | Elevation residual | Mechanism metric; can be inline. |
| (23) | Section 7 | Lag-1 residual correlation | Mechanism evidence; keep as display. |

## Compression option

If a target journal has a strict page limit, the equation count can be reduced without changing meaning:

- Combine Eqs. (1)--(4) into a compact signal-model block.
- Combine Eqs. (5)--(6) into one DOA block.
- Inline Eqs. (9), (19), (20), and (22).
- Keep Eqs. (10)--(12), (21), and (23) as display equations because they are most important for reproducibility and novelty framing.

## Notation caution

The clean source currently follows the project-code convention where `x_k` can refer to both the state vector and the Cartesian coordinate in one displayed state vector. During final typesetting, consider renaming the full state to `\mathbf{x}_k` and the coordinate to `x_{p,k}` or simply keep the vector bolded to avoid reviewer confusion.
