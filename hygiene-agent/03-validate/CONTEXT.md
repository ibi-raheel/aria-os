# 03-validate — Write-time validation

Pointer file. The auto-fix policy and per-rule `auto-fix:` tags live in `../_config/checks.md`. The runtime flow lives in `../../.claude/commands/validate-writes.md`.

## What this stage does

On-demand validation called by other agents at write-time. For each newly-written file, run the same checks `/integrity-check` runs daily, but inline at write-time so the originating agent can repair before committing.

## Auto-fix policy

Each rule in `../_config/checks.md` carries an `auto-fix: yes|no` tag. `yes` = validator repairs inline (idempotent, reversible). `no` = validator reports + originating agent decides.

## Output

Validation report at `../integrity/_runs/validate-<YYYY-MM-DD>T<HH-MM-SS>.md`. Auto-fixes are applied to the in-flight file before the originating agent's write completes.
