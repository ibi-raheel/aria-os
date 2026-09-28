# 02-classify

Applies value-pass rules to each candidate from `01-sweep/output/<date>/new-acceptees.md`. Produces a classification with reason.

## Layout

```
02-classify/
  output/
    YYYY-MM-DD/
      _classify-summary.md       # counts: value-pass, value-pass-soft, value-skip
      passed/<slug>.md           # candidates accepted into draft pipeline
      skipped/<slug>.md          # candidates skipped (one file per skip with reason)
```

## How classification works

For each candidate from `new-acceptees.md`:

1. Open their LinkedIn profile (Chrome MCP) and capture: headline, current role, follower count, education + dates, mutual count, last post date.
2. Apply `_config/excluded-roles.md` exclusion patterns. If any match → `value-skip` immediately with reason.
3. Apply `_config/valuable-person-rules.md` score model. Compute total.
4. Check operator override (`followup_override` field in the dossier frontmatter, if a dossier exists).
5. Final decision:
   - exclusion match → `value-skip`
   - score ≥ 5 → `value-pass`
   - score 3-4 AND operator-known → `value-pass-soft` (flagged for operator review)
   - score < 3 → `value-skip`
6. Write the result to `passed/<slug>.md` or `skipped/<slug>.md`.

## File shape

`passed/<slug>.md`:

```yaml
---
slug: <slug>
linkedin: <url>
headline: <captured>
firm: <captured>
title: <captured>
followers: <count>
mutuals: <count>
last_post_date: <ISO date or null>
score: <total>
score_breakdown:
  title: <points>
  firm: <points>
  activity: <points>
  mutuals: <points>
classification: value-pass | value-pass-soft
classified_at: <ISO timestamp>
---
```

`skipped/<slug>.md`:

```yaml
---
slug: <slug>
linkedin: <url>
headline: <captured>
classification: value-skip
skip_reason: <"exclusion-list: student" | "insufficient signal: score=2" | etc.>
score: <total>
classified_at: <ISO timestamp>
---
```

## Throughput

Classify all candidates from the sweep. The cap (5-10) is applied at draft time, not classify time — having more value-pass candidates than slots lets the draft stage prioritize on score + freshness.
