# Manuscript insertion plan

## Section 2 insertion

Target file:

- `85. Manuscript draft v0/manuscript_draft_v0.md`

Target section:

- `## 2. System and Signal Model`

Insert after first paragraph:

- coordinate and array notation
- range definition

Insert after current observation vector explanation:

- full observation vector equation
- TOA/TDOA equations
- azimuth/elevation equations

Insert before adaptive-R paragraph:

- state vector
- constant-velocity transition
- process covariance

## Section 2.4 insertion

Add conditional adaptive-R equation:

```math
R_k = R_0 if g_k <= tau, otherwise R_inflated
```

Explain that this is a backbone, not the novelty.

## Section 4 insertion

Target section:

- `## 4. Carrier-Sensitive Coherent Interference Mechanism`

Insert:

- `phi(f, delta) = 2*pi*f*delta + theta_r`
- fixed static condition
- carrier-agile condition
- moving self-whitening condition

## Section 5 insertion

Target section:

- `## 5. Frequency-Agile Whitening Method`

Insert:

- fixed baseline `f_k = 32 kHz`
- agile schedule `f_k in [30,34] kHz`
- frozen 20-ping linear sweep statement

## Section 6/7 insertion

Add settled RMSE definition before reporting results.

Add lag-1 residual correlation definition before reporting whitening result.

## Style note

If target journal is IEEE, convert all display math to LaTeX numbered equations. If target journal is Ocean Engineering / Applied Acoustics, fewer numbered equations and more prose may be preferable.
