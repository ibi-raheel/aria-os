---
title: Posting cadence + day-N anchor
updated: 2026-05-10
---

# Cadence

```yaml
# === 3-slot/day cadence (decision: 2026-05-09-twitter-agent-3-slot-restart-and-ICP-pivot) ===
# Overrides the 2026-05-06 1-slot decision after Day 2 + Day 3 deletions.
# Operator directive 2026-05-09: 3 posts/day + 3 engagements/day are MANDATORY MINIMUMS.
# The agent does NOT have permission to skip slots. Quality is enforced through *rewrite* and
# *fallback content tracks* (see marketing-brain.md), never through cutting volume.
# All visuals attached to tweets must be Arcadia product visuals only — no charts, no graphs,
# no external imagery. Per marketing-brain.md Gate 3 + evergreen rotation library.

slots_per_day: 3
slot_times:
  slot_1: "12:00 ET"   # ANCHOR — build-in-public / Day-N; posted by twitter-agent-post-1 task
  slot_2: "18:00 ET"   # filler — insight / hot-take; posted by twitter-agent-post-2 task
  slot_3: "20:00 ET"   # filler — news / reshare with sharp take; posted by twitter-agent-post-3 task

engagements_per_day: 3   # replies / quote-tweets on ICP cohort posts
engagement_window: "posted with slot 1 at 12:00 ET after Slack approval"

weekday_only: false    # agent runs all 7 days (Mon-Sun)
holidays_file: "../../networking-agent/_config/holidays.md"

content_track_per_slot:
  slot_1: feature_spotlight                    # Daily feature rotation; name + screenshot + one sharp line; Arcadia image MANDATORY
  slot_2: insight_or_hot_take                  # conviction post, named competitor flaw; visual optional
  slot_3: news_commentary_or_curated_reshare   # quote-with-take on industry news; text-only by default

feature_rotation: "_config/feature-rotation.md"   # 7-day cycle through Arcadia surfaces

day_n:
  start_date: 2026-05-10                    # Day 1 shipped 2026-05-10
  current_n_on_start: 1                     # Day 1 anchors here
  monotonic: true                           # never skip a day's number
  format: "Day [N]."                        # placement: closer-not-opener per marketing-brain.md hook ban-list

# === Pipeline architecture (decision: 2026-05-10 Playwright migration + Slack approval loop) ===
# Replaces the monolithic twitter-agent-daily-run with 6 discrete scheduled tasks.
# Native Twitter scheduler is NO LONGER used — each slot has its own posting task.
# All browser work uses Playwright MCP (Chrome MCP retired).

pipeline:
  prep_task: "twitter-agent-prep"           # 06:00 ET — generate drafts + screenshots + engage targets + Slack review
  post_tasks:
    slot_1: "twitter-agent-post-1"          # 12:00 ET — read Slack approval, post slot 1 + 3 engagements
    slot_2: "twitter-agent-post-2"          # 18:00 ET — read Slack approval, post slot 2
    slot_3: "twitter-agent-post-3"          # 20:00 ET — read Slack approval, post slot 3
  metrics_tasks:
    daily: "twitter-agent-daily-metrics"    # 23:00 ET — scrape engagement on recent posts
    weekly: "twitter-agent-weekly-metrics"  # Sunday 23:00 ET — holistic rollup
  slack_channel: "#twitter-arcadia"
  slack_channel_id: "C0B1R99G9FV"
  approval_flow: "prep sends bundle to Slack; operator replies approved/rewrite/reject; posting tasks read thread"
```

## Engagement spec (3/day with ICP cohort) — NEW 2026-05-09

ICP for Twitter audience-building (broad — operator directive 2026-05-09):

- **Gaming industry** (broad). Indie game devs, game designers, gaming creators, cozy/community/social-sim builders, Phaser/Godot/Unity Twitter, gaming-tech investors.
- **Tech / AI industry** (broad). AI researchers, dev-tool builders, AI founders, tech operators in agent / tooling / community-software space.

Note: this is **audience ICP** — who Arcadia's Twitter strategy targets for follower growth. Distinct from **product-buyer ICP** (paying-community creators on Skool / Circle / Mighty / Discord) — that's who pays, not who we engage with on Twitter.

### How the agent picks engagement targets

- Each Sunday, operator OR agent generates a weekly cohort to `_config/engagement-cohorts/<YYYY-WW>.md` — minimum 15 handles, target 20-25.
- Daily, agent walks the cohort, picks 3 posts with concrete hooks (specific claim, named competitor, technical detail), and drafts replies/quote-tweets.
- Replies must add a layer (insight, contrarian take, related angle, gentle question that opens a thread). No "great post" / "love this" / single-emoji replies.
- Default mode: drafts to `06-engage/<date>/` for operator approval. Live mode flips when operator confirms quality.

### Cohort generation (when uncurated)

