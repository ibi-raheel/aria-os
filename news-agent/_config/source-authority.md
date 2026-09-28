# Source Authority — anti-false-news guardrails

Every news item carries a source. Not all sources are equal. This file defines the 4 authority tiers and the explicit denylist. Stage 02 (categorize) reads this file at run-start and applies the gating rules below.

**Why this exists:** the system already prevents agent fabrication (verbatim excerpt + source URL required per item). This file adds a layer up: even when the agent is honest, a satirical or fringe source can still pass content through unless we filter at the source. This file is that filter.

---

## Tier 1 — Primary sources (no corroboration required)

These are the sources OF the news, not commentary about it. Government feeds, official filings, firm-published press releases. If Tier 1 says it, it's the original authority.

**Domains and feeds:**
- Federal Register: `federalregister.gov`
- SEC EDGAR: `sec.gov` (10-K, 10-Q, 8-K, Form D, 13F, 13G filings)
- Congress.gov: `congress.gov`
- DOJ: `justice.gov`
- FTC: `ftc.gov`
- FCC: `fcc.gov`
- White House: `whitehouse.gov`
- CourtListener: `courtlistener.com`
- Firm-official press release domains:
  - `mckinsey.com/about-us/news` (and similar /press, /newsroom paths for Bain, BCG, Deloitte)
  - `a16z.com` (when the post is firm-authored, not just hosted)
  - VC firm official news pages where the firm is the publisher
- Person-authored content where the person IS the news (e.g., a CEO's official Substack post about their own company's announcement counts as Tier 1 for that company; a partner blog post about their own deal counts as Tier 1 for that deal)

A Tier 1 source is sufficient evidence on its own — no second-source corroboration needed. The classic example: an SEC Form D filing IS the fund formation event, not a story about it.

---

## Tier 2 — Established journalism

Reputable news organizations with editorial standards, fact-checkers, and a track record. A Tier 2 source on its own is *probably* right, and any item with 2+ independent Tier 2 sources counts as corroborated.

**Domains:**
- Reuters: `reuters.com`
- Bloomberg: `bloomberg.com`
- The New York Times: `nytimes.com`
- The Wall Street Journal: `wsj.com`
- The Financial Times: `ft.com`
- The Washington Post: `washingtonpost.com`
- The Economist: `economist.com`
- The Information: `theinformation.com`
- TechCrunch: `techcrunch.com`
- The Verge: `theverge.com`
- Wired: `wired.com`
- Ars Technica: `arstechnica.com`
- CNBC: `cnbc.com`
- AP News: `apnews.com`
- Forbes (editorial only — not Forbes Council/contributor pieces): `forbes.com`
- Fortune: `fortune.com`
- Axios: `axios.com`
- Politico: `politico.com`
- HBR: `hbr.org`
- Bisnow (real estate): `bisnow.com`
- The Real Deal (real estate): `therealdeal.com`
- GlobeSt (real estate): `globest.com`
- Commercial Observer: `commercialobserver.com`
- Reuters Tech: `reuters.com/technology`
- Crunchbase News: `news.crunchbase.com`

Forbes Council, Forbes Contributor, and similar by-line-without-editorial-oversight pieces are Tier 3, not Tier 2.

---

## Tier 3 — Aggregator / secondary

These cover news but rarely break it. Useful for confirming a Tier 2 story is real, less useful as standalone authority. A single Tier 3 source making a factual claim about a named person needs Tier 1 OR Tier 2 corroboration before the claim becomes an anchor.

**Domains:**
- GeekWire: `geekwire.com`
- 9to5Mac: `9to5mac.com`
- 9to5Google: `9to5google.com`
- MacRumors: `macrumors.com`
- VentureBeat: `venturebeat.com`
- TechMeme: `techmeme.com`
- Hacker News (HN): `news.ycombinator.com` — the comments and submissions; aggregator
- The Star (`thestar.com.my`)
- Yahoo Finance, Yahoo News
- LinkedIn News
- Google News index pages
- Newsletters with a single author and no editorial board (most Substacks, Mediums)
- Mid-size industry trade pubs without strong fact-checking (varies by domain)

Forbes Council pieces and Forbes Contributor by-lines belong here.

---

## Tier 4 — Social / opinion / unverified

Tweets, LinkedIn posts, podcast clips, blog posts by individuals, Reddit threads. Useful as candidate signals — leads to investigate — but **never sufficient on their own** for a factual claim about a named person, deal, or law.

