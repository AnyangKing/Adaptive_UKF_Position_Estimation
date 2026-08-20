# Claim-to-source map after 204

| claim in paper | source | boundary |
|---|---|---|
| static 600 m carrier-agile schedule reduces RMSE 13.01 to 8.87 m | 61 static validation | static 600 m simulation, not moving or real-water |
| plain hopping decorrelates moving residuals but does not by itself prove moving RMSE gain | 63 moving validation and 64--67 failure series | mechanism/failure boundary only |
| transition-aware soft-R improves structured 0--1000 m moving simulation | 191 independent validation | structured motion simulation only |
| transition-aware soft-R retains OOD aggregate advantage | 204 OOD full validation | OOD family simulation only, not arbitrary motion |
| quasi-static continuous boundary is only 0.005 m/s | 82 quasi-static speed boundary | no broad speed claim |
| two-ray carrier-locked bias mechanism predicts bias-vs-carrier curves | 137--138 theory/overlay | simplified two-ray model, not full ocean model |

## Important wording

Use:

- “simulation-level OOD robustness evidence”
- “transition-aware routing”
- “plain hopping remains tail-prone”

Avoid:

- “real-water validated”
- “arbitrary moving target”
- “frequency hopping solves moving targets”
- “first frequency-hopping USBL”
