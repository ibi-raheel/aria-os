# Aria Agent OS - Design Document

> **Read this first.** This is the architectural canon for Aria Agent OS. Any
> Claude session - Cowork or Claude Code - entering this folder should read
> `CLAUDE.md` and then this document before doing anything else.
>
> For build chronology, status, and scoping decisions, see `HISTORY.md`.

---

## What this is

A folder-based agent operating system following the **Interpretable Context
Methodology (ICM)** developed by Jake Van Clief. The folder structure IS the
agent. Files are state. There is no orchestration framework, no database, no
service layer. Plain markdown files in a deliberate directory layout, read by
a single LLM session at a time.

**Canonical reference:**
- Paper: [arXiv:2603.16021 - Interpretable Context Methodology: Folder
  Structure as Agentic Architecture](https://arxiv.org/abs/2603.16021)
  (Van Clief & McDermott, 2026)
- Repo: [github.com/RinDig/Interpreted-Context-Methdology](https://github.com/RinDig/Interpreted-Context-Methdology)
- Origin video: [Stop Building AI Agents. Use This Folder System Instead.](https://www.youtube.com/watch?v=MkN-ss2Nl10)

## The 5-layer ICM model

The agent reads down through these layers and stops as soon as it has enough
to act. Most tasks don't need all five. Total context per task: ~2,000–8,000
tokens.

```
Layer 0:  CLAUDE.md                   "Where am I?"            always loaded (~800 tok)
Layer 1:  <project>/CONTEXT.md        "Where do I go?"          on project entry (~300)
Layer 2:  <project>/stages/<n>/CONTEXT.md   "What do I do?"     per-task (~200–500)
Layer 3:  vault folders, _config/,    "What rules apply?"       loaded selectively
          shared/, skills/
Layer 4:  stages/<n>/output/          "What am I working on?"   loaded selectively
```

Layer 3 has two scopes:
- **3a - `memory/` at OS root** (`memory/people/`, `memory/companies/`,
  `memory/decisions/`, `logs/daily/`, `memory/inbox/`,
  `memory/templates/`) - facts about people, companies, topics, decisions;
  shared across all projects, written to by any agent.
- **3b - `_config/`** (project-scoped) - factory configuration for one
  agent (ICP, voice, offer, etc.). Lives inside the agent's project folder.

## Memory model — Option B (person-canonical, agent-engagement)

The OS root **is** an Obsidian vault. `.obsidian/` lives at
`/Users/aria/Documents/Aria Agent OS/.obsidian/`. Every markdown file in the
OS is part of the same graph and reachable by `[[wiki link]]`.

**Key principle: agents are processes, not graph nodes. The PERSON is the
graph node; what the agent did is per-engagement.**

- **Person dossier** lives at `memory/people/<slug>.md`. Describes who they
  are: background, business, stack, voice, audience, disqualifiers. Written
  once when first encountered; extended as new facts emerge. Read by every
  agent. Single source of truth for identity.
- **Engagement record** lives at `<agent>/<stage>/output/<slug>.md`.
  Describes what THIS agent did with this person: anchor, drafted message,
  send state, outreach log. Owned by exactly one agent. Files MOVE between
  the agent's stage folders to encode pipeline state.
- **Linkage.** Every engagement record carries `dossier_ref:
  '[[memory/people/<slug>]]'` in frontmatter and a body line `See dossier:
  [[memory/people/<slug>|<Name>]]`. Every dossier carries a `## Engagements`
  section listing wikilinks to all engagement records. Bidirectional graph.

Concretely, when the outreach agent meets Sarah Kim at Acme Corp:
- Dossier → `memory/people/sarah-kim.md` (who she is — agent-agnostic)
- Outreach engagement → `outreach-agent-arcadia/stages/05-send/output/sarah-kim.md` (Why-this-pitch, messages, send log)
- Decision recorded → `memory/decisions/2026-04-25-skip-acme-corp.md`
- Activity logged → appended to `logs/daily/2026-04-25.md`

If networking-agent later engages Sarah, it reads the existing dossier (no
re-enrichment) and writes its own engagement record at
`networking-agent/06-send/output/sarah-kim.md`. The dossier gains a second
row in its `## Engagements` table. Two engagements, one shared dossier.

`memory/companies/`, `memory/decisions/`, and `logs/daily/` remain
shared canonical knowledge stores across all agents.

## Architecture decisions

### Structure: Umbrella
All active projects live INSIDE Aria Agent OS. The OS is the parent, not a
sibling. The vault at the OS root sees inside every project; projects can
backlink to vault entries.

### Location: Top of `Documents/`
`/Users/aria/Documents/Aria Agent OS/` - surfaced next to other folders, easy
to find. Cowork mounts this folder; Claude Code is invoked from inside it.

### Active projects inside the OS
Three top-level peer projects:
- `Arcadia/` - MVP product (PRD-driven, software codebase).
- `SpriteMaker/` - existing software project.
- `outreach-agent-arcadia/` - first ICM agent (multi-channel outreach pipeline). Sibling of
  Arcadia, not nested inside it. Currently configured to source leads for
  Arcadia (via `_config/offer.md`) but designed to be retargetable to other
  projects later.

### Sibling projects (outside the OS, untouched)
- `Arcadia World/` - relationship to Arcadia TBD by user.
- `Codex/` - existing project, kept separate by user choice.

### Tool split - Cowork vs Claude Code
- **Cowork** = design / setup / review. Conversational UI, AskUserQuestion,
  visual artifacts, mac driving. Use for: scaffolding new agents, editing
  CONTEXT.md and `_config/`, reviewing daily outputs, anything human-in-loop.
- **Claude Code** = runtime. Terminal-native, slash commands per stage,
  pre/post-tool hooks, scriptable, scheduled. Use for: running the pipeline,
  executing stages, validation, automated runs.
- Both read the same filesystem and both honor `CLAUDE.md` files.

### Tool stack: free-only
Default to free tools. **Do not propose paid SaaS unless the user already
pays for it and asks.** Allowed defaults:

- **Research / sourcing:** `WebSearch`, `web_fetch`, Google dorks
  (`site:linkedin.com/in/`), Reddit JSON API, Hacker News Algolia API,
  GitHub public API + GitHub MCP.
- **Web automation:** Chrome MCP (browser tier - can read DOM, navigate,
  scrape public pages).
- **Native automation:** computer-use MCP (drives Mac apps), AppleScript via
  `mcp__Control_your_Mac__osascript`.
- **Email / inbox:** Gmail MCP (free with Google account; ~500/day personal,
  ~2000/day Workspace send limits).
- **Scheduling:** none. Agents run via slash commands manually invoked in Claude Code (per `/followup` etc.). No background scheduler. Bump cadence lives as date fields in lead frontmatter.
- **File / doc creation:** the `docx`, `xlsx`, `pdf`, `pptx` skills.

**Forbidden by default:** Apollo, Clay, Apify, Sales Navigator, Hunter,
Crunchbase Pro, any paid scraper. Mention only if user already pays.

## Target folder structure (current state - built)

```
Aria Agent OS/                      ← Obsidian vault root
├── .obsidian/                      ← Obsidian config (graph, templates, daily notes)
├── .claude/
│   ├── settings.json
│   └── commands/                   ← 10 slash commands
│       ├── status.md               ← /status - pipeline state + what's due today
│       ├── log.md                  ← /log - append to today's daily note
│       ├── decision.md             ← /decision - structured decision capture
│       ├── triage.md               ← /triage - triage memory/inbox/
│       ├── discovery.md            ← /discovery - run stage 01
│       ├── qualify.md              ← /qualify - run stage 02
│       ├── enrich.md               ← /enrich - run stage 03
│       ├── personalize.md          ← /personalize - run stage 04
│       ├── send.md                 ← /send - run stage 05
│       └── followup.md             ← /followup - run stage 06
├── CLAUDE.md                       ← OS identity, project index, routing
├── README.md                       ← human-facing entry
├── DESIGN.md                       ← THIS FILE - architectural canon
├── SETUP-FOLDER-WORKSPACE.md       ← ICM scaffolding template (generic, not Aria-specific)
├── conventions.md                  ← naming source of truth
│
├── memory/                         ← UNIFIED VAULT - shared knowledge
│   ├── _taxonomy.md                ← agreed tag list (single source of truth)
│   ├── people/                     ← person dossiers (full identity records, one per person; shared across agents)
│   ├── companies/                  ← platform hub nodes (skool, circle, etc.)
│   ├── decisions/                  ← load-bearing - see "Vault risks"
│   ├── daily/                      ← append-only activity log, one per day
│   ├── inbox/                      ← unsorted captures, triaged via /triage
│   └── templates/
│       ├── person.md               ← dossier template (identity-only)
│       ├── engagement.md           ← engagement-record template (per-agent)
│       ├── company.md
│       ├── decision.md
│       └── daily.md
│
├── cowork/                         ← Cowork session outputs (per-day subfolders)
│
│   ── projects ──
├── Arcadia/                        ← software project (Next.js, has its own git)
├── SpriteMaker/                    ← software project
└── outreach-agent-arcadia/         ← first agent - Arcadia outreach campaign
    ├── CLAUDE.md                   ← agent identity + routing into stages
    ├── CONTEXT.md                  ← workspace overview
    ├── _config/
    │   ├── icp.md                  ← who we target (creators $20k+/mo)
    │   ├── voice.md                ← how we sound
    │   ├── offer.md                ← what we pitch (DFY $7.5k-$15k)
    │   └── send-protocol.md        ← cadence, caps, tier rules
    ├── _archive/                   ← dormant agent state (post-engagement closed-won)
    ├── shared/
    ├── skills/
    │   ├── discovery-sources.md    ← Skool + Twitter + YouTube recipes
    │   ├── icp-scoring-rubric.md   ← 5-dim scoring
    │   ├── dossier-rubric.md       ← comprehensive enrichment schema
    │   ├── hook-library.md         ← creator-economy hooks
    │   ├── loom-script-template.md ← 30-sec personalized intro
    │   ├── volume-templates.md     ← email/DM templates for volume tier
    │   ├── reply-routing.md        ← reply triage decision tree
    │   └── bump-templates.md       ← bump cadence templates
    ├── workflows/                  ← Playwright browser recipes (per-platform)
    │   ├── twitter-dm.md
    │   ├── instagram-dm.md
    │   ├── linkedin-dm.md
    │   ├── skool-dm.md
    │   ├── gmail-send.md
    │   ├── twitter-post.md
    │   └── x-profile-edit.md
    ├── phase-0.1-youtube-discovery/ ← second discovery batch (YouTube + LinkedIn)
    │   ├── CONTEXT.md
    │   ├── output/                 ← 40+ enriched lead files
    │   ├── targets/
    │   ├── outreach-message.md
    │   └── questions.md
    └── stages/
        ├── _phase-0-archive/       ← archived phase-0 docs (CONTEXT, templates, batches)
        ├── 01-discovery/CONTEXT.md + output/
        ├── 02-qualification/CONTEXT.md + output/{parked/,_disqualified/}
        ├── 03-enrichment/CONTEXT.md + output/{_resolved/}
        ├── 04-personalization/CONTEXT.md + output/
        ├── 05-send/CONTEXT.md + output/  ← 96 phase-0 canonical files live here
        └── 06-followup/CONTEXT.md + output/{active,dormant,closed-won,closed-lost}/

├── networking-agent/             ← second agent — LinkedIn networking
│   ├── CLAUDE.md                 ← agent-specific instructions
│   ├── README.md                 ← operator-facing overview
│   ├── _config/
│   │   ├── targets.md            ← per-category filter definitions (8 buckets)
│   │   ├── message-templates.md  ← 300-char connect-note templates
│   │   ├── daily-quota.md        ← 20/run cap, MWF cadence, follow-up cap
│   │   ├── exclusions.md         ← never-contact list
│   │   └── holidays.md
│   ├── 01-sources/<category>/    ← saved searches per category
│   ├── 02-discovery/output/<date>/<category>/   ← MWF 02:30 — vetted candidate pools
│   ├── 03-qualify/output/<date>/<category>/     ← MWF 02:50 — ranked send queue
│   ├── 06-send/output/<slug>.md                 ← MWF 05:00 — canonical engagement records (accreted by send + follow-up)
│   ├── 07-track/{accepted,ignored,declined,job-pipeline}/   ← post-send routing
│   ├── 08-followup/              ← Tue/Thu 09:00 — coffee-chat ask DM stage (added 2026-05-04)
│   │   ├── CLAUDE.md
│   │   ├── _config/{coffee-ask-templates,valuable-person-rules,excluded-roles}.md
│   │   ├── 01-sweep/             ← Connections page diff
│   │   ├── 02-classify/          ← value-pass / value-skip per candidate
│   │   ├── 03-anchor/            ← shape 1 (continuation) / 2 (fresh anchor) / 3 (drop)
│   │   ├── 04-draft/             ← templated DM + voice checklist
│   │   ├── 05-review/            ← dry-run gate (operator opt-in only via `dry-run-only` flag — calibration window retired 2026-05-06)
│   │   └── 06-send/              ← appends to ../06-send/output/<slug>.md (no parallel record)
│   └── log/                      ← per-run summaries (counts + anomalies)
```

**Scheduled tasks driving networking-agent:**
- `networking-agent-discovery` — 02:30 Mon/Wed/Fri
- `networking-agent-qualify` — 02:50 Mon/Wed/Fri
- `networking-agent-daily-run` — 05:00 Mon/Wed/Fri (sends)
- `networking-agent-followup-run` — 09:00 Tue/Thu (coffee-ask DMs)

**Scoping principle (Option B):**
- **`memory/` at OS root** holds shared canonical knowledge: person
  dossiers (`memory/people/<slug>.md` — the WHO of every person any agent
  has touched), companies/platforms, decisions, daily logs, taxonomy,
  templates, and inbox. Any agent reads/writes here, but writes to
  `memory/people/` are constrained to dossier sections (Who, Business,
  Stack, Voice, etc.) — never engagement state.
- **Agent folders** (`outreach-agent-arcadia/`, `networking-agent/`,
  future agents) hold per-agent engagement records, configs, skills,
  workflows, and stage outputs. Each engagement record references the
  shared dossier via `dossier_ref` and adds itself to the dossier's
  `## Engagements` table.
- **`conventions.md`** lives at OS root (naming truth applies to every
  project).

**Multi-campaign pattern:** each outreach campaign gets its own top-level
agent folder (e.g., `outreach-agent-arcadia/`,
`outreach-agent-realestate/`). Same pipeline shape, different ICP / voice
/ offer / skills per campaign. They share the `memory/` graph - leads
discovered for one campaign that get rejected can still be visible to
another campaign as `memory/people/<name>.md` entries.

**Folders deliberately NOT pre-created:** `memory/topics/`,
`memory/projects/`. Empty vault folders are noise. Add on first use.

## First agent: `outreach-agent-arcadia` (multi-channel outreach)

ICM-compliant 6-stage pipeline. Lives at
`Aria Agent OS/outreach-agent-arcadia/`.
Each stage has its own `CONTEXT.md` with an **Inputs** table (which files /
sections to load), a **Process** (numbered steps), and an **Outputs** table
(artifact, location, format).

| # | Stage | Job | Tools |
|---|---|---|---|
| 01 | discovery | Find raw leads | WebSearch (Google dorks), Reddit JSON, HN Algolia, GitHub API, Chrome MCP |
| 02 | qualification | Score against ICP, accept/reject | LLM only (reads `skills/icp-scoring-rubric.md`) |
| 03 | enrichment | Add context per lead | Chrome MCP (public profile pages), WebSearch |
| 04 | personalization | Draft multi-channel send package | LLM only (reads `_config/voice.md`, `_config/offer.md`, `skills/hook-library.md`) |
| 05 | send | Dispatch across ALL channels per person | Playwright MCP (browser-automated sends on all platforms), Gmail MCP (email) |
| 06 | followup | Handle replies + manual-trigger bumps | Gmail MCP (optional), Playwright MCP; **no scheduler** - bump dates in lead frontmatter, fired via `/followup` |

**Lead model (Option B):** each person has TWO files:
1. **Dossier** at `memory/people/<slug>.md` — who they are. Shared
   across all agents. Contains Who, Business, Stack, Voice, Audience
   metrics, Engagement signals, Disqualifiers, Related, Engagements
   table. No outreach state.
2. **Engagement record** at `outreach-agent-arcadia/stages/<NN>/output/<slug>.md`
   — what THIS agent did about this person. Owned by exactly one agent.
   Frontmatter carries engagement state (status, sent_at, sent_channel,
   failed_channels, primary_channel, secondary_channel, segment, priority).
   Body has Why-this-engagement, Discovery angle, Outreach messages,
   Outreach log. **Engagement files MOVE between stage `output/` folders
   to encode pipeline state.** No DB.

**Person-by-person send workflow:** the unit of work at send time is ONE
PERSON. For each person, attempt every available channel in order: email,
Instagram DM, Twitter DM, LinkedIn DM, any other. The engagement record's
`sent_channel` field and outreach log are updated after every successful
send, and `failed_channels` after every failure (with reason). The
dossier in `memory/people/` is NOT touched by send actions — only by
enrichment when new facts about the person are learned. Never batch
updates across people. Never move to the next person until the current
person's engagement record is fully up to date.

### Inputs (all resolved)

All config files are populated: `_config/icp.md` (creators $20k+/mo),
`_config/voice.md`, `_config/offer.md` (DFY $7.5k-$15k), `_config/send-protocol.md`
(50/day volume target).

## The five non-negotiable ICM rules

1. **One stage, one job.** A research stage doesn't write. A writer doesn't
   send. Otherwise stages bloat and per-stage context budgets blow.
2. **Plain markdown only.** No JSON, no SQLite, no proprietary formats.
   Anything you can't open in a text editor breaks the "every output is an
   edit surface" property.
3. **Files move, they don't get copied.** A lead is in exactly one folder.
   State is unambiguous.
4. **Configure the factory, not the product.** ICP / voice / offer go in
   `_config/` once. Per-run details stay in lead files.
5. **One-way references.** Stage N reads stage N-1's output. Stage N never
   reads stage N+1's output. Prevents loops, keeps the pipeline linear.

## Vault discipline (for any agent writing into the OS-root vault)

Five moves an agent must obey:

1. **Single dossier per person at `memory/people/<slug>.md`.** Every agent
   that engages a person reads (and may extend) this dossier. No agent
   creates a parallel dossier inside its own folder. Dossier writes are
   limited to identity sections (Who, Business, Stack, Voice, Audience,
   Engagement signals, Disqualifiers, Related, Notes) — never engagement
   state.
2. **One engagement record per agent×person pair**, at
   `<agent>/<stage>/output/<slug>.md`. The agent owns this file and
   moves it between its stage folders to encode pipeline state. Engagement
   records carry `dossier_ref: '[[memory/people/<slug>]]'` in frontmatter
   and update the dossier's `## Engagements` table on creation.
3. **Use `[[wiki links]]` everywhere.** Plain markdown, agent reads as
   text, Obsidian renders as graph.
4. **Tag against `_taxonomy.md`.** Don't invent new tags. If a needed
   tag is missing, propose it (and add it to `_taxonomy.md`) before using.
5. **Append to today's daily note.** When an agent does meaningful work
   (state-changing actions: engagement moved between stages, decision
   recorded, dossier extended), append a timestamped block to
   `daily/YYYY-MM-DD.md` with backlinks to affected files. Pure reads
   don't need to log.

## Vault risks to manage

These are not design objections - they're things that will bite if ignored.

1. **Decisions folder is load-bearing.** The whole reason an agent gains
   value over time is by remembering past calls ("we tried Acme last
   quarter and they ghosted twice, skip them"). That only works if
   decisions actually get logged at the moment they're made. Without a
   `/decision` slash command or a hook prompting structured logging, the
   folder stays half-empty and untrustworthy. Build `/decision` into
   `.claude/commands/` from day one.

2. **Schema drift.** Six months in, one agent adds `linkedin_last_seen`,
   another adds `lastContacted` (different naming), and Dataview queries
   break while agents read inconsistent shapes. Mitigation: strict
   templates in `templates/`, a write-time hook that validates frontmatter
   against `_taxonomy.md`, and naming conventions enforced from day one.

3. **Concurrent writes.** Once scheduled tasks run, they can collide with
   Cowork sessions writing to the same `daily/YYYY-MM-DD.md` or vault
   entry. Mitigation: structure daily notes as append-only with
   timestamped sections (`## HH:MM - [agent-name] - what happened`) so
   each write is atomic. Don't try to merge cleverly.

4. **Inbox triage cadence.** Without one, `inbox/` becomes a graveyard.
   Decide who triages and when - either user does it weekly, or agents
   triage at end of every meaningful session. Bake into a slash command
   (`/triage`).

5. **Don't pre-build empty folders.** If `topics/` has no content for
   three weeks, it's noise in the file tree. Build `people/`,
   `companies/`, `decisions/`, `daily/`, `inbox/`, `templates/` now -
   add the others on first use.

## How to resume from cold

If a future Claude session arrives here without prior context:

1. Read `CLAUDE.md` at the OS root.
2. Read this `DESIGN.md` for the full architectural context.
3. Read `conventions.md` for naming and operational rules.
4. Check `HISTORY.md` for build status and next steps.
