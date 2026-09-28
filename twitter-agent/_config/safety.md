---
title: Safety rules — never-post + never-engage
updated: 2026-05-02
---

# Safety

Hard rules. Anything matching these gets killed before it leaves dry-run.

## Never post about

```yaml
- The agent OS itself ("we built Arcadia's outreach agent as markdown files")
- Other agents (networking-agent, outreach-agent, news-agent, hygiene-agent)
- Specific people in our pipeline by name without explicit operator approval
  (engagement records are private, dossiers are private — never quote them publicly)
- Customer / member counts that aren't public knowledge
- Revenue / MRR figures unless explicitly approved in this file's "approved-numbers" section
- Specific bug details that could be exploited (security / abuse / spam vectors)
- Internal architecture decisions that competitors could exploit
- Anything from memory/decisions/ that isn't already publicly stated
- Hot takes about specific competitors by name beyond what's in the conviction-post template
  (saying "Skool is forum-flavored" is fine; saying "Skool's CEO is wrong about X" is not)
- Politically charged topics
- Religious topics
- Health / medical / financial advice
- Anything that could be construed as legal / regulatory commentary
```

## Never engage with

```yaml
- Crypto / NFT promo accounts
- Engagement-farming bot accounts
- Politically charged content (even from accounts we follow)
- Brand crisis content (any cluster of 3+ negative replies on the same feature/topic in 24h)
- Anyone the operator has explicitly added to never-engage below
```

## Approved numbers (whitelist of public-safe figures to cite)

```yaml
# Operator: add real public-safe Arcadia metrics here as they become quotable.
# Examples of what would go here:
# - "Day [N] of building Arcadia" — N derived from cadence.md, always safe
# - Number of design preview pages: 20 (public in Arcadia/design/kit/preview/)
# - Number of UI kits: 5 (tavern, tent, academy, dashboard, market)
# - Specific shipped features by name (in-world dashboard overlay, persistent ambient music, four-stall market, single-session-per-member, role-aware icons, mono-font nameplates with level badges)
#
# What does NOT go here without explicit approval:
# - Member count (until X public)
# - MRR / ARR
# - Funding amount
# - Team size
# - Anything that's privileged business info
```

## Operator-flagged never-engage list

```yaml
# Add Twitter handles here when the operator wants the agent to never engage with that account.
# Reasons captured in inline comment.
never_engage:
  # - "@example_handle"  # reason
```

## Hard regex gates

The draft / reply pipelines should fail-closed if any of these appear in generated text:

```regex
"\\$\\d+[KMB]?"                          # any dollar figure → confirm against approved-numbers
"(MRR|ARR|revenue|annualized)"           # revenue claims → confirm public
"(\\d+(?:K|M)?\\s+(?:members|users|customers))"  # user-count claims → confirm public
"(I think|I believe) [^.]*(should|must) (?:die|fail|burn|rot)"  # extreme negative takes → kill
"\\b(woke|woketard|MAGA|libtard|leftist|rightwing)\\b"  # politically charged language → kill
"(invest|investing|buy now|sell now|HODL|to the moon)"  # financial advice flavor → kill
```

## Pre-publish checklist

Before any post goes from `02-draft/` to live (or from `05-replies/draft/` to live), the agent must:

1. Run the voice checklist from `voice.md`
2. Run the regex gates above
3. Confirm content source is in `content-sources.md` whitelist
4. Confirm no member of the never-engage list is mentioned
5. If a number is cited, confirm it's in approved-numbers OR it's the Day-N counter

If any check fails, draft is **killed** — moved to a `_killed/` subfolder under `02-draft/<date>/` with a `kill_reason:` line, not pushed to `03-review/`.

## Brand-crisis pause

If the agent detects a brand crisis (3+ negative replies on the same feature/topic in 24h), it:
1. Does NOT post slot 1 / slot 2 / slot 3 the next day
2. Does NOT respond to mentions
3. Does NOT engage outbound
4. Writes a flag file at `twitter-agent/_brand-crisis-flag.md` with the cluster details
5. Operator manually clears the flag after deciding response

The operator decides post-crisis tone; the agent never tries to handle a crisis itself.
