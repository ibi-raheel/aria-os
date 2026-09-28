---
title: Marketing brain — pre-ship gates + engagement construction
status: active (introduced 2026-05-09)
updated: 2026-05-09
related: voice.md, arcadia-capture-targets.md, cadence.md
canonical_decision: 2026-05-09-twitter-agent-3-slot-restart-and-ICP-pivot
---

# Marketing brain

> Voice tells the post how to sound. Marketing brain decides whether the post earns the slot.

A layer applied AFTER `voice.md`'s gates pass. The voice rules ensure quality (em-dashes, hashtags, name-swap, etc.). The marketing brain ensures **resonance** — that the post will actually compete for attention in feed, not just pass a checklist.

The 2026-05-07 + 2026-05-08 posts (Day 2 + Day 3) passed every voice rule and still didn't go viral. They were "good but boring" — four-paragraph stacks of correct sentences with no visual, no stop-scroll hook, no quotable spine. This file fixes that.

---

## Why this exists (the problem statement)

Twitter's feed is a stop-scroll competition. The voice spec produces sharp posts that read well **standalone**. They don't necessarily *land in feed*. Three failure modes the voice rules don't catch:

1. **Blog-opener structure.** "Day 1. Spent today building..." reads like the first paragraph of a Substack. Feed punishes paragraph stacks; rewards single-claim posts and contrast pairs.
2. **No visual hook.** A wall of text in feed loses to anything with motion, a number on a chart, or a recognizable surface.
3. **Multi-claim density.** Most failed posts try to make 2-3 points at once. Each claim weakens the others. One sharp claim per post lands; three claims cancel out.

Voice rules say "be specific" and "end on a landing." Marketing brain says "compress to one claim, lead with the hook, attach an Arcadia product visual or rotate from the evergreen library."

---

## Master gate (the resonance check — used to inform rewrite, NOT to skip)

Before any post ships:

> **If this got 5 likes and 0 reposts, would I still want it up?**

If the answer is no, the agent **rewrites or shifts content angle** until the answer is yes. The agent does NOT skip the slot — operator directive 2026-05-09 fixed 3 posts/day as the **minimum floor**, not a ceiling. The resonance check informs *how to rewrite*, not whether to ship.

Voice gate runs first; marketing-brain gates run second; resonance gate runs third. All three must pass before ship. If any gate fails, the agent rewrites or pivots to a fallback content track (defined below). Failing all rewrite paths is a brand-level emergency, not a daily-skip option.

---

## The four pre-ship gates (every post, every slot)

Each gate runs after the voice checklist passes. **A post that fails any gate is rewritten or pivoted to a fallback content track — never softened past the gate, never skipped (3 posts/day is the operator-defined minimum).**

### Gate 1 — Hook (first line earns the second)

The first line must function alone as a stop-scroll hook. Not a label. Not a frame. Not "Day N." (Day-N is a *closer* now, not an opener — moved per this spec.) The first line is whatever makes someone stop scrolling.

Hook patterns that work:
- **Specific contrarian claim** — "Stripe builds dashboards that read like compliance docs."
- **Number-first observation** — "600 members. 11 active. 3 regulars. 1 who pays."
- **Named-thing reveal** — "We built a courses dashboard called 'the kiln.'"
- **Honest failure** — "9 of 12 people I pitched this to said 'that's interesting' (they hated it)."
- **Hot take with stakes** — "Belonging compounds. Engagement decays."

Hook patterns that fail:
- **Day-N as opener** — "Day 1. Today I built..." (Day-N is a closer; reader doesn't know what's at stake yet)
- **Setup labels** — "Some thoughts on...", "Quick observation about...", "Here's a thing I noticed:"
- **Vague openers** — "Communities are interesting", "I've been thinking about engagement"
- **Title-of-blog energy** — "Why community is the future" (works for SEO; dies in feed)

**Test:** strip the first line and post it alone. Would anyone read past it? If no — rewrite.

