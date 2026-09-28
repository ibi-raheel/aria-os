# Stage 04 - Personalization

## Job

Produce send packages for all enriched leads in two tiers. Every message
generated MUST pass every rule in `_config/voice.md` - word count, you/we
ratio, CTA style, subject line format, link rules. If it doesn't pass,
rewrite until it does.

**Volume tier (all leads):** Templated cold email with demo Loom URL +
one personalized signal. Templated DM for their primary platform - NO
link in first-touch DM.

**Top-10 tier (leads marked `tier: top-10` from stage 03):** Custom Loom
intro script + personalized multi-channel messages. Full cross-referencing
across channels. NO links in DMs - permission-first approach.

## Inputs

| File | Why |
|---|---|
| Canonical lead file (wherever it currently is in the pipeline) | The dossier with Loom hooks |
| The lead's `memory/people/<slug>.md` | Canonical voice / channel data |
| `_config/voice.md` | How we sound, word limits, CTA rules, framework selection, link rules |
| `_config/offer.md` | What we pitch (DFY, $7.5k-$15k) |
| `skills/hook-library.md` | Reusable opening hooks keyed by trigger |
| `skills/loom-script-template.md` | Personalized intro + demo structure |
| `skills/volume-templates.md` | Email and DM templates for volume tier |

## Process - Volume tier (all leads)

1. Read enriched dossier
2. Extract the `{signal}` - one specific, non-generic thing about this
   lead (recent milestone, content topic, hiring signal, platform
   migration, specific post). This must pass the voice.md test: "could
   NOT be said to 1,000 other people"
3. Select email framework based on what the dossier reveals:
   - Unknown problem → Becc Holland variant
   - Tool fragmentation → PAS variant
   - Vision-oriented creator → BAB variant
   - Default → standard template from volume-templates.md
4. Fill the email template with variables: `{name}`, `{community_name}`,
   `{member_count}`, `{platform}`, `{signal}`, `[DEMO_LOOM_URL]`
5. Fill the DM template for their primary reachable channel - **NO link**
   in the DM. Use the permission-first tease.
6. Verify word count (email: 50-80 words, DM: per-platform limit in
   voice.md)
7. Verify you/we ratio (≥2:1)
8. Verify subject line (1-3 words, lowercase, curiosity-driven - see
   voice.md subject line hierarchy)
9. Verify CTA is interest-based (no Calendly, no meeting request)
10. Write to `stages/04-personalization/output/<slug>/email.md` and
    `<slug>/dm.md`
11. Create/update engagement record at `stages/04-personalization/output/<slug>.md` with frontmatter `status: personalized`, `messages_drafted: [email, dm]`

## Process - Top-10 tier (leads with `tier: top-10`)

1. Read enriched dossier
2. Select framework from voice.md's framework table based on dossier
3. Pick the strongest Loom hook from the dossier's top-3 candidates
4. Draft the Loom intro script (30 sec, ~75-90 words) using
   `skills/loom-script-template.md`:
   - Include which of their content to show on screen
   - Quote their words if possible
   - Write 3 bullet points (notice, bridge, setup), not a word-for-word
     script
5. Write the Loom close (10 sec) referencing their specific community
6. For each reachable channel, draft a personalized message:
   - **Cold email** - 3-4 sentences, 50-80 words, `[LOOM_URL]` placeholder,
     framework noted in frontmatter
   - **Twitter DM** - 2-3 lines, ~150-200 chars, NO link, tease the Loom
   - **Skool/Discord/platform DM** - short, platform-aware, NO link
7. Cross-reference: DMs after the email mention "sent you an email
   earlier" or reference the email's hook - don't repeat the same pitch
8. All messages: voice from `_config/voice.md`, offer framing from
   `_config/offer.md`
9. Run the quality checklist (step 6-9 from volume process) on every
   message
10. Write the package as a folder per lead
11. Create/update engagement record at `stages/04-personalization/output/<slug>.md` with frontmatter `status: personalized`, `messages_drafted: [channels]`
12. Move engagement record forward and append to `logs/daily/`

