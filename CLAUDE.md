# Aria Agent OS - Root

This folder is **Aria Agent OS** - a folder-based agent operating system
following the Interpretable Context Methodology (ICM). The folder structure
IS the agent. Files are state.

The OS root is also an **Obsidian vault**. Shared canonical knowledge —
person dossiers, companies, decisions, daily logs, taxonomy, templates —
lives under `memory/`. Agents (outreach-agent-arcadia, networking-agent,
future ones) live as siblings to `memory/`, hold their own engagement
records, and link INTO `memory/` rather than duplicating its content.

Any Claude session entering this folder reads this file first, then
`DESIGN.md` for the architectural canon, then `conventions.md` for naming
rules.

---

## Output routing (Cowork default)

**This folder is the working surface. Write here, not to the session temp dir.**

When this Cowork session produces a file, route it by kind:

| Kind of output | Destination |
|---|---|
| Project work (Arcadia, SpriteMaker, agents, future projects) | That project's folder, in the appropriate subdirectory |
| Person dossier (who they are, facts, voice, audience) | `memory/people/<slug>.md` |
| Engagement record (what an agent did about a person) | `<agent>/<stage>/output/<slug>.md` |
| Company / platform hub | `memory/companies/<slug>.md` |
| Decision record | `memory/decisions/YYYY-MM-DD-<slug>.md` |
| Daily activity log entry | Append to `logs/daily/YYYY-MM-DD.md` (timestamped block) |
| Unsorted capture - fact, snippet, idea without a clear home | `memory/inbox/` (gets triaged later) |
| Session-level Cowork output without a project home - drafts, summaries, exploratory artifacts | `cowork/YYYY-MM-DD/` |
| Architectural / design / OS-level docs | Root of `Aria Agent OS/` |

**Do not** write to `/Users/aria/Library/Application Support/Claude/.../outputs`
or any session-temp directory unless the file is genuinely throwaway and
unrelated to Aria OS work. The temp dir is invisible to the user; this folder
is the one they actually see.

When sharing a created file with the user, link it via
`computer:///Users/aria/Documents/Aria Agent OS/...`.

---

## Project index

Top-level peer projects:

