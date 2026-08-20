# 214. Layout references captions final QA

## Purpose

Final paper-facing QA after folders 211--213.

This pass checks build reproducibility, unresolved references/citations, figure/caption availability, and claim-boundary risk. It does not add new experiments or new manuscript claims.

## Files

- `latex_build_qa.md` -- English/Korean build status and log warning summary.
- `caption_claim_boundary_check.md` -- check that figure/table captions remain within supported evidence.
- `next_weakness_watchlist.md` -- remaining items that can become real weaknesses before submission.

## Decision

The current manuscript state is buildable and internally synchronized at the paper-draft level. Remaining issues are submission-stage decisions or non-blocking typography warnings.
