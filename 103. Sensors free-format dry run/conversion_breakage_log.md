# Conversion breakage log

This log records what is likely to break when the current Markdown manuscript is converted into a Sensors-style Word or LaTeX submission.

## High-risk conversion items

| Item | Why it may break | Proposed fix |
|---|---|---|
| Markdown tables | Table 1 and Table 2 are wide and dense | Convert to native Word/LaTeX tables; split Table 2 if needed. |
| Fenced math blocks | Journal templates require editable equations | Convert 23 math blocks using folder-100 equation numbering plan. |
| Figure File Manifest | Internal packaging metadata should not be in final article body | Move manifest to submission checklist; keep figure captions in article. |
| Fig. 1 path | Fig. 1 now lives in folder 101, not folder 95 | Final package should collect Fig.1--6 into one submission asset folder. |
| Back matter placeholders | Human metadata is missing | Fill author contributions, funding, data availability, acknowledgments, conflicts. |
| References | Metadata exists but style is not final | Convert to journal reference style after target is chosen. |
| Abstract length | Dry-run count is about 205 words, while Sensors suggests about 200 words | Tighten by 5--20 words during English polishing. |

## Scientific overclaim checks

Keep these unchanged during conversion:

- Do not claim first frequency-hopping USBL.
- Do not claim moving-target RMSE improvement.
- Do not claim continuous quasi-static validation beyond 0.005 m/s.
- Do not claim sub-meter 600 m accuracy.
- Keep static 600 m as the main positive performance result.

## Dry-run conclusion

The next practical task is not new simulation. It is packaging and conversion hygiene: equations, tables, figures, references, and back matter.
