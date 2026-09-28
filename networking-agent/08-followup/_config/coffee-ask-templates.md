---
title: Coffee-ask DM templates
updated: 2026-05-04
char_target: 200-380
char_hard_cap: 400
voice_source: ../../../outreach-agent-arcadia/_config/voice.md
---

# Coffee-ask templates

DMs sent on Tue/Thu to LinkedIn connections who already accepted the original invite. Goal: book a 20-minute conversation (phone, video, or async voice — they pick).

## Voice rules (apply to every DM)

Inherits from `../../../outreach-agent-arcadia/_config/voice.md`. Hard gates:

- Zero em-dashes (replace with comma + parallel construction, period + new sentence, or colon)
- Zero filler openers ("hope you're well," "quick question")
- Zero stock closers ("would value your time," "look forward to hearing back")
- 200-400 chars (target 250-350)
- You/we ratio ≥ 2:1
- Name swap test: would FAIL with a different recipient
- Proper sentence case, no all-caps, no emoji
- One imperfection allowed; perfect grammar reads as machine

## Universal structure

```
[name], thanks for connecting. <follow-up beat — picks up the original
question OR introduces a new anchor>. <sharp question rooted in the beat>.
<one-line honest frame: I'm exploring X / I'm building Y / your read on
[specific thing] would be useful>. Can I have <N> minutes of your time
next <day1> or <day2>?
```

## Hard rules for the ask line

- One sentence, plain English
- No format menu (no "phone, video, or async voice")
- No "morning/afternoon" — let them pick
- Two days, not three (specific = answerable; vague = ignored)
- 20 min default; 15 for the most senior; 30 only if operator overrides
- "Can I have" — not "would you be open to" or "would you have time for"

## Re-ask cadence (in-thread DM continuation)

When the recipient replies to a coffee-ask DM with substantive engagement on the question but does NOT commit to a time, the next DM should re-ask the meeting **once**, softly. After that, read the signal.

| DM # | Their last reply | Meeting ask in this DM? | How |
|---|---|---|---|
| 2 (first follow-up reply) | substantive, no time committed | YES — soft | "Tue or Thu still good?" or "Want to push the rest live next Tue or Thu?" |
| 3 | substantive again, still no time | **NO** — drop the ask | continue the thread, let them re-introduce timing if they want it |
| 4+ | continued substance, no time | NO | accept they prefer async; relationship compounds in DM |
| Any | committed a time | stop asking, switch to confirmation | "Tue 9am works — calendar invite incoming" |
| Any | said no / not now | stop asking | accept gracefully, leave the door open |
| Silent 7+ days after re-ask | — | next DM uses a fresh angle, no meeting ask | new anchor + sharp question, not "checking in" |

**Why this rule exists.** Senior people answer the question they want to engage with. If they answer your *substance* twice while skipping your *meeting ask* twice, they're telling you they prefer async. Pushing past that converts a productive async conversation into a pressure dynamic, and senior people read pressure fast. The relationship still compounds in DM; most who become real conversations eventually offer the meeting on their own timing once they've decided you're worth their time. Forcing it earlier costs more than it gains.

**Operator override.** This rule can be broken when the conversation is *clearly* substantive enough that the operator wants to lock time before it cools. In those cases, the re-ask in DM #3 should be even softer ("if it's easier in 10 min on the phone, I'm around Tue/Thu — otherwise happy to keep this thread going") and never present in DM #4+.

## Two shapes (matched to acceptee state)

### Shape 1 — recent accept, original anchor still hot

The connect-note's question is fresh in their mind. Pivot it forward into a sharper version. Continuity signals you meant the first question; you weren't running a template.

**Pattern:**
```
[name], thanks for connecting. More on [original question topic]:
[contrast / where the question goes next]. <sharp follow-up question
that pays off the original>. <honest frame>. Can I have 20 minutes of
your time next [day1] or [day2]?
```

**Worked example — Scott Blackburn (consulting, recent accept, JOB TARGET):**

