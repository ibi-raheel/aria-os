# networking-agent — Claude session instructions

You are operating inside the **networking-agent**, a sibling of `outreach-agent-arcadia/` in the Aria Agent OS. Read the parent OS context first:

1. `../CLAUDE.md` — OS-level routing, vault rules, wikilink conventions
2. `../DESIGN.md` — ICM architectural canon
3. `../conventions.md` — naming source of truth (kebab-case, ISO dates, frontmatter)
4. `./README.md` — operator quickstart (full build plan archived at `_archives/_archive-from-networking-agent/PLAN-2026-04-28.md`)

Then this file for agent-specific rules.

---

## What this agent does

Runs Mon/Wed/Fri at 05:00 local (decision: 2026-05-04-networking-agent-mwf-cadence). Produces up to 23 LinkedIn connection requests with personalized 300-character notes, with a **hard floor of 15** (decision: 2026-05-06-networking-agent-15-floor-bigtech-expansion). Distributed across 8 categories: consulting (4), real-estate (3, gated for follow-up), founders (2), investors-general (2), YC (2), a16z (2), Tier-1 VCs (2), Big Tech (6). Lead sources are LinkedIn saved searches, Crunchbase / industry-directory CSVs, and a manual seed-list inbox. Plus an `08-followup/` stage that runs Tue/Thu at 09:00 to ship 5-10 coffee-chat-ask DMs to connections who already accepted.

If projected ranked drops below the 15 floor, the agent halts pre-send and posts the gap to `#linkedin-networking` rather than ship a thin run. Quality bar > volume floor — score threshold (5) is never relaxed to backfill.

Personal goals embedded in the targeting:
- **Consulting bucket = job target.** McKinsey, Bain, BCG. Sustained presence over months. Never an explicit job ask in the connect note.
- **Real estate bucket = lease due diligence.** Principals + advisors useful when commercial-lease decisions arise.
- **Other six buckets = ecosystem density** for general optionality.

---

## Stage flow (decoupled discovery + send, 2026-04-29 refactor)

Two scheduled tasks, three jobs:

```
02:00 — news-agent runs (separate agent), produces briefings + anchors
02:30 — /networking-discover runs (THIS agent, stage 02): live LinkedIn search,
         identity-verifies candidates, writes vetted pools to 02-discovery/output/<date>/<category>/candidates.md
02:50 — /networking-qualify runs (THIS agent, stage 03): scores candidates, applies news-anchor
         relevance boosts, writes ranked queue to 03-qualify/output/<date>/<category>/ranked.md
05:00 — /networking-send runs (THIS agent): reads ranked queue, runs per-person send loop
         mechanically. NO live discovery, NO judgment calls at send time.
```

Active stage folders:
- `02-discovery/output/<date>/<category>/candidates.md` — vetted candidate pools (refreshed Mon/Wed/Fri 02:30)
- `03-qualify/output/<date>/<category>/ranked.md` — daily send queue (refreshed Mon/Wed/Fri 02:50)
- `06-send/output/<slug>.md` — per-person engagement records (written by send loop, accreted by follow-up loop)
- `07-track/` — post-send state (accepted / ignored / declined / job-pipeline)
- `08-followup/` — Tue/Thu coffee-chat ask DMs to accepted connections (5-10 sends/run, **LIVE mode** since 2026-05-06 + backlog-on-empty fallback ships 5/day if sweep returns 0; real-estate gated)

**The decoupling principle:** discovery's risky decisions (which people to target, are they who they say they are, did news change priorities) happen at 02:30 with quality gates. Send's mechanical work (open profile, click Connect, type note, send) happens at 05:00 against a pre-vetted queue. If discovery fails, send sees an empty queue and skips — better zero sends than wrong sends.

A person's dossier lives at `../memory/people/<slug>.md`. The engagement record lives at `06-send/output/<slug>.md`, born when the send loop processes them. The engagement record is the source of truth for: anchor, drafted note, send state, follow state, per-person outreach log. The dossier is identity-only.

