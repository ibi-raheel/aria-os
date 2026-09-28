# Stage 01 - Discovery

## Job

Surface 50 candidates/day earning ~$20k+/month from creator-economy work,
across **all community platforms** (Skool, Discord, Circle, Patreon,
Teachable, Kajabi, Mighty Networks, Maven, and more). **No scoring** -
that's stage 02. Just capture the catch and create the lead file.

## Inputs

| File | Why |
|---|---|
| `_config/icp.md` | Hard requirements + disqualifiers - filter at capture, don't capture obvious misses |
| `skills/discovery-sources.md` | Concrete search recipes per source |
| `memory/people/` (existing entries) | Skip already-known leads (dedup) |

## Process

1. Run the source-by-source recipes from `skills/discovery-sources.md`
   (Skool first, Twitter via Google site:, then Reddit/YouTube/HN as
   secondary)
2. For each candidate, gather the minimum capture set:
   - Name + handle
   - Source + source URL
   - One-line revenue evidence
   - Follower count or member count
3. Skip if name already exists in `memory/people/` with status that isn't
   `discovered` (they've already been processed)
4. Write a lead file in `output/<firstname>-<handle>-<source>.md`
5. Create stub `memory/people/<slug>.md` from `memory/templates/person.md` with
   status `discovered`
6. After the batch, append to `logs/daily/YYYY-MM-DD.md`

## Output

| Artifact | Location | Format |
|---|---|---|
| Lead file | `stages/01-discovery/output/<slug>.md` | Frontmatter + 1-paragraph "why this person" |
| Vault stub | `memory/people/<slug>.md` | Person template, status `discovered` |
| Daily log entry | `logs/daily/YYYY-MM-DD.md` | `## HH:MM - outreach-agent - discovery batch: N candidates: [[memory/people/x]] [[memory/people/y]]` |

## Frontmatter schema (lead file)

```yaml
---
name:
handle:
source: skool | twitter | youtube | reddit | hn | github
discovered: YYYY-MM-DD
revenue_evidence: "one-line evidence string"
source_url:
follower_count:
stage_status: discovered
vault_ref: '[[memory/people/<slug>]]'
---
```

## What good looks like

- 50 candidates per daily batch (starts 6 AM, ~2.5 hours runtime)
- Sources diversified across platforms, not just Skool
- Every candidate has at least one piece of revenue evidence with a link
- Zero duplicates with existing `memory/people/` entries
- Lead files are skim-able in 30 seconds each (frontmatter tells the
  story)

## What to avoid

- Sourcing only from Skool - diversify across platforms daily
- Capturing leads with no revenue evidence - wastes stage 02 budget
- Investing in deep research at this stage (that's stage 03)
- Hunting beyond the source recipes (chasing rabbits)
- Skipping the dedup check - re-scoring the same lead is wasted work
- **Writing lead files without creating `memory/people/` stubs** - every
  lead file MUST have a matching vault stub created in the same step
- Writing names/platforms as plain text - use `[[wikilinks]]` (see root
  `CLAUDE.md` § "Wikilink rules")

## Tools used

- Playwright MCP (Skool browse, Twitter profile inspection, Reddit/YouTube)
- WebSearch (Google `site:` queries for Twitter)
- YouTube Data API (free tier, channel stats)
- Reddit JSON API
- HN Algolia API

## Tier check

Stage 01 reads + writes only. No outreach actions. No external messaging.
