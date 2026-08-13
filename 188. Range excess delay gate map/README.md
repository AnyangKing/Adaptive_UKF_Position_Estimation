# Range--excess-delay--gate map

## Purpose

The review asked for an explicit distance--excess-delay--gate relation. This folder computes a compact physics table that connects:

- horizontal range,
- direct-path travel time,
- surface-reflection excess delay,
- bottom-reflection excess delay,
- the 5 ms DOA processing gate,
- observed diagnostic carrier-agility gain from folder 184.

This is not a new localization benchmark. It is a mechanism-interpretation aid.

## Representative geometry

- sound speed: 1500 m/s
- water depth: 100 m
- receiver depth: 30 m
- representative source depth: 40 m
- DOA gate: 5 ms after direct-path arrival

The source depth of 40 m is chosen as a central representative value inside the static validation depth range used by the project. The actual simulation randomizes depth, so this table should be read as a mechanism map, not a complete per-trial truth table.

## Manuscript claim boundary

Allowed:

> In representative shallow-water geometry, surface-reflection excess delay falls from well outside the 5 ms gate at short horizontal ranges to inside the gate at long ranges, matching the observed emergence of larger carrier-agile gains beyond about 600 m.

Forbidden:

> Every geometry at every depth crosses the gate exactly at the same range.

