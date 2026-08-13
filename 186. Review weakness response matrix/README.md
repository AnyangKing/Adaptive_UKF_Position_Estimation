# Review weakness response matrix

## Purpose

This folder converts the external review into an engineering checklist. It separates:

1. weaknesses already corrected in the local manuscript,
2. weaknesses that can be tested immediately in the current simulator,
3. weaknesses that must remain as limitations until a higher-fidelity channel model or real-water data are available.

The goal is not to make the paper look stronger by wording. The goal is to keep every claim tied to an experiment that the current code actually ran.

## Current manuscript direction

The project did **not** remain a generic "TOA/TDOA/DOA + UKF" paper. That baseline already exists in the literature and is too ordinary for a strong IEEE-style contribution.

The current direction is:

> A small-aperture USBL localization pipeline that extracts TOA, seven reference TDOAs, and one array-level DOA from received acoustic signals, feeds them into a causal UKF/Adaptive-UKF estimator, and studies how carrier scheduling changes the temporal structure of coherent DOA bias in shallow-water long-range conditions.

The strongest validated line is currently:

- fixed-carrier and carrier-agile schedules are compared with the same trajectory/channel/noise seeds;
- static and quasi-static shallow-water long-range cases show reproducible carrier-agility benefit;
- ordinary moving-target frequency agility failed to generalize;
- a transition-aware Adaptive-R moving-target variant was independently validated at 600 m in folder 181;
- extended static range checks in folders 182--184 show useful long-range behavior up to 1000 m, but not uniform benefit at all ranges;
- folder 185 shows that a pure "multipath-only" explanation is too strong because direct-only 1000 m still showed a carrier-dependent gain.

## Response matrix

| review weakness | status after response | action taken / required |
|---|---|---|
| CRLB was interpreted as an irreducible systematic-bias floor | corrected locally | Manuscript wording changed to "CRLB-excess reference"; no formal bias decomposition is claimed. |
| "Whitening" was too strong from lag-1 only | corrected locally | Manuscript wording changed to temporal decorrelation / reduction of positive lag-1 / phase diversification. Multi-lag whiteness is not claimed. |
| ΔFδ≥1 was treated too deterministically | corrected locally | Reframed as a finite-schedule phase-coverage heuristic, not a sufficient theorem. Carrier-span/order ablation remains desirable. |
| Channel is too favorable compared with real sea | partially addressed | Current simulator has direct/surface/bottom paths, sensor noise, sound-speed error, sensor mismatch metadata. Rough surface, 3-D ray model, transducer response, and real water data remain limitations. |
| Signal equation did not match implementation | corrected locally | Manuscript now avoids implying a complex-baseband-only implementation where the code uses a real passband chirp pipeline. |
| Adaptive-R thresholds/caps are heuristic | partially addressed | Threshold provenance and routing behavior are documented. Sensitivity ablation is still a useful next experiment. |
| Consistency wording too strong with high NEES | corrected locally | Consistency language is bounded; NEES results are treated as partial inconsistency, not full statistical calibration. |
| Static validation n=20 is small for final claim | partially addressed | Existing independent validations are documented, but a final larger grid over distance/SNR/reflection/seed is still needed before submission. |
| Fixed vs agile may change more than multipath phase | actively addressed | Folder 185 ran direct-only control and found residual carrier effects at 1000 m, weakening pure attribution. Folder 187 should remove noise too. |
| Need distance--excess-delay--gate map | pending immediate | A compact physics table should be generated from the 5 ms gate and representative depths. |
| Schedule selection / development split clarity | corrected in audit docs | Development, validation, and final-test boundaries are documented. Any post-test threshold change must demote that test to development. |
| Need real-water or high-fidelity independent model for JOE-level confidence | not yet satisfied | Cannot be solved by wording. This is a future validation requirement. |

## What the current 600 m and 1000 m story actually means

The user's summary is close, but needs one important correction.

- Earlier validated work focused on 600 m because that range came from the previous project lineage and the coherent-bias problem was visible there.
- Carrier hopping / carrier agility improved static and quasi-static long-range behavior in repeated simulations.
- Folder 181 found a newer transition-aware Adaptive-R method that made moving-target results much better at 600 m, but with a known fixed-baseline tail-risk caveat.
- Folders 182--184 extended static/diagnostic carrier-agility checks to 800 m, 1000 m, and then 0--1000 m in 100 m steps.
- Therefore the current result is **not** simply "frequency hopping solved everything up to 1000 m." It is:

> Carrier agility is promising for long-range static/quasi-static conditions and the transition-aware Adaptive-R variant is promising for moving targets at 600 m, but the mechanism and operating envelope still need tighter controls before the manuscript can claim practical generality.

## Immediate next experiments

1. No-noise direct-path-only carrier control: if 1000 m gain remains with no multipath and no noise, the gain is not mainly noise or multipath.
2. Distance--excess-delay--gate map: show where reflected paths can physically fall inside the 5 ms measurement gate.
3. Carrier schedule ablation: vary carrier count, span, and order using paired seeds.
4. Adaptive-R sensitivity: test routing threshold/cap choices on development seeds, then freeze and validate independently.