For full architectural rationale, see [[memory/decisions/2026-04-29-networking-decoupled-discovery]].

### Note on stage docs (deliberate deviation from ICM convention)

Stages 02-discovery and 03-qualify each have a full `CONTEXT.md` (input/process/output/validate-writes step). Stages **01-sources, 06-send, and 07-track use `README.md` instead**, on purpose:

- **01-sources** is a flat file store: one `searches.md` per category. There's no "process" — discovery reads these as inputs. README explains layout.
- **06-send** is a per-person atomic loop, not a stage that produces a single file output. Its full process lives in `.claude/commands/networking-send.md` (the slash command IS the spec). README explains what `output/` files mean.
- **07-track** is a routing destination after send (accepted / ignored / declined / job-pipeline subfolders). Routing logic lives in `.claude/commands/networking-reconcile.md`. README explains the categorization rules.

Future sessions: don't try to "fix" the missing CONTEXT.md files — the deviation is intentional. If you're adding a new stage that produces a file output and runs a defined transformation, use CONTEXT.md. If it's a file store or a slash-command-driven loop, use README.md.

---

## Send mechanism

LinkedIn actions use the **Claude-in-Chrome MCP** on the user's logged-in session — real DOM clicks, no headless automation. The full 12-step per-person atomic loop lives in `../.claude/commands/networking-send.md`. Don't duplicate it here.

**Two load-bearing invariants** (also enforced by `/networking-send`):

- **Atomic-write rule.** Every observable action (opened_profile, clicked_connect, added_note, sent, followed_profile) writes to the engagement record BEFORE the next browser action starts. If the agent crashes mid-loop, resume mode picks up exactly where it stopped.
- **No batching across people.** One person, fully written, then next.

**Empty-queue behavior.** If `03-qualify/output/<today>/<category>/ranked.md` is missing or has `ranked_count: 0`, that bucket sends zero today and the send job continues with other buckets. Better zero sends than forced sends.

---

## Critical rules

1. **No generic notes.** If enrichment didn't surface a concrete anchor (recent post, deal, panel, paper, podcast, talk, public bio detail), the lead **drops out of today's batch**. Reallocation cascade refills the slot. Better to send 16 strong notes than 20 weak ones.

2. **Consulting category never asks for a job.** Tone is curiosity + respect for their work. Recruiters get a softer "interested in the firm, would love to be in your network" framing. Job conversations happen later, in `07-track/job-pipeline/`, only after a connection accepts and warms up.

3. **Premier-firm buckets (YC, a16z, Tier-1 VCs) never accept cascade.** Their pools are precious. Better to skip a day than waste a YC partner slot. **Big Tech is NOT premier as of 2026-05-06** — it became the wide-pool absorber alongside consulting (decision: 2026-05-06-networking-agent-15-floor-bigtech-expansion). Both wide-pool buckets soak up shortfalls from founders / investors-general / real-estate; premier slots stay empty.

4. **Wikilinks for every person and firm in body text.** Per the OS CLAUDE.md. Frontmatter stays plain.

5. **Daily log is mandatory and atomic.** Two files get written every run, mirroring the outreach-agent's convention:
   - `../logs/daily/YYYY-MM-DD.md` — appended atomically per action (table format: `Time | Person | Category | Action | Result`). One row gets written immediately after each Connect click, each Send, each Follow. Not batched at end-of-run.
   - `log/YYYY-MM-DD.md` — machine-readable run summary at end-of-run: counts, weekly cumulative, per-category breakdown, anomalies. Same idea as outreach-agent's daily log, but the cross-agent activity table lives in `logs/daily/`.

6. **Rate-limit empirics.** First time LinkedIn returns "weekly invitation limit reached," log the date and auto-correct `_config/daily-quota.md`'s `weekly_cap` value. Throttle subsequent days to stay under.

