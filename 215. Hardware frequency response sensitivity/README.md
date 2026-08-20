# 215. Hardware frequency response sensitivity

## Purpose

This folder tests one computer-checkable weakness left by the current manuscript:

> Carrier hopping was validated in the simulator, but real transducers and receivers may not have a flat response over 30--34 kHz.

This is not a real hardware validation. It is a sensitivity simulation that applies carrier-dependent effective SNR changes during signal synthesis.

## What was tested

The frozen 191 moving full-range protocol was reused:

- distances: 0, 200, 400, 600, 800, 1000 m;
- motion conditions: the four 191 structured moving conditions;
- seeds: 8 per distance/condition;
- policies: fixed carrier, plain hopping, transition-aware soft-R;
- signal-level TOA/TDOA/DOA extraction and the same UKF/update logic as 191.

Three response profiles were added:

- `flat_reference`: no carrier-dependent penalty;
- `edge_loss_3db`: 30 and 34 kHz suffer up to 3 dB loss relative to 32 kHz;
- `edge_loss_6db`: 30 and 34 kHz suffer up to 6 dB loss relative to 32 kHz.

## Files

- `run_hardware_response_sensitivity.py` -- executable validation script.
- `test_hardware_response_sensitivity.py` -- smoke tests for response profiles and case enumeration.
- `hardware_response_sensitivity.json` -- result payload.
- `result_summary.md` -- human-readable summary.

## Claim boundary

This folder can support only the following wording:

> Under idealized carrier-dependent response penalties up to the tested profile, the transition-aware soft-R protocol remained robust in the current signal-level simulator.

It cannot support:

- real transducer response validation;
- hydrophone calibration claims;
- arbitrary frequency-response robustness;
- real-water USBL performance.
