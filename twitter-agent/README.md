# twitter-agent

Daily Twitter/X posting + audience engagement for **Arcadia**. **3 posts/weekday MINIMUM** at 12:00 / 18:00 / 20:00 ET (anchor + 2 filler), 3 substantive engagements/day on the gaming + AI/tech ICP cohort.

> **State (2026-05-10):** **ACTIVE.** Day 1 shipped 2026-05-10. Migrated to Playwright MCP + 6-task pipeline with Slack approval loop. Decision: `memory/decisions/2026-05-10-twitter-agent-playwright-migration-and-slack-approval-loop.md`. Anchor/filler hierarchy: slot 1 is the daily anchor (feature spotlight from 7-day rotation, Arcadia image MANDATORY); slots 2-3 are filler (visual optional, text-only fine). Skip not allowed — quality enforced through rewrite + fallback content tracks.

## Quick reference

| | |
|---|---|
| Daily target | **3 posts MINIMUM** (Mon-Sun) - slot 1 anchor 12:00 ET + slots 2 & 3 filler 18:00 / 20:00 ET |
| Daily engagements | **3 substantive replies/QTs MINIMUM** on cohort posts (gaming + AI/tech) |
| Send mechanism | Playwright MCP on persistent Chromium browser with x.com session |
| Slot 1 visual | **MANDATORY** Arcadia image (per marketing-brain.md Gate 3) |
| Slot 2-3 visual | Optional, Arcadia-only if attached; charts/graphs/external visuals forbidden |
| Char target | 80-180 (research-backed; reference tweets average ~125) — hard cap 280 |
| Replies | Mentions + own-comments swept daily, dry-run by default |
| Engagement ICP | Gaming industry + tech/AI industry (broad). Cohort self-generates if uncurated |
| Content scope | Arcadia only (whitelist in `_config/content-sources.md`) |

## How to run

**Auto:** 6 scheduled tasks drive the pipeline (register via `/twitter-register-tasks`):
- `twitter-agent-prep` — 06:00 ET daily: signals + drafts + screenshots + engagement targets, sends review bundle to Slack `#twitter-arcadia`
- `twitter-agent-post-1` — 12:00 ET: reads Slack approval, posts slot 1 (anchor) + 3 engagement replies
- `twitter-agent-post-2` — 18:00 ET: reads Slack approval, posts slot 2
- `twitter-agent-post-3` — 20:00 ET: reads Slack approval, posts slot 3
- `twitter-agent-daily-metrics` — 23:00 ET: scrapes engagement metrics for last 30 days
- `twitter-agent-weekly-metrics` — Sunday 23:00 ET: weekly rollup + Slack summary

**Manual:** From any folder in OS:
- `/twitter-prep` — full prep pipeline (what the 06:00 task runs)
- `/twitter-post` — post a slot (what the post-1/2/3 tasks run)
- `/twitter-status` — read-only state
- Or any individual stage: `/twitter-signals`, `/twitter-draft`, `/twitter-screenshot`, `/twitter-respond`, `/twitter-engage`, `/twitter-track`

## Folder structure

```
twitter-agent/
├── README.md                ← this file
├── CLAUDE.md                ← agent-specific instructions
├── _config/                 ← voice, content-sources, cadence, reply-rules, engagement-rules, safety
├── 01-signals/<date>/       ← daily content seeds (git, design, decisions)
│   └── inbox/               ← drop manual seed ideas here
├── 02-draft/<date>/         ← drafts for the 3 slots
├── 03-review/               ← drafts awaiting operator OK (dry-run holding pen)
├── 04-posted/<date>/        ← canonical posted records (one per tweet, with URL + post_id)
├── 05-replies/              ← mention-handling pipeline (queue / draft / posted)
├── 06-engagement/<date>/    ← outbound engagement records (likes + replies on followed creators)
├── 07-metrics/<date>/       ← post-fact engagement metrics on prior posts
├── screenshots/<date>/      ← captured visuals referenced in posts
└── log/<date>.md            ← daily run log
```

## Remaining setup tasks

1. Operator: profile rebuild in Twitter UI — banner image, profile pic, bio (variant C with logistics from 2026-05-09), website field.
2. Operator: clean offensive test course in Arcadia `/dashboard/courses` so the kiln screenshot is shippable.
3. Bootstrap Arcadia visual library across all 7 rotation features (currently only world-spawn captured fresh).

## See also

- `CLAUDE.md` — agent-specific rules
- `_config/voice.md` — Twitter voice (separate from `Arcadia/design/system/voice.md` which is product copy voice)
- `../CLAUDE.md` — OS routing rules
- `../networking-agent/` — sibling agent (different goal, same scaffold patterns)
- `memory/decisions/2026-04-29-arcadia-loom-pivot-strategy.md` — related but distinct: outreach-agent's deferred Twitter DM pivot (not what this agent does)
