---
title: Valuable-person filter — who gets a coffee-ask DM
updated: 2026-05-04
applies_to: 08-followup/02-classify
---

# Valuable-person rules

The follow-up agent reads the LinkedIn Connections list and classifies each candidate as `value-pass` or `value-skip`. Only `value-pass` people get drafted; `value-skip` people are logged with reason and dropped for this cycle.

The point of this filter is to focus the 5-10 daily DM budget on connections where a 20-minute conversation would meaningfully advance one of the operator's goals (job at MBB, real-estate diligence, founder/investor learning, customer for Arcadia, ecosystem density). Students, junior ICs, and inactive accounts get filtered out.

## Score model

Each candidate is scored across four dimensions. **Value-pass requires ≥ 5 points AND no exclusion-list match (see `excluded-roles.md`).**

### Dimension 1: Title seniority (0 to +5)

Read the candidate's current LinkedIn headline. Score the highest single match:

| Match | Points |
|---|---|
| Senior Partner / Managing Partner / Managing Director / MD / Partner / GP / General Partner / Founder / Co-Founder / CEO / President / Chair | +5 |
| Principal / VP / SVP / EVP / Director / Head of [Practice] / Lead [Function] / SVP / EVP | +4 |
| Senior Manager / Senior Engineering Manager / Group Product Manager / Senior Counsel | +3 |
| Engagement Manager / Manager / Senior Associate (consulting) / Senior Engineer / Staff Engineer | +2 |
| Associate / Consultant / Engineer / Analyst (with no other modifiers) | 0 |

Notes:
- "Associate Partner" at McKinsey = +4 (it's a senior tier, despite the "Associate" word)
- "Senior Associate" at a PE/VC firm = +3 (track-to-Partner role)
- "Vice President" at investment banks = ambiguous; default to +3, override if other signals say junior
- Where unclear, prefer the LOWER score (false negatives are cheaper than false positives at this stage)

### Dimension 2: Firm / institution match (0 to +5)

If the candidate is at a firm in one of the 8 networking-agent target categories, add points:

| Match | Points |
|---|---|
| Tier-1: McKinsey, Bain, BCG, a16z, Sequoia, Benchmark, Founders Fund, Greylock, Accel, Index, Khosla, Lightspeed, USV, YC (current/former Group Partner), Goldman Sachs IBD, Morgan Stanley M&A, BlackRock, Brookfield, Blackstone, Apollo, KKR | +5 |
| Tier-2 consulting / banking / VC: Deloitte S&O, Bain Capital, Strategy&, Oliver Wyman, T1VC firms not above, named PE shops, named REITs (BXP, AVB, EQR, Prologis, Realty Income), MAANG (Senior+ engineer or PM), Anthropic, OpenAI, Google DeepMind, Microsoft AI | +3 |
| Founder of a venture-backed startup with $1M+ raised AND/OR a paid community of 1K+ paying members | +3 |
| Tier-3: any other recognizable firm in target category (small VC, regional PE, mid-market consulting, Series-A startup founder) | +1 |
| Unknown / no firm visible | 0 |

The list of named firms updates as the operator's targets evolve. Source for tier-1 + tier-2 firms: `../../_config/categories/<category>/searches.md` for each of the 8 categories.

### Dimension 3: Activity + audience signal (0 to +4)

| Signal | Points |
|---|---|
| 10,000+ followers OR 5,000+ followers + posted in last 14d | +3 |
| 1,000+ followers + posted in last 30d | +2 |
| Has authored a substantive post (not a repost) in last 30d | +1 |
| Inactive (last post > 90d ago, < 1k followers) | -1 |

### Dimension 4: Mutual connections (0 to +2)

| Mutuals | Points |
|---|---|
| 3+ mutual connections | +2 |
| 1-2 mutual connections | +1 |
| 0 mutuals | 0 |

## Category gates (auto-skip before scoring)

Before computing the score, check the candidate's bucket against `_config/daily-quota.md` `followup_category_gates`. Currently gated:

- `real-estate` — value-skip with reason `real-estate-template-pending`. The candidate is logged in `02-classify/output/<date>/skipped/<slug>.md` for visibility. Real-estate candidates remain eligible for the regular MWF send pipeline (only the follow-up coffee-ask is gated).

Lift the gate by removing the bucket from `daily-quota.md`'s `followup_category_gates` list AND adding a Shape 1/2 template variant in `coffee-ask-templates.md`.

## Decision

```
total_score = title_seniority + firm_match + activity_signal + mutuals
            - exclusion_penalty (if any exclusion-list match, see excluded-roles.md)

if any exclusion match:                    → value-skip (reason: "exclusion-list-match: <rule>")
elif total_score >= 5:                     → value-pass
elif total_score >= 3 and operator_known:  → value-pass-soft (operator approves manually)
else:                                       → value-skip (reason: "insufficient signal: score=<n>")
```

`operator_known` = the candidate is in the operator's `memory/people/<slug>.md` dossier (i.e., previously researched). Soft-pass exists for cases where the operator has private context (e.g., warm intro from a friend, met them at an event) that LinkedIn doesn't capture.

## Worked examples (from current connections)

**Maurice Obeid** — Senior Partner, McKinsey & Co (consulting). Title +5 / Firm +5 / Activity +3 (3,975 followers, posts weekly) / Mutuals +2 (Thais + Maggie + 1 other). **Total = 15 → value-pass.**

**Scott Blackburn** — Senior Partner, McKinsey US Public Sector. Title +5 / Firm +5 / Activity +2 (followers ~unknown but recent post 6d ago) / Mutuals 0. **Total = 12 → value-pass.**

**Hypothetical: Jane Doe — MBA Candidate at Wharton, Class of 2027.** Exclusion match: "Candidate" + currently enrolled. **value-skip.**

**Hypothetical: John Smith — Associate at Goldman Sachs (M&A), 280 followers, no recent posts.** Title 0 / Firm +3 / Activity 0 / Mutuals 0. **Total = 3 → value-skip (insufficient signal).**

**Hypothetical: Sarah Lee — Founder & CEO, Series-A SaaS startup, 8.2K followers, posts 2x/week, 2 mutual connections.** Title +5 / Firm +1 / Activity +3 / Mutuals +1. **Total = 10 → value-pass.**

## Override mechanism

Operator can force-pass or force-skip a specific person by editing their dossier frontmatter:

```yaml
followup_override: pass    # force include regardless of score
followup_override: skip    # force exclude regardless of score
followup_override_reason: "Met at TechCrunch — wants to chat about real estate"
```

Read by the classify stage; takes precedence over the score model.

## When in doubt, skip

The follow-up budget is small (5-10 DMs/day, two days a week = 10-20/week max). False positives (DMing someone who isn't actually valuable) are worse than false negatives (skipping someone who would have been). False negatives just wait — they get re-evaluated on the next sweep when more signal exists. False positives waste a slot and can read as spammy.
