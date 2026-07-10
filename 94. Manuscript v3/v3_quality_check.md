# v3 quality check

## Automated / command checks

`python "93. Method 세부 코드 대조/test_diagnostic.py"`:

- PASS `test_adaptive_R_rule`
- PASS `test_channel_and_array`
- PASS `test_gate_and_filter`
- PASS `test_protocols`

## Text checks

Searched `manuscript_draft_v3.md` for old or risky wording.

| Check | Result | Note |
|---|---|---|
| `Draft v2` remains | PASS | Header now says Draft v3. |
| Binary `R_inflated` adaptive-R equation remains | PASS | Replaced by two-stage rule. |
| `will show/report/summarize/distinguish/compare` callouts remain | PASS | No future-tense figure/table callouts found. |
| `fig7` remains as active callout | PASS | Only appears in the figure manifest as a legacy filename note. |
| 5 ms gate appears in method and mechanism | PASS | Section 2.1 and Section 4 both mention it. |
| Static n=20 protocol appears | PASS | Section 6 records it. |
| Moving n=64 protocol appears | PASS | Section 7 records it. |
| Quasi-static 132 paired accounting appears | PASS | Section 7 records it. |

## Claim consistency

- Static 600 m improvement remains the main positive performance claim.
- Moving target RMSE improvement is still not claimed.
- Moving whitening remains a mechanism claim.
- Quasi-static use is still conservatively limited to continuous validation up to 0.005 m/s.
- Sub-meter long-range performance is not claimed.
- Frequency hopping itself is not claimed as new.

## Known remaining issues

1. Citation placeholders still need exact references.
2. Fig. 5 still lacks a PNG export in the canonical figure set.
3. Journal equation numbering and reference style are not finalized.
4. The manuscript may still need final compression after target journal selection.