## Quality checklist (run on EVERY message before writing)

- [ ] Word count within channel limit (voice.md)
- [ ] You/we ratio ≥ 2:1
- [ ] Does NOT start with "I"
- [ ] CTA is interest-based (no Calendly, no meeting request)
- [ ] Subject line is 1-3 words, lowercase, curiosity-driven (voice.md
      subject line hierarchy)
- [ ] DMs contain NO links
- [ ] Email contains max 1 link
- [ ] `{signal}` is specific to THIS lead (fails if swappable)
- [ ] No spam-trigger words (voice.md list)
- [ ] No phrases from the "never say" list (voice.md)
- [ ] Framework is noted in email frontmatter
- [ ] Plain text only (no HTML, no formatting, no images)

## Output

| Artifact | Location | Format |
|---|---|---|
| Send package folder | `stages/04-personalization/output/<slug>/` | Folder with sub-files |
| Loom script (top-10 only) | `04/output/<slug>/loom-script.md` | 3 bullet points + close, with face/screen notes |
| Cold email | `04/output/<slug>/email.md` | Subject + body, framework noted, Loom URL placeholder |
| DM (primary channel) | `04/output/<slug>/<platform>-dm.md` | Body, NO link, permission-first tease |
| Other DMs as needed | `04/output/<slug>/<platform>-dm.md` | Body, NO link |
| Daily log | `logs/daily/YYYY-MM-DD.md` | `## HH:MM - outreach-agent - personalized [[memory/people/x]] (N channels)` |

## Frontmatter (per channel file)

```yaml
---
lead: <slug>
channel: email | twitter-dm | skool-dm | linkedin-dm | discord-dm | instagram-dm
status: draft
framework: 3c | pas | bab | unknown-problem | ccq | prize-frame | reply-method
loom_url: [LOOM_URL]   # filled when Ibi records the Loom in stage 05
contains_link: true | false
send_priority: 1-N     # send order across the package
word_count: <N>
created: YYYY-MM-DD
---
```

## What good looks like

- Each message reads like a specific person wrote it to a specific person
- The `{signal}` is verifiable - you could click a link in the dossier
  and find the exact thing referenced
- Email is 50-80 words. DMs are under their platform char limit.
- "You" appears 2x more than "we/I"
- CTA is a soft interest question, not a calendar grab
- DMs contain zero links - the Loom is teased, not sent
- Subject line creates curiosity (1-3 words, lowercase, per voice.md
  hierarchy: specific reference > pattern interrupt > co-brand > idea)
- Voice matches `_config/voice.md` (lowercase, humble young entrepreneur,
  genuine admiration, rhythm variation, human texture, no filler)
- Framework is selected per lead situation, not one-size-fits-all

## What to avoid

- **Mail-merge outputs.** Templates in `skills/volume-templates.md` and
  `skills/hook-library.md` are structure guides, not fill-in-the-blank
  forms. Every message must be LLM-generated from the dossier with a
  unique signal per person. If you can swap in another creator's name
  and the message still works, it fails. Rewrite until it passes.
- Templated hooks ("hope you're well", "saw your great content")
- Generic specificity - praising without proof ("love what you're
  building" with no concrete detail)
- Feature lists in messages (the Loom carries features)
- Stacking asks ("would love to chat AND get your feedback")
- Mentioning price (save for the Calendly call)
- Generating without reading the dossier first
- Personalizing for channels they aren't actually on (verify in dossier)
- Including links in first-touch DMs (spam signal on every platform)
- Exceeding word count limits
- Using the same framework for every lead
- Writing a word-for-word Loom script (write 3 bullet points)

## Tools used

- LLM only. No external calls.

## Tier check

Reads dossier + config + skills. Writes to stage output only. No outreach
actions.

## Hand-off to stage 05

A finished package signals stage 05 to:
1. Cue Ibi to record the Loom (3-5 min recording)
2. Replace `[LOOM_URL]` placeholders in email files (DMs have no link)
3. Execute warm-up protocol for top-10 leads (3-5 days)
4. Run the send sequence per `_config/send-protocol.md`
