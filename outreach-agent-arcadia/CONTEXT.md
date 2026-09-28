# outreach-agent-arcadia - Workspace

## Purpose

Lead-generation and outreach pipeline that lands the first 10 paying
customers for **Arcadia** (currently sold as a $7.5k–$15k done-for-you
Realm-setup engagement). Six-stage ICM workflow.

## Process

1. **Discovery** finds creators earning $20k+/month across community platforms (Skool, Twitter, YouTube, LinkedIn).
2. **Qualification** scores them against the ICP rubric, accepts ~3-5/week.
3. **Enrichment** builds a comprehensive dossier per accepted lead.
4. **Personalization** drafts the multi-channel send package (Loom shot-list
   + per-channel messages).
5. **Send** dispatches via Playwright browser automation (all platforms).
   Agent reads `workflows/` for per-platform steps and sends autonomously.
6. **Followup** handles bumps and replies, routes warm leads to a
   user-sent Calendly link.

## Files in this workspace

- `CLAUDE.md` - agent identity + routing into stages
- `CONTEXT.md` - this file
- `_config/` - factory config (ICP, voice, offer, send-protocol). Edit
  these to change *what* the agent does without touching *how*.
- `workflows/` - repeatable browser tasks (DMs, emails, posts, profile
  edits). Each .md file is a self-contained Playwright recipe the agent
  executes autonomously. New browser tasks get new workflow files.
- `shared/` - cross-stage references (currently empty; add as patterns
  emerge)
- `skills/` - rubrics, libraries, templates the stages call
- `stages/` - the six numbered stages, each with its own `CONTEXT.md` and
  `output/` folder. Also contains `_phase-0-archive/` (originals from
  the initial phase-0 discovery batch).
- `phase-0.1-youtube-discovery/` - second discovery batch (YouTube +
  LinkedIn sourced). Separate from stages; will migrate after sends.

## What good looks like

- Each stage produces output that the next stage can act on without
  re-doing work.
- Lead files **move** between `stages/N/output/` folders rather than
  being copied - the location encodes the state.
- Every meaningful action lands in the OS-root vault: stub or update
  to `memory/people/<name>.md`, timestamped block in `logs/daily/YYYY-MM-DD.md`.
- Decisions worth remembering (closed-won, closed-lost with reason,
  ICP refinements) become `memory/decisions/...md` files.
- 8–16 weeks from today the agent has produced 10 closed-won deals
  with full case-study data captured for the platform launch.

## What to avoid

- Skipping enrichment to "just send something." Generic outreach to
  $20k+/mo creators is dismissed instantly.
- Inventing tags or schemas not in `memory/_taxonomy.md` or `memory/templates/`.
- Storing canonical knowledge inside this folder instead of in the
  OS-root vault. Lead files here are operational; world-facts go to
  `memory/people/`, `memory/companies/`, `memory/decisions/`.
- Sending without checking daily caps, quiet hours, and voice.md rules.
- Spending more than 75 min of agent time on enrichment for one lead.
  Ship the dossier with `unknown` fields rather than perfect-paralyzing.

## Tools this workspace uses

- **Playwright MCP** (`@playwright/mcp`) - primary tool for all browser
  tasks: sending DMs (Twitter, Instagram, LinkedIn, Skool), sending emails
  (Gmail), posting tweets, editing profiles. Per-platform steps live in
  `workflows/`. Agent reads the workflow file and executes autonomously.
- **Gmail MCP** (claude.ai connector) - email draft fallback if Playwright
  has issues with Gmail. Also used for inbox monitoring in stage 06.
- **`WebSearch` (built-in)** - discovery via Google `site:` queries
- **`web_fetch` (built-in)** - direct URL fetches, Reddit/HN/YouTube JSON APIs, Substack pages
- **YouTube Data API (free tier, no MCP needed)** - subscriber counts, video stats via `web_fetch`

**Bump cadence is manually triggered** via `/followup` slash command - no
scheduler. Lead frontmatter carries `bump_1_due` / `bump_2_due` /
`dormant_after` / `re_touch_after` date fields; `/status` flags what's due
today.

## Open questions

- **Final pricing.** Anchored at $7.5k-$15k tentative. Refine after first
  2-3 sales calls tell us what people will pay.
- **Loom personalization depth.** Hybrid (30s personalized intro + 2 min
  reusable demo) is the working assumption. Refine after first 5 sends
  measure reply rate.
