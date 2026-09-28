# 02-consolidate — Weekly hygiene + retention

Pointer file. The mechanical operations and retention rules live in `../_config/checks.md` § "Mechanical operations". The runtime flow lives in `../../.claude/commands/memory-consolidate.md`.

## What this stage does

Sundays at 22:00: heavier sweep — re-run all daily checks, apply retention archives, regenerate `memory/_INDEX.md`, derive `../integrity/dormancy-<date>.md`.

## Rules + operations

See `../_config/checks.md` § "Mechanical operations (auto-applied during weekly consolidate)" — MO-1 through MO-7.

## Output

- `../integrity/weekly-<YYYY-WW>.md` — full report
- `../integrity/dormancy-<YYYY-MM-DD>.md` — derived dormancy snapshot
- `../../memory/_INDEX.md` — regenerated
- One-line append to `../../logs/daily/<date>.md`
