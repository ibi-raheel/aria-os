# Stage 03 - Enrichment

**The most important stage in this pipeline.** For high-touch DFY at
$20k+/mo creators, the message that converts is the one that proves we
understand their business. That understanding lives here.

## Job

Build a comprehensive dossier per qualified lead. Deep enrichment runs
for **all qualified leads** - compute is free, so no light-vs-deep split.
Time budget: 30-45 min agent per lead. At 30-40 qualified leads/day, this
stage runs 15-30 hours of compute - the agent runs unsupervised from
early morning. Ship with `unknown` fields rather than perfect-paralyzing.

## Inputs

| File | Why |
|---|---|
| Accepted leads in `stages/02-qualification/output/` | The leads to enrich |
| `skills/dossier-rubric.md` | The "good enough" specification - what must be captured |
| `memory/templates/person.md` | The dossier schema |

## Process

1. Read the lead from stage 02 (has minimum: name + handle + source +
   one-line evidence)
2. Open `memory/templates/person.md` schema - the dossier has 11 required
   sections (Profile, Business, Stack, Voice, Channels, Engagement,
   Fit, Momentum, Loom hooks, Pitch justification, Disqualifiers)
3. Run the data-collection sweep (see `skills/dossier-rubric.md` for
   easy vs hard sources):
   - Personal site / About page (WebSearch + Playwright MCP)
   - Twitter profile + recent 50 tweets (Playwright MCP)
   - Skool community page (Playwright MCP)
   - YouTube About + recent video titles (YouTube Data API)
   - LinkedIn profile (Playwright MCP, careful)
   - Newsletter (Substack/Beehiiv profile pages)
   - Cross-platform handle search (their name + each platform name)
4. Fill out each section. Mark unknowns explicitly as `unknown` - never
   fabricate.
5. Write 3 specific Loom hooks to the dossier (must be real and recent,
   not generic praise)
6. Surface any disqualifiers - if found, **back-edge to stage 02 for
   re-scoring**, do NOT push to stage 04
7. Write `human_checks.md` next to the dossier listing 3-5 things the
   user must verify manually (anti-scraping blocks, login walls, etc.)
8. Write the comprehensive dossier to `memory/people/<slug>.md` (extends existing dossier if person already exists — never overwrites; merges section-by-section). Create an engagement record at `stages/03-enrichment/output/<slug>.md` with frontmatter `dossier_ref: '[[memory/people/<slug>]]'` and a body line `See dossier: [[memory/people/<slug>|<Name>]]`.
9. **Use `[[wikilinks]]` in dossier body** - link other people as
   `[[memory/people/slug|Name]]` and platforms as
   `[[memory/companies/slug|Platform]]`. First mention only. See root
   `CLAUDE.md` § "Wikilink rules."
10. Move lead file to `stages/03-enrichment/output/<slug>.md`
11. Append to `logs/daily/YYYY-MM-DD.md`

## Output

| Artifact | Location | Format |
|---|---|---|
| Person dossier | `memory/people/<slug>.md` | Full template filled, all 11 sections (identity-only, shared across agents) |
| Engagement record | `stages/03-enrichment/output/<slug>.md` | Frontmatter with `dossier_ref`, status `enriched`, stage-specific notes |
| Human checks list | `stages/03-enrichment/output/<slug>-human_checks.md` | Bullet list of manual verifications |
| Daily log | `logs/daily/YYYY-MM-DD.md` | `## HH:MM - outreach-agent - enriched [[memory/people/x]] (45 min, 9/11 sections, 2 human checks)` |

## What good looks like

- All 11 sections present (with `unknown` where data isn't accessible)
- 3 specific, recent Loom hooks per lead - not generic praise (used for
  top-10 personalized DMs; all leads still get hooks captured)
- Pitch justification paragraph is in the lead's language, not ours
- Channel list is exhaustive - every reachable surface is captured
- Time-to-ship per lead: 30-45 min, predictable
- **Top-10 flag**: after enrichment, rank leads by score + dossier quality.
  Mark top 10 with `tier: top-10` in frontmatter - these get personalized
  Loom intros + custom DMs in stage 04.

## What to avoid

- **Perfect-paralyzing** - better to ship with 9/11 sections complete
  than to spend 4 hours hunting the missing 2
- Fabricating data - `unknown` is always better than a guess
- Skipping the disqualifier check - finding "they're already on Whop"
  in stage 03 saves 5+ hours downstream
- Burning agent time on hard-to-scrape sources (Instagram engagement,
  Substack subscriber count) - push those to `human_checks.md`
- Personalizing the language at this stage (that's stage 04). Capture
  the raw material here.

## Tools used

- WebSearch (broad discovery)
- Playwright MCP (Twitter, Skool, LinkedIn, personal sites, Substack)
- YouTube Data API (free tier - channels.list, search.list)
- Reddit JSON API (their post history)
- HN Algolia API (if technical creator)
- GitHub MCP (if dev-adjacent)

## Tier check

Reads broadly. Writes only to vault and stage outputs. No outreach
actions.

## Closing human checks

When a checklist item in a `*_human_checks.md` file is resolved:

1. Write the verified value back to the canonical file
2. Check the box in the `_human_checks.md` file (`- [x]`)
3. When ALL boxes are checked, move the `_human_checks.md` file to
   `stages/03-enrichment/output/_resolved/`

Do not auto-resolve human checks. Present findings to the user and apply
only after approval.

## Back-edge to stage 02

If during enrichment we discover:
- Revenue evidence is weaker than scored (e.g., Skool community is free,
  not paid)
- A disqualifier (already on Whop, anti-spatial stance, no community)
- Audience demographic is wrong (e.g., enterprise B2B not creator)

→ Move the lead back to `stages/02-qualification/output/` with frontmatter
`back_edge_reason: "..."`. Stage 02 will re-score and likely reject.

This is the only sanctioned back-edge in the entire pipeline.

---

## Validate writes (final step before declaring stage complete)

Run `/validate-writes <output-dir-of-this-stage>`. Read the resulting verdict at `hygiene-agent/integrity/validate-<timestamp>.md`.

- **If PASS:** declare stage complete.
- **If FAIL:** fix every hard fail (apply auto-fixes where the validator marks them available; manual repair otherwise). Re-run `/validate-writes`. Repeat until PASS.
- **Do NOT declare stage complete until you have a PASS verdict file.**

This is the prevention layer — no bad data should propagate to the next stage. See `hygiene-agent/03-validate/CONTEXT.md` for what the validator checks.
