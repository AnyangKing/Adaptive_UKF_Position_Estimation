# 196. IEEE structure and length pass after moving update

## Purpose

Check the English IEEE-format manuscript after the 191 moving validation was integrated into the claim structure and figures.

## Local manuscript checked

- `paper/manuscript.tex`
- output: `paper/manuscript.pdf`

`paper/` remains local-only and is not committed.

## Result

The manuscript builds successfully in IEEEtran format.

- PDF pages: 13
- Fatal LaTeX errors: 0
- Overfull boxes: 0 found in final log scan
- Hyperref warnings after heading cleanup: 0 found in final log scan
- Remaining warnings: 3 underfull vbox messages, caused by float/page balancing; acceptable for current draft

## Structural judgment

The current section flow is coherent for an IEEE-style journal draft:

1. Introduction
2. Related Work and Problem Statement
3. System Model and UKF Fusion
4. Baseline Tracking Performance
5. Proposed Carrier-Agile Temporal Decorrelation Method
6. Experimental Validation and Applicability Boundary
7. Discussion
8. Conclusion

The structure now supports the “failure to narrowed success” story:

- baseline filtering alone is insufficient;
- static carrier-agility validates the mechanism;
- plain hopping fails as a moving-target performance claim;
- transition-aware Adaptive-R recovers moving-tail risk in 0--1000 m simulation;
- limitations remain explicit.