### Gate 2 — Specificity (one number, name, or moment minimum)

The post must contain at least one of:
- A real number (`600 members`, `28 seconds`, `Month 6`, `4 published courses`, `$0 MRR`)
- A named thing (Arcadia feature name, competitor name, person name, place name)
- A concrete moment (a sentence someone actually said, a specific decision, a specific shipped artifact)

Vague claims fail this gate even if they're true. "We're building something different" — fail. "We named ours after a thing that turns clay into vessels" — pass (names a kind of thing, even if abstract).

Voice.md already requires specificity at the *pillar* level. Marketing brain enforces it at the *gate* level — no specific anchor → no post.

### Gate 3 — Visual (anchor/filler hierarchy; **Arcadia-product visuals ONLY** when attached)

**Anchor/filler hierarchy (operator directive 2026-05-09):**

- **Slot 1 is the daily ANCHOR.** It spotlights a specific Arcadia feature from the 7-day rotation (`_config/feature-rotation.md`). It MUST attach a fresh Arcadia screenshot of that feature. Every visit to the profile shows a different product surface. This is non-negotiable.
- **Slot 2 is filler.** Image is optional. If attached, it must be Arcadia-only (same as slot 1). If no Arcadia visual fits the angle, ship text-only.
- **Slot 3 is filler.** Text-only by default. Image only if an Arcadia visual genuinely connects to the news/reshare angle.

**Hard rule on what counts as an image:** every image the agent attaches to ANY tweet is an Arcadia product visual. NO charts, NO graphs, NO comparison tables, NO news-headline screenshots, NO external memes, NO generated illustrations of abstract concepts. Every visual reinforces product recognition.

Acceptable visuals — only these:
- Arcadia dashboard screenshots — `the-kiln`, `studio-overview`, `the-stage`, `members-roll`, etc. per `arcadia-capture-targets.md`
- Arcadia in-world captures — `world-spawn`, `world-stroll` (when GIF pipeline works), `the-tavern`, `the-market`, etc.
- Arcadia design-kit assets — SVGs / illustrations FROM `Arcadia/design/kit/` only (not generic icon libraries, not Gemini outputs of abstract concepts)
- Operator-supplied product captures — operator can drop pre-recorded MP4s / PNGs into `screenshots/<date>/` and the agent uses them

Forbidden visuals (apply to all 3 slots):
- Charts of abstract metrics ("engagement vs belonging curves over 6 months") — even if the data is from Arcadia
- Comparison tables of competitors — visual is words pretending to be a graphic
- News-headline screenshots — slot 3 stays text-only when commenting on news
- Memes, stock illustrations, AI-generated abstract art
- Anything from `Arcadia/design/kit/` that depicts non-product content (logos for unrelated experiments, etc.)

**Per-slot visual rules:**

| Slot | Role | Visual rule | If no Arcadia visual fits |
|---|---|---|---|
| **Slot 1** (feature spotlight / Day-N, 12:00) | **ANCHOR** | **MANDATORY** Arcadia screenshot of today's rotation feature (per `feature-rotation.md`). Fresh capture every day. | If today's feature route is broken, advance to next feature in rotation. Slot 1 NEVER ships without an Arcadia image. |
| Slot 2 (insight/hot-take, 18:00) | filler | Optional. If attached, must be Arcadia-only. Default text-only when no visual fits. | Ship text-only. Don't force a visual that doesn't connect. |
| Slot 3 (news/reshare, 20:00) | filler | Text-only by default. Attach Arcadia visual only if it genuinely connects to the angle. | Text-only is the norm. |

### Feature rotation (replaces evergreen rotation)

Slot 1 no longer uses an "evergreen" library. Instead, a **7-day feature rotation** (`_config/feature-rotation.md`) cycles through Arcadia's product surfaces: world, studio overview, the kiln, the stage, members, billing, world (new angle). Each day's prep task captures a fresh screenshot of that day's feature and drafts copy around it.

