---
title: Daily quota config
updated: 2026-05-06
---

# Daily quota

```yaml
# === Send stage (Mon/Wed/Fri 05:00) — decision 2026-05-04-networking-agent-mwf-cadence ===
daily_target: 23                # spec total across all 8 categories (raised from 20 on 2026-05-06 to give the 15-floor headroom against weak-pool shortfalls)
daily_floor: 15                 # HARD MINIMUM. If a run projects below 15 ranked candidates, abort send and ping #linkedin-networking with the gap and which categories are short. Decision: 2026-05-06-networking-agent-15-floor-bigtech-expansion.
weekly_cap: 140              # Premium-tier nominal. Hallucinated cap-toast on 2026-04-30 led to false 5; real cap-hit on 2026-05-01 confirmed the cap CAN fire. The /networking-send corroborate-before-throttle step now prevents false trips.
weekly_send_days: [Mon, Wed, Fri]
weekend: skip
holidays_file: holidays.md

# === Follow-up stage (Tue/Thu 09:00) — decision 2026-05-04-followup-stage-launch ===
followup_dm_cap: 10                   # max coffee-ask DMs per follow-up run when sweep produces enough net-new acceptees
followup_backlog_on_empty_cap: 5      # if sweep returns 0 net-new, fall through to backlog and ship up to 5/day
followup_days: [Tue, Thu]
followup_default_mode: live           # was: dry-run during calibration. Flipped to live 2026-05-06 (decision: 2026-05-06-followup-live-default-and-backlog-on-empty)
followup_category_gates:              # categories gated from follow-up stage until a different message structure is drafted
  - real-estate                       # gated 2026-05-06; pending RE-specific template

# === Category split — rebalanced 2026-05-06 (decision: 2026-05-06-networking-agent-15-floor-bigtech-expansion) ===
# Old split (4/3/3/2/2/2/2/2 = 20) hit a 9-of-20 ceiling because RE was gated, Big Tech was VP-Eng-only,
# and premiers (YC/a16z/Tier-1) refused cascade. New split widens Big Tech to absorb the slack.
category_split:
  consulting: 4
  real_estate: 3            # GATED for follow-up; send stage still runs but pool is structurally thin pending broker/IR template
  founders: 2               # tightened from 3 — pool thinner than expected
  investors_general: 2
  yc: 2                     # PREMIER — never accept cascade, never push beyond 2
  a16z: 2                   # PREMIER — never accept cascade
  tier1_vcs: 2              # PREMIER — never accept cascade
  big_tech: 6               # WIDE-POOL ABSORBER (was 2). Scope opened to ANY function (HR, recruiters, PMs, EMs, design, GTM, finance, ops). Active-poster gate stays.
# total: 23 spec, 20 effective with RE gate, 15 floor.

# Wide-pool absorber categories — accept cascaded slots from undersupplied weak-pool buckets
wide_pool_categories:
  - consulting
  - big_tech

# Premier categories — NEVER accept cascade (slots stay empty rather than burn anchors)
premier_categories:
  - yc
  - a16z
  - tier1_vcs

# Cascade order (top to bottom; each step only fills if its own queue is short, then cascades down)
cascade_order:
  - consulting        # wide pool — fill first AND absorb cascaded slots
  - real_estate       # concrete utility — currently structurally thin
  - founders          # easiest reply, but pool thinner than spec assumed
  - investors_general # broad pool but quality bar high
  - big_tech          # WIDE POOL — absorbs everything else's shortfall
  - yc                # PREMIER — fixed slot, never cascade-receive
  - a16z              # PREMIER — fixed slot, never cascade-receive
  - tier1_vcs        # PREMIER — fixed slot, never cascade-receive

# Cascade rule:
#   When a category undersupplies, redistribute its empty slots IN ORDER to wide_pool_categories.
#   Premier categories NEVER accept cascade — their pool is bounded and the relationship cost
#   of a forced send is higher than the cost of an empty slot.
#   If wide_pool_categories together cannot absorb the shortfall AND total ranked < daily_floor,
#   ABORT the send and post the gap to #linkedin-networking.

minimum_score_threshold: 5  # below this, candidate is parked, slot cascades

# Within consulting: split partners vs recruiters
consulting_subsplit:
  partners: 3
  recruiters: 1

# Auto-correction: when LinkedIn returns "weekly invitation limit reached"
# and logs the event in log/YYYY-MM-DD.md plus memory/decisions/
auto_throttle: true

# Warning threshold — log a warning when within 10% of weekly_cap
warn_at_pct: 90
```

## Notes

- **First run on a new Premium tier:** keep `weekly_cap` conservative (140) until empirically validated. The first time the cap-reached error fires (with corroboration), `weekly_cap` self-corrects.
- **Backfill rules:** if Monday's run fails to ship the daily target (Chrome closed, profile errors, etc.), Wednesday does NOT add Monday's shortfall. Quota is per-run, not per-week. This prevents cascading bursts that look like spam to LinkedIn.
- **Weekend + Tue/Thu skip (send stage):** Sat/Sun + Tue/Thu neither send invites nor run discovery/qualify (MWF cadence). The follow-up stage runs on Tue/Thu instead. Reconcile can still run on weekends if manually invoked.
- **Follow-up cap is independent of invite cap.** LinkedIn DMs to existing connections are not subject to the weekly invitation cap; the 10/run follow-up cap is a self-imposed quality limit, not a platform limit.
- **Daily floor is a halt, not a relax.** When projected ranked < 15, the agent does NOT lower the score threshold to backfill. It aborts the send, posts the gap to `#linkedin-networking`, and leaves it to the operator to either widen seeding or accept the short day. Quality bar > volume floor.
- **Big Tech function-open since 2026-05-06.** The category was previously seeded for engineering execs only (VP Eng / Distinguished Engineer / Senior Director Engineering). It now seeds across HR, recruiters, PMs, EMs, design, GTM, finance, and ops at FAANG/MSFT/Nvidia/Stripe/OpenAI/Anthropic/Databricks-tier. The active-poster gate (post in last 30d) stays — quality bar is "creator-leaning," not "executive-only."
