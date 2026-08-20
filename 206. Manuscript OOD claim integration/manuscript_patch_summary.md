# Manuscript patch summary

## Added OOD evidence

The manuscript now states that 204 tested the transition-aware soft-R protocol on:

- accelerating radial motion,
- curved arc motion,
- mixed radial+tangential motion,
- vertical sine maneuver,
- 0--1000 m in 100 m increments,
- 528 paired cases.

## Numbers inserted

- fixed: mean RMSE 10.832 m, P90 22.339 m, divergence 0.049.
- plain hop: mean RMSE 10.691 m, P90 21.611 m, divergence 0.057.
- transition-aware soft-R: mean RMSE 7.809 m, P90 15.936 m, divergence 0.006.
- soft-R vs hop: +2.881 m, p=9.076e-22.
- soft-R vs fixed: +3.023 m, p=1.015e-18.

## Language tightened

The manuscript separates:

1. plain hopping failure/tail risk,
2. structured moving validation in 191,
3. OOD moving robustness validation in 204,
4. remaining real-water and arbitrary-motion limitations.