**Treatment:** an item sourced only from Tier 4 enters `01-fetch/output/<date>/<bucket>.md` as a candidate but **never enters a briefing as a confirmed item.** It can become a briefing item only if a Tier 1, 2, or 3 source corroborates the claim. The exception: a Tier 4 post by the named person themselves about themselves (e.g., a CEO tweets about their own company) gets promoted to Tier 1 for facts about the person and the company they lead, with a note that it's self-reported.

**Domains/platforms:**
- Twitter / X: `twitter.com`, `x.com`
- LinkedIn posts: `linkedin.com/posts`, `linkedin.com/pulse`
- Substack (individual newsletters without an editorial board)
- Medium
- Reddit
- Personal blogs
- Podcast transcripts (the host's claim is opinion; what a guest says about themselves is self-report, see exception above)

---

## Denylist — drop these at fetch time, never enter the pipeline

Satirical sites, known fake-news/disinformation domains, and parody accounts. If WebSearch returns a result from any domain on this list, the item drops at stage 01 (fetch) before WebFetch is even called. Saves bandwidth and prevents satire from ever shaping a briefing.

**Satirical / parody:**
- `theonion.com`
- `babylonbee.com`
- `clickhole.com`
- `thehardtimes.net`
- `reductress.com`
- `waterfordwhispersnews.com`
- `thedailymash.co.uk`
- `private-eye.co.uk` (some pieces are journalism, some are satire — flag for human review rather than auto-include)

**Known disinfo / low-quality / agenda-laden:**
- `infowars.com`
- `naturalnews.com`
- `breitbart.com` (flagged as advocacy, not denied — Tier 3 with caveat; team can decide to denylist if preferred)
- `dailymail.co.uk` (frequently inaccurate; Tier 3 with required corroboration)

**Generic content farms:**
- `medium.com/@*` posts that auto-republish other content (often misattributed)
- AI-generated news sites (hard to enumerate; check if a domain has "AI-written" in its disclosure)

This list is not exhaustive — operators should add domains that have caused false-news incidents in the past. Update this file when a denylist addition is needed.

---

## Twitter handle exception (Tier 4 → Tier 1 self-report rule)

When a partner / exec / public figure posts on X about themselves or their firm, that post is **self-report** — it's Tier 1 for facts about the speaker, but Tier 4 for opinion-content. Stage 02 should:

- Treat self-report posts as confirmed for facts about the person ("I joined Acme as VP of X")
- Treat opinion posts as Tier 4 (need corroboration before becoming a briefing item)
- Flag the difference in the briefing item — for self-report items, label as "self-reported" so anchors can use phrasing like "saw your post about joining Acme" rather than "Acme announced your appointment."

The Marc Andreessen "AGI is here" example: it's his opinion, not a news event. Goes in the briefing as an opinion item with `tier: 4 (opinion)`, not as a confirmed news item. Anchors derived from it must phrase as "your take that..." not "the news that...".

---

## How stage 02 applies these tiers

After categorization, but before signal scoring:

1. **Drop denylist items.** If `source_url`'s domain is on the denylist, drop the item, log the drop reason ("denylist: <domain>").
2. **Tag each item with `source_tier: 1 | 2 | 3 | 4`** based on the domain.
3. **For items making factual claims about named people, deals, or laws:**
   - Tier 1: keep, mark `corroboration: not_required`
   - Tier 2 single source: keep, mark `corroboration: single_tier_2 — sufficient for briefing, anchors allowed`
   - Tier 2 + 1 corroborating source (Tier 1, 2, or 3): keep, mark `corroboration: corroborated`
   - Tier 3 single source making a factual claim: keep in briefing as `confirmation_status: unconfirmed`. Drop from anchor generation. Operator can manually upgrade if they verify.
   - Tier 4 single source: drop from briefing unless self-report rule applies. If self-report, keep with `tier: 4_self_report`.

4. **Apply de-duplication** (existing rule: prefer Tier 1 over Tier 2 over Tier 3 over Tier 4 for the same story).

5. **Persist `source_tier` and `corroboration` fields in the briefing item's YAML** so downstream agents (networking-agent reading anchors) can see them. An anchor derived from an unconfirmed item should NOT be used in a connection note — the anchor file generator drops these.

---

## Maintenance

- Audit this file every 90 days.
- Add domains as they emerge (new fact-checked outlets to Tier 2; new fake-news domains to denylist).
- Log any incident where a false-news item slipped through — that's a signal to add a denylist entry or downgrade a tier.
- Keep the per-tier domain list small enough to scan in 30 seconds. If it grows beyond 30 domains in a tier, split or restructure.

This file changes the source-authority dimension from a soft 0-3 score (where a low-authority item could still pass on other criteria) to a hard gating rule for factual claims. The agent's signal-score system still runs, but it scores items that have already cleared the authority gate.