- `Arcadia/` - MVP product, software codebase. Target customer of the outreach agent.
- `SpriteMaker/` - existing software project.
- `outreach-agent-arcadia/` - first ICM agent. Multi-channel outreach pipeline targeting creators for Arcadia. Future outreach campaigns get their own folder (e.g., `outreach-agent-realestate/`).
- `networking-agent/` - LinkedIn networking agent. 8 categories with split 4/3/2/2/2/2/2/6 = 23 spec on a Mon/Wed/Fri 05:00 cadence (decisions: 2026-05-04-networking-agent-mwf-cadence + 2026-05-06-networking-agent-15-floor-bigtech-expansion). **Hard floor of 15/run** — agent halts and pings `#linkedin-networking` rather than ship under-floor. Big Tech expanded from eng-execs-only to all functions (HR/PM/EM/design/GTM/finance/ops) — now wide-pool absorber alongside consulting; premier buckets (YC/a16z/Tier-1) never accept cascade. Plus an `08-followup/` stage that ships up to 10 coffee-chat-ask DMs Tue/Thu 09:00 to connections who already accepted, with a backlog-on-empty fallback that ships 5/day from the historical Connections backlog when the sweep returns 0 net-new (decision: 2026-05-06-followup-live-default-and-backlog-on-empty). Real-estate category gated for follow-up — pending different message structure.
- `news-agent/` - intelligence agent paired to networking. Runs 02:00 Mon/Wed/Fri (matches networking so each send-day uses same-morning fresh anchors). Produces per-category briefings + candidate anchor questions consumed by the outreach + networking agents at 05:00.
- `hygiene-agent/` - vault integrity agent. Runs daily 22:00 weekdays (`/integrity-check` — validates today's writes) + Sundays 22:00 (`/memory-consolidate` — regen `_INDEX.md`, apply retention, mark dormants, full-vault soft-warning sweep). Reports to `hygiene-agent/integrity/`.
- `twitter-agent/` - public Twitter/X posting agent for Arcadia. **ACTIVE as of 2026-05-10.** Day 1 shipped. Migrated from Chrome MCP to **Playwright MCP** (decision: 2026-05-10-twitter-agent-playwright-migration-and-slack-approval-loop). **6 scheduled tasks** replace the old monolithic run: prep at 06:00 (drafts + screenshots + engagement targets sent to Slack for review), post-1/2/3 at 12:00/18:00/20:00 (each reads Slack approval before posting), daily-metrics at 23:00, weekly-metrics Sunday 23:00. **Slack approval loop:** operator reviews 6 AM prep bundle in `#twitter-arcadia`, replies approved/rewrite/reject; posting tasks parse the thread. **3 posts/day + 3 engagements/day MINIMUM** (hard floor). **Anchor/filler hierarchy:** slot 1 12:00 ET = anchor (feature spotlight from 7-day rotation, fresh Arcadia screenshot MANDATORY); slot 2 18:00 ET = filler (insight/hot-take, visual optional); slot 3 20:00 ET = filler (news/reshare, text-only by default). All visuals Arcadia-product only. **ICP pivot**: Twitter audience = gaming + AI/tech (broad); product-buyer ICP stays creator-economy. See `twitter-agent/CLAUDE.md` for full spec.
- `daily-digest` (slash command, no folder) - **On-demand only as of 2026-05-06.** Each agent now posts its own run summary directly to its dedicated Slack channel at end-of-run (`#news`, `#linkedin-networking`, `#hygiene`), so the daily 06:00 digest is redundant for current volume. The scheduled task `daily-digest-run` is `enabled: false` but the slash command + spec remain — operator can run `/daily-digest` manually anytime for a cross-agent synthesis (useful when catching up after time off). Spec at `.claude/commands/daily-digest.md`. Channel routing source-of-truth: `_config/slack-channels.md`.

Plus session/working folders:

- `cowork/` - this Cowork session's one-off outputs (per-day subfolders).

OS-wide shared knowledge:

- `memory/` - the unified vault: `people/` (dossiers), `companies/`, `decisions/`, `daily/`, `inbox/`, `templates/`, `_taxonomy.md`. Any agent reads/writes.
- `conventions.md` - naming source of truth (kebab-case, ISO dates, frontmatter rules).

Top-level meta docs:

- `CLAUDE.md` (this file), `DESIGN.md`, `README.md`, `SETUP-FOLDER-WORKSPACE.md`.

OS-level Claude Code config:

- `.claude/commands/` - 38 slash commands across the OS-level (`/status`, `/log`, `/decision`, `/triage`, `/who`, `/validate-writes`), networking-agent (`/networking-discover`, `/networking-qualify`, `/networking-send`, `/networking-followup-run`, `/networking-followup-backlog`, `/networking-reconcile`, `/networking-status`), news-agent (`/news-run`, `/news-fetch`, `/news-categorize`, `/news-anchors`, `/news-status`), hygiene-agent (`/integrity-check`, `/memory-consolidate`, `/hygiene-status`), twitter-agent (`/twitter-run`, `/twitter-draft`, `/twitter-post`, `/twitter-respond`, `/twitter-engage`, `/twitter-screenshot`, `/twitter-signals`, `/twitter-track`, `/twitter-status`), and `/daily-digest` (manual on-demand). Plus the original outreach-agent pipeline commands (`/discovery`, `/qualify`, `/enrich`, `/personalize`, `/send`, `/followup`).
- `.obsidian/` - Obsidian vault config (graph, daily notes, templates).

---

## Memory model — Option B (person-canonical, agent-engagement)

**Each person has ONE dossier at `memory/people/<slug>.md`.** This file
describes who they are: background, business, stack, voice, audience,
disqualifiers. Written once when first encountered; extended as new facts
emerge. Read by every agent that touches this person. The dossier is the
single source of truth for identity.

**Each agent×person interaction has ONE engagement record** at
`<agent>/<stage>/output/<slug>.md`. The engagement record describes what
this agent did: anchor, drafted message, send state, outreach log. Owned
by exactly one agent. Lives in the agent's stage folders and moves between
them to encode pipeline state.

**The link.** Every engagement record carries `dossier_ref: '[[memory/people/<slug>]]'`
in frontmatter and a body line `See dossier: [[memory/people/<slug>|<Name>]]`.
Every dossier carries a `## Engagements` table with one row per agent that
has engaged this person, wikilinking to each engagement file. Bidirectional —
the graph works in both directions.

**Multi-agent example.** Creator B in this vault:
- Dossier: `memory/people/creator-b.md` (Who, Business, Voice, etc. — agent-agnostic).
- Outreach engagement: `outreach-agent-arcadia/stages/05-send/output/creator-b.md`
  (Why-this-pitch, Discovery angle, messages, log).
- Networking engagement (when it happens): `networking-agent/06-send/output/creator-b.md`
  (anchor, personalized note, log).

The dossier is shared infrastructure. Engagements are owned per-agent. New agents
read the dossier instead of re-enriching what's already known, and write only their
own engagement records.

**Companies, decisions, daily logs.** `memory/companies/`, `memory/decisions/`,
and `logs/daily/` remain shared canonical stores across all agents,
unchanged from before.

---

## Wikilink rules (Obsidian graph connectivity)

This vault is browsed in Obsidian. Every file must participate in the
graph - **isolated nodes are bugs.**

### Hard requirements

1. **Every person has a dossier at `memory/people/<slug>.md`.** Created
   the first time a person enters any agent's pipeline. Never deferred.

2. **Every agent×person engagement has its own record** at
   `<agent>/<stage>/output/<slug>.md`. The engagement record carries
   `dossier_ref` frontmatter pointing at the dossier and a body wikilink
   in the form `See dossier: [[memory/people/<slug>|<Name>]]`.

3. **Use `[[wikilinks]]` for all cross-references in markdown body text:**
   - People: `[[memory/people/creator-a|Creator A]]`
   - Companies/platforms: `[[memory/companies/skool|Skool]]`
   - Decisions: `[[memory/decisions/2026-04-25-skip-acme|Skip Acme]]`
   - Engagement files: `[[outreach-agent-arcadia/stages/05-send/output/creator-a]]`
   - Never write a person's name or platform name as plain text if a
     vault entry exists for it.

4. **Link the first mention only** - don't litter every paragraph.

5. **Don't add wikilinks inside YAML frontmatter values.** Frontmatter
   field values stay plain (handles, status, tags). The one exception is
   `dossier_ref`, which carries a wikilink as its value because it's
   structurally a reference.

6. **Platform hub nodes exist in `memory/companies/`.** Known platforms:
   `skool.md`, `circle.md`, `mighty-networks.md`, `whop.md`,
   `patreon.md`, `kajabi.md`, plus per-agent additions (e.g.,
   `linkedin.md`, `mckinsey.md` for networking-agent). When a new
   platform or firm is encountered, create a stub.

7. **Person dossiers (`memory/people/`) must include:**
   - `**Platform:** [[memory/companies/X|X]]` line near the top
   - `## Engagements` section with one row per active/past engagement
   - `## Related` section with `[[wikilinks]]` to known connections
     (co-founders, mentors, mutual community members)

8. **When spawning sub-agents** to write dossiers or enrich leads, the
   prompt MUST include instructions to: (a) write to the dossier at
   `memory/people/<slug>.md` (extending, not overwriting), (b) write a
   matching engagement record in the agent's stage output folder,
   (c) use wikilinks for people and platforms in body text.

---

## Operating principles (from DESIGN.md)

1. One stage, one job.
2. Plain markdown only.
3. Engagement files move between stage folders to encode pipeline state.
4. Configure the factory (`_config/`), not the product.
5. One-way references: stage N reads N−1, never N+1.
6. Free tools only by default - no paid SaaS unless the user already pays.
7. **Person dossier in `memory/people/` is shared. Engagement records in
   agent folders are per-agent.** Never duplicate dossier content into an
   engagement record; link via `dossier_ref` instead.
8. **Archives are cold storage. No agent reads `_archive/` content unless
   the operator explicitly names the path.** Any folder named `_archive/`
   anywhere in the vault — `<agent>/_archive/`, `news-agent/_archive/briefings/`,
   `logs/daily/_archive/`, `memory/_archive/`, etc. — holds retired or
   invalidated state. Reading archived content as if it were live state
   corrupts agent reasoning. The rule applies to: scheduled tasks, slash
   commands, hygiene sweeps that walk the vault, Cowork sessions doing
   contextual reads, indexer regens, validator passes. Hygiene sweeps that
   MOVE files INTO archives are allowed; READING from archives is not.
   The operator can always direct an explicit read ("read
   `<agent>/_archive/X/Y.md`"); that's the documented escape hatch.

For the full design, read `DESIGN.md`. For naming rules, read
`conventions.md`.

---

## Outreach send model (applies to all outreach agents)

The unit of work is **one person**. For each person, attempt every
available channel in sequence: email, Instagram DM, Twitter DM, LinkedIn
DM, and any other available channel. Update the engagement record's
`sent_channel` field and outreach log after every successful send, and
`failed_channels` after every failure (with the reason). Never batch
file updates across people. Never move to the next person until the
current person's engagement record is fully up to date.

**The engagement record is the source of truth for engagement state.**
If `sent_channel` says a channel was sent, it was sent. If
`failed_channels` says it failed, it failed. If neither field mentions a
channel, it has not been attempted. The dossier in `memory/people/` is
NOT updated by send actions — only by enrichment (when new facts about
the person are learned).
