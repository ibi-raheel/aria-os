# Send Protocol

Cadence, caps, sequencing, and warm-up rules for stage 05 (send) and
stage 06 (followup). Read `_config/voice.md` for link rules and CTA
rules - this file governs timing and mechanics.

---

## Volume caps

| Action | Cap |
|---|---|
| New leads contacted per day | 50 |
| Automated cold emails per day | 50 (across warmed sending accounts) |
| Templated DMs per day (volume tier) | 40-50 (spread across platforms) |
| Personalized DMs per day (top-10 tier) | 5-10 |
| Messages to one lead within 24h | ≤2 (different channels) |
| Twitter DMs per day per account | ≤20 (Twitter throttles aggressive senders) |
| Skool DMs per day | ≤30 |
| Instagram DMs per day | ≤15 |
| LinkedIn connection requests per day | ≤20 |

## Follow-after-DM

**After every DM send, immediately follow the person on that platform.**
This is mandatory, not optional. The follow notification alongside the
DM makes the message feel less cold.

---

## Phase-0 discovery send rules (separate from sales)

Phase-0 outreach has different rules from the sales pipeline:

| Segment | Messages | Bump? | Effort share |
|---|---|---|---|
| mega-creator | 1 | No - if they don't reply, move on | 5% |
| established-creator | 1 | 1 bump at day 5 | 15% |
| mid-tier-creator | 1 | 1 bump at day 5 | 40% |
| consultant-operator | 1 | 1 bump at day 5 | 25% |
| niche-builder | 1 | 1 bump at day 5 | 15% |

Phase-0 bump text: "totally get it if busy - the offer stands whenever."
No new value-add needed, just a nudge.

**No Loom, no Calendly, no product pitch in any phase-0 message.**
See `stages/_phase-0-archive/outreach-message.md` for templates.

---

## Cold email infrastructure (required for volume)

Automated cold email requires dedicated sending infrastructure:
- Dedicated cold email domain (not primary domain)
- Cold email tool (Instantly, Smartlead, or similar) for domain warming +
  rotation
- 2-3 sending accounts to distribute volume
- SPF/DKIM/DMARC configured on sending domain
- Plain text only - no HTML, images, or attachments in cold email

Personal Gmail is NOT used for volume cold email - only for manual
follow-ups and warm replies.

## Warm-up protocol (top-10 leads only)

Before DMing a top-10 lead, warm up their awareness of you:

| Day | Action | Platform |
|---|---|---|
| Day -5 to -3 | Like 4-5 of their recent posts | Twitter, Instagram, LinkedIn |
| Day -3 to -1 | Leave 2-3 thoughtful public replies (not "great post!" - add substance) | Twitter, YouTube, Skool |
| Day -1 | Quote-tweet or comment on one of their takes with genuine insight | Twitter |
| Day 0 | Send cold email | Email |
| Day 0 (later) | Send personalized DM referencing the public interaction | Twitter, Skool, etc. |

For volume-tier leads: like 1-2 recent posts before DMing. This is
the minimum viable warm-up at scale.

## Two-tier send model

### Volume tier (all leads)

| # | Day | Channel | Method | Link? |
|---|---|---|---|---|
| 1 | Day 0 morning | Cold email | Template + demo Loom URL + variables | Yes (1 link) |
| 2 | Day 0 afternoon | DM (best available) | Template, NO link - tease the Loom, send after reply | No |

The email carries the Loom link. The DM teases it and earns a reply
first. When they reply to the DM, send the Loom link as message 2.

### Top-10 tier (deep-enriched leads with highest scores)

| # | Day | Channel | Method | Link? |
|---|---|---|---|---|
| 1 | Day 0 morning | Cold email | Custom email + personalized Loom URL | Yes (1 link) |
| 2 | Day 0 afternoon | Twitter DM | Personalized, NO link - tease | No |
| 3 | Day +1 | Skool/Discord/platform DM | Personalized, references email, NO link | No |
| 4 | Day +1-2 | Other channels as available | Personalized, permission-first | No |

The email is the spine. DMs reinforce it - they reference the email
without duplicating it.

## DM → reply → link flow

When a lead replies to any DM (even "sure" or "?"):
1. Send the Loom link immediately
2. Add one line: "3 min. shows what {community_name} could look like."
3. Do NOT pitch further in this message

## Bump cadence (stage 06)

| When | What | Channel | Rules |
|---|---|---|---|
| +4 days, no reply | Bump 1: new angle - screenshot mockup of their Realm, or a different value prop | Same channel as original, or strongest active channel | Must add NEW value, not restate the pitch |
| +10 days, no reply | Bump 2: social proof (when available) or different problem angle | Best-performing channel | Include an explicit opt-out: "last ping - no worries if not" |
| +14 days, no reply | Mark dormant. Move to `stages/06-followup/dormant/` | - | - |
| +90 days from dormant | Re-touch with genuinely new context (product update, case study, their new milestone) | Strongest channel | - |

### Bump rules

- **Never say** "just checking in," "bumping this," "following up,"
  "did you see my message," "I emailed you 3 times"
- Each bump must offer something the previous message didn't
- Never reference their silence or prior ignored messages
- DMs get max 2 bumps (3 total messages). A 4th triples spam risk.
- Cold email can get 3-4 bumps (5 total) spread over 4-6 weeks
- Best day for bumps: Wednesday. Launch new sequences Monday.

## Reply triage rules (stage 06)

| Reply tone | Action |
|---|---|
| Positive interest | Notify Ibi immediately. Draft Calendly send + warm-up reply. |
| Question (not yet a yes) | Draft answer in user's voice, route for review |
| Pushback / objection | Draft response addressing the concern; escalate to user if beyond template-able |
| Soft no ("not now") | Park in dormant; mark `re_touch_after: <date+90d>` |
| Hard no | Mark `closed-lost`; write `memory/decisions/YYYY-MM-DD-closed-lost-<slug>.md` with reason |
| Unclear / cold | Bump once with a clarifying re-ask |

## Send tiers

### Tier A - Browser-automated (Playwright MCP)
Agent uses Playwright MCP to drive a real browser. Per-platform steps
live in `workflows/` (e.g. `workflows/twitter-dm.md`,
`workflows/gmail-send.md`). Agent reads the workflow file and executes
autonomously - navigates to the platform, finds UI elements via
accessibility snapshots, types the message, and sends. Ibi should have
the browser visible to monitor if needed.

### Tier B - Gmail draft fallback
If Playwright has issues with Gmail, use Gmail MCP to create drafts
that Ibi reviews and sends manually.

## Quiet hours

- No sends to a recipient before 9am or after 7pm in their local timezone
  (use timezone field from `memory/people/<name>.md` Profile section).
- No new outreach on weekends (replies and bumps allowed).
- Best send times: Tuesday-Wednesday, 7:30-9:00 AM or 11:30 AM-1:00 PM
  recipient's timezone.

## Per-batch checklist

Before sending a batch, agent confirms:

- [ ] All email drafts pass voice.md rules (word count, you/we ratio,
      CTA style, subject line format)
- [ ] All DM drafts contain NO links
- [ ] Each lead has Loom URL recorded (email) or Loom tease (DM)
- [ ] Each lead's `memory/people/<name>.md` is current
- [ ] Send order is staged across day per the tier table
- [ ] Quiet hours checked against lead timezone
- [ ] Platform daily caps not exceeded
