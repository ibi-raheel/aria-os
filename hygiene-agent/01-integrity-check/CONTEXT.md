# 01-integrity-check — Daily integrity sweep

Pointer file. The checks themselves and the auto-fix policy live in `../_config/checks.md`. The runtime flow lives in `../../.claude/commands/integrity-check.md`. This file exists so the stage folder isn't empty.

## What this stage does

Daily at 22:00 weekdays: validate the day's writes against canonical rules and write a per-day report to `../integrity/<date>.md`.

## Rules to run

See `../_config/checks.md` § "Hard fails" + sample-based soft warnings. Auto-fix per the per-rule `auto-fix:` tag.

## Output

`../integrity/<date>.md` — clean (one line) or broken (structured findings + repair recs). Plus a one-line summary appended to `../../logs/daily/<date>.md`.
