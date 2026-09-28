# news-agent — Claude session instructions

You are operating inside the **news-agent**, a sibling of `outreach-agent-arcadia/` and `networking-agent/` in the Aria Agent OS. Read the parent OS context first:

1. `../CLAUDE.md` — OS-level routing, vault rules, wikilink conventions
2. `../DESIGN.md` — ICM architectural canon
3. `../conventions.md` — naming source of truth
4. `./README.md` — what this agent does, how to operate it

Then this file for agent-specific rules.

---

## What this agent does

Runs **daily at 02:00 local on weekdays**, an hour before networking-agent's 05:00 run. Pulls news from yesterday/day-before across the same 8 categories networking-agent targets, categorizes items, generates candidate anchor questions, and produces one consumable briefing per category per day. Output feeds the 05:00 outreach pipelines as fresh, source-grounded material so connection notes and outreach messages reference real recent events instead of stale dossier facts.

**This agent does not contact anyone.** It produces context. networking-agent and outreach-agent-arcadia are the only agents that initiate contact; news-agent is a read-only producer of `briefings/<date>/<category>.md` files.

---

## Output the agent produces

For each weekday run, news-agent writes:

1. **Per-category briefings** at `briefings/<date>/<category>.md` (8 files):
   - `consulting.md` — McKinsey/Bain/BCG/Deloitte news, plus consulting-relevant FTC/regulatory items
   - `real-estate.md` — REIT/CRE news, zoning/tax law changes, lease-market shifts
   - `founders.md` — TechCrunch/Strictly VC startup news, fundraising rounds
   - `investors-general.md` — VC/angel news, SEC adviser rulings, fund formations (Form D), Strictly VC
   - `yc.md` — Y Combinator partner news, batch announcements, alumni events
   - `a16z.md` — Andreessen Horowitz portfolio + thought-leadership news
   - `tier1-vcs.md` — Sequoia/Greylock/Benchmark/Founders Fund/Index/Accel news
   - `big-tech.md` — Meta/Apple/Google/Amazon/Microsoft/Netflix exec moves, regulatory pressure, product launches

2. **Per-category anchor lists** at `briefings/<date>/<category>-anchors.md` (8 files): pre-written candidate connection-note hooks derived from the day's news, ready for networking-agent / outreach-agent-arcadia to use directly or as starting points.

3. **Run log** at `log/<date>.md`: machine-readable summary of items fetched per source, items kept after categorization, anchors generated.

4. **Daily activity entry** appended to `../logs/daily/<date>.md`: a timestamped block per the OS-wide daily log convention.

---

## Categories — the same 8 buckets networking-agent targets

Bucket definitions and source lists live in `_config/categories.md`. The agent reads that file at the start of every run. The 8 buckets:

1. **Consulting** — MBB + Deloitte S&O / Strategy& / PwC Strategy
2. **Real estate** — REIT execs, RE PE, family offices, tenant-rep brokers, RE attorneys, plus zoning/tax law
3. **Founders** — peer-level founders, seed → Series B
4. **Investors (general)** — VCs/angels/family offices outside premier-firm buckets
5. **YC** — Y Combinator partners, group partners, ops staff
6. **a16z** — Andreessen Horowitz GPs, partners, principals
7. **Tier-1 VCs** — Sequoia, Greylock, Benchmark, Founders Fund, Index, Accel
8. **Big Tech execs** — VP+ at Meta/Apple/Google/Amazon/Microsoft/Netflix

**Laws and regulation are NOT a 9th bucket.** Legislative items get categorized into whichever bucket they affect (e.g., a new SEC marketing rule lands in `investors-general.md`; a new commercial-lease law lands in `real-estate.md`). This matches how recipients actually consume news — via their professional context, not as a generic "laws" feed.

---

## Stage flow

```
01-fetch          → 02-categorize       → 03-anchor-generation  → briefings/<date>/
(per-source raw)    (bucketed by category)  (candidate questions)    (consumable output)
```

Each stage has its own folder and CONTEXT.md. Files are plain markdown. The agent reads stage N-1's output to produce stage N's output.

---

## Critical rules

1. **Cite source URL + date + verbatim excerpt for every news item.** No item enters a briefing without these three fields. If the agent can't find them, the item drops. Same "no anchor, no send" discipline networking-agent uses.

