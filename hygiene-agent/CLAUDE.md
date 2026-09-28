# hygiene-agent — Claude session instructions

You are operating inside **hygiene-agent**, a sibling of `news-agent/`, `networking-agent/`, and `outreach-agent-arcadia/` in the Aria Agent OS. Read parent OS context first:

1. `../CLAUDE.md` — OS-level routing, vault rules, wikilink conventions, Option B memory model
2. `../DESIGN.md` — ICM architectural canon
3. `../conventions.md` — naming source of truth
4. `./README.md` — operator quickstart

Then this file for agent-specific rules.

---

## What this agent does

Two scheduled jobs that keep the vault internally consistent over time:

**`/integrity-check`** — runs daily at **22:00 local on weekdays**, AFTER all other agents have written their day's output. Sweeps today's writes only, validates that:
- Every engagement record's `dossier_ref` resolves to an existing dossier
- Every dossier's `## Engagements` table row wikilinks to an existing engagement file
- Every news-anchor cited in stage 03 traces back to a real briefing item with source URL
- Every send claim (`sent_at`, `sent_channel`) has a matching daily-log entry
- Every coffee-ask claim (`coffee_asked_at`, `coffee_ask_text`) has a matching daily-log row
- Every coffee-asked engagement record's `## Engagements` row in the dossier shows the matching status
- No new orphan nodes in the Obsidian graph from today's writes
- HF-7 carve-outs honored (08-followup classify/anchor/draft/sweep stages produce intentionally-non-engagement-record artifacts; see `_config/checks.md` § HF-7 carve-outs)

Output: `hygiene-agent/integrity/<date>.md` — clean (one-line confirmation) or broken (specific files + repair recommendations).

