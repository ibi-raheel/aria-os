---
title: Content sources — what the agent draws from
updated: 2026-05-02
---

# Content sources

Every post must mine from one of these sources. Anything outside the whitelist is out of scope.

## Whitelist (allowed content surface)

```yaml
- Arcadia/                                          # the product (codebase, design, docs)
- Arcadia/design/                                   # design system + areas (rich source)
- Arcadia/design/kit/ui_kits/                       # 5 UI kits (HTML files — screenshot source)
- Arcadia/design/kit/preview/                       # 20 design preview pages
- Arcadia/design/kit/assets/                        # SVG assets (wax-seal, medallion, etc.)
- Arcadia/design/areas/                             # area docs (doorway, hub, market, etc.)
- Arcadia/apps/                                     # app code (commits = build-in-public source)
- Arcadia/packages/                                 # shared packages (commits = same)
- Arcadia/docs/                                     # public docs
- Arcadia/phases/                                   # phase plans (occasional roadmap content)
- git log -- Arcadia                                # commit messages = the daily build feed
- memory/decisions/<*-arcadia-*>.md                 # Arcadia-tagged decisions only
- memory/decisions/<*-loom-*>.md                    # if relevant to Arcadia direction
- twitter-agent/01-signals/inbox/                   # operator-dropped seed ideas
```

## Blacklist (explicitly out of scope)

```yaml
- networking-agent/                                  # different audience (recruiters / RE / VCs)
- outreach-agent-arcadia/                            # outbound DMs, not public content
- news-agent/                                        # industry signal, not Arcadia
- hygiene-agent/                                     # vault meta-system, no audience
- _archives/                                         # historical artifacts
- memory/people/                                     # individual dossiers — never tweet about specific people without explicit operator approval
- logs/                                              # operational telemetry
- cowork/                                            # session-level scratch
- CLAUDE.md / DESIGN.md / conventions.md             # OS-level meta — never relevant to Arcadia audience
- Anything in ~/Library/, /Users/, etc.              # outside the project
```

## Why this matters

The Twitter agent's audience is **Arcadia's potential customers** — paying-community creators on Skool / Circle / Mighty / Discord. They care about: the product, the build journey, the differentiation. They do NOT care about the agent OS, the markdown-as-database approach, the bloat refactor, or any meta-system content. Posting about that pulls AI-builder Twitter, the wrong audience.

If the agent ever drafts a tweet about something on the blacklist, that's a content-source violation. The voice checklist + `_config/safety.md` should catch it; if it slips through, kill in dry-run review and add a regex pattern to safety.

## Signal harvest order (rough priority each morning)

1. **Today's git log** in `Arcadia/` (last 24h commits) → strongest build-in-public source
2. **Files modified in `Arcadia/design/`** in last 24h → design-reveal source
3. **New entries in `memory/decisions/`** filtered to Arcadia-tagged → decision-quote source
4. **Operator inbox** (`twitter-agent/01-signals/inbox/`) → manual seeds beat anything else if present
5. **Existing UI kit pages** (`Arcadia/design/kit/preview/*.html`, `Arcadia/design/kit/ui_kits/*/index.html`) → visual reveal source on slow days

## What "high signal" looks like for this agent

- A merged PR shipping a user-visible feature (e.g., #59 four-stall market)
- A bug-fix commit with a story behind it (e.g., #54 tavern feed didn't refetch)
- A new design preview page going up
- An architectural decision recorded with rationale
- A milestone (e.g., first multiplayer session, X members onboarded, Y feature shipped)

## What "weak signal" looks like (skip days where this is all there is)

- Dependency bumps
- Lint / formatter changes
- Internal refactors with no user-visible effect
- Pure infra commits (no story, no UI change)

If the day's signal is all weak, slot 1 falls back to a conviction post (which doesn't depend on what shipped today) and slot 2/3 use older un-surfaced commits or design assets.
