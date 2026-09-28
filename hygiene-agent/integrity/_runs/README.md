# hygiene-agent/integrity/_runs — ad-hoc validation artifacts

This folder holds artifacts from ad-hoc `/validate-writes`-style runs. **It is non-canonical.** The canonical hygiene reports live one level up:

- `hygiene-agent/integrity/<YYYY-MM-DD>.md` — the daily integrity-check report
- `hygiene-agent/integrity/weekly-<YYYY-WW>.md` — the weekly memory-consolidate report
- `hygiene-agent/integrity/dormancy-<YYYY-MM-DD>.md` — the weekly dormancy snapshot

Files here are timestamped per-run records of one-off validations the operator ran manually. They are NOT part of the canonical audit trail and may be deleted at any time.

## Naming pattern

`validate-<YYYY-MM-DD>T<HH-MM-SS>.md` or any `validate-*` filename — they all sort by run-time naturally.

## Why this folder exists

Per audit finding #4 (2026-04-30): non-canonical artifacts were polluting `hygiene-agent/integrity/` alongside the canonical reports. This folder gives them a clear, sorted-to-bottom home (the leading `_` puts it after canonical YYYY-MM-DD files in alphabetical sort), preserves their content, and makes the canonical area easy to scan again.
