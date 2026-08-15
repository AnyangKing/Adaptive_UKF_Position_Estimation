# 203. Overnight OOD validation runner

## Purpose

Folder 202 showed a small first-pass OOD motion probe. This folder turns that probe into a checkpoint/resume validation runner that can be left running for a long time.

The goal is not to introduce a new algorithm. The goal is to make large OOD validation practical and safe:

- save every completed case immediately,
- skip completed cases on resume,
- aggregate partial or complete runs,
- keep the same signal-level TOA/TDOA/DOA extraction and transition-aware Adaptive-R rule used in folders 191 and 202.

## Files

- `overnight_ood_config.json`: default large-run configuration.
- `run_overnight_ood_validation.py`: checkpoint/resume case runner.
- `aggregate_overnight_ood_results.py`: aggregates per-case JSON files into summary JSON/Markdown.
- `checkpoint_format.md`: explains the saved case/result format.
- `test_overnight_runner.py`: smoke checks for config parsing and case enumeration.

## Typical use

Run the long validation:

```bash
python "203. Overnight OOD validation runner/run_overnight_ood_validation.py" --config "203. Overnight OOD validation runner/overnight_ood_config.json"
```

Resume after interruption:

```bash
python "203. Overnight OOD validation runner/run_overnight_ood_validation.py" --config "203. Overnight OOD validation runner/overnight_ood_config.json" --resume
```

Aggregate current results:

```bash
python "203. Overnight OOD validation runner/aggregate_overnight_ood_results.py" --config "203. Overnight OOD validation runner/overnight_ood_config.json"
```

Quick smoke run:

```bash
python "203. Overnight OOD validation runner/run_overnight_ood_validation.py" --config "203. Overnight OOD validation runner/overnight_ood_config.json" --max-cases 1 --overwrite
```

## Claim boundary

This folder is infrastructure. It does not by itself add a manuscript result until a sufficiently large run is completed and aggregated.

## Smoke verification

Verified in this folder:

- default config enumerates 528 cases,
- `--max-cases 1 --overwrite` writes one checkpoint JSON successfully,
- aggregator can summarize a partial one-case checkpoint set,
- smoke-generated result files were deleted so they are not mistaken for validation results.
