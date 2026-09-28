# 05-review

Dry-run gate — **operator opt-in only as of 2026-05-06**. By default `/networking-followup-run` ships DMs live. If the operator wants to inspect drafts before they ship, they pass `dry-run-only` to that run; drafts then stop here for manual approval before reaching `06-send`. The original 2-week calibration window (default through 2026-05-21) was retired early.

## Layout

```
05-review/
  YYYY-MM-DD/
    <slug>.md              # one file per drafted DM awaiting review
```

## File shape

```yaml
---
slug: <slug>
draft_source: 04-draft/output/<slug>.md
review_status: pending | approved | rejected | revise
operator_review_at: <ISO or null>
operator_notes: <text>
---

# <Name> — review

## Drafted DM
> <full DM text>

## Why we're DMing this person
- Score: <int> (title <p>, firm <p>, activity <p>, mutuals <p>)
- Shape: <1|2>
- Anchor: <one-line>
- Original engagement: [[../../../06-send/output/<slug>|06-send/<slug>.md]]

## Voice checklist
- [x] Opens with first name + thanks-for-connecting
- [x] Anchor is specific & verifiable
- [x] Sharp dichotomous question
- [x] Honest frame
- [x] One ask line, no menu
- [x] Zero em-dashes
- [x] 200-400 chars
- [x] You/we ratio ≥ 2:1

## Decision
- [ ] Approve as-is (will send on next /networking-followup-send run)
- [ ] Revise (operator edits dm_text in 04-draft/output/<slug>.md, re-flags for review)
- [ ] Reject (drop this candidate, log reason)
```

## Approval workflow

Operator reviews each file in this folder by hand. To approve:

1. Set `review_status: approved` in the file's frontmatter.
2. The next `/networking-followup-send` run reads only `review_status: approved` files.

To revise:
1. Edit the `dm_text` field in `04-draft/output/<slug>.md`.
2. Set `review_status: revise` in the review file.
3. Next run will re-read the draft and refresh the review file.

To reject:
1. Set `review_status: rejected` and add `operator_notes: "<why>"`.
2. The candidate is logged in the engagement record as `coffee-ask-rejected-by-operator` with the reason. They become eligible again only via manual re-flag.

## Live mode (default)

The orchestrator's default routes drafts directly to `06-send` for any draft passing voice checklist + cap, no `05-review/` stop. Operator can opt in to dry-run review on a per-call basis with `/networking-followup-run dry-run-only`.
