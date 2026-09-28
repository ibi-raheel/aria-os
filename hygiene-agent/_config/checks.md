# Hygiene checks — validation rules + thresholds

What gets validated, what counts as a hard fail vs a soft warning, what each issue should report, **and whether the validator may auto-fix it inline**.

Read by `/integrity-check` (daily), `/memory-consolidate` (weekly), and `/validate-writes` (on-demand, write-time).

**Per-rule `auto-fix:` tag.** Every rule below is tagged `auto-fix: yes` (validator repairs it inline by default) or `auto-fix: no` (validator reports it, originating agent must repair). The tag is the policy source of truth — see `../03-validate/CONTEXT.md` § "Auto-fix policy" for context.

---

## Hard fails (must surface immediately, block-worthy)

### HF-A: Broken wikilink

**Check:** every `[[memory/people/X]]`, `[[memory/companies/X]]`, `[[news-agent/briefings/X]]`, `[[<agent>/<stage>/output/X]]` wikilink in body text must resolve to an existing file. Resolution tries both `<path>` and `<path>.md` (Obsidian doesn't require `.md` extension in wikilinks).
**Fail mode:** target file does not exist after both resolution attempts.
**Report:** `file <path> line <N>: wikilink [[<target>]] does not resolve.`
**Repair:** create the missing target file (stub), OR replace the wikilink with plain-text bold + `(memory/<type>/<slug>.md stub needed)` note.
**auto-fix: yes** — replace the wikilink with `**<display>** (<resolved-target>.md stub needed)` plain-text. Reversible: creating the stub later restores the link.

### HF-1: Broken `dossier_ref` in engagement record

**Check:** every `<agent>/<stage>/output/<slug>.md` file with `dossier_ref:` frontmatter must point at an existing `memory/people/<slug>.md`.
**Fail mode:** the wikilink target doesn't resolve.
**Report:** `engagement record <path> has broken dossier_ref pointing to <target> — dossier missing or renamed.`
**Repair recommendation:** create the dossier from `memory/templates/person.md`, OR fix the slug in the engagement record's frontmatter.
**auto-fix: no** — creating a dossier from scratch requires identity facts the validator doesn't have; fixing the slug requires knowing the correct one. Originating agent must repair.

### HF-2: Engagement row in dossier points at non-existent engagement file

**Check:** every `[[<agent>/<stage>/output/<slug>]]` wikilink in a dossier's `## Engagements` table must point at an existing engagement file.
**Fail mode:** the engagement file is missing.
**Report:** `dossier memory/people/<slug>.md has Engagements row pointing to <target> — engagement file missing or moved.`
**Repair:** restore the engagement file from backup, OR remove the row from the dossier.
**auto-fix: no** — removing a row destroys engagement history; restoration requires knowing whether the file was deleted intentionally. Originating agent decides.

### HF-3: Send claim with no daily-log evidence

**Check:** every engagement record with `sent_at: <timestamp>` and `sent_channel: <channel>` must have a corresponding row in `logs/daily/<date-of-sent_at>.md` mentioning that send.
**Fail mode:** no matching daily-log row found within ±5 min of the sent_at timestamp.
**Report:** `engagement <path> claims sent_at=<ts>, sent_channel=<channel> but no matching row in logs/daily/<date>.md.`
**Repair:** investigate — did the send actually happen? If yes, append the missing row. If no, set `status: skipped` and clear sent_at/sent_channel.
**auto-fix: no** — investigation required. Auto-appending a log row could falsely confirm a send that didn't happen. Originating agent must verify and decide.

### HF-4: News anchor with no source URL or verbatim excerpt

**Check:** every anchor in `news-agent/briefings/<date>/<category>-anchors.md` must reference a source URL AND a verbatim excerpt from a real briefing item.
**Fail mode:** anchor body lacks source_url, OR cites a briefing item that doesn't exist in `<category>.md`.
**Report:** `anchor <date>/<category>-anchors.md anchor #N is unverifiable.`
**Repair:** drop the anchor.
**auto-fix: no** — even though the fix (drop) is mechanical, the consequence is loss of an outreach hook the originating agent intentionally generated. Better to surface to news-agent for re-derivation than silently drop.

### HF-5: Dossier modified by send action

**Check:** dossier file mtime changed AND the change includes engagement-state fields (`status: sent`, `sent_at`, etc.) — these belong in engagement records, not dossiers.
**Fail mode:** dossier contains `status: sent` or other engagement-state fields.
**Report:** `dossier memory/people/<slug>.md has engagement-state fields — violates Option B (engagement state belongs in agent folder).`
**Repair:** move engagement-state fields to the engagement record. The dossier should only have identity fields per `memory/templates/person.md`.
**auto-fix: no** — the fields might already exist in the engagement record (duplicate) or might be the only copy (unique). Migrating safely requires reading the engagement record context. Originating agent must repair.

### HF-NEW-1: Kept candidate with weak verification

**Check:** in any `<agent>/<stage>/output/<date>/<bucket>/candidates.md`, no candidate marked `kept` may have a `recent_activity` or status field with weasel-word phrasing — `pending`, `needs verification`, `profile-visit needed`, `requires full verification`, etc.
**Fail mode:** kept candidate with weasel-word verification status.
**Report:** `<file> candidate <N> (<slug>) marked kept but verification is weak: "<phrase>".`
**Repair:** drop the candidate from the kept list and add to drop log with reason `failed verification at validate-writes`, OR re-run profile click-through to capture real activity.
**auto-fix: no** — drop vs re-verify is a judgment call. Discovery agent might want to retry with a different search strategy rather than drop.

### HF-NEW-2: identity_verified=true without click-through evidence

**Check:** every candidate with `identity_verified: true` must have evidence of profile click-through (location confirmed live, recent activity captured with date, mutuals named).
**Fail mode:** `identity_verified: true` but no supporting fields populated.
**Report:** `<file> candidate <N> (<slug>) claims identity_verified but lacks click-through evidence.`
**Repair:** flip to `identity_verified: false` until evidence is captured, OR re-run click-through.
**auto-fix: no** — same reasoning as HF-NEW-1; originating agent decides whether to retry or drop.

### HF-NEW-3: Stale recent_activity

**Check:** every candidate with a populated `recent_activity` field must reference a date within the last 30 days.
**Fail mode:** activity date is >30 days old.
**Report:** `<file> candidate <N> (<slug>) recent_activity dated <date>, >30d old.`
**Repair:** drop the candidate (we want active LinkedIn users), OR flag for stage 03 review if there's a strong fit despite staleness.
**auto-fix: no** — drop vs flag is a judgment call.

---

## Soft warnings (track, surface in weekly report, don't block)

### SW-1: Dossier without `## Engagements` section

**Check:** every dossier in `memory/people/` should have a `## Engagements` section, even if empty.
**Warn:** missing section.
**Report:** `dossier memory/people/<slug>.md missing ## Engagements section — graph backlinks won't work.`
**Recommendation:** add the empty section per `memory/templates/person.md`.
**auto-fix: yes** — append empty `## Engagements` section with the template's table header. Idempotent: skip if section already present.

### SW-2: Person stub with no incoming engagement wikilinks

**Check:** dossier exists at `memory/people/<slug>.md` but no engagement record anywhere in the OS references it via `dossier_ref`.
**Warn:** orphan dossier.
**Report:** `dossier memory/people/<slug>.md is orphaned — no agent has an engagement record citing it.`
**Recommendation:** if intentional (research-only contact), add a note. Otherwise, archive.
**auto-fix: no** — archive vs keep is a judgment call (could be intentional research contact).

### SW-3: Engagement record older than 90 days, no follow-up

**Check:** engagement record with `sent_at` > 90 days ago, no further action logged.
**Warn:** dormant engagement.
**Report:** `engagement <path> last activity <date> — consider 07-track/dormant move.`
**Recommendation:** move to `07-track/dormant/`, or schedule a re-touch.
**auto-fix: no** — moving files between stages encodes pipeline state; originating agent owns that decision.

### SW-4: Daily log file >5 MB

**Check:** `logs/daily/<date>.md` file size.
**Warn:** unusually large daily log.
**Report:** `logs/daily/<date>.md is <size> — abnormally large, possible runaway logging.`
**Recommendation:** investigate; archive if appropriate.
**auto-fix: no** — investigation required (could be runaway loop, could be a legitimately busy day).

### SW-5: Stale `_INDEX.md`

**Check:** `_INDEX.md` modification time vs newest dossier creation.
**Warn:** dossiers added since last index regen.
**Report:** `_INDEX.md is stale — N dossiers added since last weekly consolidate.`
**Recommendation:** regenerate via the next `/memory-consolidate` run, or run manually.
**auto-fix: no** — handled by weekly consolidate's MO-1; not in validator's scope at write-time.

### SW-6: Briefing >90 days in active folder

**Check:** `news-agent/briefings/<date>/` where date is > 90 days ago.
**Warn:** retention not applied.
**Report:** `briefing <date> is past retention — should be in _archive/briefings/<YYYY-MM>/.`
**Recommendation:** weekly consolidate will move on next run.
**auto-fix: no** — handled by weekly consolidate's MO-2; not in validator's write-time scope.

### SW-7: Cross-doc fact conflict (dossier vs briefing)

**Check:** for each person whose name appears in a recent briefing item, compare the briefing-cited firm/role/topic against the dossier's identity fields.
**Warn:** mismatch.
**Report:** `dossier memory/people/<slug>.md says firm=<A>, briefing <date>/<category>.md item #N says firm=<B>. Conflict.`
**Recommendation:** human review — which is current? Update whichever is wrong; do NOT auto-resolve.
**auto-fix: no** — explicitly judgment-call; auto-resolution risks erasing correct facts.

### SW-8: Active candidate that's already been sent

**Check:** name appears in `02-discovery/output/<today>/candidates.md` AND has `06-send/output/<slug>.md` with `status: sent` in last 30 days.
**Warn:** dedup miss.
**Report:** `candidate <slug> is in today's discovery but was sent <date> (within 30-day cooldown).`
**Recommendation:** discovery should have caught this; check why dedup failed.
**auto-fix: no** — surfaces a process failure in discovery; silent removal would hide the underlying bug.

---

## Mechanical operations (auto-applied during weekly consolidate)

### Archive-walk exclusion (applies to ALL MOs and HFs)

Per OS `CLAUDE.md` operating principle #8, **the hygiene agent must NOT read content from `_archive/` or `_archives/` folders during any walk, indexer regen, validator pass, or sweep.** This applies even to walks rooted at `memory/`, `<agent>/`, or the OS root.

Rule for every walk operation in this file:
- Skip any directory whose basename starts with `_archive` (matches `_archive`, `_archives`, `_archive-from-X`, etc.).
- The hygiene agent IS allowed to MOVE files INTO archive folders (per MO-2, MO-4, etc.) — that's a write, not a read.
- The hygiene agent IS allowed to NAME archive paths in its reports (e.g., "moved <file> to <archive-path>") — that's metadata, not content.
- The hygiene agent is NOT allowed to read or summarize the contents of files inside any archive folder.

If a check below conflicts with this rule, the rule wins. Update the check.

### MO-1: Regenerate `_INDEX.md`

Walk `memory/people/` and `memory/companies/`, extract names, write fresh alphabetized index. **Skip any `_archive*/` subdirectory encountered in the walk** (per the archive-walk exclusion above).

### MO-2: Apply retention to `news-agent/briefings/`

Move briefing files older than 90 days to `news-agent/_archive/briefings/<YYYY-MM>/<filename>`. Same for anchor files.

### MO-3: Delete `news-agent/01-fetch/output/<date>/` older than 14 days

Intermediate fetch data — regenerable, no need to keep.

### MO-4: Archive daily logs >180 days

Move `logs/daily/<date>.md` (date >180d) to `logs/daily/_archive/<YYYY-MM>/<date>.md`.

### MO-5: Derive dormancy report at `hygiene-agent/integrity/dormancy-<YYYY-MM-DD>.md`

For each dossier, find the most recent date in its `## Engagements` table. If >90 days ago, list the person in this week's dormancy report. If most recent is <90 days, omit them. **Do NOT write `status: dormant` to dossier frontmatter** — `conventions.md` forbids `status` on dossiers. The dormancy report is the single source of truth for "who is dormant right now"; it regenerates each Sunday from the live engagement graph.

Format of the dormancy report:

```yaml
---
date: YYYY-MM-DD
threshold_days: 90
generated_by: hygiene-agent /memory-consolidate
---

# Dormancy report — YYYY-MM-DD

| Slug | Last engagement | Last engagement file | Days since |
|---|---|---|---|
| jane-doe | 2025-12-15 | networking-agent/06-send/output/jane-doe | 137 |
```

Older dormancy reports are retained for audit. The most recent file is authoritative for current dormancy state.

### MO-6: Regenerate `_INDEX.md` against the live vault

Walk `memory/people/` and `memory/companies/`, extract `name:` from each file's frontmatter, group active vs deprecated stubs, write the index. Update `people_count`, `people_stub_count`, `companies_count` in the file's frontmatter. **This is part of every weekly consolidate** — `_INDEX.md` should never be more than 7 days behind reality.

### MO-7: Append summary to `logs/daily/<date>.md`

Both daily and weekly runs append a timestamped block to today's daily log per OS convention.

---

## New checks added 2026-04-30 (post-audit hardening)

The audit on 2026-04-30 surfaced eight findings, of which several would have been caught earlier had hygiene-agent had these checks. They're added now to prevent recurrence.

### HF-6: Engagement-record `status` outside the canonical enum

**Check:** every engagement record's `status:` frontmatter value must be one of: `discovered`, `qualified`, `parked`, `disqualified`, `personalized`, `sent`, `accepted`, `replied`, `declined`, `ignored`, `failed`, `unverified-failure`, `dormant`, `coffee-asked`, `coffee-scheduled`, `coffee-completed`, `coffee-declined`, `coffee-ignored`, `coffee-failed`. (See `conventions.md` § "Engagement-status enum (CANONICAL)".)
**Fail mode:** value not in the enum.
**Report:** `engagement <path>: status="<value>" is not in the canonical enum. Map to one of [...].`
**Repair:** map to the closest canonical value per the deprecated-values mapping in conventions.md.
**auto-fix: no** — semantic mapping requires reading context (e.g., `attempted` → `failed` vs `unverified-failure` depends on whether the failure signal is reliable). Originating agent must repair.

### HF-7: Non-canonical file in `<agent>/<stage>/output/`

**Check:** every file in any agent's `<stage>/output/` directory must be a canonical engagement record — i.e., must have `dossier_ref:` in frontmatter AND a slug pattern matching `<kebab-case>.md` (no `<firstname>-<handle>-<platform>` patterns, no `_human_checks` suffix, etc.).
**Fail mode:** file lacks `dossier_ref` OR has a non-canonical slug.
**Report:** `<path> is in output/ but is not a canonical engagement record. Move to a non-output subfolder (e.g., `_human_checks/`, `_drafts/`).`
**Repair:** move to a clearly non-canonical sibling folder.
**auto-fix: no** — move target depends on the helper file's purpose. Originating agent decides.

**Carve-outs (do NOT flag — these stages produce intentionally non-engagement-record artifacts):**

- `networking-agent/02-discovery/output/<date>/<category>/candidates.md` — candidate pool, not a per-person engagement record yet
- `networking-agent/03-qualify/output/<date>/<category>/ranked.md` — ranked queue, not yet a per-person engagement record
- `networking-agent/08-followup/01-sweep/output/<date>/_sweep-summary.md` and `new-acceptees.md` — sweep state, not engagement records
- `networking-agent/08-followup/02-classify/output/<date>/_classify-summary.md` — classify summary, not a per-person record
- `networking-agent/08-followup/02-classify/output/<date>/passed/<slug>.md` — pre-engagement classification stub (no `dossier_ref` required because the classifier hasn't yet decided to ship; the dossier_ref relationship is established when the candidate transitions through to `06-send`)
- `networking-agent/08-followup/02-classify/output/<date>/skipped/<slug>.md` — skip decision with reason; intentionally not an engagement record
- `networking-agent/08-followup/03-anchor/output/<slug>.md` — anchor pick metadata; the engagement record itself is in `06-send/output/<slug>.md`
- `networking-agent/08-followup/04-draft/output/<slug>.md` — drafted DM awaiting review/send
- `news-agent/01-fetch/output/<date>/`, `news-agent/02-categorize/output/<date>/` — pipeline intermediates

The validator should match these path patterns and exclude them from HF-7. Anything else under `<agent>/<stage>/output/` still needs to be a canonical engagement record.

### HF-8: Engagement-state fields ON dossier (the inverse of HF-5)

**Check:** dossier file frontmatter must NOT contain any of: `status` (any value, including `dormant`), `sent_at`, `sent_channel`, `failed_channels`, `agent`, `dossier_ref`, `processing_started_at`. Identity-only.
**Fail mode:** dossier has any of these fields.
**Report:** `dossier memory/people/<slug>.md has engagement-state field <field> — violates Option B (identity vs engagement separation).`
**Repair:** remove the field from the dossier; if it represents real state, ensure it's tracked in the matching engagement record.
**auto-fix: no** — a wrongly-placed field could be the only copy; deletion without verification risks losing data.

### SW-9: Dossier missing required body sections

**Check:** every `memory/people/<slug>.md` must include `## Engagements` and `## Related` sections (per `memory/templates/person.md`). Stubs that redirect to a canonical may have minimal placeholder text in these sections, but the section headings must exist.
**Warn:** missing section.
**Report:** `dossier memory/people/<slug>.md is missing required section <name>.`
**Recommendation:** add the section with a placeholder if currently empty.
**auto-fix: yes** — append empty section headings with a one-line "(empty — fill when there's data)" placeholder. Reversible by replacing with real content.

### SW-10: Validation report in canonical `hygiene-agent/integrity/` area with off-spec name

**Check:** files in `hygiene-agent/integrity/` must match one of: `<YYYY-MM-DD>.md` (daily integrity), `weekly-<YYYY-WW>.md` (weekly), `dormancy-<YYYY-MM-DD>.md` (dormancy report). Anything else (`validate-*.md`, ad-hoc artifacts) must live in `hygiene-agent/integrity/_runs/`.
**Warn:** off-spec name in canonical area.
**Report:** `hygiene-agent/integrity/<filename> doesn't match canonical naming. Should be in hygiene-agent/integrity/_runs/.`
**Recommendation:** move to `_runs/`.
**auto-fix: yes** — move `validate-*.md` and similar transient artifacts into `hygiene-agent/integrity/_runs/`. The canonical files (`<date>.md`, `weekly-<week>.md`, `dormancy-<date>.md`) are not touched.

### SW-11: Nested `.obsidian/` outside the OS root

**Check:** any `.obsidian/` directory whose path is NOT exactly `<OS-root>/.obsidian/` is a competing vault config and should not exist.
**Warn:** split-brain Obsidian vault.
**Report:** `Found nested .obsidian/ at <path>. Root vault is canonical.`
**Recommendation:** archive to `<parent>/_archive-obsidian-config-<date>/` and delete on next sweep if no objection.
**auto-fix: yes** — move to `_archive-obsidian-config-<YYYY-MM-DD>/` adjacent to the parent. Reversible if needed.

### SW-12: Schema drift between agent CLAUDE.md and `conventions.md`

**Check:** for each agent's `CLAUDE.md`, look for any rule that contradicts `conventions.md` — specifically: status enum values used in examples, dossier-vs-engagement state assignment, frontmatter field definitions.
**Warn:** drift.
**Report:** `<agent>/CLAUDE.md uses term <X> in context <Y>; conventions.md says <Z>. Possible drift.`
**Recommendation:** reconcile during next agent CLAUDE.md edit.
**auto-fix: no** — semantic; requires understanding which doc is "right" (often conventions.md, but not always).

### SW-13: Stale `_INDEX.md` count

**Check:** `_INDEX.md` frontmatter `people_count` / `companies_count` vs live vault file count.
**Warn:** count mismatch >5 (indicates the index is materially stale, not a one-off).
**Report:** `_INDEX.md says people_count=<N>, vault has <M>. Stale by <delta>.`
**Recommendation:** regenerate via `/memory-consolidate` (or manually) — covered by MO-6.
**auto-fix: yes** — regenerate inline using the same logic as MO-6. Reversible.

---

## Escalation thresholds

- **Daily:** >5 hard fails or >20 soft warnings = surface as red banner via `/hygiene-status`.
- **Weekly:** any unresolved hard fails from prior week = escalate.
- **Trend:** if same SW recurs >3 weeks in a row, recommend a process fix (not just repeat warnings).

## Maintenance

- Add new check IDs sequentially (HF-N, SW-N).
- When a soft warning becomes critical, promote to hard fail.
- When a hard fail is consistently false-positive, demote or refine the check.
- Audit this config quarterly — checks that haven't fired in 90 days should be examined for relevance.
