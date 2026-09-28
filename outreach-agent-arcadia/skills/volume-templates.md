# Volume Templates

Structure guides for the volume tier (all non-top-10 leads). Stage 04
uses these as shape references - **every actual message must be
LLM-written from the dossier, never fill-in-the-blank.**

**Read `_config/voice.md` first.** Every message must pass every rule in
that file. The tone is a young entrepreneur who admires their work and
genuinely believes their product could help - humble but confident in
what you've built.

---

## Variables (filled from dossier frontmatter)

| Variable | Source |
|---|---|
| `{name}` | Lead's first name |
| `{community_name}` | Their community/course name |
| `{member_count}` | Paid member count (or "your members" if unknown) |
| `{platform}` | Platform they're on (Skool, Discord, Circle, etc.) |
| `{signal}` | One company-level signal from the dossier: recent milestone, content topic, complaint, launch, platform migration. Must be specific enough to fail the name-swap test. |
| `{framework}` | Frontmatter field - which framework was used (PAS, BAB, 3C, etc.) |
| `[DEMO_LOOM_URL]` | Reusable demo Loom URL (same for all volume sends) |

---

## Email templates

### Template A - Default (observation + demo)

**Subject:** `{community_name}`
**Framework:** `observation`

```
{name} - {signal}.

been looking at how {community_name} runs on {platform} - your
{member_count} members are doing a lot just to participate right
now (different logins, content in different places, the usual).
what if that was all in one place?

recorded a 3-min walkthrough of what your setup could look like:
[DEMO_LOOM_URL]

worth exploring?

- ibi
```

~65 words. Parenthetical, dash, question pivot, interest CTA. You/we: 3:0.

### Template B - PAS (use when dossier shows tool fragmentation)

**Subject:** `quick thought`
**Framework:** `PAS`

```
{name} - {community_name} across {platform} means your
{member_count} members are juggling multiple places just to be
part of one community. every tool you add makes their experience
a little worse and your admin a little harder (and they feel it,
even if they don't say it).

we put everything in one place. 3-min walkthrough of what it
looks like for your community: [DEMO_LOOM_URL]

relevant to where you're focused right now?

- ibi
```

~75 words. Parenthetical, rhythm varies (long → medium → long → short
CTA). You/we: 4:1.

### Template C - BAB (use when dossier shows vision-oriented creator)

**Subject:** `idea for {community_name}`
**Framework:** `BAB`

```
{name} - right now your {member_count} members sign up, get a
login email, and land in a feed that looks like everyone else's.

what if instead they got an avatar, walked through your academy,
and earned XP for actually engaging? the community becomes the
product - not just a tab they check sometimes.

put together what that looks like for {community_name}:
[DEMO_LOOM_URL]

curious?

- ibi
```

~70 words. Dash, contrast structure (current vs. future), specific
imagery. You/we: 3:0.

### Template D - 3C (use when strong case study match in their niche)

**Subject:** `{community_name}`
**Framework:** `3C`

```
{name} - {signal}. genuinely - your community is doing something
different on {platform} and it caught my attention.

we just built something similar for a [niche]-focused community
and the response has been kind of surprising. recorded a 3-min
walkthrough of what it could look like for yours: [DEMO_LOOM_URL]

worth a look?

- ibi
```

~60 words. Conversational aside ("genuinely"), conditional ("kind of
surprising"). You/we: 2:1.

---

## DM templates (NO LINK in first message)

All DMs tease the Loom. Link is sent after any reply signal.

### Twitter DM (~150-200 chars)

```
{name} - {signal}. been building something for communities
like {community_name} - recorded a walkthrough that might be
worth your time. want me to send it?
```

### Skool DM (~200-250 chars)

```
{name} - {community_name} with {member_count} members caught
my eye. your community's outgrowing the forum layout (kind of
ironic to say on skool) - put together a demo of what your
setup could look like. want to see it?
```

### Discord DM (~100-150 chars)

```
{name} - been looking at {community_name}. built something
your members would actually get - want me to send a
walkthrough?
```

### Instagram DM (~200-250 chars)

```
{name} - been looking at {community_name}. your content and
your community deserve better than a feed layout - built
something around that idea. recorded a quick demo if you're
curious.
```

### LinkedIn DM (~300-350 chars)

```
{name} - came across {community_name} on {platform}. your
members are spread across a few different tools right now
(most communities at your stage are) - we've been building
something that puts all of it in one place. recorded a 3-min
walkthrough if you want to see what it could look like.
```

---

## After they reply (send Loom link)

When a lead replies to a DM (even "sure" or "?"):

```
here it is - [DEMO_LOOM_URL]

3 min. shows what {community_name} could look like. curious
what you think.
```

---

## Rules

- Never start with "I" - start with their name or their community
- One link per email, zero links per first-touch DM
- No emojis unless the lead uses them heavily (mirror, don't initiate)
- No price mention - save for Calendly call
- DMs are 2-3 lines max - the Loom does the selling
- Email is 3-4 sentences - Loom is the payload
- `{signal}` must reference something specific to THAT lead - if you can
  swap in any other creator's name and the message still works, it fails
- Subject line: 1-3 words, lowercase, curiosity-driven (see voice.md
  subject line hierarchy)
- CTA: interest-based only - "worth exploring?" / "curious?" / "want me
  to send it?"
- At least one dash, parenthetical, or aside per email
- No 3+ sentences of similar length in a row
- **Framework tag in frontmatter:** every personalized email must note
  which framework was used

---

## Updating these templates

After every 50 sends, review:
- Open rate on emails (if trackable via cold email tool)
- Reply rate per template variant
- Which platform DMs get responses
- Whether "permission-first" DM approach earns more replies than direct
  tease

Iterate the templates based on data. Log changes in
`memory/decisions/YYYY-MM-DD-template-iteration.md`.
