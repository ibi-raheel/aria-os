# Retention — how long to keep briefings and intermediate outputs

The agent generates ~10 files per weekday (8 briefings + 8 anchor lists + 1 log + 1 daily-log block). Without a retention rule, this grows ~50 files per week.

## Defaults

| Artifact | Retain | Then |
|---|---|---|
| `briefings/<date>/<category>.md` | 90 days | Move to `_archive/briefings/<YYYY-MM>/` |
| `briefings/<date>/<category>-anchors.md` | 90 days | Move to `_archive/anchors/<YYYY-MM>/` |
| `01-fetch/output/<date>/` raw scrapes | 14 days | Delete (intermediate, regenerable) |
| `02-categorize/output/<date>/` bucketed items | 14 days | Delete (intermediate) |
| `log/<date>.md` | 365 days | Move to `_archive/logs/<YYYY>/` |

Reasoning: briefings have downstream consumers (networking-agent reads yesterday's; outreach-agent might reference 7-day-old anchors as fallback) and historical analysis value (grep for patterns). 90 days is enough for trend-spotting without bloating the active tree.

Intermediate stages (01-fetch raw scrapes, 02-categorize bucketed items) are regenerable from sources if needed — 14 days is plenty for debugging recent runs.

Logs are tiny and useful for forensics — keep them long.

## How retention runs

The agent's `/news-run` master command includes a final `prune` step:

```
1. fetch
2. categorize
3. anchor-generation
4. write briefings
5. log
6. prune (this step)
```

Prune logic:
- For each file in `briefings/`, if `<date>` is older than 90 days, move to `_archive/briefings/<YYYY-MM>/`.
- For each file in `01-fetch/output/`, if `<date>` is older than 14 days, delete (or `mv` to `/dev/null` equivalent).
- Same for `02-categorize/output/`.
- For each file in `log/`, if older than 365 days, move to `_archive/logs/<YYYY>/`.

If the prune step fails (file permissions, paths missing), log the failure but don't fail the whole run. The next day's run will retry.

## Manual override

Edit the windows in this file. The agent reads this file at the start of every prune step. Changes take effect the next run.

If you want to keep a specific briefing forever (say, the day a major news cycle hit), copy it to `_archive/keepers/<date>-<note>.md` before the 90-day window expires. Items in `_archive/keepers/` are never pruned.

## Archive folder structure

```
news-agent/_archive/
├── briefings/
│   └── 2026-01/
│       ├── 2026-01-15/
│       │   ├── consulting.md
│       │   ├── consulting-anchors.md
│       │   └── ... (other categories)
│       └── ... (other days)
├── anchors/
│   └── 2026-01/...
├── logs/
│   └── 2026/
│       ├── 2026-01-15.md
│       └── ...
└── keepers/
    └── 2026-04-29-sec-marketing-rule.md
```

Grouping by year-month prevents the archive from becoming a flat folder of thousands of files.

## What to never archive

- Today's briefing — downstream agents are still reading it.
- Yesterday's briefing — networking-agent's 5 AM run uses it as fallback if news-agent fails.
- The current `log/` file (still being written).