2. **Yesterday means yesterday.** A 02:00 Tuesday run pulls items dated Monday (the prior calendar day in the user's timezone). For weekend coverage, Monday's 02:00 run pulls Friday + Saturday + Sunday items (3 days). Holidays follow the same rule — Tuesday after a Monday holiday pulls Friday + Sat + Sun + Mon.

3. **No hallucinated news.** If a source returned no items for a category on a given day, the briefing for that category includes a single line: "No notable items in this category for <date>." It does NOT pad with stale items, paraphrased rumors, or invented stories. Empty briefings are fine — they tell the operator "nothing in this bucket today."

4. **One briefing file per category per day.** Never combine. Never split. The file path is part of the contract: `briefings/<YYYY-MM-DD>/<category>.md`.

5. **Anchor questions are derived from real news items.** Every candidate anchor in `<category>-anchors.md` cites the briefing item it's derived from (line number reference or quoted excerpt). networking-agent should be able to trace any anchor back to a real source.

6. **Free tools only** — Federal Register API, Congress.gov API, SEC EDGAR, WebSearch with date-filtered Google dorks, HN Algolia, Reddit JSON API, free tier of YouTube Data API, and Chrome MCP for X (Twitter) since the X API moved to credit-based pricing. No paid SaaS.

7. **Append to the OS daily log.** Every run writes a timestamped block to `../logs/daily/<date>.md` summarizing items fetched per category and anchors generated. Per the OS-wide convention.

8. **Briefings are append-only as files but rewrite-okay.** The agent writes the full briefing content for the day in one shot — there's no "extending yesterday's briefing." Yesterday's briefing stays static; today's is a fresh file.

9. **Retention is 90 days.** The retention rule lives in `_config/retention.md`. After 90 days, briefings older than that get moved to `_archive/briefings/`. Anchors get pruned. The user can adjust the retention window in the config without touching agent code.

10. **Source-authority gating before categorization.** Every fetched item is tier-tagged per `_config/source-authority.md` (Tier 1 = primary/official, 2 = established journalism, 3 = aggregator, 4 = social/opinion). Stage 02 drops denylisted domains, drops Tier-4-only items unless the self-report exception applies, and flags Tier-3 single-source claims about named people as `unconfirmed` (kept in briefing, dropped from anchor generation). Tier-2 single-source factual claims about named people need either Tier-1 corroboration or another Tier-2/3 corroborating source before anchors can use them. The dossier facts an anchor cites must match the source's verbatim excerpt — drift drops the anchor.

---

## Slash commands (in `../.claude/commands/`)

```
/news-run          — chain all stages; called by the 02:00 scheduled task
/news-fetch        — pull raw items from sources (stage 01)
/news-categorize   — bucket fetched items by category (stage 02)
/news-anchors      — generate candidate anchors per item (stage 03)
/news-status       — read-only summary: today's run, briefings produced, items per category
```

Specs for each command live at `cowork/2026-04-29/news-slash-commands.md` for now (`.claude/commands/` writes are blocked in some Cowork sessions). Move them to `.claude/commands/` to activate.

---

## Configs (in `_config/`)

- `categories.md` — what's in each of the 8 buckets, plus per-bucket source list and law-sources mapping
- `sources.md` — WebSearch query templates, API endpoints, X handles to scrape via Chrome MCP
- `source-authority.md` — 4-tier source classification, denylist, corroboration rules (anti-false-news guardrails)
- `retention.md` — 90-day window, archive policy

Read configs at the start of every run. If you change a config, write a decision file at `../memory/decisions/YYYY-MM-DD-<slug>.md` explaining what and why.

---

## Integration with downstream agents

**networking-agent** reads `news-agent/briefings/<today>/<category>.md` during its 03-qualify and per-person send loop:
- Filtering: a person whose firm appears in today's briefing gets a small score boost (recency signal).
- Anchor sourcing: during the send loop's "live enrich" step, the agent first checks if a pre-generated anchor for this person's bucket exists in `<category>-anchors.md` — if yes and it's fresh, use it; if no, generate fresh.

**outreach-agent-arcadia** reads briefings during stage 03-enrichment and stage 04-personalization for the community-creators / founders buckets, using anchor questions as discovery angles or cold-email opening hooks.

Both downstream agents handle "what if news-agent didn't run today" gracefully: they use yesterday's briefings as fallback (briefings retained 90 days), or fall back to their own enrichment/anchor-generation if no briefings exist.

---

## What good looks like

- Every weekday by 04:30, 8 briefings exist at `briefings/<today>/`. None empty (some "nothing in this bucket today" placeholders OK).
- Every briefing item has source URL + date + verbatim excerpt + 2-paragraph distillation.
- Every candidate anchor traces back to a specific briefing item.
- Networking-agent's 05:00 run finds material it can use within 30 seconds of opening the briefing file — no hunting.
- The user can read a single briefing file in 5 minutes to feel caught up on a category.
- 4 weeks in, the briefings folder is large enough to spot patterns ("Sequoia mentioned tier-1 VCs 14 times this month") via grep.

## What to avoid

- Padding empty buckets with stale items.
- Generating anchors that aren't traceable to a real news item.
- Letting any briefing item lack a source URL.
- Running fetch + categorize + anchor-generation as one giant batch — keep the stages separated so failures are isolatable.
- Re-running for past dates without explicit user request — the schedule covers ~yesterday, not history.

## Dossier reads — fold-line convention (added 2026-04-30)

Person dossiers at `../memory/people/<slug>.md` use a fold-line layout per `../conventions.md`:

- **Above** the `---` + `## Deep notes` line: `## Who`, `## Voice`, `## Engagements`, `## Related`. **Read these by default.**
- **Below** the fold: `## Business`, `## Stack`, `## Audience metrics`, `## Momentum`, `## Disqualifiers`, etc. **Read only when your current task explicitly needs the data.**

For routine work (dedupe checks, last-touch lookups, slug resolution), agents stop reading at the `---`. Only descend below when an action requires deep enrichment data the header section doesn't carry.


## Slack channel — `#news`

End-of-run summary posts to **`#news`** (channel ID `C0B1XLKMR18`) via the Slack MCP. Routing source-of-truth: `../_config/slack-channels.md`. The scheduled-task prompt at `news-agent-daily-run` includes the formatting template.

Slack post failure does NOT halt the run — log to daily log + continue. Run files are authoritative; Slack is the notification layer.
