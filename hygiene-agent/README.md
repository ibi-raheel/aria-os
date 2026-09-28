# hygiene-agent

Vault-maintenance agent for the Aria Agent OS. Two scheduled jobs that keep the system internally consistent over time so the architecture doesn't rot.

## Quick start

Read today's integrity report:
```bash
cat "Aria Agent OS/hygiene-agent/integrity/$(date +%Y-%m-%d).md"
```

Or get a 7-day rollup:
```bash
ls -lt "Aria Agent OS/hygiene-agent/integrity/" | head -10
```

## What it does

**Daily 22:00 — `/integrity-check`** (weekdays). Sweeps today's writes from news-agent, networking-agent, outreach-agent-arcadia. Validates:
- Engagement record dossier_refs resolve
- Dossier `## Engagements` table rows point at real engagement files
- News anchors cited at stage 03 trace back to briefing items with source URLs
- Send claims have matching daily-log entries
- No new orphan nodes from today

Output: `hygiene-agent/integrity/<date>.md` — clean = one line, broken = specific files + repair recommendations.

**Weekly Sunday 22:00 — `/memory-consolidate`**. Heavier sweep:
- Regenerate `memory/_INDEX.md`
- Apply retention rules (archive >90d briefings, delete >14d intermediates, archive >180d daily logs)
- Mark dormant people (no engagement update in 90d → `status: dormant`)
- Sweep orphan nodes
- Cross-check dossier facts vs briefings (flag conflicts, don't auto-rewrite)

Output: `hygiene-agent/integrity/weekly-<YYYY-WW>.md`.

## What it does NOT do

- Not auto-repair. Reports + recommends. Humans or originating agents fix.
- Not modify dossier identity content.
- Not rewrite engagement records or daily logs.
- Not run during outreach windows.

## Folder layout

```
hygiene-agent/
├── CLAUDE.md              ← agent identity + rules
├── README.md              ← this file
├── _config/
│   └── checks.md          ← validation rules, thresholds
├── 01-integrity-check/
│   └── CONTEXT.md
├── 02-consolidate/
│   └── CONTEXT.md
└── output/                ← per-run intermediates (rare)
```

Reports live at `hygiene-agent/integrity/`, not inside this agent's folder. They're vault-wide artifacts.

## Activation

Three steps (similar to news-agent and networking-agent):

1. Move `cowork/2026-04-29/hygiene-slash-commands.md` sections into `.claude/commands/`:
   - `.claude/commands/integrity-check.md`
   - `.claude/commands/memory-consolidate.md`
   - `.claude/commands/hygiene-status.md`

2. Register two scheduled tasks via Cowork's `create_scheduled_task`:
   - "integrity-check daily" — `0 22 * * 1-5` — `/integrity-check`
   - "memory-consolidate weekly" — `0 22 * * 0` — `/memory-consolidate`

3. Manual test:
   ```
   /integrity-check
   /hygiene-status
   ```

## Status

- [x] Scaffolded 2026-04-29
- [ ] Slash commands moved to `.claude/commands/`
- [ ] Scheduled tasks registered
- [ ] First daily integrity check run
- [ ] First weekly consolidate run
