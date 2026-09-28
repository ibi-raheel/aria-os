# 03-anchor

For each `value-pass` candidate, picks the right anchor source (Shape 1 / Shape 2 / drop) and writes it to `output/<slug>.md`. Reads from `02-classify/output/<date>/passed/`.

## Three shape paths

**Shape 1 — recent accept, original anchor still hot (< 14d since accept).**
Reuse the original connect-note anchor. Pivot the question forward.

**Shape 2 — old accept (or silent recent accept), fresh activity available.**
Open the candidate's `recent-activity` page and pick the most relevant new post / panel / piece (last 30d). Make this the new anchor.

**Shape 3 — old accept, no fresh activity in 30d.**
Drop for this cycle. Logged with reason; retried on next sweep when they post.

## Logic

```
state_a (replied):  shape = 1   (continue original thread)
state_b (silent, accepted < 14d ago):  shape = 1
state_b (silent, accepted ≥ 14d ago):
    if has_post_in_last_30d:  shape = 2
    else:                     shape = 3 (drop)
```

State A (replied) vs State B (silent) is detected by opening the LinkedIn message thread and checking for a post-acceptance message from the candidate.

## File shape

```yaml
---
slug: <slug>
shape: 1 | 2 | 3
state: a | b
accepted_date: <ISO>
days_since_accept: <int>
anchor:
  type: original-connect-note | recent-post | recent-panel | recent-deal
  source: <URL>
  date: <ISO of anchor>
  topic: <one-line>
  point: <one-line — what the anchor argues>
  excerpt: <30-50 word verbatim>  # only if Shape 2
original_question: <only if Shape 1 — the question from the connect-note>
template_path: <category>-shape<1|2>
---
```

If `shape: 3`, write a stub with `dropped_reason: "no-fresh-anchor"` and skip downstream stages.
