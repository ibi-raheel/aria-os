---
title: LinkedIn connect-note templates
updated: 2026-04-28
char_limit: 300
target_chars: 140-200
voice_source: ../../outreach-agent-arcadia/_config/voice.md
---

# Connect-note templates

LinkedIn Premium caps connect notes at 300 chars. **Target 140–200 chars.** Voice rules below override the cap — shorter and sharper always wins.

The personalize stage selects a template by category, fills bracketed slots from enrichment data, runs the voice checklist, and only ships the note if every rule passes. If a slot can't be filled with a concrete anchor, the lead **drops out of today's batch** rather than getting a generic note.

---

## Voice rules (apply to every category)

These mirror `outreach-agent-arcadia/_config/voice.md`. Same user, same voice.

**Structure: name - observation - question.** Two parts. That's it.

1. **Open with their first name + dash + straight into the observation.** No "Hi Sarah, hope you're well." No throat-clearing.
2. **Observation = a specific, verifiable fact about their work.** A particular post, deal, paper, panel, podcast, talk, or bio detail. Generic praise fails.
3. **End with one genuine question they could answer in a reply.** The question IS the CTA. No "would value the connection," no "would love to chat," no "appreciate the connection."

**Hard gates — automatic fail if any of these appear:**

- Robo-opener ("I hope this finds you well," "I was impressed by your...")
- Filler ("quick question," "just wanted to reach out")
- Stock closer ("would value the connection," "appreciate the connection," "would love to be in your network")
- SAT vocabulary (leverage, optimize, myriad, plethora, furthermore, facilitate, utilize, streamline, paradigm)
- Generic specificity (praise without proof — "your work in the community space")
- Begging ("if you could spare a minute," "I know you're busy")
- Stacked asks (more than one question)
- Self-promo ("I'm building in [vertical]" preamble — drop unless it's load-bearing for the question)
- **Em-dashes — zero of them** (AI tell as of 2026; replace with comma + parallel construction, period + new sentence, or colon. Hyphens in compound modifiers like "earn-the-trip" are fine; em-dashes — not.)

**Pass tests:**

- Read it out loud — does it sound like you'd say it to someone at a bar?
- Would the message FAIL with a name-swap? If it works for any random person at the same firm, it's not specific enough.
- You/we ratio at least 2:1 — focus on them, not you.

**Length:** 140–200 chars target, 300 hard cap. If it's over 200, cut.

---

## Templates

Each template is `<First name> - <observation>. <follow-up beat>. <question>?` Slots in `[brackets]`.

### 1. Consulting — partner *(JOB TARGET, never explicit)*

> [first_name] - your [firm] [anchor: piece/post/podcast] on [topic] argues [point]. [contrast or implication beat]. [sharp question rooted in the point]?

**Why this works as a job signal:** asking a McKinsey-specific question grounded in a McKinsey-published piece is harder evidence of firm interest than saying "I admire McKinsey." Specificity is the signal.

### 2. Consulting — recruiter

> [first_name] - [firm]'s work on [practice/positioning] [observation about their angle]. Curious if [implication for their hiring pipeline]?

### 3. Real estate — principal

> [first_name] - the [deal_or_property_short_name] [anchor: deal action] [point about timing/structure/market]. Curious what made [specific tactical question]?

### 4. Real estate — advisor (broker / attorney)

> [first_name] - your [anchor: panel/piece/talk] argued [point]. [contrast / where you'd expect the data to land]. What's [data question rooted in their observation]?

### 5. Founder

> [first_name] - your [anchor: launch/post/pivot] [observation about the specific tradeoff they made]. [contrast: what most of the thread expected]. [question on the deciding factor]?

### 6. Investor (general)

> [first_name] - your [anchor: essay/post/panel] argued [point]. Curious if [follow-on question testing the implication]?

### 7. YC partner / group partner

> [first_name] - your [anchor: post/talk] framed [topic] as [point]. Curious how that lens shaped [specific decision they had to make]?

### 8. a16z (GP / partner)

> [first_name] - your [anchor: post/podcast] argued [point]. That implies [follow-on consequence]. Is that how you'd sequence it?

### 9. Tier-1 VC

> [first_name] - your [anchor: post/investment] pattern-matches to [historical analog]. [observation about the analog]. Which [analogous question rooted in the present]?

### 10. Big Tech exec (VP+ at FAANG)

> [first_name] - your [anchor: talk/paper/post] flagged [specific technical tradeoff]. Curious what [use case or data point] finally pushed you to make that call?

---

## Worked examples — ILLUSTRATIVE ONLY

> ⚠️ **These examples use placeholder names and fabricated anchors.** They show what a *filled* template looks like at the right rhythm and length. **Do not copy these phrasings into production sends.** In production, every anchor must come from actual LinkedIn enrichment, citing a real URL and date. If enrichment didn't surface a verifiable anchor, the lead drops — never substitute a plausible-sounding guess.

### 1. Consulting partner

> *Placeholder target: a McKinsey partner who recently published on agentic AI*
> *Placeholder anchor: their published piece arguing workflow comes before tool*

[first_name] - your McKinsey piece on agentic AI argues workflow before tool. Most enterprise AI I see flips that. What made you sequence it the other way?

*(~148 chars)*

### 2. Consulting recruiter

> *Placeholder target: a Bain experienced-hire recruiter*
> *Placeholder anchor: Bain firm-level posts about a practice positioning shift*

[first_name] - [firm]'s [practice] frames [topic] as [recasting], not [default frame]. Curious if that's pulling experienced hires from atypical backgrounds yet.

*(~155 chars after fill)*

### 3. Real estate principal

> *Placeholder target: a senior REIT exec at an office REIT*
> *Placeholder anchor: a refinancing announcement they led*

[first_name] - the [property_short_name] refi pushed the maturity ladder out two years. Curious what made now the right window vs. waiting for the next pivot.

*(~145 chars after fill)*

### 4. Real estate advisor

> *Placeholder target: a tenant-rep broker who appeared on an industry panel*
> *Placeholder anchor: their panel argument about a counter-intuitive market dynamic*

[first_name] - your [conference] panel argued [point]. That's backwards from where I'd expect [the data] to land. What's the data showing?

*(~150 chars after fill)*

### 5. Founder

> *Placeholder target: a founder who recently shipped a public launch*
> *Placeholder anchor: a tradeoff in their launch that runs counter to community expectation*

[first_name] - your launch shipped [feature] but went [their_choice]-only. The thread expected [other_choice] given [common_expectation]. What pushed you to [their_choice]?

*(~150 chars after fill)*

### 6. Investor (general)

> *Placeholder target: a seed-fund partner who published a thesis essay*
> *Placeholder anchor: an argument in their essay testing a common assumption*

[first_name] - your essay argued [point]. Curious if [founder_archetype] mistake that gap for [common_misread] by default.

*(~150 chars after fill)*

### 7. YC group partner

> *Placeholder target: a YC group partner who posted about a batch composition*
> *Placeholder anchor: a framing in their post that implies a selection lens*

[first_name] - your post framed the [batch] [cohort] as [framing]. Curious how that lens shaped which apps got cut at partner round.

*(~155 chars after fill)*

### 8. a16z

> *Placeholder target: an a16z GP who recently appeared on a podcast*
> *Placeholder anchor: an argument from the podcast with a downstream implication*

[first_name] - your podcast argued [point]. That implies [follow_on_consequence]. Is that how you'd sequence it?

*(~155 chars after fill)*

### 9. Tier-1 VC

> *Placeholder target: a Tier-1 VC GP who published a public market post*
> *Placeholder anchor: a historical-analog argument in the post*

[first_name] - your [topic] post pattern-matches to [historical_analog]. [observation about analog]. Which [present_day_analog_question] would you bet against today?

*(~155 chars after fill)*

### 10. Big Tech exec

> *Placeholder target: a senior Big Tech engineering / product leader*
> *Placeholder anchor: a specific tradeoff flagged in their conference talk or paper*

[first_name] - your [conference/paper] flagged [specific technical tradeoff]. Curious what use cases finally pushed you to make that call.

*(~155 chars after fill)*

---

## The voice checklist (run on every note before send)

1. [ ] Opens with first name, dash, straight into observation
2. [ ] Observation is a specific, verifiable fact about their actual work
3. [ ] Question is genuinely interesting AND answerable in a reply
4. [ ] No filler opener
5. [ ] No stock closer ("would value the connection" etc.)
6. [ ] Read out loud — sounds like a person, not a webinar script
7. [ ] Sentence rhythm varies (no 3 same-length sentences in a row)
8. [ ] Zero SAT vocabulary
9. [ ] Would FAIL with a name-swap (the specifics would be wrong)
10. [ ] You/we ratio ≥ 2:1
11. [ ] Within 140–200 char target
12. [ ] One question, never stacked