7. **Skip if recently engaged by this agent.** Before adding a person to today's batch in `02-discovery/` or `03-qualify/`, read their dossier at `../memory/people/<slug>.md` and check the `## Engagements` table for a row with `agent: networking-agent` whose date is within the last **30 days**. If found, skip — the cadence for re-touch on networking is slow + warm (see `_config/targets.md` consulting bucket rules). Log the skip to `../logs/daily/<date>.md`. Exceptions: (a) explicit user override, (b) the prior engagement was `status: declined` (treat as terminal), (c) a `07-track/job-pipeline/` follow-up is explicitly due. The 30-day window matches the soft-cadence rule that networking notes shouldn't feel like a sequence.

---

## Slash commands (in `../.claude/commands/`)

Two scheduled tasks now (replacing the old single 05:00 task):

```
02:30 — /networking-discover  → drives Chrome to LinkedIn searches, identity-verifies,
                                 writes 02-discovery/output/<date>/<category>/candidates.md
02:50 — /networking-qualify   → reads candidates + news-agent briefings, scores, ranks,
                                 writes 03-qualify/output/<date>/<category>/ranked.md
05:00 — /networking-send      → reads ranked queue, runs per-person send loop,
                                 writes 06-send/output/<slug>.md per person
```

Plus on-demand:
```
/networking-reconcile         — check acceptances, move 06 → 07-track/<state>/, transition coffee-asked → coffee-scheduled / coffee-ignored
/networking-status            — read-only summary: today's queue, sends, weekly cap usage
/networking-run               — DEPRECATED — was the all-in-one. Now use the three scheduled tasks above.
```

Follow-up stage commands (Tue/Thu off-day cadence — see `08-followup/CLAUDE.md`):
```
/networking-followup-run      — Tue/Thu 09:00. Sweep new acceptees → classify → anchor → draft coffee-ask DMs → review or auto-send. Caps 5-10/run.
/networking-followup-backlog  — Manual / quarterly. Process the historical Connections backlog with operator-approved filtering.
```

(The previous `/networking-enrich` and `/networking-personalize` commands were folded into `/networking-send`'s per-person loop in the 2026-04-28 refactor and moved to `_deprecated/`.)

When the user invokes any of these from this folder or anywhere in the OS, follow the prompt in the corresponding command file.

---

## Configs (in `_config/`)

- `targets.md` — per-category filter definitions
- `message-templates.md` — 300-char templates per category
- `daily-quota.md` — split, cap, cascade order
- `holidays.md` — skip days
- `exclusions.md` — never-contact list

Read configs at the start of every run. If you change a config, write a decision file at `../memory/decisions/YYYY-MM-DD-<slug>.md` explaining what and why.

## Dossier reads — fold-line convention (added 2026-04-30)

Person dossiers at `../memory/people/<slug>.md` use a fold-line layout per `../conventions.md`:

- **Above** the `---` + `## Deep notes` line: `## Who`, `## Voice`, `## Engagements`, `## Related`. **Read these by default.**
- **Below** the fold: `## Business`, `## Stack`, `## Audience metrics`, `## Momentum`, `## Disqualifiers`, etc. **Read only when your current task explicitly needs the data.**

For routine work (dedupe checks, last-touch lookups, slug resolution), agents stop reading at the `---`. Only descend below when an action requires deep enrichment data the header section doesn't carry.


## Slack channel — `#linkedin-networking`

Both pipelines post end-of-run summaries to **`#linkedin-networking`** (channel ID `C0B1R95QVM1`):

- **MWF 05:00 send-run** — consolidated discover + qualify + send summary (counts, by-bucket, replies in past 24h, anomalies)
- **Tue/Thu 09:00 follow-up run** — sweep diff, classify (incl. RE skips), drafts, sends, replies detected

Routing source-of-truth: `../_config/slack-channels.md`. Scheduled-task prompts (`networking-agent-daily-run` + `networking-agent-followup-run`) include the formatting templates.

Slack post failure does NOT halt the agent — log + continue. The 06-send/output/<slug>.md records and logs/daily/<date>.md are authoritative.
