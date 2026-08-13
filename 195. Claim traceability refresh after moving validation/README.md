# 195. Claim traceability refresh after moving validation

## Purpose

Refresh claim-to-evidence mapping after 193--194 changed the manuscript from a static-centered claim to a static + transition-aware moving claim.

## Audit scope

Local-only manuscript files checked:

- `paper/manuscript.tex`
- `paper/manuscript_ko.tex`

Tracked source folders checked:

- 61 static independent validation
- 63--67 earlier moving negative/boundary line
- 82 quasi-static boundary validation
- 177 runtime audit
- 181 transition-aware 600 m moving validation
- 185/187 direct-path controls
- 188 range-excess-delay gate map
- 189 carrier schedule ablation
- 191 moving full-range independent validation

## Result

No fatal claim mismatch found after the 193--194 edits.

The manuscript now correctly separates:

- static positive evidence;
- plain-hopping moving failure;
- transition-aware moving success;
- quasi-static limited boundary;
- simulation-only/real-water limitation.

