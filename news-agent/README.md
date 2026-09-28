# news-agent

Daily intelligence/news agent for the Aria Agent OS. Runs at 02:00 local on weekdays, pulls news from yesterday across 8 categories (matching networking-agent's buckets), produces consumable briefings + candidate anchor questions, feeds the 05:00 outreach pipelines.

## Quick start

```bash
cd "Aria Agent OS/news-agent/"
# read what's been generated today:
cat briefings/$(date +%Y-%m-%d)/consulting.md
# or any of the 7 other categories
```

## Folder layout

```
news-agent/
├── CLAUDE.md              ← agent identity + rules
├── README.md              ← this file
├── _config/
│   ├── categories.md      ← 8 buckets, what's in each
│   ├── sources.md         ← RSS feeds, dorks, APIs per bucket
│   └── retention.md       ← 90-day window
├── 01-fetch/output/<date>/<source>.md     ← raw scrapes
├── 02-categorize/output/<date>/<category>.md  ← bucketed items
├── 03-anchor-generation/output/<date>/<category>-anchors.md  ← candidate questions
├── briefings/<date>/      ← consumable output (8 .md files per day)
├── log/<date>.md          ← machine-readable run summary
└── _archive/briefings/    ← items >90 days old
```

## Categories (8)

1. consulting — MBB + Deloitte S&O / Strategy& / PwC Strategy
2. real-estate — REIT/CRE/family-office/tenant-rep/RE law
3. founders — peer-level seed → Series B
4. investors-general — VCs/angels outside premier firms
5. yc — Y Combinator partners + program staff
6. a16z — Andreessen Horowitz GPs + partners
7. tier1-vcs — Sequoia, Greylock, Benchmark, Founders Fund, Index, Accel
8. big-tech — VP+ at Meta/Apple/Google/Amazon/Microsoft/Netflix

Laws and regulation are NOT a 9th category — they're a TYPE of news folded into whichever of the 8 buckets they affect.

## How to operate

- **The 02:00 scheduled task** runs `/news-run` automatically Monday–Friday. Skip days are configured in the same Cowork scheduled-task panel.
- **Manual runs:** `/news-run` from inside the OS to refresh briefings on demand.
- **Status check:** `/news-status` shows today's briefings, items per category, anchors generated.
- **Stage-by-stage debugging:** `/news-fetch`, `/news-categorize`, `/news-anchors` run individual stages.

## Free tools used

- Federal Register API (`federalregister.gov/api/v1/`)
- Congress.gov API
- SEC EDGAR (Form D for fund formations, 13F/13G for investor positioning)
- RSS feeds (per-bucket list in `_config/sources.md`)
- WebSearch with date-filtered Google dorks
- YouTube Data API v3 (already configured at OS level)
- Twitter API v2 (bearer token, already configured)
- Reddit JSON API
- Hacker News Algolia API
- Chrome MCP for sites that don't expose RSS or APIs (sparingly)

## Output contract for downstream agents

Every briefing item carries 4 fields:
- `source_url` — direct link to the article/post/filing
- `published_date` — ISO date, in the source's stated timezone
- `verbatim_excerpt` — quoted line or short paragraph from the source (no paraphrase)
- `summary` — 2-paragraph agent-written distillation

Every anchor in `<category>-anchors.md` references the briefing item it's derived from.

If any field is missing on a fetched item, that item drops. Empty buckets are written as "No notable items in this category for <date>" — never padded with stale or invented content.

## Status

- [x] Scaffolded 2026-04-29
- [ ] First fetch run (manual `/news-run` test)
- [ ] Scheduled task registered (`/news-run` at 02:00 weekdays)
- [ ] Integration confirmed with networking-agent's 05:00 run
