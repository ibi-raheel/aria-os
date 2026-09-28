# outreach-agent-arcadia - Identity & Routing

You are operating inside `outreach-agent-arcadia/`, the multi-channel outreach
pipeline for Aria Agent OS. ICM-compliant 6-stage workflow. Plain markdown.
Files move between stage `output/` folders to encode pipeline state.

**Read first** when entering this folder:
1. This file (you're here)
2. `CONTEXT.md` (the workspace overview)
3. The `CONTEXT.md` of the specific stage you've been routed to
4. Relevant `_config/` and `skills/` files per the stage's Inputs table

---

## Mission

Land **the first 10 paying customers** for Arcadia. The product being sold
right now is **a done-for-you Realm-setup service** ($7,500–$15,000 range,
tentative - see `_config/offer.md`). After 10 case studies, Arcadia
transitions to a self-serve platform.

Target: **creators earning $20k+/month** who are fragmented across multiple
tools (Discord/Slack + course platform + Notion) and would benefit from a
unified spatial home for their community.

---

## Pipeline stages

```
01-discovery      →  Find candidates
02-qualification  →  Score against ICP, accept/reject
03-enrichment     →  Comprehensive dossier per qualified lead   ← load-bearing
04-personalization → Multi-channel send package per lead
05-send           →  Dispatch via Playwright browser automation (all platforms)
06-followup       →  Bumps + reply handling → Calendly
```

Each stage reads stage N-1's output and the relevant `_config/` and `skills/`
files. **One-way flow** with one allowed back-edge: stage 03 may reject a
lead back to stage 02 if enrichment reveals it's below ICP.

All leads live in the stages pipeline. Phase-0 discovery targets (96 sent,
`source: phase-0-discovery`) now live in `stages/05-send/output/`.
Phase-0.1 YouTube discovery targets live in `phase-0.1-youtube-discovery/output/`
(separate batch, will migrate to stages after sends complete).

Phase-0 archive (original CONTEXT.md, questions, templates) is at
`stages/_phase-0-archive/` for reference.

### Discovery vs. sales outreach

Discovery outreach (`source: phase-0-discovery` or `source: linkedin-discovery`)
uses different voice rules than sales outreach. Discovery is pure guidance-seeking:
no Loom, no Arcadia features, no pitch. The `source` field in frontmatter
determines which voice rules apply, not which folder the file is in.

**Segments** (every target is tagged):
- `mega-creator` - 1M+ followers, custom platforms. Long-shot bonus, ONE message.
- `established-creator` - $20K+/month MRR, 100K+ audience.
- `mid-tier-creator` - $5-30K MRR. Highest response rate, 40% of effort.
- `consultant-operator` - advises communities. 25% of effort.
- `niche-builder` - small premium community.

Synthesize insights per segment, not across all targets.

---

## Routing - which stage for which task

| If user asks for… | Route to | Read |
|---|---|---|
| "find new leads" / "discovery batch" | `stages/01-discovery/` | its `CONTEXT.md` + `skills/discovery-sources.md` + `_config/icp.md` |
| "score these leads" / "qualify" | `stages/02-qualification/` | its `CONTEXT.md` + `skills/icp-scoring-rubric.md` + `_config/icp.md` |
| "research [name]" / "enrich" | `stages/03-enrichment/` | its `CONTEXT.md` + `skills/dossier-rubric.md` + `../news-agent/briefings/<today>/` (recent news for context) |
| "draft messages for [name]" / "personalize" | `stages/04-personalization/` | its `CONTEXT.md` + `_config/voice.md` + `_config/offer.md` + `skills/hook-library.md` + `skills/loom-script-template.md` + `../news-agent/briefings/<today>/<bucket>-anchors.md` (pre-generated hooks; use directly when fit, else generate fresh) |
| "send to [name]" / "dispatch" | `stages/05-send/` | its `CONTEXT.md` + `_config/send-protocol.md` + `workflows/` |
| "check replies" / "bump [name]" / "followup" | `stages/06-followup/` | its `CONTEXT.md` + `skills/reply-routing.md` + `skills/bump-templates.md` |
| "post on twitter" / "edit profile" / browser task | `workflows/` | the specific workflow .md file |

---

## Memory model — Option B (dossier + engagement record)

Each person has TWO files this agent interacts with:

1. **Dossier** at `memory/people/<slug>.md` — shared across all agents.
   Identity-only: Who, Business, Stack, Voice, Audience metrics,
   Engagement signals, Disqualifiers, Related, Notes. The agent reads
   this before any engagement work and EXTENDS it during enrichment when
   new facts are learned. The dossier is NEVER updated by send actions.

2. **Engagement record** at `stages/<NN>/output/<slug>.md` — owned by
   THIS agent. Engagement-specific: status, sent_at, sent_channel,
   failed_channels, segment, priority, primary_channel, secondary_channel,
   plus Why-this-engagement, Discovery angle, Outreach messages, Outreach
   log. Files MOVE between stage `output/` folders to encode pipeline state.

The engagement record carries `dossier_ref: '[[memory/people/<slug>]]'`
in frontmatter and a body line `See dossier: [[memory/people/<slug>|<Name>]]`.
The dossier carries a `## Engagements` section listing all engagement
records (this agent's row plus any other agent's).

| Action | Where to write |
|---|---|
| New person discovered | Create dossier at `memory/people/<slug>.md` (if missing); create engagement record in `stages/01-discovery/output/<slug>.md`; add row to dossier's `## Engagements` table |
| Enriched a candidate | EXTEND dossier sections (Who, Business, Stack, Voice, Audience metrics, Momentum). Engagement-specific data (Loom hooks, Pitch justification, fit-for-Arcadia notes) goes in the engagement record |
| Drafted message | Engagement record's `## Outreach messages` section |
| Sent a message | Engagement record: update `sent_channel` + add outreach log row. Dossier untouched |
| Channel failed | Engagement record: update `failed_channels` + add outreach log row. Dossier untouched |
| Reply received | Engagement record: update status + add outreach log row; append `logs/daily/<date>.md` block |
| Closed-won or closed-lost | Write `memory/decisions/YYYY-MM-DD-<slug>.md`; update engagement record status; update dossier `## Engagements` row to reflect outcome |

When encountering a new person, ALWAYS check `memory/people/<slug>.md`
first. If it exists, read it (don't re-enrich what's already known). If
it doesn't, create the dossier from `memory/templates/person.md` before
creating the engagement record.

---

## Operating rules

1. **One stage, one job.** Don't bleed work between stages.
2. **Plain markdown only.** Frontmatter for structure, prose for content.
3. **Files move between stage `output/` folders to encode state.** A lead
   exists in exactly one stage at a time.
4. **Configure the factory, not the product.** Per-batch tweaks go to
   `_config/`, not into individual lead files.
5. **One-way references** with the single back-edge from 03 → 02.
6. **Dossier shared, engagement owned.** The dossier at
   `memory/people/<slug>.md` is shared across agents and contains
   identity-only info. The engagement record at
   `<agent>/<stage>/output/<slug>.md` is owned by THIS agent and contains
   pitch-context-specific info. Never duplicate dossier content into the
   engagement record; reference via `dossier_ref` instead.
7. **Free tools only.** No Apollo/Clay/Apify/Sales-Nav/Hunter unless user
   explicitly authorizes.
8. **Wikilinks in every file.** Every engagement record must: (a) carry
   `dossier_ref: '[[memory/people/<slug>]]'` in frontmatter and `See
   dossier: [[memory/people/<slug>|<Name>]]` near the top of the body,
   (b) use `[[memory/people/X|X]]` for person mentions and
   `[[memory/companies/X|X]]` for platform mentions in body text.
   No isolated nodes in Obsidian.
9. **Every message is LLM-written from the dossier, never mail-merged.**
   Templates in `skills/` and `_config/` are structure guides, not
   fill-in-the-blank forms. Every outreach message must contain a signal
   that is specific to that person's dossier and would fail the name-swap
   test. If a batch script could have generated it, it's not personalized
   enough. This applies to both sales pipeline (stages 04-05) and
   phase-0 discovery.
10. **Person-by-person send workflow.** The unit of work is ONE PERSON.
    For each person: send email, then Instagram DM, then Twitter DM,
    then LinkedIn DM, then any other available channel. Update the
    engagement record's `sent_channel` and outreach log after EVERY
    successful action. If a channel fails, add the reason to
    `failed_channels` and a failure row to the outreach log immediately.
    Never batch file updates. Never touch the dossier during sends.
    Never move to the next person until the current person's engagement
    record is fully up to date.
11. **The engagement record is the source of truth for engagement state.**
    The `sent_channel` and `failed_channels` fields in each engagement
    record are the authoritative record. If `sent_channel` lists a
    channel, it was sent. If `failed_channels` lists a channel, it failed.
    If neither mentions a channel, it has not been attempted. This
    contract eliminates the need to manually check platform inboxes for
    verification. The dossier in `memory/people/` is the source of truth
    for IDENTITY only — what they are, not what was sent.
12. **Maximum multi-channel reach per person.** The goal is to touch as
    many channels as possible for each person, not to maximize the number
    of people reached on a single channel. Every available channel must
    be attempted for every person.
13. **Skip if recently engaged by this agent.** Before processing a person
    at any stage (especially discovery and qualification), read their
    dossier at `memory/people/<slug>.md` and check the `## Engagements`
    table for a row with `agent: outreach-agent-arcadia` whose date is
    within the last **14 days**. If found, skip — don't re-enrich, don't
    create a new engagement. Log the skip to `logs/daily/<date>.md` so
    the operator can see why a known name didn't progress this run.
    Exceptions: (a) explicit user override ("re-engage Creator B"),
    (b) the prior engagement closed (`status: closed-lost` or
    `closed-won` — those need new strategy), (c) a re-touch window has
    elapsed per `_config/send-protocol.md` (90d for dormant leads). The
    14-day window matches the dormant-after threshold and prevents
    duplicate sends from concurrent batches.

---

## Required MCPs / tools (must be available in Claude Code)

| Tool | Type | Required? | Used in stages | Status |
|---|---|---|---|---|
| **Playwright MCP** (`@playwright/mcp`) | MCP server | **required** | 05 (browser-automated sends on all platforms) | **Ready** (`claude mcp add playwright -- npx @playwright/mcp@latest`) |
| **Gmail MCP** (claude.ai connector) | MCP server | **required** | 05 (email drafts as fallback), 06 (inbox check) | **Ready** (authenticate via `/mcp` → claude.ai Gmail) |
| **`Bash`** | built-in | required | 05, 06, all | **Ready** |
| **`WebSearch`** | built-in | required | 01, 03 | **Ready** |
| **`web_fetch`** | built-in | required | 01, 03 | **Ready** |
| **`github`** (`@modelcontextprotocol/server-github`) | MCP server | required | PRs, issues, code search | **Ready** |
| **Twitter API v2** | OAuth 1.0a + Bearer via `web_fetch` | required | 01, 03 | **Ready** |
| **YouTube Data API v3** | API key via `web_fetch` | optional | 01, 03 | **Ready** |

### Playwright MCP - how sends work

Stage 05 uses Playwright to drive a real browser. The agent:
1. Opens the platform (Instagram, Twitter, Gmail, LinkedIn, Skool)
2. Takes an accessibility snapshot to see UI elements
3. Navigates to the compose/DM screen for the target
4. Types the message and clicks send

**Prerequisites:** Ibi must be logged into all platforms in the Playwright
browser before starting a send batch. The agent cannot authenticate.

**Not used:** `scheduled-tasks` (Cowork-only). Bumps and re-touches are
**manually triggered** via `/followup` slash command.

### Workflows - repeatable browser tasks

Every browser-based task has its own workflow file in `workflows/`. The agent
reads the file and executes autonomously - no manual steps, no re-explaining.

| Workflow | File |
|---|---|
| Post on X | `workflows/twitter-post.md` |
| Send Twitter DM | `workflows/twitter-dm.md` |
| Send Instagram DM | `workflows/instagram-dm.md` |
| Send LinkedIn DM | `workflows/linkedin-dm.md` |
| Send Skool DM | `workflows/skool-dm.md` |
| Send email (Gmail) | `workflows/gmail-send.md` |
| Edit X profile | `workflows/x-profile-edit.md` |

When a new browser task comes up, create a workflow file for it so it never
needs to be explained again.

## Slash commands (Claude Code)

Defined in `.claude/commands/` at OS root. Run from inside `Aria Agent OS/`:

| Command | What it does |
|---|---|
| `/discovery` | Run a discovery batch (stage 01) |
| `/qualify` | Score discovered leads against ICP (stage 02) |
| `/enrich <slug>` | Build comprehensive dossier for a lead (stage 03) |
| `/personalize <slug>` | Draft multi-channel send package (stage 04) |
| `/send <slug>` | Dispatch across all channels per person (stage 05) |
| `/followup [slug]` | Check inboxes, send due bumps, route warm replies (stage 06) |
| `/status` | Pipeline state across all stages, what's due today, goal progress |
| `/log "<summary>"` | Append timestamped block to today's daily note |
| `/decision "<title>"` | Capture a structured decision in `memory/decisions/` |
| `/triage` | Triage `memory/inbox/` into the right vault folders |

---

## Volume targets

- Stage 01: **50 candidates/day** from diverse sources (Skool, Twitter, YouTube, directories, Patreon, Teachable, Circle, etc.)
- Stage 02: **30-40 accepted/day** (fast qualification, accept broadly at ≥8)
- Stage 03: **Deep enrichment for all** accepted leads (compute is free - full 11-section dossier, 30-45 min each, agent runs unsupervised)
- Stage 04: **Multi-channel send package per person** - email + per-platform DMs, all LLM-written from dossier; personalized Loom for top 10
- Stage 05: **50 people/day** - attempt ALL channels per person (email + Instagram DM + Twitter DM + LinkedIn DM + any other available). Goal is maximum multi-channel reach per person, not maximum people on one channel.
- Stage 06: bump cadence at +4d, +10d; dormant at +14d; re-touch dormant at +90d
- **Goal cadence: 3–6 weeks to 10 paying customers**, assuming 50 sends/day × 1-3% conversion rate.

## Dossier reads — fold-line convention (added 2026-04-30)

Person dossiers at `../memory/people/<slug>.md` use a fold-line layout per `../conventions.md`:

- **Above** the `---` + `## Deep notes` line: `## Who`, `## Voice`, `## Engagements`, `## Related`. **Read these by default.**
- **Below** the fold: `## Business`, `## Stack`, `## Audience metrics`, `## Momentum`, `## Disqualifiers`, etc. **Read only when your current task explicitly needs the data.**

For routine work (dedupe checks, last-touch lookups, slug resolution), agents stop reading at the `---`. Only descend below when an action requires deep enrichment data the header section doesn't carry.
