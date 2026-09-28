# Aria Agent OS — Localhost Dashboard

A polished read-only dashboard over your agent OS. Reads files **directly** from the OS folder — no cached data layer. If a number on the dashboard looks weird, click through and the source file opens in Obsidian. The file IS the source of truth.

## What it shows

Two tabs:

### Operations tab

- **Hero stats** — sends today, briefings produced, latest integrity verdict, tokens used
- **Scheduled tasks** — 6 known tasks with "ran today" / "queued" status (inferred from daily log)
- **Memory health** — counts of people, companies, decisions, integrity reports, daily logs, inbox; `_INDEX.md` staleness
- **Today's pipeline** — per-stage counts: news → discovery → qualified → sent
- **Recent activity timeline** — every timestamped block from today's daily log

### CRM tab

- One row per person, aggregated from `memory/people/` (dossiers) + every agent's engagement records
- Status pill (Replied / Sent / Drafted / Qualified / Enriched / No engagement / Orphan)
- Last touch date, platform, segment, engagement count
- Agent badges (Outreach / Networking) showing which agents have engagements with this person
- Search by name / platform / slug / segment
- Filter by status
- Click any row → opens dossier in Obsidian (or first engagement record if no dossier exists)
- Surfaces "orphans" — engagement records that exist with no matching dossier (data integrity hint)

Click anything to open the corresponding file in Obsidian.

## Setup

One-time:

```bash
cd "/Users/aria/Documents/Aria Agent OS/dashboard"
npm install
```

Run:

```bash
node server.js
```

Then open `http://localhost:4321` in any browser.

## Auto-refresh

The page refreshes every 30 seconds. Manual refresh button in the header.

## Token tracking — how it works

The dashboard reads `tokens: ~N` or `tokens_used: N` patterns from each timestamped block in `memory/daily/<today>.md`. Until each scheduled task is instrumented to write its own token count to its daily-log entry, this section will show "0 — none recorded yet."

To wire it up, update each scheduled task's prompt to include a final step like:

> After your run completes, append a line `tokens: ~<N>` to the timestamped block you wrote in `memory/daily/<today>.md`, where `<N>` is your approximate token usage for this session.

Future runs auto-populate the dashboard.

## Data sources

| Panel | Reads from |
|---|---|
| Sends today | `networking-agent/06-send/output/*.md` (mtime today) |
| Briefings | `news-agent/briefings/<today>/*.md` |
| Integrity | latest `memory/integrity/validate-*.md` |
| Tokens | `memory/daily/<today>.md` (parsed from `tokens:` lines) |
| Scheduled tasks | `memory/daily/<today>.md` (inferred from `## HH:MM — agent — ...` headers) |
| Memory stats | `memory/people/`, `memory/companies/`, `memory/decisions/`, `memory/integrity/`, `memory/daily/`, `memory/inbox/` |
| Pipeline counts | discovery `candidates.md`, qualify `ranked.md`, send `output/*.md` |
| Recent activity | `memory/daily/<today>.md` block headers |
| _INDEX age | `memory/_INDEX.md` mtime |
| CRM | `memory/people/*.md` (dossiers) + frontmatter from every engagement record across `outreach-agent-arcadia/stages/*/output/` and `networking-agent/06-send/output/`, `networking-agent/07-track/*/` |

## Architecture

```
dashboard/
  server.js          Node + Express server (~210 lines, no build step)
  public/index.html  single-file UI (HTML + inline CSS + inline JS)
  package.json       only dep: express
```

No build pipeline. No database. No cache. Edit a file in the OS, hit refresh, see the change.

## Troubleshooting

**"Cannot find module 'express'"** → run `npm install` first.

**Port 4321 already in use** → set a different port: `PORT=5173 node server.js`.

**Click on a row doesn't open Obsidian** → the dashboard issues `open obsidian://...` URLs. Make sure Obsidian is installed and your vault is named exactly `Aria Agent OS`. If you renamed the vault, change `VAULT_NAME` in `server.js`.

**Dashboard shows 0 for everything on first load** → expected if today's pipeline hasn't run yet. The autonomous chain fires at 02:00 weekdays. Tomorrow morning the dashboard should populate.

## What's NOT in v1

Deferred to v2 (when needed):

- Send breakdown by category (8-bucket grid with anchor coverage)
- Trend lines over the last 7 days
- Issue surface (parsed integrity reports)
- Mobile / multi-device access (Tailscale or cloud-deploy this)
- Token tracking actually wired up (needs scheduled-task instrumentation)
