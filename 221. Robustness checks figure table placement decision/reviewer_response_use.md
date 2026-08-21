# Reviewer-response use of 215/216

## Likely reviewer challenge: hardware response

Possible challenge:

> Frequency hopping assumes the transducer/receiver response is flat over 30--34 kHz.

Prepared response:

> We agree that measured hardware calibration is required before field deployment. To test whether the reported simulation result depends solely on a perfectly flat response, we added an idealized sensitivity study with 3 and 6 dB band-edge effective-SNR loss. The transition-aware soft-R result remained essentially unchanged, but we explicitly report this as simulation sensitivity, not measured hardware validation.

## Likely reviewer challenge: arbitrary moving targets

Possible challenge:

> The moving result may be tuned to the selected trajectories.

Prepared response:

> We therefore added an extended OOD-family check with stop--go, direction reversal, spiral climb, and burst-turn trajectories. The transition-aware soft-R protocol retained the lowest mean RMSE in this additional stress set. We still do not claim arbitrary-motion robustness; the result is presented as additional OOD-family evidence.

## Manuscript-use rule

Use 215/216 as defense and supplement. Do not let them replace the primary evidence chain: 191 structured moving validation and 204 OOD validation.