If `_config/engagement-cohorts/<this-week>.md` is missing or empty, the agent:
1. Walks Twitter searches for gaming + AI/tech keywords (e.g., "indie game dev posting in last 24h", "AI founder commenting on community tools")
2. Filters by: ≥1K followers, posted in last 24h, post has ≥3 replies / ≥10 likes (real engagement signal)
3. Picks 15 handles, writes them to a fresh `<this-week>.md`
4. Proceeds to draft 3 engagements

Empty cohort + offline operator = agent generates one and proceeds. Hard fail = skip the engagement step for the day, log it, ping Slack.

## Slot track rules — what each slot is for

### Slot 1 — Feature spotlight (the daily ANCHOR)

**Slot 1 spotlights a different Arcadia feature each day** with a fresh screenshot. The feature rotation cycles through the product surface (world, studio, kiln, stage, members, billing) on a 7-day cycle defined in `_config/feature-rotation.md`. Each post names the feature, shows it, and says what it does in one sharp sentence.

- **Anchor role.** Slot 1 is the post that matters most. Slots 2 and 3 are filler. The anchor MUST attach an Arcadia screenshot of today's feature (per marketing-brain.md Gate 3). Operator directive 2026-05-10.
- **Feature rotation.** `cycle_day = ((day_n - 1) % 7) + 1`. Look up the feature in `feature-rotation.md`. Capture a fresh screenshot. If the feature changed since last capture, lead with what's new. If not, lead with what it IS.
- **Copy formula.** Hook: name the feature or what it does. Optional: contrast with competitors. Close: Day N. Target 80-150 chars. The screenshot does the heavy lifting.
- **N is monotonic.** Even on holidays / weekends / unposted days, N still increments by 1 per calendar day.
- **Day 1** is `day_n.start_date`. Operator sets this when launch is greenlit.
- **Format:** Day-N is a closer or omitted, NEVER the opener (per marketing-brain.md hook ban-list).

### Slot 2 — Insight / hot take (filler, visual OPTIONAL)

What's wrong with current platforms, sharp insights about communities / creator economy / creator-tool space, or a contrarian take that reframes a known problem.

- **Filler slot.** Slot 2 is filler — it supports slot 1 (the anchor) but doesn't carry the day's product context on its own. Operator directive 2026-05-09 demoted slot 2 visual from REQUIRED to OPTIONAL.
- **Visual rule:** optional. If a visual is attached, it must be Arcadia-product only (per marketing-brain.md Gate 3). NO charts, NO graphs, NO comparison tables, NO external screenshots, NO generated illustrations. If no Arcadia visual genuinely fits the angle, ship text-only.
- **Voice:** conviction-post pattern (specific number + named competitor flaw + the answer + close).
- **No Day-N counter on this slot** — that's slot 1 only.

### Slot 3 — News commentary / industry reshare (with sharp take)

A recent news item in the gaming / AI / community-tools space, commented on with a sharp take. Or a curated reshare of an ICP-relevant post with a layered angle.

- **Source:** `news-agent/briefings/<recent>/founders.md`, `investors-general.md`, `big-tech.md` (filter to gaming/AI/tech-relevant items).
- **Voice:** opinion-led, contrarian if warranted, never just summary. Quote the news source briefly + add a layer.
- **Visual:** optional but recommended. Screenshot of the news headline if relevant.
- **No Day-N counter on this slot.**

## Ship-every-slot rule (no skip)

3 posts/day is the operator-defined minimum (decision 2026-05-09). The agent does NOT skip slots. When a slot's primary content track has no fresh signal, the agent pivots to the fallback content track for that slot — see `marketing-brain.md`'s "Fallback content tracks (per slot)" section. Examples:

- Slot 1 fallback (feature rotation covers every day; if a specific feature's route is broken) → next feature in rotation, or re-angle a previously featured surface
- Slot 2 fallback (no fresh insight) → curated reshare from cohort + layered take, or founder-honesty post
- Slot 3 fallback (no news angle) → curated reshare or industry observation from public data

Visuals also fall back via the **evergreen Arcadia visual rotation** in `marketing-brain.md`. When fresh signal doesn't produce a slot-specific Arcadia capture, the agent rotates from `world-spawn`, `studio-overview`, `the-kiln`, `the-stage`, etc. Slots 1 + 2 always ship with an Arcadia visual; slot 3 ships text-only by default.

If after rewrite + fallback library NO content passes gates, the agent posts to Slack `#twitter-arcadia` and the operator decides — this should happen <1× per quarter, not weekly.

## Off-week / vacation

Set `personal_blackouts:` in `holidays.md` for vacation dates. Day N still increments during blackouts (the build doesn't stop counting); the agent just doesn't post.

## When to revisit cadence

- After 30 posts, look at engagement vs. effort.
- If slot 3 (afternoon) consistently skips for "no news angle," consider replacing it with a second build-in-public window (e.g., demo clip / progress shot) instead of dropping it.
- If slot 1's day-N becomes the only thing that ever lands, that's a signal the marketing-brain visual upgrade isn't carrying slot 2 — investigate before dropping slots.

The agent doesn't auto-tune cadence. Operator decides based on observed metrics in `07-metrics/`.
