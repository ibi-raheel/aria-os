# Stage 06 - Followup

## Job

Watch for replies. Send bumps on the cadence. Route warm leads to a
user-sent Calendly. Mark dormant when bumps fail. Log everything to the
vault.

## Inputs

| File | Why |
|---|---|
| Sent leads in `stages/05-send/output/` | Active conversations to watch |
| Inbox sources (Gmail MCP, Twitter DMs via Playwright, Skool DMs) | Where replies arrive |
| `skills/reply-routing.md` | Decision tree for reply classification + actions |
| `skills/bump-templates.md` | Bump 1, bump 2, re-touch templates |
| `_config/send-protocol.md` | Cadence rules, quiet hours, dormant-after-N-days |

## Process

### Daily inbox check

Run once per day (scheduled, ~10am Ibi's TZ):

1. Check Gmail for replies on cold-emailed leads (Gmail MCP)
2. Check Twitter DMs for replies (Playwright - see `workflows/twitter-dm.md`)
3. Check Skool DMs for replies (Playwright - see `workflows/skool-dm.md`)
4. Check other channel inboxes per active leads (Playwright per workflow)
5. For each new reply:
   - Classify per `skills/reply-routing.md`
   - Take the action prescribed (draft, escalate, mark)
   - Update engagement record at `stages/06-followup/output/<slug>/replies.md` with reply log
   - Append to `logs/daily/`

### Bump cadence (manual-trigger model - no scheduler)

Bumps are NOT auto-scheduled. Lead frontmatter carries date fields set at
stage 05: `bump_1_due`, `bump_2_due`, `dormant_after`, `re_touch_after`.

When `/followup` is run, the agent checks every active lead's frontmatter:

1. If lead has replied since original send → skip (no bump needed)
2. If `today >= bump_1_due` and no reply → generate bump 1 from
   `skills/bump-templates.md` (screenshot mockup angle), run Tier A send
   via stage-05 mechanic, set `bump_1_sent: <today>`
3. If `today >= bump_2_due` and no reply → generate bump 2 (different
   angle), Tier A send, set `bump_2_sent: <today>`. This is the explicit
   "last ping" close - no further bumps.
4. If `today >= dormant_after` and no reply → mark `status: dormant`,
   move folder to `dormant/`, set `re_touch_after: <today + 90 days>`
5. For dormant leads, if `today >= re_touch_after` → generate re-touch
   from bump-templates.md with new context, Tier A send. After this
   attempt, no further bumps - mark `closed-ghost` if no response.

**`/status` surfaces what's due today** by scanning frontmatter dates
across active and dormant leads.

### Reply triage - see `skills/reply-routing.md`

Six buckets, each with prescribed action:
- Positive interest → notify Ibi, draft Calendly send → user sends
- Question → draft answer, escalate
- Pushback → draft response, escalate (high-stakes)
- Soft no → mark dormant, schedule +90d
- Hard no → mark closed-lost, write decision file
- Unclear → bump once with clarifying re-ask

## Output

| Artifact | Location | Format |
|---|---|---|
| Active leads | `stages/06-followup/output/active/<slug>/` | Lead folder while in conversation |
| Reply log | `06/output/active/<slug>/replies.md` | Append-only log of every reply received |
| Bump drafts | `06/output/active/<slug>/bump-N-draft.md` | Drafts before send |
| Calendly send draft | `06/output/active/<slug>/draft-calendly.md` | When status = positive interest |
| Dormant leads | `06/output/dormant/<slug>/` | After +14d or soft no |
| Closed-won | `06/output/closed-won/<slug>/` | Paying customer |
| Closed-lost | `06/output/closed-lost/<slug>/` | Hard no |
| Decision (closed-won OR closed-lost) | `memory/decisions/YYYY-MM-DD-<status>-<slug>.md` | The reason - gold for ICP refinement |
| Daily log | `logs/daily/YYYY-MM-DD.md` | Per-action timestamped block |

## State transitions

```
sent  →  active  →  in-conversation  →  booked  →  closed-won
                 ↘                                  ↘
                  dormant (+14d, no reply)           closed-lost (hard no)
                  ↓ (+90d re-touch)
                  active OR closed-ghost
```

Each transition triggers:
- Engagement record status update (`stages/06-followup/output/<status>/<slug>/`)
- Folder move
- `logs/daily/` log entry
- Decision file IF transition is to `closed-won` or `closed-lost`
- Dossier status field updated ONLY if transition is final (closed-won or closed-lost)

## What good looks like

- Every reply is classified and acted on within 24 hours of the user
  running `/followup`
- Bumps go out on the cadence the frontmatter dates demand - when the
  user runs `/followup`, due bumps fire (Tier A) and the user only
  intervenes for non-template responses (questions, pushback, positive
  interest)
- Calendly drafts are warm and specific, never templated
- Dormant leads have `re_touch_after` set so they're not forgotten
- Closed-won and closed-lost both produce a `memory/decisions/` file
  with the reason - gold for refining ICP and offer

## What to avoid

- Bumping after the explicit "last ping" close in bump 2 (kills trust)
- Auto-sending pushback responses (always escalate)
- Forgetting to mark dormant when +14d hits (clogs active list)
- Treating soft no as hard no (loses re-touch opportunity)
- Skipping the decision file on closed-lost (loses the learning)
- Sending Calendly link in cold messages (CTA is Loom-then-reply, locked)

## Tools used

- **Playwright MCP** - browser automation for sending bumps on all
  platforms (Instagram, Twitter, LinkedIn, Skool). Agent navigates via
  accessibility snapshots and sends autonomously.
- Gmail MCP - inbox check + email drafts as fallback
- **No scheduler.** Manual trigger via `/followup` slash command. Bump
  due-dates live in lead frontmatter; `/status` surfaces what's due today.

## Tier check

Reads inboxes (no risk). Bump sends use Playwright MCP (browser
automation). Calendly send uses Playwright. Status updates write to
vault freely.

## End of pipeline

A lead exits the pipeline at:
- `closed-won` → write decision, become a case study (move into
  `outreach-agent-arcadia/_archive/closed-won/<slug>/` once the engagement is
  complete and case-study material is captured)
- `closed-lost` → write decision, archive
- `closed-ghost` → archive after 90d re-touch fails

The 10-customer goal is met when 10 leads reach `closed-won`. At that
point: pause new discovery, focus on case-study capture, prepare for
platform launch.