The rotation ensures:
- The profile always shows variety (never the same feature two days in a row)
- Every Arcadia surface gets regular visibility
- New features get added to the rotation when they ship

Rotation state tracked in `_config/feature-rotation-state.md`. Captures must pass `arcadia-capture-targets.md` preconditions (Simulation ON for dashboard routes + content-safety scan).

For slots 2 and 3, the old evergreen library still applies as a fallback if a visual is attached (rare for these filler slots).

### Gate 4 — Pattern-fit (added 2026-05-09 from viral-tweet research)

Every post must map to ONE of these recognized viral patterns. Posts that don't fit a pattern feel formless and get scrolled. Patterns are how readers' brains pattern-match in 0.3 seconds; without one, the post can't compete in feed.

| Pattern | Template | Reference example |
|---|---|---|
| **Setup-reveal** | "X isn't Y, it's Z" | "members feel like subscribers, not neighbors" |
| **Specific paradox** | superlative + counterintuitive truth | "The loneliest place on the internet is a Discord with 10K members" |
| **Hidden-problem reveal** | "X dressed up as Y" | "loneliness problem dressed up as an engagement problem" |
| **Contrast list** | "Things that don't: X. Things that do: Y." | the #general / town square contrast |
| **Timeline reveal** | "Month X → Month Y → that last one" | the creator-onboarding timeline |
| **Number-first observation** | specific number leading | "600 members → 11 active → 3 regulars → 1 paying" |
| **Honest failure → pivot → epiphany** | meme×founder, vulnerability + reframe | "9 of 12 said 'that's interesting' (they hated it)" |

If a draft doesn't fit one of these, rewrite it into one. Don't ship "kind of" pattern-shaped posts.

### Gate 5 — Quote-tweetability (the spine test)

Pull the strongest single line from the post. Could it be screenshotted and posted alone, and still mean something?

Pass: "The loneliest place on the internet is a Discord server with 10,000 members and no reason to talk." (works alone, top-rated reference tweet)

Fail: "Building tools for people who care." (true but generic — could be any company)

Pass: "We built a courses dashboard called 'the kiln.' Stripe's read like compliance docs." (specific, contrastive, names two things)

Fail: "Day 1. Spent today building..." (frame, not spine)

If no line in the post passes the standalone test, the post has no spine — rewrite. The agent doesn't skip on a Gate 5 fail; it pivots to a fallback content track until the spine test passes.

The spine test is sharper than "any line that works alone." It's specifically: **mock-frame the strongest line as a Tweetshot. Does it travel? If you saw this fragment screenshotted in someone else's reply with no other context, would it still hit?** If not, the post has no exportable spine.

---

## Hook ban-list (added 2026-05-09 from viral-tweet research)

The first line of every post must be substance, not a label. The hook IS the post's chance to stop scroll. Banned opening patterns:

- ❌ `Day 1.` / `Day [N].` as standalone first line — Day-N becomes a *closer*, not a label
- ❌ `Some thoughts on...` / `Quick observation about...` / `Here's a thing I noticed:`
- ❌ `Hot take:` / `Unpopular opinion:` (the take should BE the take, not announce one)
- ❌ `Just shipped...` / `Just deployed...` (specific version is fine: "Spent today building...")
- ❌ Vague openers like "Communities are interesting" or "I've been thinking about engagement"
- ❌ Title-of-blog-post energy ("Why community is the future")

Allowed hook formulas (per the pattern-fit gate):
- ✓ Setup-reveal opener — "X isn't Y, it's Z"
- ✓ Number-first opener — "600 members → 11 active..."
- ✓ Named-thing reveal — "Built a courses dashboard. Named it 'the kiln.'"
- ✓ Honest failure opener — "9 of 12 said 'that's interesting' (they hated it)"
- ✓ Specific paradox — "The loneliest place on the internet is..."

