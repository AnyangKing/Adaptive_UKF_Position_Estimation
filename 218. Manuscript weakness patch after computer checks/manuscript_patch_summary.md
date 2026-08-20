# Manuscript patch summary

## English manuscript

Local file patched:

```text
paper/manuscript.tex
```

Changes:

1. Added a paragraph after the 204 OOD result explaining:
   - 215 idealized 3/6 dB hardware-response edge-loss sensitivity;
   - 216 stop--go, direction-reversal, spiral-climb, and burst-turn OOD-family validation.
2. Added a practical-costs paragraph clarifying that 215 is only simulation sensitivity and not measured calibration.
3. Updated the limitations table:
   - moving claim now mentions the additional 144-case OOD-family check;
   - added a row for unmeasured hardware frequency response.
4. Updated the conclusion with one sentence summarizing 215/216.
5. Updated Supplementary Material/Data Availability to map 215/216 to supplementary robustness checks.

## Korean manuscript

Local file patched:

```text
paper/manuscript_ko.tex
```

Changes:

1. Added the same 215/216 explanation after the 204 OOD discussion.
2. Added the hardware-response caveat in the discussion.
3. Added one conclusion sentence noting that 215/216 retained the soft-R advantage.

## Claim boundary retained

Allowed wording:

- idealized hardware-response mismatch sensitivity;
- additional OOD-family simulation evidence;
- supplementary robustness check.

Forbidden wording:

- real-water validated;
- measured hardware calibrated;
- arbitrary moving-target guarantee;
- frequency hopping alone solves moving tracking.
