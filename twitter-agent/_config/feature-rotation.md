---
title: Feature rotation - daily slot 1 spotlight schedule
updated: 2026-05-10
cycle_length: 7
---

# Feature rotation

Slot 1 (the daily anchor) spotlights a different Arcadia feature each day with a fresh screenshot. The rotation cycles through the product surface so the profile always shows variety, never the same screen twice in a row.

## The rotation

| Cycle day | Feature | Route | capture_intent | What to show | Copy angle |
|---|---|---|---|---|---|
| 1 | **The World** | `/world` | `world-spawn` | Character at The Square, torchlight, NPCs, ambient atmosphere | "Your community isn't a feed. It's a place." The world IS the product. |
| 2 | **Studio Overview** | `/dashboard` | `studio-overview` | Keeper's studio greeting, 5 metric tiles (revenue, MRR, one-time, subs, return-on-spend) | The dashboard that talks to you. "Good evening, ibi.raheel." Not a grid of numbers. |
| 3 | **The Kiln** | `/dashboard/courses` | `the-kiln` | Courses dashboard, published/draft states, course tiles, "ink a new course" | Where you publish what's finished and keep what's drying. Named after a thing. |
| 4 | **The Stage** | `/dashboard/events` | `the-stage` | Events timeline, live now, upcoming, scheduled, "ink the calendar" | The weekly Q&A, the kickoff, the office hour. Events as gatherings, not webinars. |
| 5 | **Members** | `/dashboard` (modal) | `members-roll` | Member list, roles, activity, the people in the world | Not "users." Wanderers, keepers, scribes. The people who chose to stay. |
| 6 | **Billing** | `/dashboard` (modal) | `billing-ledger` | Revenue view, subscriptions, the money side | The ledger. What your community actually earns. No dashboards dressed as compliance docs. |
| 7 | **The World (new angle)** | `/world` | `world-spawn` | Different time of day or character position than cycle day 1 | Return to the world. Different angle, same place. The thing that makes this not another SaaS. |

## How prep uses this

1. Compute `cycle_day = ((day_n - 1) % 7) + 1`
2. Look up the feature for that cycle day
3. Navigate Playwright to the route, capture the screenshot
4. Draft slot 1 around the feature's copy angle
5. If the feature has been shipped/changed since last capture, lead with what's new. If not, lead with what the feature IS and why it's different.

## Adding new features

When a new Arcadia feature ships:
1. Add a row to the rotation table
2. Increment `cycle_length` in frontmatter
3. Add a capture recipe to `arcadia-capture-targets.md`
4. The feature gets its first spotlight on the next matching cycle day

New features that ship mid-cycle get priority - bump them to tomorrow's slot 1 regardless of rotation, then resume the cycle.

## Slot 1 copy formula

```
[Hook: name the feature or what it does, one sharp specific line]
[Optional: one line of contrast - what competitors do vs what this does]

Day [N].
```

Target: 80-150 chars. Screenshot attached. Day-N as closer. The screenshot does the heavy lifting - the text names and frames it.

## Capture notes

- **Dashboard routes** (`/dashboard`, `/dashboard/courses`, `/dashboard/events`): Simulation toggle must be ON. Metrics must show populated numbers, not zeros.
- **Modal tabs** (Members, Billing): Navigate to `/dashboard` first, then click the tab button, wait for content, screenshot.
- **The World** (`/world`): No simulation toggle needed. Wait 5s for Phaser render. Character spawns at The Square by default.
- **All captures**: 1280x720 viewport. Content-safety scan post-capture.

## Rotation state

Track which features have been posted in `twitter-agent/_config/feature-rotation-state.md` (created by prep task after first full cycle). Prevents the same feature posting on consecutive days even if the cycle resets.

```yaml
last_posted:
  world-spawn: 2026-05-10
  studio-overview: null
  the-kiln: null
  the-stage: null
  members-roll: null
  billing-ledger: null
```