**Day-N policy:** Day-N is a structural anchor for slot 1 only. It appears as a closer (after the substance) or is omitted entirely if the substance carries. NEVER as a label-only first line.

## Single-claim enforcement (added 2026-05-09)

One post = one idea. If a draft has three sentences each making a different claim, kill two and pick one. The strongest one stays; the others become future posts.

The deleted Day 2 + Day 3 posts and the original kiln draft all violated this — each tried to do 2-3 things in one post. The reference tweets each do exactly ONE thing. Compression is the work.

Test: read the draft. Pull each distinct claim into a list. If you have more than one claim, the post is doing too much. Pick the sharpest claim, build the post around it, save the others.

## Char range (tightened 2026-05-09 from viral-tweet research)

- **Target: 80-180 chars.** Reference tweets in voice.md average ~125 chars. The tightest (80 chars) hit hardest.
- **Hard cap: 280 chars** (Twitter's limit). But anything pushing past 200 chars should re-pass the single-claim test — usually the post is doing too much.
- **Was: 200-260** in earlier drafts of this spec. Replaced because the 5/6 launch arc drafts at 254-265 chars were 2× too long versus what the references prove works.

## Engagement-velocity awareness (added 2026-05-09 from viral-tweet research)

Twitter's algorithm rewards engagement velocity in the first 30-60 minutes. 80% of total engagement happens in the first 3 hours. The hook does the heavy lifting in that critical window — if the first line doesn't earn the second, the post is dead before noon.

Implication for the draft stage: the hook gate (Gate 1) is more important than any other gate. A post that fails Gate 1 is essentially un-savable; a post that fails Gates 2-5 can usually be rewritten. Allocate rewrite cycles accordingly.

## Ship-every-slot enforcement (3 posts/day MINIMUM, no skip)

**Operator directive 2026-05-09:** 3 posts/day is the minimum floor. The agent does NOT have permission to skip slots. Quality is enforced through *rewrite* and *fallback content tracks*, never through cutting volume.

The pipeline:

```
For each slot:
  1. Try the primary content track for that slot (build-in-public / insight-with-visual / news-commentary)
  2. Run voice checklist (voice.md gates 1-13)
  3. If voice fails → rewrite. If repeated rewrite fails → pivot to fallback track (below)
  4. Run marketing-brain gates 1-4
  5. If hook/specificity/quote-tweetability fails → rewrite. If repeated rewrite fails → pivot to fallback track
  6. If visual gate fails (slot 1 or 2 needs Arcadia visual) → use evergreen rotation. NEVER skip the slot.
  7. Run resonance check
  8. If "no, I wouldn't want this up" → rewrite OR pivot to fallback track. Never skip.
  9. Ship.
```

The fallback content tracks (defined below) ensure every slot has a content angle that passes gates even on slow product days.

### Fallback content tracks (per slot)

When the primary content track has no fresh signal, the agent picks from the fallback library for that slot. Each fallback is pre-engineered to pass voice + marketing-brain gates by design.

**Slot 1 — Feature spotlight fallbacks** (when today's rotation feature is unreachable):

| Fallback | What it is | When to use |
|---|---|---|
| Next feature in rotation | Advance to the next feature in the 7-day cycle | Today's feature route is broken or returns an error |
| Re-angle a prior feature | Same feature, different copy angle (e.g., world-spawn posted Day 1 as "place not feed"; re-angle Day 8 as "your members are the NPCs") | Full cycle complete, all features posted, need fresh angle on repeat |
| New-ship override | A feature that just shipped TODAY gets priority over the rotation | Arcadia git log shows a user-visible change in the last 24h |

**Slot 2 — Insight/hot-take fallbacks** (when no fresh insight):

| Fallback | What it is | When to use |
|---|---|---|
| Curated reshare | Quote-tweet of a strong post from the cohort (gaming/AI/tech) with our sharp take added as a layer | Most days when no fresh original insight lands |
| Pillar restatement | One of voice.md's reference tweets, rephrased for today's frame | Rare — limit to 1× per 2-week window |
| Founder honesty | A specific operating struggle or non-obvious learning, not a hot take (e.g., "Month 4 mistake: I built features the loudest 3 members asked for. They left. The quiet 80% who stayed needed something else.") | When a hot take feels forced |

**Slot 3 — News/reshare fallbacks** (when no news angle):

| Fallback | What it is | When to use |
|---|---|---|
| Curated reshare | Same as slot 2 fallback — quote-tweet from cohort with layered take | Most quiet news days |
| Industry observation | Sharp observation about a public data point (e.g., "Discord IPO filings show $X in revenue but $Y users per server. The math says people are paying to be lonely.") | When public data has a clean story |
| Heritage tweet (rare) | Republish + reframe one of our own past tweets that aged well | Rare — operator-only override; agent doesn't pick this autonomously |

### What does NOT happen

- The agent does NOT log "skipped — no signal" and exit.
- The agent does NOT post obvious filler ("just thinking about communities today!") to fill the slot.
- The agent does NOT recycle yesterday's post or duplicate.
- The agent does NOT pad word count to hit a number; the post still respects voice.md char-count rules.

If after rewriting + walking the fallback library, NO content passes gates — that is a brand-level emergency, not a daily-skip option. The agent posts to Slack `#twitter-arcadia` with the failure detail, and **the operator decides** whether to manually compose, allow a low-bar post for that slot, or treat it as the rare exception. This should happen <1× per quarter, not weekly.

---

## Worked examples — rewrites of failed drafts

### Example 1 — "the kiln" (slot 1 launch arc, 5/6)

**Original** (254 chars, 4 paragraphs):
> Day 1.
>
> Spent today building "the kiln." A courses dashboard where you publish what's finished and keep what's drying.
>
> Stripe builds dashboards that read like compliance docs. We named ours after a thing that turns clay into vessels.
>
> Building tools for people who care.

Diagnosis: blog-opener structure (Day 1 as label, not hook), three claims layered (the kiln / Stripe contrast / people who care), no visual, last line is generic.

**Rewrite** (after marketing-brain pass, ~140 chars):

> Stripe builds dashboards that read like compliance docs.
> We built one called "the kiln."
>
> Day 1.

Attached: `the-kiln` PNG (per arcadia-capture-targets.md, after operator cleans test data).

What changed:
- Hook now leads with the contrast claim (Gate 1 ✓)
- Names two things — Stripe + the kiln (Gate 2 ✓)
- Visual attached (Gate 3 ✓)
- Spine line is screenshot-ready: "Stripe builds dashboards that read like compliance docs. We built one called 'the kiln.'" (Gate 4 ✓)
- Day-N moved to closer beat — anchors without front-loading

### Example 2 — "the right question" (slot 2 launch arc, 5/6)

**Original** (245 chars):
> Most platforms ask: "how do we get more engagement?"
>
> The right question: "what reason do my members have to come back tomorrow if there's no new content?"
>
> In Arcadia, the answer is the tavern. The same people in the same room.
>
> Belonging compounds.

Diagnosis: not bad! Hook is the contrastive question. But text-heavy and the visual is missing — slot 2 needs an Arcadia product visual.

**Rewrite** (compressed + Arcadia visual attached):

> Most platforms ask: "how do we get more engagement?"
> The right question: "what reason do members have to come back if there's no new content?"
>
> Belonging compounds.

Attached: `the-tavern` in-world capture (when bootstrapped) OR an evergreen `world-spawn` Arcadia capture rotating from the library.

What changed:
- Compressed by removing "the same people in the same room" — redundant with the visual
- Visual is an **Arcadia in-world capture**, NOT a chart of "engagement curves vs belonging curves." That kind of abstract-data chart is forbidden under the product-only visual rule.
- Spine: "Belonging compounds" (saved by the contrastive question above it being quote-tweetable)
- If no in-world capture available, evergreen rotation pulls `world-spawn`. Slot ships either way; never skipped.

### Example 3 — "loneliest place" (slot 3 launch arc, 5/6)

**Original** (188 chars):
> The loneliest place on the internet is a Discord server with 10,000 members and no reason to talk.
>
> Engagement metrics treat this as a success case.
>
> We're building Arcadia because it isn't.

Diagnosis: this one already passes most gates. Hook is strong (named thing + specific number). Spine is screenshot-ready. Compact. Even text-only this lands.

**Marketing-brain pass: ship as-is.** Optional visual if available — a screenshot of a Discord with grayed-out timestamps, or a simple "10,000 / 11" graphic. Not required for slot 3.

This is the model — the kind of post the marketing brain *encourages*. Use it as a positive reference.

### Example 4 — "place is harder" (slot 4, 5/6 — was operator-dropped slot 4 of 4-tweet arc)

**Original** (265 chars):
> First day shipping in public.
>
> I keep wanting to call this "the platform" or "the tool." It's neither. It's a place.
>
> Place is harder to build. The metrics don't tell you it's working until someone says "I made a friend here."
>
> Building until someone says it.

Diagnosis: vulnerable, specific, ends on the human. But "First day shipping in public" is a label opener (fails Gate 1). And it's three paragraphs.

**Rewrite** (~160 chars):

> "Platform." "Tool." Both are wrong.
>
> What we're building is a place.
>
> Place is harder. The metrics don't tell you it's working until someone says "I made a friend here."

What changed:
- Hook is now the contrastive name-swap (Gate 1 ✓)
- Compressed by 40%, drops the "First day shipping in public" frame
- Spine: `"I made a friend here"` is the screenshot line (Gate 4 ✓)

Day-N closer is optional here; the post stands without it.

---

## Engagement layer

3 engagements/day = 15/week. The cohort is gaming + tech/AI (broad). Two pieces: how the agent picks targets, how it constructs replies.

### Cohort generation — auto-fill when uncurated

`_config/engagement-cohorts/<YYYY-WW>.md` is the operator's curated weekly list. If it's missing or empty when the agent runs, **the agent generates one and proceeds** rather than skipping.

Generation procedure:
```
1. Walk Twitter searches for ICP keywords:
   - Gaming: "indie game dev", "Phaser", "Godot", "cozy game", "game design",
             "social sim", "community game", "Stardew clone"
   - Tech/AI: "AI founder", "dev tools", "Anthropic", "OpenAI", "Vercel",
              "Stripe engineering", "agent infrastructure"
2. Filter results:
   - ≥1K followers
   - Posted in last 24 hours
   - Most recent post has ≥3 replies AND ≥10 likes (real engagement signal —
     filters zombie accounts, AI bots, follow-back farmers)
   - Not in cohort within last 30 days (de-dup)
3. Pick 15+ handles. Write to <YYYY-WW>.md with frontmatter:
   ---
   week: 2026-W19
   generated_by: agent (operator-curated cohort missing)
   generated_at: <ISO timestamp>
   handles: [@x, @y, @z, ...]
   ---
4. Proceed to engagement step.
```

### Engagement target selection (within cohort, daily)

From the cohort, pick 3 posts per day with hooks worth engaging:
- **Specific claim** with named competitor or specific number — strong hook
- **Contrarian take** — adjacency for our take
- **Technical detail** about something we know (Phaser, AI agents, community tools)
- **Question post** — open invitation for thoughtful response

Avoid:
- Pure self-promotion ("just shipped X!") — nothing for us to add
- Personal life posts — not relevant to brand
- Already-engaged posts (we replied or QT'd within 30 days)

### Reply construction (the three patterns)

Every reply must add a layer. Three approved patterns:

**1. Specific contrarian take.**
Format: "Agree on X, but..." OR "True, except..."
Example: "Agree the algorithm rewards engagement. But the engagement it rewards (rage replies, bot likes) is the kind that makes communities lonelier — that's why everyone's burning out."

**2. Adjacent angle.**
Format: "Yes, and..." OR "This connects to..."
Example: "This rhymes with what we found in Arcadia — a 600-member Discord can have 11 active and 3 regulars, and the metrics still call it a 'thriving community.'"

**3. Probing question that opens a thread.**
Format: "Does this hold for X?" OR "Is the same true when..."
Example: "Does this break down for invite-only communities? Curious whether the curve is steeper or flatter when there's no public discovery."

Forbidden:
- "Great post" / "Love this" / "Couldn't agree more" — these are noise; algorithm de-prioritizes them
- Single-emoji replies
- Pure summary of what they said
- Hard product pitches ("Arcadia solves this!") — references to our work are fine if they actually apply (pattern 2), pitches are spam

### Authenticity check

The reply should sound like a human who happens to be building Arcadia, not a marketing bot. Test:

> If we removed the Arcadia mention from this reply, does it still add value?

If yes — ship. If no — the reply is a sales pitch dressed up. Rewrite or skip.

### 30-day rule

Don't engage with the same person twice in 30 days. Avoids stalker pattern.

Tracked in `06-engage/<date>/engage.md` records — agent reads back 30 days when picking today's targets.

---

## Implementation

### Where this lives

- This file: `twitter-agent/_config/marketing-brain.md` — the spec.
- Read by: `/twitter-draft` slash command (gates applied per slot during draft) and `/twitter-engage` slash command (cohort gen + reply construction).
- Referenced by: `voice.md` (cross-link), `cadence.md` (3-posts-minimum rule + fallback content tracks), `arcadia-capture-targets.md` (visual sourcing — Arcadia-product only).

### When the gates fire

```
/twitter-draft per-slot pipeline:

  1. Pull signal for the slot (signals.md / news brief / build-in-public source)
  2. Draft initial post per voice.md hybrid mode for that slot's content track
  3. Run voice.md checklist (gates 1-13 in voice.md)
  4. If voice gates fail → rewrite. If repeated rewrite fails → pivot to fallback content track. Re-run voice gates.
  5. If voice gates pass:
     a. Run Gate 1 — Hook test. Check first line against the hook ban-list. If fail, rewrite hook. If repeated rewrite fails → fallback track.
     b. Run Gate 2 — Specificity. If no number/name/moment, rewrite to add one. If repeated rewrite fails → fallback track.
     c. Run Gate 3 — Visual.
        - Slot 1 (anchor): MANDATORY Arcadia image. If no fresh capture, pull from evergreen rotation. NEVER ships text-only.
        - Slot 2 (filler): optional. If a visual fits, use Arcadia-only. Otherwise text-only.
        - Slot 3 (filler): text-only by default. Attach only if Arcadia visual genuinely connects.
     d. Run Gate 4 — Pattern-fit. Map the post to one of the 7 viral patterns. If no pattern fits, rewrite to fit one. If repeated rewrite fails → fallback track.
     e. Run Gate 5 — Quote-tweetability (spine test). If no exportable spine line, rewrite. If repeated rewrite fails → fallback track.
     f. Single-claim check. Count distinct claims. If >1, kill the weaker ones, save them as future-post candidates.
     g. Char range check. Target 80-180; hard cap 280. If over 200, re-run single-claim — almost always the post is doing too much.
     h. Run resonance check (master gate). If "no, I wouldn't want this up at 5 likes / 0 reposts" → rewrite or pivot to fallback.
  6. Ship to /twitter-screenshot (for slot 1 always; for slots 2-3 only if visual attached) and /twitter-post.

The agent ships every slot every weekday. Skipping is not allowed.
If after rewrite + ALL fallback tracks NOTHING passes — that's a brand-level emergency.
Post the failure to Slack #twitter-arcadia and stop the slot.
This should occur <1× per quarter.
```

### Logging shape (rewrite + fallback used)

```yaml
# 04-posted/2026-05-15/slot-2.md
---
slot: 2
date: 2026-05-15
status: posted                       # always "posted" for routine days; "emergency_held" if op intervention needed
content_track: fallback_curated_reshare  # primary | fallback_<name>
rewrites: 2                          # how many revision passes before passing all gates
visual_source: evergreen_rotation    # fresh_capture | evergreen_rotation | text_only_slot_3
visual_used: world-spawn             # for trace
day_n: 8
permalink: https://x.com/IbiRaheel/status/...
---

# Optional: notes on why fallback was used (informs next sprint's content planning)
- No fresh insight signal today; pivoted to curated reshare of @<handle>'s post.
- Evergreen world-spawn used because no /world fresh capture available.
```

### Metrics + feedback loop

Track per-week (in `07-metrics/<week>/`):
- Primary vs fallback content-track ratio per slot — if slot 1 is hitting fallbacks >40% of weekdays, the build-in-public signal pipeline is thin; investigate Arcadia signal sourcing.
- Rewrites per slot before ship — if average rewrites/slot > 3, the agent is straining; voice or gates may be miscalibrated.
- Reply rate per post — target ≥1 reply per post by week 4.
- Quote-tweet rate — target ≥1 QT per 5 posts by week 8.
- Engagement quality on our cohort replies — did they reply back? Did they reciprocate?
- Emergency hold rate — `<1 per quarter` is healthy. More frequent = the fallback library is undersized; expand it.

If posts are shipping (which they will, every weekday) but resonance metrics are flat after 4 weeks, the gates need tightening, not loosening. Loosening gates is the wrong response to weak resonance.

---

## What this changes vs. the prior agent

| Old | New |
|---|---|
| Day-N is label opener of slot 1 | Day-N is closer or omitted; substance is the hook (per hook ban-list) |
| Slot 2 visual REQUIRED, skip if missing | Slot 1 visual MANDATORY; slot 2 + 3 visual OPTIONAL |
| Voice gate is final filter | Voice gate first, 5 marketing-brain gates next, resonance gate last |
| Cohort missing → engagement step skipped | Cohort missing → agent self-generates from gaming/AI Twitter |
| Replies allowed if voice-correct | Replies must add a layer (3 patterns) — generic replies forbidden |
| Skip-rather-than-ship | 3 posts/day MINIMUM, skip not allowed; rewrite + fallback tracks enforced |
| Visuals optional, any kind allowed | Arcadia-product visuals ONLY when attached; charts/graphs/external screenshots forbidden |
| Char range 200-260 | Char range 80-180 (research-backed; reference tweets average ~125) |
| No pattern-fit gate | Posts must map to 1 of 7 recognized viral patterns (Gate 4) |
| No hook ban-list | Banned: "Day N." opener, "Some thoughts on...", "Hot take:", vague openers |
| No single-claim rule | One post = one idea; multi-claim drafts get the weakest claims killed |

---

## Open items (future iterations)

- **Image-generation pipeline.** When slot 2's visual needs to be a graph or chart we don't have a screenshot for, the agent needs to generate it. Options: HTML+Chart.js+Playwright screenshot (no API cost), or Gemini API (when key configured). Spec lives in `image-generation.md` — not yet wired.
- **GIF/MP4 capture.** Playwright MCP has no built-in GIF recorder (Chrome MCP's `gif_creator` retired). PNG captures only for now. Operator can manually record MP4 via QuickTime as fallback.
- **Profile-surface check.** Bio + banner + pic must match the post energy. If profile is thin and posts are sharp, the follow-conversion still suffers. Operator-managed, not agent-managed; flagged here for awareness.
- **Threading mode.** For genuine multi-claim ideas, marketing brain currently forces compression. A future "thread mode" would let one slot ship a 3-tweet thread instead of a single tight post. Not enabled yet — too easy to abuse as filler.
