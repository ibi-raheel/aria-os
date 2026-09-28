---
name:                          # display name (denormalized from dossier for readability)
slug:                          # MUST match the dossier slug at memory/people/<slug>.md
dossier_ref: '[[memory/people/<slug>]]'
agent: outreach-agent-arcadia | networking-agent | <future-agent>
status: target | qualified | enriched | sent | replied | closed-won | closed-lost | dormant | disqualified
source:                        # how THIS agent found this person
segment:                       # agent-specific segmentation tag
priority:
created: YYYY-MM-DD
updated: YYYY-MM-DD
# engagement-state fields — populated as the engagement progresses
primary_channel:
secondary_channel:
sent_at:                       # ISO 8601 datetime
sent_channel:                  # comma-separated successful channels (e.g., "email, instagram-dm")
failed_channels:               # "channel: reason" entries (e.g., "twitter-dm: DMs closed")
tags: []
---

# {agent} engagement — {name}

See dossier: [[memory/people/<slug>|<Name>]]

## Why this engagement

Why is THIS agent reaching out, in THIS pitch context. Different from "who they are" (that's in the dossier).

## Anchor / Discovery angle

The specific recent thing the message hooks on:
- For networking-agent: anchor object — source URL + date + verbatim excerpt.
- For outreach-agent-arcadia: discovery questions or signal that drives the message.

## Outreach messages

The actual messages drafted for this engagement, by channel.

### Email

**Subject:** `subject line`

```
message body
```

### Primary DM — <platform>

```
message
```

### Secondary DM — <platform>

```
message
```

## Outreach log

| Date | Channel | Action | Outcome |
|---|---|---|---|

## Notes

Engagement-specific notes (different angle to try next, dropped channels, follow-up reminders, etc.).