> Scott, thanks for connecting. More on the centennial-discipline question: private centennials are disciplined; federal centennials famously aren't. Does your VA + America@250 lens read that gap as selection pressure or as a capability-building story? I'm exploring strategy roles at MBB and your read on the public-sector cut would be useful. Can I have 20 minutes of your time next Tuesday or Thursday?

(~380 chars)

### Shape 2 — old accept (or silent recent accept), need new anchor

The original anchor is stale or never landed. Lead with a NEW anchor (their recent post, panel, deal, paper). Make the original invite invisible scaffolding — don't reference it.

**Pattern:**
```
[name], thanks for connecting. <new anchor: "saw your [recent thing]" /
"your [deal/paper/post] caught my eye">. <observation about specific
point in the new anchor>. <sharp question rooted in that point>. <honest
frame>. Can I have 20 minutes of your time next [day1] or [day2]?
```

**Worked example template — founder, silent accept, new anchor:**

> [name], thanks for connecting. Saw your launch-day post on the four-stall market UI — the "build the room first, monetize later" call ran counter to most of the thread. I'm building Arcadia (community-as-place) and your read on how you sequenced that bet would be useful. Can I have 20 minutes of your time next Tuesday or Thursday?

(~310 chars)

## Category × shape templates

Each category gets two template variants (Shape 1 / Shape 2). Slots in `[brackets]` filled from the dossier + sweep snapshot.

### Consulting — partner / senior partner *(JOB TARGET)*

**Shape 1:**
> [first_name], thanks for connecting. More on the [original_question_topic]: [contrast or extension]. [sharp follow-up question]. I'm exploring strategy roles at MBB and your read on [specific cut] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Your [recent_anchor: piece/post/talk] on [topic] argued [point]. [contrast or implication]. [sharp question]. I'm exploring strategy roles at MBB and your perspective on [specific area] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

### Consulting — recruiter

**Shape 1:**
> [first_name], thanks for connecting. Following our exchange on [original_topic]: [extension]. [sharp question]. I'd value your read on what experienced-hire pipelines into [practice] are looking for in 2026. Can I have 15 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Your [firm]'s recent [anchor: report/post/initiative] on [topic] reframes the [practice] story. Curious what that's pulling into the experienced-hire pipeline. I'm exploring [specific role/level] roles and your read on fit would be useful. Can I have 15 minutes of your time next [day1] or [day2]?

### Real estate — GATED (template pending)

> ⚠️ **Real-estate is currently gated from the follow-up stage** (decision: 2026-05-06).
>
> The two earlier RE template variants below are draft-only — they were never validated against the operator's actual real-estate goal (lease diligence ≠ networking peer-talk). The operator wants a different message structure for RE candidates that doesn't read like a peer founder/investor ask. Until that structure is drafted and approved, RE candidates auto-skip in `02-classify/` with reason `real-estate-template-pending`.
>
> Lift the gate by:
> 1. Drafting the new RE template variants here (replace this gated note)
> 2. Removing `real-estate` from `_config/daily-quota.md` `followup_category_gates`
> 3. Documenting the lift in a decision record
>
> Until then, RE candidates remain eligible for the regular MWF send pipeline. Only the coffee-ask follow-up is gated.

**Earlier draft variants (DO NOT SEND, kept for reference until the new template is drafted):**

```
[draft — RE principal Shape 1]: [first_name], thanks for connecting. More on [topic]: [extension]. [question]. Our shop's lease diligence keeps running into [tension]; your read would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

[draft — RE principal Shape 2]: [first_name], thanks for connecting. Your team's [deal/refi] on [property] is interesting against [market backdrop]. [question on tactics]. We're underwriting a similar [deal type]; your perspective would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

[draft — RE advisor Shape 1]: [first_name], thanks for connecting. More on the [topic]: [extension]. [data question]. We're working through similar lease-diligence on [property type]; your read on [market dynamic] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

[draft — RE advisor Shape 2]: [first_name], thanks for connecting. Your [panel/piece] on [topic] argued [point]. That contradicts where I'd expect [data] to land. We're working through lease-diligence on [property type]; your read would be useful. Can I have 20 minutes of your time next [day1] or [day2]?
```

### Founder

