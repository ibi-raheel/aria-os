# Reply Routing

Decision tree for stage 06 (followup) when a reply lands. Routes the lead
to the right next action.

---

## Step 1 - Classify the reply

Read the reply and bucket it:

| Bucket | Looks like | Example replies |
|---|---|---|
| **Positive interest** | "yes," "let's chat," "interesting," "tell me more," "send the link" | "yeah let's set something up", "this is cool, when can we chat" |
| **Question** | They ask a specific thing before committing | "how does it compare to skool?", "what's the pricing?", "can my members keep their existing accounts?" |
| **Pushback / objection** | They raise a concern | "looks cool but my community is too small", "we just moved to skool", "i'm not sure my audience would use a 3D thing" |
| **Soft no** | Polite decline with door open | "not right now but interesting", "ping me in a few months", "love what you're building but timing's off" |
| **Hard no** | Explicit, closed | "not interested", "please remove me", "stop emailing me" |
| **Unclear / cold** | Single word, ambiguous | "thx", "hmm", emoji-only |

---

## Step 2 - Take the action

### Positive interest

1. **Notify Ibi immediately** (mention in `logs/daily/YYYY-MM-DD.md`,
   surface in next conversation)
2. Draft a warm-up reply + Calendly link in the lead's
   `06-followup/output/active/<lead>/draft-calendly.md`:

```
[their name], appreciate you replying - let's chat.

[1 sentence acknowledging what they said specifically]

here's my calendly: [calendly url]

grab whatever works. 30 min should be enough to walk through what a realm
build for [their community name] would look like.

- ibi
```

3. Update `memory/people/<name>.md`: `status: in-conversation`,
   `first_reply: YYYY-MM-DD`, log the reply in Outreach log table
4. User reviews, sends manually
5. Once Calendly is booked: `status: booked`, write the call date in
   the `memory/people/<name>.md`

### Question

1. Identify if the question is template-able (price, comparison to
   competitor, technical capability, member account migration)
2. If template-able: draft answer in user's voice using existing
   knowledge from `_config/offer.md` and Arcadia PRD content
3. Always end the answer by re-issuing the soft ask: "happy to walk
   through more on a quick call if useful - calendly here: [link]"
4. Save draft to
   `06-followup/output/active/<lead>/draft-reply-<topic>.md`
5. Escalate to user for review before send

**Common Q answers:**

- *"How does it compare to Skool?"* → "Skool is great for forum-style
  community + courses. Arcadia is the same idea but spatial - your
  members actually 'are' somewhere together, with avatars, real-time
  presence, a tavern for chat, an academy for courses. Different feel,
  same primitives. Loom showed the spatial part - the rest works
  similar to what you're used to."
- *"What's the pricing?"* → "Setup engagements run $7.5k-$15k depending
  on community size and content volume. Happy to walk through specifics
  on a call: [calendly link]"
- *"Can my members keep their accounts?"* → "Members create new accounts
  in Arcadia (it's a different product), but we handle the migration
  comms - we draft the announcements, set up the invite flow, walk you
  through the cutover. Done-for-you means done-for-you."

### Pushback / objection

1. Acknowledge the concern (don't argue)
2. Reframe with one specific counter-point if defensible; otherwise
   accept it
3. Leave the door open with a low-pressure close

Template:

```
[their name], fair.

[acknowledge: "you're right that...", "totally hear that...", etc.]

[reframe IF you have a real counter - otherwise skip]

if anything changes or you want to think about it for [their community],
i'm here.

- ibi
```

Escalate to user before send. Don't auto-send pushback responses - too
high-stakes.

### Soft no

1. Mark `status: dormant` in `memory/people/<name>.md`
2. Set `re_touch_after: <date+90d>`
3. Move lead folder to `stages/06-followup/dormant/`
4. Send a brief acknowledgment if they wrote more than one sentence:

```
all good - appreciate you replying. i'll check back in a few months.

- m
```

5. Set `re_touch_after: <today + 90 days>` in `memory/people/<slug>.md` frontmatter (manual-trigger model - `/followup` will surface it on that date)

### Hard no

1. Mark `status: closed-lost` in `memory/people/<name>.md`
2. Move lead folder to `stages/06-followup/closed-lost/`
3. Write a `memory/decisions/YYYY-MM-DD-closed-lost-<slug>.md` with the reason
   (their literal words if available)
4. Do NOT reply unless they explicitly asked to be removed (in which
   case send a one-line acknowledgment)
5. Add their email/handle to a do-not-contact list (TBD: where this
   lives - propose `outreach-agent-arcadia/_config/do-not-contact.md`)

### Unclear / cold

1. Bump once with a clarifying re-ask:

```
[their name] - quick clarification: what would be useful here?

[a] more detail on what arcadia does vs your current setup
[b] a calendly to talk it through
[c] not the right time

happy with any of those.
```

2. If still no response after 4 days, treat as no-reply and continue
   bump cadence per `_config/send-protocol.md`

---

## Step 3 - Update memory

Every reply, regardless of bucket, triggers:

- Append to `memory/people/<name>.md` Outreach log table:
  `| YYYY-MM-DD | channel | reply | bucket - first 80 chars of reply |`
- `logs/daily/YYYY-MM-DD.md`:
  `## HH:MM - outreach-agent - reply from [[memory/people/x]] - bucket: [name]`
- If reply triggered a status change, update frontmatter on
  `memory/people/<name>.md`

---

## Edge cases

- **Reply from a different person** (e.g., their assistant): treat as
  positive - that's good signal. Adapt warm-up to address the assistant.
- **Reply that's actually a pitch back** (they're trying to sell us
  something): polite acknowledgment, no further engagement, mark dormant
- **Aggressive / hostile reply:** mark closed-lost immediately, do not
  respond, log to decisions
- **Reply on a different channel than we sent on:** still counts.
  Continue conversation on whichever channel they chose.
