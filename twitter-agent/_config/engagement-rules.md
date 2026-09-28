---
title: Engagement rules — weekly cohort of 5 (rotating)
updated: 2026-05-02
---

# Engagement rules

How the agent picks who to engage with publicly. **Weekly cohort of 5 model** — every weekday the agent engages with the same 5 people. Next Monday, the cohort rotates to a fresh 5.

## What "engagement" means here

**Outbound** activity on the cohort's public posts:
- A substantive reply on a recent post (preferred — relationship-building)
- A like (supplemental, when no good reply hook exists)
- (Optional) a retweet / quote-tweet if their post is genuinely valuable to Arcadia's audience

**Not** part of this surface:
- Replying to mentions / own-post comments → see `reply-rules.md`
- DMing → outreach-agent's job, not this one
- Following new accounts → operator decides who Arcadia follows

## Daily volume

```yaml
cohort_size: 5                  # 5 specific people per week
engagements_per_person_per_day: 1   # one substantive engagement per cohort member per weekday
total_engagements_per_day: 5

dry_run_default: true           # drafts go to 03-review/ for OK
auto_engage_after: 21d          # after 3 weeks of approved drafts, can flip to auto
```

## Weekly cohort file

Current week's cohort lives at `twitter-agent/_config/engagement-cohorts/<YYYY-WW>.md`. Format:

```yaml
---
week: 2026-W19
starts: 2026-05-04
ends: 2026-05-08
rotated_from: 2026-W18
operator_curated: true
---

# Cohort — week of 2026-05-04

5 creator-economy / community-platform voices to engage with this week. One substantive engagement per person per weekday.

## The 5

### 1. @<handle1>
- Real name: <name>
- Role: <e.g., creator with 12K-member Skool community in personal-finance>
- Why this week: <e.g., they posted Sunday about platform-fatigue — high-relevance>
- Public post focus: <e.g., daily threads on community-building>

### 2. @<handle2>
...

### 3. @<handle3>
...

### 4. @<handle4>
...

### 5. @<handle5>
...

## Notes for the agent

- Engage on each person's **most recent qualifying post** (last 48h, has substance, not pure RT).
- If a person hasn't posted in 48h that day, skip them for the day — log "no qualifying post." Don't force.
- **Don't repeat the same reply pattern across the 5.** Each engagement should be specific to that person's tweet — not a template.
- **Don't engage on the same post twice in one week.** If we replied Monday, look for a different post Tuesday.
```

## Selection rules (for operator when curating each week's 5)

**Tier A — top priority (1–2 of the 5):** people whose audiences overlap with Arcadia's ICP — paying-community creators on Skool / Circle / Mighty / Discord with active followings.

**Tier B — second priority (1–2 of the 5):** notable voices in the creator economy who don't directly compete but whose readers care about community-building (writers, podcasters, indie founders).

**Tier C — third priority (1 of the 5):** wildcard — someone in adjacent space (design-driven indie, prop-tech, AI-and-community intersection) whose engagement compounds in unexpected ways.

**Avoid:** direct competitors' founders (Creator A at Skool, etc. — engaging there draws scrutiny), accounts on `safety.md` never-engage list, anyone the operator has ever publicly disagreed with.

## How rotation works

```
Sunday evening (or Monday 06:00, whichever is earlier):
  /twitter-engage pre-flight reads `engagement-cohorts/<this-week>.md`
  if the file doesn't exist: STOP and notify operator
                              → drop a flag at twitter-agent/_pending-cohort.md
                              → engagement step skipped for the day until cohort is set

Monday 09:00:
  agent picks up the new cohort, engages once per person
  Tuesday-Friday: same 5 people, new posts each day
  Saturday-Sunday: no engagement (weekend skip)

Following Sunday:
  operator drops `engagement-cohorts/<next-week>.md` with a fresh 5
  agent picks it up Monday 09:00
```

## What goes in a cohort over time

Old cohort files at `twitter-agent/_config/engagement-cohorts/<YYYY-WW>.md` stay forever as a record. Useful signals when curating future cohorts:

- Which past cohort members responded? Re-add to a future cohort.
- Which past members never engaged back? Don't repeat soon — try someone else.
- Patterns — if two consecutive cohorts produced strong reply chains, the curation logic is working.

## For each engagement, agent draft format

`twitter-agent/06-engagement/<date>/<handle>-<post-id>.md`:

```yaml
---
date: <date>
cohort_week: <YYYY-WW>
handle: @<handle>
their_post_url: <URL>
their_post_text: <verbatim quote>
their_followers: <count>
posted_at_relative: <e.g., "2h ago">
engagement_type: substantive_reply | like_only | retweet | quote_tweet
dry_run: true
operator_approved: pending
---

# Engagement — @<handle>

## Their post
> <verbatim quote>

## Context
<1-2 lines: why we're engaging with them this week, any relevant history>

## Drafted reply (or like-only / quote-tweet)
<the actual content>

## Voice check
- [x] Specific, not generic
- [x] Adds substance (answers, builds, or asks a sharp follow-up)
- [x] Doesn't beg engagement
- [x] No filler ("great post!" / "love this")
- [x] No hashtags, no emojis (rare exception)
- [x] Reads like a human at a bar, not a webinar
```

## Hard rules (never)

1. **Never reply with vapid agreement.** "This." / "Exactly." / "Great point." / "💯" → kill.
2. **Never engage with anyone on `safety.md` never-engage list.**
3. **Never engage in pile-ons, dunks, or sub-tweets.**
4. **Never engage on politically charged content** even if a cohort member posts about it. Skip the day for that person.
5. **Never reply with a link to Arcadia** unless their post is directly asking about something Arcadia solves — and even then, prefer a substantive answer over a link drop.
6. **Never DM a cohort member from this agent.** That's outreach-agent's job, and only after explicit operator approval.

## Tracking

After 4 cohort weeks (~30 engagements per person), look at:
- Reply-back rate per cohort member (did they engage back? at what cadence?)
- Inbound followers from engagement period (did our follower count tick up?)
- Whether any cohort members became actual customers / mutuals

Surface findings to operator weekly via `07-metrics/<date>/cohort-trends.md`.