**Shape 1:**
> [first_name], thanks for connecting. More on [original_question_topic]: [extension]. [sharp follow-up question on the deciding factor]. I'm building Arcadia (community-as-place); your perspective on [specific tradeoff] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Saw your [recent_anchor: launch/post/pivot] on [topic] — [observation about the tradeoff]. [sharp question]. I'm building Arcadia (community-as-place); your read on [specific question] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

### Investor (general / seed / Series A-B)

**Shape 1:**
> [first_name], thanks for connecting. More on [original_question_topic]: [extension into thesis or implication]. [sharp question testing the implication]. I'm building Arcadia in the community-platform space; your perspective on [specific area] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Your [recent_anchor: essay/post/panel] on [topic] argued [point]. [sharp follow-on question]. I'm building Arcadia (community-as-place); your read on [specific angle] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

### YC partner / group partner

**Shape 1:**
> [first_name], thanks for connecting. More on [original_question_topic]: [extension into batch / cohort lens]. [sharp question on selection or sequencing]. I'm building Arcadia in [specific bucket]; your perspective on the cohort patterns would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Your [recent_anchor: post/talk] framing [topic] as [point] reframes how I think about [specific decision]. [sharp question rooted in their frame]. I'm building Arcadia (community-as-place); 20 minutes on [specific area] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

### a16z (GP / partner)

**Shape 1:**
> [first_name], thanks for connecting. More on [original_question_topic]: [extension]. [sharp follow-on question on sequencing or implication]. I'm building Arcadia in [specific space]; your perspective on [specific question] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Your [recent_anchor: post/podcast] argued [point]. [sharp question on the consequence]. I'm building Arcadia (community-as-place); your read on [specific angle] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

### Tier-1 VC

**Shape 1:**
> [first_name], thanks for connecting. More on [original_question_topic]: [extension into pattern-match]. [sharp question rooted in the analog]. I'm building Arcadia in [specific space]; your perspective on the pattern would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Your [recent_anchor: post/investment/panel] pattern-matches to [historical analog]. [sharp question on the present-day cut]. I'm building Arcadia (community-as-place); your read on [specific area] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

### Big Tech exec (VP+ at FAANG)

**Shape 1:**
> [first_name], thanks for connecting. More on [original_question_topic]: [extension into the technical tradeoff]. [sharp question on the deciding factor]. I'm building Arcadia (community-as-place) and your read on [specific technical area] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

**Shape 2:**
> [first_name], thanks for connecting. Your [recent_anchor: talk/paper/post] flagged [specific technical tradeoff]. [sharp question on the use case that pushed the call]. I'm building Arcadia (community-as-place); your perspective on [specific area] would be useful. Can I have 20 minutes of your time next [day1] or [day2]?

## Inbound-connection variant

If the candidate originally sent the invite (we accepted theirs), use this opener instead of "thanks for connecting":

> [first_name], appreciate the invite from your end. <new-anchor or follow-up>. <sharp question>. <honest frame>. Can I have 20 minutes of your time next [day1] or [day2]?

## Voice checklist (run before send)

1. [ ] Opens with first name + "thanks for connecting" (or inbound variant)
2. [ ] Anchor is specific, verifiable, and either (a) continues the original question (Shape 1) or (b) cites a fresh post/piece/deal (Shape 2)
3. [ ] Question is sharp, dichotomous, answerable in 1-2 sentences but interesting for 10 minutes
4. [ ] Honest frame ("exploring strategy roles at MBB" / "building Arcadia") — no vague "would love to chat"
5. [ ] Single ask line: "Can I have 20 minutes of your time next [day1] or [day2]?"
6. [ ] Zero em-dashes
7. [ ] Zero filler openers / stock closers
8. [ ] Zero SAT vocabulary
9. [ ] Sentence rhythm varies (no 3 same-length sentences)
10. [ ] You/we ratio ≥ 2:1
11. [ ] Name swap fails the message
12. [ ] 200-400 chars
13. [ ] Read out loud — sounds like a person, not a bot

If any check fails, revise once. If it still fails, drop the candidate from this run and let the next sweep retry.
