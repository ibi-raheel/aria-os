# Bump Templates

For stage 06 (followup) when a lead doesn't reply. Two bumps before
dormant.

---

## Cadence (from `_config/send-protocol.md`)

| When | Bump | Channel |
|---|---|---|
| +4 days | Bump 1 - fresh angle | Same as original most-active channel |
| +10 days | Bump 2 - different angle | Best-performing channel from history |
| +14 days | Mark dormant | - |
| +90 days from dormant | Re-touch with new context | Strongest channel |

---

## Bump 1 - Screenshot mockup angle (+4 days)

Lead with a *new asset*, not a chase.

```
{name} - put together something for {community_name}.

mocked up what your community would look like as an arcadia
realm - figured it'd be easier to just show you than explain.
[attach screenshot or short clip]

the original 3-min walkthrough is still here if you want it:
[loom url]

worth a look?
```

Why this works: it's not "did you see my last message" energy. It's
"here's more value, no pressure." The mockup proves we did the work.

**Mockup generation:** stage 04 should pre-render a static screenshot of
Arcadia's world with the creator's brand colors / logo / community name
if accessible. If not pre-generated, stage 06 creates it on demand using
WebSearch for their brand assets + image gen tool (TBD; for now,
placeholder mock).

---

## Bump 2 - Different angle (+10 days)

Pick the angle they're MOST likely to respond to based on what's in
their dossier:

### A) Social proof angle (use when we have case studies)

```
{name} - last note from me on this.

{case study creator} just launched their realm - took their
{member_count} discord and moved them in two weeks. members are
more active than before (which honestly surprised us too).

if {community_name} could use something similar, happy to send
a calendly: [link]

if not, totally fine - won't ping you again.

- ibi
```

### B) "They shipped something new" angle (use if they launched
something recent)

```
{name} - saw {thing they launched}. nice.

still think arcadia would slot in well with what you're building
- here's the walkthrough if you want a fresh look: [loom url]

if the timing's off, no worries at all. just didn't want to
assume you'd written it off without seeing it.
```

### C) "Different angle on the value" (default if no specific trigger)

```
{name} - one more thought before i drop off.

most of what we talk about is the spatial experience - members
walking through a world instead of scrolling a feed. but the
reason {case study creator} actually picked us was
{specific operational reason - fewer notifications, unified
billing, one place for members}. that might matter more for
{community_name}.

walkthrough still here: [loom url]

last note. all good either way.

- ibi
```

---

## Bump 2 closing rule

**Always include "last note" / "won't ping you again" / equivalent.**
This:
- Removes pressure (paradoxically increases reply rate)
- Closes the loop respectfully
- Avoids looking desperate

After bump 2 with the explicit close, **do not bump again** until
the +90 day re-touch.

---

## Re-touch (+90 days)

Only if status is `dormant`, not `closed-lost`. Open with NEW context:

```
{name} - been a while. wanted to share something new.

{new development since last contact - new feature, case study,
market shift, something they posted recently}

if arcadia's worth a fresh look for {community_name}, i'm here.
if not, i'll leave it here.

- ibi
```

90-day re-touch is one shot. If no response, mark `closed-ghost` (a
distinct status from closed-lost - they never actively rejected us, just
didn't engage).

---

## Channel switching during bumps

If the original channel got no read receipt (visible on Skool DM,
sometimes Twitter), bump on a *different* channel to surface from
notification noise.

Channel switch logic:
- Email no-reply → bump on Twitter DM
- Twitter DM no-reply → bump on email
- Skool DM no-reply → bump on Twitter
- LinkedIn no-reply → bump on email or Twitter

When switching channels, reference the previous one naturally:
*"sent you something on email a few days ago - figured this might
surface better here."*

---

## What never to write in a bump

- "Just bumping this up" → screams desperate
- "Did you see my last message?" → guilt-trips, never works
- "Following up on my previous email" → sales-y filler
- "Per my last note..." → confrontational
- "Circling back" / "wanted to circle back" → cliché, feels automated
- Any version of "I haven't heard back from you"
- Restating the entire pitch - they already saw it once

---

## Updating this file

After each cohort of bumps, log:
- Which bump format got the most replies
- Average reply rate by bump type
- Any new bump angle that worked surprisingly

Keep `## Bumps that worked` and `## Bumps that flopped` lists at the
bottom. Build empirically.

## Bumps that worked

(Empty - fill after first batch of bumps gets responses.)

## Bumps that flopped

(Empty.)