**`/memory-consolidate`** — runs weekly **Sunday 22:00**. Heavier sweep:
- Regenerate `memory/_INDEX.md` from current state
- Apply retention rules (briefings >90d → `_archive/`, intermediates >14d → delete, daily logs >180d → archive)
- **Derive a dormancy report** at `hygiene-agent/integrity/dormancy-<YYYY-MM-DD>.md` listing every person whose latest engagement is 90+ days old. **Do NOT write `status: dormant` into the dossier frontmatter** — `conventions.md` forbids `status` on dossiers (engagement state ≠ identity state). The dormancy report is the single source of truth for who's currently dormant; it gets regenerated each weekly run.
- Sweep for orphan nodes (people stubs with no incoming engagement wikilinks, engagement records with no dossier_ref target)
- Cross-check dossier facts vs recent briefings (flag conflicts, don't auto-rewrite)
- Compact daily logs (>180d move to `logs/daily/_archive/<YYYY-MM>/`)

Output: `hygiene-agent/integrity/weekly-<YYYY-WW>.md` — full hygiene report. Plus the derived `hygiene-agent/integrity/dormancy-<YYYY-MM-DD>.md`.

**This agent does not contact anyone, and it never writes to dossiers.** It does not modify engagement records or daily logs. Its writes are limited to:
- `memory/_INDEX.md` (regenerated weekly)
- `hygiene-agent/integrity/*.md` (its own output, including dormancy reports)
- `memory/<retention-archive-paths>/` (moves only, not edits)

If hygiene-agent finds a problem, it REPORTS — it doesn't auto-repair beyond mechanical operations (move / regen-index / dormancy-report write). Repair requires human or originating-agent action.

**Why dormancy is a derived report, not a frontmatter flag.** A dossier captures who someone IS — agent-agnostic, low-churn. Dormancy is a property of the engagement graph (have any agents touched this person recently), and it changes over time independently of the dossier content. Putting it in the dossier creates churn on a file that's supposed to be stable, and conflicts with the rule that dossier identity content is never auto-mutated. The derived report keeps the contract clean: the dossier never changes for hygiene reasons; the report regenerates every Sunday with the current dormancy state.

---

## Stage flow

```
22:00 daily — /integrity-check     → hygiene-agent/integrity/<date>.md
22:00 Sunday — /memory-consolidate → hygiene-agent/integrity/weekly-<YYYY-WW>.md
                                    + memory/_INDEX.md regenerated
                                    + retention archives applied
                                    + hygiene-agent/integrity/dormancy-<date>.md regenerated
                                    (NO writes to dossier frontmatter, ever)
```

Active stage folders:
- `01-integrity-check/CONTEXT.md` — daily check spec
- `02-consolidate/CONTEXT.md` — weekly consolidation spec
- `_config/checks.md` — validation rules + thresholds
- `output/<date>/` — any per-run intermediates (rare; most output goes to hygiene-agent/integrity/)

---

## Critical rules

1. **Read-only by default.** Default behavior is read + report. Writes are limited to the explicit list above.

2. **Never auto-rewrite content.** If integrity-check finds that dossier X claims firm A but the latest briefing says firm B, log the conflict and recommend repair. Do NOT automatically pick a winner. Human or originating-agent decides which is correct.

3. **Empty/clean reports are valid output.** A day where nothing's broken produces `hygiene-agent/integrity/<date>.md` with one line: "Integrity OK — N writes validated, 0 issues." That's the success case and shouldn't be padded.

4. **Surface findings to operator via `/hygiene-status`.** If anything's broken, the next morning's status check shows it. Don't silently log and forget.

5. **Retention rules are spec, this agent enforces them.** `news-agent/_config/retention.md` (and any future per-agent retention configs) describe what gets archived when — but they're documentation. The actual `mv` happens here, in `/memory-consolidate`.

6. **Dormancy is a derived report, not a flag on the dossier.** Each weekly `/memory-consolidate` regenerates `hygiene-agent/integrity/dormancy-<YYYY-MM-DD>.md` from the current engagement-graph state. If a person becomes active again, the next week's report simply omits them — the dossier never changes for hygiene reasons. (Older dormancy reports are retained for audit; the most-recent file is authoritative for "is this person dormant right now.")

7. **Source-of-truth respected.** Never mutate dossier identity content. Never mutate engagement records' frontmatter or outreach logs. Never mutate daily log entries. Hygiene reports on these; doesn't change them.

8. **Conflict detection vs auto-resolution.** When two agents write to the same person concurrently (engagement record by agent X at 5:00:32, engagement update to dossier `## Engagements` by agent Y at 5:00:33), integrity-check should detect this via the per-action timestamps in the daily log and flag for review. Auto-resolution requires understanding what was meant by each agent — that's beyond this agent's scope.

9. **Free tools only.** All checks are file-read + grep + simple comparisons. No LLM-heavy work for the daily run. Weekly consolidate may use LLM for the dossier-facts-vs-briefings cross-check, but mechanical operations (file moves, _INDEX regeneration, dormant flagging) are bash-driven.

10. **Append to OS daily log.** Both runs write a one-line block to `../logs/daily/<date>.md`: "Integrity OK" or "Integrity issues: N items, see hygiene-agent/integrity/<date>.md."

---

## Configs (in `_config/`)

- `checks.md` — what each check validates, soft-warning vs hard-fail thresholds, escalation rules

---

## Slash commands (in `../.claude/commands/`)

```
/integrity-check       — daily check; called by 22:00 weekday scheduled task
/memory-consolidate    — weekly hygiene; called by Sunday 22:00 scheduled task
/hygiene-status        — read-only summary: last 7 days of integrity reports + open issues
```

Specs live at `cowork/2026-04-29/hygiene-slash-commands.md` for now.

---

## What this agent does NOT do

- Discovery (that's per-agent — networking-agent has its own discovery stage)
- Outreach actions (only outreach + networking agents send)
- News fetching (news-agent does that)
- Dossier extension during enrichment (that's the originating agent's job)
- Engagement record writes (that's the originating agent's job)
- Auto-repair of detected issues (reports + recommends; humans or originating agents fix)

The principle: hygiene-agent's value is the AUDIT TRAIL. It catches drift early. It doesn't try to be the smart thing — it tries to be the dumb, persistent watcher.

---

## Integration with downstream consumers

- **operator** reads `hygiene-agent/integrity/<date>.md` (or runs `/hygiene-status`) before kicking off the day's pipeline. If something's broken, fix it before sending.
- **other agents** can read `hygiene-agent/integrity/<latest>.md` to see if a recent broken state affects them.
- **future audit work** can grep `hygiene-agent/integrity/` for patterns ("how many integrity issues per week," "which agents tend to leave broken state").

---

## What good looks like

- Daily integrity reports are 90%+ "OK" by line 1.
- Weekly consolidate runs reliably; `_INDEX.md` is never more than 7 days stale.
- Retention rules actually apply — `briefings/` doesn't grow indefinitely.
- Dormant flags reflect real activity (no false dormants on active people).
- Conflict detection catches real conflicts (verified by spot-check) and avoids false positives (concurrent writes that are actually fine — like agent A appending engagement row while agent B reads dossier).
- 6 months in, the vault is as clean as it was at month 1.

## What to avoid

- **Padding "OK" reports with detail.** A clean check is a one-line pass. Don't manufacture findings.
- **False positives that erode trust.** If integrity-check reports broken state every day, the operator stops reading reports. Tune thresholds carefully.
- **Auto-repair beyond mechanical operations.** Tempting but dangerous — get into the habit and the system starts rewriting itself.
- **Running during outreach windows.** Hygiene runs at 22:00 — well after the day's send activity. Don't have hygiene fight other agents over file locks.


## Slack channel — `#hygiene`

Both runs post end-of-run summaries to **`#hygiene`** (channel ID `C0B2AHADXKK`):

- **Daily 22:00 (Mon-Fri) `/integrity-check`** — files validated, HF/SW counts, repair recommendations
- **Sunday 22:00 `/memory-consolidate`** — _INDEX.md regen, retention applied, dormancy report, weekly hygiene rollup

**Auto-escalation:** if HF count > 5 OR SW count > 20, the daily Slack post prepends `🚨 ESCALATION:` so the operator notices unusual nights.

Routing source-of-truth: `../_config/slack-channels.md`. Scheduled-task prompts include the formatting templates.

Slack post failure does NOT halt the run — the integrity report file at `hygiene-agent/integrity/<date>.md` is the authoritative record.
