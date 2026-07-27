# 169. Korean discussion and conclusion tightening

## Purpose

This pass stabilizes the Discussion and Conclusion of the local Korean manuscript:

`paper/manuscript_ko.tex`

The goal is to keep the same claim boundary established in folders 166--168:
static and very-slow quasi-static benefit may be claimed, while moving-target
RMSE improvement and real-water performance must not be claimed.

## What changed in the local paper

- The Discussion no longer says carrier-agile pinging bypasses the whole
  long-range error floor. It now says the method targets the carrier-locked
  component of the floor.
- The mechanism is framed as reducing temporal correlation in the observation
  residuals, not as fully removing multipath bias.
- Results from folders 160--162 are explicitly placed under limitations and
  future work, not under headline performance claims.
- The Discussion now states that tank or real-water validation remains open.
- The Conclusion now avoids saying that post-gating coherent multipath DOA bias
  is the sole cause of the long-range floor.
- The final conclusion is narrowed to a verified observation-design claim:
  carrier agility reduces temporal correlation of carrier-locked coherent
  multipath DOA bias under static and very-slow shallow-water USBL conditions.

## Claim boundary preserved

- Static 600 m headline result remains:
  fixed 13.01 m -> agile 8.87 m, paired improvement 4.14 m, p = 0.0008.
- Moving target claim remains limited to residual whitening.
  No pooled RMSE gain is claimed.
- Quasi-static claim remains limited to very slow drift up to 0.005 m/s.
- Sparse, four-carrier, and TOA-guard experiments from folders 160--162 are not
  promoted to manuscript performance claims.
- No real-water performance claim is made.

## Repository rule

The paper itself is local-only. The edited file is under `paper/`, which must
not be staged or pushed. This folder records only the process summary and
claim-safety judgment.

## Next recommended step

Folder 170 should be:

`170. Korean manuscript v3 integration audit`

That step should check the abstract, introduction, methods, results, discussion,
conclusion, tables, and captions against one shared claim boundary before the
later English IEEE manuscript port.
