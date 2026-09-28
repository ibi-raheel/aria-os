---
title: Reply rules — mentions + own-post comments
updated: 2026-05-02
---

# Reply rules

The agent sweeps two surfaces at 09:00 daily and drafts replies for operator review. **Dry-run by default** — drafts land in `05-replies/draft/` for OK before going live.

## Surfaces swept

1. **Mentions of @Arcadia** (or whatever the handle is) — `https://x.com/notifications/mentions`
2. **Comments on Arcadia's own posts** — last 7 days of posts, check the reply tree for new threads

## Triage rules

For each new thread:

```yaml
SKIP (no draft, no log entry beyond "ignored"):
  - Spam, crypto, follower-baiting, unsolicited self-promo
  - Politically charged unrelated topics
  - Bots / fake-engagement accounts (heuristic: <50 followers + recent account + generic profile)
  - "Great post 🚀" / pure-affirmation replies (no substance to reply to)
  - Replies from accounts on safety.md never-engage list

DRAFT (write reply to 05-replies/draft/, dry-run by default):
  - Substantive engagement (asks a real question, makes a real point)
  - Potential customers (creator economy / community-platform ICP)
  - Existing customers / users of Arcadia
  - Notable voices in the creator-platform space (even if not ICP — engagement compounds)

ESCALATE (don't draft, just flag):
  - Press / journalist / podcast inquiry
  - VC / investor reaching out
  - Negative feedback on a feature (operator should respond personally, not the agent)
  - Anything mentioning legal / privacy / security concerns
```

## Draft format (per thread)

Each drafted reply is a markdown file at `05-replies/draft/<date>-<thread-id>-<slug>.md`:

```yaml
---
thread_id: <Twitter thread ID>
parent_post: <URL of post being replied to>
their_handle: <@handle>
their_followers: <count>
their_role: <inferred role / archetype>
detected_at: <ISO timestamp>
triage: draft
draft_attempts: 1
---

# Reply to @<handle>

## Their tweet
> <verbatim quote of their tweet>

## Context
<1-2 lines: who they are, why we're replying, any relevant history with this account>

## Drafted reply
<the actual reply text — same voice rules as own posts apply>

## Voice checklist
- [x] Specific, not generic
- [x] Doesn't beg engagement
- [x] No filler ("great point!" / "love this")
- [x] Adds substance — answers, builds, or asks a sharp follow-up
- [x] No hashtags, no emojis (rare exception)
- [x] Max 1 em-dash
```

## Tone rules for replies

Same as posts (see `voice.md`), plus:

- **Don't say "great point" or "love this"** — adds nothing, reads as low-effort.
- **Match their energy.** If they wrote 4 words, don't reply with 50.
- **Answer the question if they asked one.** Don't pivot to your pitch.
- **Disagreement is OK if substantive.** "I'd push back on that — [specific reason]" beats sycophancy.
- **Quote-tweets vs. replies:** if their post is broadly interesting and our reply adds a substantive layer, quote-tweet (extends our reach). If the reply only makes sense in their thread context, reply.

## Auto-post promotion

After ~3 weeks of dry-run reviews where the operator approves >85% of drafts, replies can flip to auto-post. This is an explicit operator decision — change `dry_run_default: true` to `false` in this file's frontmatter.

## Hard rules (never)

1. Never auto-reply to anything mentioning a real person by name without operator review.
2. Never post anything that could read as legal/medical/financial advice.
3. Never engage in pile-ons, dunks, or sub-tweets even if technically substantive.
4. Never reply during a brand crisis without operator review (define: any cluster of 3+ negative replies in 24h about the same feature/topic).
