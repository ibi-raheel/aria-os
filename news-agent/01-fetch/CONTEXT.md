# Stage 01 — Fetch (v2: WebSearch + Twitter)

## Job

Pull raw news items from yesterday across all 8 buckets using **WebSearch queries** and **Twitter API monitoring**. No RSS feed dependence. No categorization here (stage 02). No filtering for relevance beyond the date window.

## Inputs

| File | Why |
|---|---|
| `../_config/sources.md` | Per-bucket query templates + curated Twitter handle lists |
| `../_config/categories.md` | Used only for the law-source mappings (which agencies/courts to filter for) |
| Today's date | Determines "yesterday" (Mon → Fri+Sat+Sun, otherwise prev day) |

## Process — per bucket (run all 8 in parallel)

1. **Determine the date window:**
   - Tuesday–Friday runs: yesterday = previous calendar day
   - Monday run: yesterday = Friday + Saturday + Sunday (3 days)
   - Holidays: extend backward to last workday

2. **Run the bucket's WebSearch queries** (3-5 templates from `_config/sources.md`):
   - Substitute `<yesterday>` in each template with the actual date
   - For each query, run `WebSearch` and capture the top 10-15 result URLs + titles
   - Reads-deeply: take the top 3-7 by relevance and call `WebFetch` to get article body
   - Items missing `source_url`, `published_date`, or a `verbatim_excerpt` (first paragraph or quoted line ≤500 chars) get dropped — log the drop reason

3. **Run the bucket's Twitter API search** (1-2 query patterns):
   - First try direct API: `curl -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" "https://api.twitter.com/2/tweets/search/recent?query=...&start_time=<yesterday>T00:00:00Z&end_time=<yesterday>T23:59:59Z&max_results=50&tweet.fields=created_at,author_id,text,entities"`
   - If the token isn't available or the API fails, fall back to WebSearch with `site:x.com OR site:twitter.com (from:handle1 OR from:handle2)` dorks
   - For each tweet, capture: tweet URL (`https://x.com/<author>/status/<id>`), `created_at` as `published_date`, `text` as `verbatim_excerpt`
   - Drop retweets and replies — only original tweets

4. **Run cross-cutting API queries** if relevant to this bucket:
   - Federal Register agencies per `categories.md` law-flags
   - SEC EDGAR Form D for investors-general
   - Congress.gov for buckets with legislation relevance

5. **De-dup by URL.** Same story via search + Twitter is common — keep the more authoritative source (article > tweet > aggregator).

6. **Write per-bucket raw output:**
   ```
   output/<date>/<bucket>.md
   ```
   File format:
   ```markdown
   ---
   bucket: consulting
   date: 2026-04-29
   date_window: 2026-04-28
   fetched_at: 2026-04-29T04:05:12
   sources_queried: [websearch, twitter, federal-register]
   item_count: 12
   queries_run: 5
   tweets_pulled: 8
   ---
   
   ## Item 1
   - **title:** <title>
   - **url:** <full URL>
   - **published:** 2026-04-28
   - **source_type:** article | tweet | filing | post
   - **excerpt:** "<verbatim quote>"
   - **discovered_via:** WebSearch query "<query string>" / Twitter handle @<handle>
   
   <article body or first 2000 chars>
   
   ---
   
   ## Item 2
   ...
   ```

7. **Append a per-bucket success/failure summary to `../log/<date>.md`:**
   ```markdown
   ## consulting — fetch
   - WebSearch queries: 5 run, 47 candidate URLs, 6 fetched, 4 kept
   - Twitter API: 12 tweets pulled, 3 kept after retweet/reply filter
   - Federal Register (FTC): 0 items in window
   - Total kept: 7
   - Failures: 1 (bain.com WebFetch geo-blocked)
   ```

## Output

| Artifact | Location | Format |
|---|---|---|
| Per-bucket raw items | `01-fetch/output/<date>/<bucket>.md` | YAML frontmatter + per-item blocks |
| Run log entries | `../log/<date>.md` | Markdown summary per bucket |

## What good looks like

- Every bucket either produces a file with kept items OR has a logged "0 kept, sources reachable" entry. No silent fails.
- Every kept item has source URL, published date, verbatim excerpt. No exceptions.
- Total run time: 45-60 minutes when all 8 buckets parallelize.
- Output is regenerable — re-running is idempotent (same queries → similar item set, modulo source flux).

## What to avoid

- **Padding empty buckets.** If a bucket genuinely had no news yesterday, write a file with `item_count: 0` and a one-line note. Don't make up items.
- **Treating Twitter retweets as primary signal.** Only original tweets count. Filter `-is:retweet -is:reply` in queries.
- **Reading every result deep.** Top 3-7 per query is enough; the rest are scanned for headlines only.
- **Fabricating excerpts.** If WebFetch can't get the article body but you have a search-result snippet, the snippet IS your excerpt — don't paraphrase.
- **Heavy categorization here.** Stage 02 does that. This stage gathers candidates for one bucket using that bucket's queries. Cross-bucket items get noted in stage 02.

## Tools used

- `WebSearch` (built-in) — primary discovery mechanism
- `WebFetch` (built-in) — read article body for top candidates
- `mcp__workspace__bash` — for Twitter API curl + Federal Register / SEC EDGAR / Congress.gov / HN Algolia API calls
- (No `Chrome MCP` for stage 01 — that's heavier, save for sites that block both WebSearch and WebFetch)

## Tier check

Read-only against external sources. Writes to `01-fetch/output/` and appends to `../log/`. No outreach actions. No vault writes.

## Failure handling

- A single-query failure (search returned 0, or fetch 404'd) logs a row in `../log/<date>.md` and continues.
- A whole-bucket failure (no queries reached anything, all sources down) writes an empty bucket file with the failure reason and stage 02 detects it and skips that bucket gracefully — yesterday's briefings remain available as fallback.

## What changed from v1

| v1 (RSS) | v2 (WebSearch + Twitter) |
|---|---|
| Read RSS feeds at fixed URLs | Run WebSearch queries, read top results via WebFetch |
| Brittle to feed-URL changes | Adapts to where content actually is |
| Couldn't access partner-specific signal | Twitter handle lists capture senior thinking |
| 4 of 8 buckets empty due to source failures | All 8 buckets reachable as long as web search works |
| Per-firm RSS catalog needed maintenance | Twitter handle lists need 90-day audits, query templates are stable |

---

## Validate writes (final step before declaring stage complete)

Run `/validate-writes <output-dir-of-this-stage>`. Read the resulting verdict at `hygiene-agent/integrity/validate-<timestamp>.md`.

- **If PASS:** declare stage complete.
- **If FAIL:** fix every hard fail (apply auto-fixes where the validator marks them available; manual repair otherwise). Re-run `/validate-writes`. Repeat until PASS.
- **Do NOT declare stage complete until you have a PASS verdict file.**

This is the prevention layer — no bad data should propagate to the next stage. See `hygiene-agent/03-validate/CONTEXT.md` for what the validator checks.
