# Stage 05 - Send

## Job

Dispatch send packages across channels. The agent drives a real browser
via **Playwright MCP** to navigate to Instagram, Twitter, Gmail, LinkedIn,
etc. and sends messages autonomously. No manual copy-paste needed.

### Send tiers

- **Tier A (browser-automated):** Agent uses Playwright to open the
  platform, navigate to the recipient's profile/DM/compose screen, type
  the message, and send. This is the default for ALL channels.
- **Tier B (Gmail draft):** For email, agent can also use Gmail MCP to
  create drafts that Ibi reviews and sends. Fallback if Playwright
  has issues with Gmail.

## Inputs

| File | Why |
|---|---|
| Personalized messages in `stages/05-send/output/<slug>.md` (inline) or `stages/04-personalization/output/<slug>/` | Drafts to send |
| `_config/send-protocol.md` | Caps, send order, quiet hours, timezone |
| `_config/voice.md` | Voice rules (final quality check before send) |
| `workflows/<platform>.md` | Per-platform Playwright steps for sending |
| The lead's `memory/people/<slug>.md` | Channel handles, timezone |

## Process - Playwright browser automation

### Prerequisites

- Playwright MCP server registered: `claude mcp add playwright -- npx @playwright/mcp@latest`
- User must be logged into Instagram, Twitter, Gmail, LinkedIn in the
  browser BEFORE starting a send batch. Agent cannot authenticate.
- Browser window should be visible (not headless) so Ibi can
  monitor if needed.

### Per-send flow

1. **Read the message file** for the target (email, primary DM,
   secondary DM, segment note)
2. **Determine send order** from `_config/send-protocol.md`:
   - Day 0 morning (lead's timezone, after 9am): Email
   - Day 0 afternoon: Primary channel DM
   - Day +1: Secondary channel DM (if applicable)
3. **Execute the platform workflow.** Each platform has a dedicated
   workflow file in `workflows/` with full Playwright steps:
   - Email: `workflows/gmail-send.md`
   - Twitter DM: `workflows/twitter-dm.md`
   - Instagram DM: `workflows/instagram-dm.md`
   - LinkedIn DM: `workflows/linkedin-dm.md`
   - Skool DM: `workflows/skool-dm.md`
   Read the workflow file and follow its steps exactly.
8. **After each send:**
   - Update engagement record frontmatter: `status: sent`, `sent_at`, `sent_channel`
   - Add row to engagement record's outreach log
   - Append to `logs/daily/YYYY-MM-DD.md`
   - Do NOT update the dossier at `memory/people/<slug>.md` — the dossier is identity-only and is never touched by send actions
9. **Set bump-due dates in lead frontmatter:**
   - `bump_1_due: <send_date + 4 days>`
   - `bump_2_due: <send_date + 10 days>`
   - `dormant_after: <send_date + 14 days>`

### Batch send flow

When Ibi says "send" or triggers `/send`:

1. Read all message files with `status: draft`
2. Sort by priority (1 first), then by segment effort allocation
3. Check daily caps per platform (Twitter: 20, Skool: 30, IG: 15,
   Email: 50, LinkedIn: 20)
4. For each target in order:
   a. Send email first (morning batch)
   b. Send primary DM (afternoon batch)
   c. Log each send
5. Report: "Sent N emails, N Twitter DMs, N Instagram DMs. Updated
   all status files."

## Browser navigation tips

- **Always take an accessibility snapshot** before clicking. The snapshot
  shows clickable elements with their refs - use these to click accurately.
- **Don't guess coordinates.** Use the accessibility tree to find buttons,
  inputs, and links by their labels.
- **If a platform shows a modal/popup** (cookie consent, notification
  prompt), dismiss it first before proceeding.
- **Rate limiting:** pause 30-60 seconds between DMs on the same platform
  to avoid triggering anti-spam. Email can be faster (5-10 sec gaps).
- **If login is required:** stop and tell Ibi. Never attempt to log
  in - credentials are not stored.

## Output

| Artifact | Location | Format |
|---|---|---|
| Updated engagement record | `stages/05-send/output/<slug>.md` | Frontmatter: `status: sent`, `sent_at`, `sent_channel`, `failed_channels`. Outreach log appended. |
| Daily log | `logs/daily/YYYY-MM-DD.md` | Timestamped block with send counts |

## What good looks like

- Sends staged across the day per protocol (no firehose)
- Quiet hours respected (no sends before 9am or after 7pm their TZ)
- Bump-due dates set immediately after first send
- Every send logged in the message file, vault stub, and daily note
- Platform daily caps never exceeded

## What to avoid

- Exceeding per-platform daily DM caps
- Sending all channels same hour (looks spammy)
- Ignoring timezone
- Editing the message at send time (if it needs editing, go back to
  message generation)
- Attempting to log in to any platform - always tell Ibi

## Tools used

- **Playwright MCP** - primary send tool for all channels. Browser
  navigation, accessibility snapshots, clicking, typing.
- **Gmail MCP** (`mcp__claude_ai_Gmail__create_draft`) - fallback for
  email if Playwright has Gmail issues
- **Bash** - file updates, frontmatter changes
- **Read/Edit/Write** - message files, vault stubs, daily logs

## Tier check

**This is the only stage that touches the outside world.** The agent
sends autonomously via Playwright, but Ibi should have the browser
visible to monitor. If anything looks wrong (wrong recipient, garbled
text, platform error), Ibi can intervene.

Daily caps are hard limits - the agent stops sending on a platform once
the cap is reached, even if there are more targets queued.

## Hand-off to stage 06

After all channels sent + bumps scheduled, the lead is now in sent
status. Stage 06 (followup) takes over watching for replies and
executing the bump cadence.
