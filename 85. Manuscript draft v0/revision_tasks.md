# Revision tasks from v0 to v1

## 1. Citation audit

Must replace placeholders:

- `[RADAR_FREQ_AGILITY_REF]`
- `[FH_USBL_REF]`
- `[COSTAS_USBL_REF]`
- `[FREQ_COMB_REF]`

Required checks:

1. Exact title, authors, venue, year, DOI.
2. Whether the cited work is actually about USBL, inverted USBL, modem positioning, or sonar diversity.
3. Whether it uses frequency hopping as waveform coding, time-delay precision, baseline optimization, or DOA-bias whitening.

## 2. Figure integration

Need to map figure numbers consistently:

- Fig. 1: system/mechanism concept
- Fig. 2: bias vs carrier
- Fig. 3: static 600 m validation
- Fig. 4: moving residual whitening
- Fig. 5: quasi-static boundary
- Fig. 6: CRLB/floor
- Fig. 7 or Table 1: related-work differentiation

## 3. Method detail expansion

Section 2 and 5 need more exact formulas:

- observation model `h(x)`
- TOA/TDOA definitions
- DOA azimuth/elevation definitions
- UKF process model and covariance summary
- adaptive-R routing rule
- carrier schedule notation

## 4. Results precision check

Before v1, verify all numerical values from source JSON/README:

- 61 static validation
- 63 moving validation
- 82 quasi-static boundary
- 45/79 CRLB/floor

## 5. Tone and target journal

Choose between two styles:

- IEEE/Oceanic Engineering style: concise, method/results heavy.
- Ocean Engineering / Applied Acoustics style: more narrative mechanism explanation.

Current v0 is closer to Ocean Engineering / Applied Acoustics. It can be tightened for IEEE later.

## 6. Claims to keep bounded

Do not expand beyond:

- static long-range validation
- very slow drift up to 0.005 m/s
- moving residual whitening without reliable RMSE gain

Avoid:

- general moving-target localization improvement
- sub-meter long-range claim
- first frequency-hopping USBL claim

## 7. Missing experiments?

No new experiment is required before v1, unless the user/professor asks for:

- real-water/tank validation
- exact carrier schedule ablation
- radial tail guard
- array aperture scaling

For current manuscript assembly, exact citations are more urgent than new simulations.
