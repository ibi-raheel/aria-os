# Stage 02 - Qualification

## Job

Score discovered leads against the 5-dimension ICP rubric. At 50
candidates/day, this stage is a fast filter - accept broadly (all ≥8),
park borderlines, reject obvious misses. Deep enrichment happens for all
accepted leads (compute is free).

## Inputs

| File | Why |
|---|---|
| All files in `stages/01-discovery/output/` | The leads to score |
| `_config/icp.md` | Hard requirements + disqualifiers |
| `skills/icp-scoring-rubric.md` | The 5-dimension scoring (1-3 each) |

## Process

1. Read each lead file in `01-discovery/output/`
2. Read its stub `memory/people/<slug>.md`
3. Check hard disqualifiers from `_config/icp.md` first - if any hit,
   reject regardless of score
4. Score 5 dimensions per `skills/icp-scoring-rubric.md`:
   - Revenue evidence (1-3)
   - Audience match (1-3)
   - Stack fit (1-3)
   - Timing / momentum (1-3)
   - Reachability (1-3)
5. Total → apply threshold:
   - ≥11 → accept
   - 8-10 → park
   - ≤7 → reject
6. Move file accordingly:
   - Accept → `output/<slug>.md`
   - Park → `output/parked/<slug>.md`
   - Reject → delete file (vault entry retains the rejection record)
7. Write score breakdown into the engagement record frontmatter
8. Update dossier at `memory/people/<slug>.md` ONLY with status field (`qualified`, `parked`, or `rejected`) — do NOT write score fields to the dossier; those belong in the engagement record
9. Append batch summary to `logs/daily/YYYY-MM-DD.md`

## Output

| Artifact | Location | Format |
|---|---|---|
| Accepted engagement records | `stages/02-qualification/output/<slug>.md` | Engagement record with score frontmatter, status `qualified` |
| Parked engagement records | `stages/02-qualification/output/parked/<slug>.md` | Same, status `parked` |
| Rejected | (engagement file deleted) | `memory/people/<slug>.md` dossier updated with `status: rejected` only |
| Daily log | `logs/daily/YYYY-MM-DD.md` | `## HH:MM - outreach-agent - qualified batch: N accepted, N parked, N rejected` |
| Decision (only for category-level) | `memory/decisions/YYYY-MM-DD-icp-<slug>.md` | "Rejected all <category> - outside ICP" with reason |

## Frontmatter additions (after scoring)

```yaml
score_revenue: 1-3
score_audience: 1-3
score_stack: 1-3
score_timing: 1-3
score_reachability: 1-3
score_total: 5-15
score_action: accepted | parked | rejected
score_reason: "one-line summary"
qualified_at: YYYY-MM-DD
```

## What good looks like

- 30-40 accepted per daily batch (after stage 01's 50 catch)
- Scoring is fast but consistent - 2-3 min per lead using captured data
- Reject hard disqualifiers immediately, accept broadly for enrichment
- Parked leads get re-scored next batch (some rise on Timing)
- Decisions for category-level rejections are written as evidence
  ("rejected all B2B SaaS this batch - wrong audience profile")

## What to avoid

- Manufacturing data to push a borderline lead through (better to
  invest stage 03 budget in real candidates)
- Re-scoping to source data mid-score (that's stage 03's job)
- Skipping the disqualifier check (it's the cheapest cull)
- Auto-approving high-follower leads with weak revenue evidence (high
  followers ≠ high revenue at this tier)

## Tools used

- LLM only. No external calls.

## Tier check

Reads + writes to vault only. No outreach actions.

## Disqualification workflow

When moving a file to `_disqualified/`:

1. Update frontmatter: `status: disqualified`
2. Add `disqualified_at: YYYY-MM-DD`
3. Add `disqualified_reason: "one-line reason"`
4. Add a wikilink to the relevant decision file below the `# Name` heading:
   `**Disqualified:** [[memory/decisions/YYYY-MM-DD-decision-slug|Display text]]`
5. Move the file to the `_disqualified/` subfolder of the relevant output directory

## Back-edge rule (one allowed)

Stage 03 (enrichment) may kick a lead BACK to this stage if enrichment
reveals the lead is below ICP (e.g., revenue evidence collapses on
inspection). When that happens, this stage re-scores with the new data
and likely rejects.

This is the **only** allowed back-edge in the pipeline.
