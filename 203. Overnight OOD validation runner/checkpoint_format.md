# Checkpoint format

## Per-case file

Each completed case is written as one JSON file:

```text
overnight_results/d0800_curved_arc_i003.json
```

The file contains:

```json
{
  "case_id": "d0800_curved_arc_i003",
  "case": {
    "distance_m": 800.0,
    "condition_index": 1,
    "condition": "curved_arc",
    "mode": "curved_arc",
    "index": 3
  },
  "rows": [
    {"policy": "fixed_baseline", "...": "..."},
    {"policy": "hop_baseline", "...": "..."},
    {"policy": "hop_transition_softR", "...": "..."}
  ],
  "runtime_s": 19.4,
  "config_snapshot": {
    "geometry_seed_root": 2020000,
    "ping_seed_root": 2023000,
    "truth_usage": "...",
    "claim_boundary": "..."
  }
}
```

## Resume behavior

If the per-case JSON file already exists, the runner skips that case by default.

Use `--overwrite` only when intentionally replacing an earlier run.

## Error behavior

If a case fails, the runner writes:

```text
d0800_curved_arc_i003.error.json
```

Successful aggregation ignores `*.error.json` files.

## Why this matters

Long signal-level simulations are too expensive to treat as a single all-or-nothing command. Checkpointing makes it possible to:

- stop and resume runs,
- inspect partial progress,
- aggregate partial results,
- avoid losing hours of completed simulation work.
