# ICP Scoring Rubric

Five dimensions, each 1-3 points. Total 5-15. Used in stage 02
(qualification) to accept / park / reject discovered leads.

---

## Thresholds

| Score | Action |
|---|---|
| **11-15** | **Accept.** Move to `stages/02-qualification/output/`, status `qualified`. |
| **8-10** | Park in `stages/02-qualification/output/parked/`, status `parked`. Re-check next batch. |
| **5-7** | Reject. Delete lead file. Update `memory/people/<name>.md` status `rejected` with reason. |

---

## Dimension 1 - Revenue evidence strength (1-3)

| Score | Definition |
|---|---|
| 3 | Public revenue claim with screenshot or specific figure ≥$50k/mo, or member count × visible price ≥$50k/mo |
| 2 | Evidence suggesting $20-50k/mo (mid-size paid community, course launches with dollar mentions, visible pricing × audience) |
| 1 | Indirect signal only (large following, but no revenue evidence) - risky but worth a templated send |

## Dimension 2 - Audience match (1-3)

| Score | Definition |
|---|---|
| 3 | Audience demographic clearly 18-45, comfortable with interactive/gamified UIs, community-first |
| 2 | Audience is right age but more passive (read-only) - would still benefit but harder to activate |
| 1 | Audience skews older / B2B-only / non-community-first |

## Dimension 3 - Stack fit (1-3)

| Score | Definition |
|---|---|
| 3 | Currently uses Discord + course platform + Notion - exact fragmentation Arcadia solves |
| 2 | Uses one of: Skool / Circle / Whop - already on a community-first tool, harder to win switch |
| 1 | All-in on one closed platform (e.g., Maven full-stack) - limited switching pain |

## Dimension 4 - Timing / momentum (1-3)

| Score | Definition |
|---|---|
| 3 | Recently launched/scaling, recent complaint about current stack, or visibly experimenting with new community formats |
| 2 | Steady operations, no crisis, no recent expansion - neutral timing |
| 1 | Quiet feed, no recent activity, possibly in maintenance mode or burnt out |

## Dimension 5 - Reachability (1-3)

| Score | Definition |
|---|---|
| 3 | Reachable on ≥3 channels (e.g., Twitter DM open + public email + Skool DM) |
| 2 | Reachable on 2 channels |
| 1 | Reachable on 1 channel (e.g., DMs closed everywhere except cold email) |

---

## Hard disqualifiers (override score → reject regardless)

If ANY of these are true, reject regardless of total score:

- Already on Whop, Heartbeat, Geneva, or another spatial/community-OS tool
- Public anti-metaverse / anti-spatial / anti-gaming-UI stance
- Pure solo educator with no member base (no community to migrate)
- Audience is B2B-only enterprise
- Inactive for 60+ days
- The creator IS a competitor (not a customer)

## Process per lead

1. Read the lead file in `stages/01-discovery/output/`.
2. Read its stub `memory/people/<name>.md`.
3. Score each dimension (1-3) using the data captured.
4. If any disqualifier hits, reject regardless of total.
5. Sum scores; apply threshold action.
6. Write the score breakdown into the lead's frontmatter:

```yaml
score_revenue: 3
score_audience: 2
score_stack: 3
score_timing: 2
score_reachability: 3
score_total: 13
score_action: accepted | parked | rejected
score_reason: "one-line summary"
```

7. Move the file to the appropriate next location.
8. Update `memory/people/<name>.md` status.
9. Append to `logs/daily/YYYY-MM-DD.md`: `## HH:MM - outreach-agent -
   qualified batch: N accepted, N parked, N rejected`.

---

## Scoring discipline

- **Don't manufacture data** to push a borderline lead through. If
  evidence is "1," score it "1." Better to spend stage 03 budget on real
  candidates.
- **Score from the captured data only.** Don't go back to the source to
  refine the score - that's stage 03's job. If the data is too thin to
  score, send back to stage 01 for more capture.
- **Re-score parked leads weekly.** Sometimes a parked lead becomes a 3
  on Timing because they just launched something new.
