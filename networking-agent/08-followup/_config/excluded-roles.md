---
title: Excluded roles — never DM
updated: 2026-05-04
applies_to: 08-followup/02-classify
---

# Excluded roles

Hard-stop list. If a candidate's LinkedIn headline OR current role contains any of these patterns, they get `value-skip` regardless of score.

## Exact-match exclusions (case-insensitive)

| Pattern in headline | Reason |
|---|---|
| `student` | Student/intern — not yet professional surface |
| `intern` | Intern — temporary, not decision-maker |
| `MBA candidate` / `JD candidate` / `MD candidate` / `PhD candidate` | Currently enrolled — re-evaluate post-graduation |
| `incoming` (e.g., "Incoming Analyst at Goldman") | Hasn't started role yet |
| `seeking opportunities` / `open to work` / `actively looking` | Currently between roles, not in a position to advise |
| `looking for [X]` (where X = job/role/internship) | Same as above |
| `aspiring` (e.g., "Aspiring software engineer") | Pre-professional |

## Education-state exclusions

If the LinkedIn profile shows education with a future end date (e.g., "Expected May 2027") AND the current role is intern/student/RA/TA/research assistant: **value-skip**.

If education end date is in the past AND current role is post-graduation (Associate, Engineer, etc.), normal score model applies — they're not excluded just for being recent grads.

## Role-pattern exclusions (combined with low score)

The following role patterns excuse the candidate ONLY if their total score is also < 5:

- `Junior <X>` (Junior Analyst, Junior Engineer)
- `Trainee` / `Apprentice` / `Fellow` (where Fellow is a training program, not McKinsey-style "we use Fellow as a senior IC title")
- `Recent graduate` / `New grad` / `Graduate of <Year>`
- `Influencer` with no other professional signal (vanity title, no decision-making power)

## Hard never-DM list (overrides everything)

Some people are off-limits for relationship reasons unrelated to seniority. Add specific names/handles here as the list grows:

```yaml
never_dm:
  # Format: linkedin_url | reason | added_date
  # Example:
  # - https://linkedin.com/in/jane-doe | "Operator publicly disagreed in 2025; cooling-off"  | 2026-01-15
```

(Currently empty — populate as needed.)

Also covered by the parent agent's `../../_config/exclusions.md` (which is read at the discovery stage, before invites are sent). Anyone on that list shouldn't be a connection in the first place — but this is a defense-in-depth check.

## Edge cases

### "Senior Associate" at consulting/PE/VC

NOT excluded — at MBB and PE/VC, "Senior Associate" is a senior IC tier on track to Partner/Principal. Score normally.

### "Associate Partner" at McKinsey

NOT excluded — this is the tier just below Partner. Score normally (title seniority +4).

### Founders pre-funding

A founder of a stealth / pre-seed startup may have headline "Founder, Stealth" with low followers. Score them via the Founder rule in `valuable-person-rules.md` (Dimension 2), not the exclusion list. If they have a real company entity but small audience, they can still pass.

### Hiring/recruiting roles

Recruiters at MBB / target firms are NOT excluded — their role is to talk to candidates. They have explicit permission/incentive to engage. Score normally; consulting bucket already has a "recruiter" template variant.

### People who connected with the operator from THEIR side

If the candidate originally sent the invite (we accepted theirs, they didn't accept ours), the dossier should have `connect_direction: inbound`. Different conversation dynamic — they had a reason to connect. Use the `inbound` template variant in `coffee-ask-templates.md`.

## Validation order

The classify stage runs in this order:

1. Check exact-match exclusions → if hit, `value-skip` immediately
2. Check education-state exclusions → if hit, `value-skip` immediately
3. Check hard never-DM list → if hit, `value-skip` immediately
4. Compute score from `valuable-person-rules.md`
5. Apply role-pattern exclusion (only if score < 5)
6. Apply override field (`followup_override` in dossier frontmatter)
7. Final decision: `value-pass`, `value-pass-soft`, or `value-skip`

Reason string is logged for every skip. Operator can audit `02-classify/output/<date>/skipped/` to spot pattern errors and tune these rules.
