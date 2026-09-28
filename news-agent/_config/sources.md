# Sources — WebSearch + Twitter (the v2 fetch mechanism)

**Why this version exists:** v1 was a catalog of RSS feeds. Half the URLs 404'd or auth-walled (firms moved to CMS, killed RSS, or geo-block). v2 treats news fetching as a research task: per bucket, run focused WebSearch queries + monitor curated Twitter handles. No per-firm RSS to maintain.

Stage 01 reads this file at the start of every run.

---

## How it works (per bucket)

For each of the 8 buckets:

1. **Run 3-5 WebSearch queries** from the bucket's query template list, swapping `<yesterday>` for the actual date (`2026-04-28` for a 2026-04-29 run).
2. **Read the top 3-7 results** from each search via WebFetch — capture `source_url`, `published_date`, `verbatim_excerpt`, and the article body.
3. **Drive Chrome MCP to the bucket's curated X handle pages** (X formerly Twitter). Same browser-automation pattern networking-agent uses for LinkedIn. Real DOM clicks against an already-logged-in Chrome session. For each handle:
   - `navigate` to `https://x.com/<handle>`
   - `find` for "tweet posts in the timeline" → returns 5-10 article refs
   - `read_page` per ref to extract: post URL (e.g., `/cdixon/status/2042434957600076181`), timestamp ("8 hours ago" / "Apr 17"), text content
   - **Skip pinned tweets** (always at top, marked "Pinned")
   - **Skip pure quote-RTs and replies** unless the original quote text is itself substantive (>20 chars of original commentary, not just "this 👆")
   - **Filter to the date window** by parsing the timestamp. "Xh" / "Xm" relative timestamps from a 02:00 run map to "yesterday" if X ≥ 4. Older timestamps ("Apr 17", "Mar 3") need explicit date comparison.
4. **Drop items missing source_url, published_date, or text.** Pad nothing.
5. **De-dup by URL** before writing.

**X login requirement:** Ibi must be logged into X in the Chrome session that runs at 02:00. Same constraint networking-agent has for LinkedIn. If Chrome is closed or logged out, the X step degrades gracefully — WebSearch results still produce briefings, just without partner-voice signal.

Each search is bounded — top 5-10 results read deeply, the rest scanned for headlines only. X scraping is ~5-10 sec per handle (real DOM). Across 8 buckets × ~10 handles = ~80 handle visits = ~10 minutes for the full Twitter pass. Total wall-clock per run: ~45-60 min including WebSearch + WebFetch.

**Why Chrome MCP not Twitter API:** The X API moved to credit-based pricing — even read endpoints require purchased credits ("CreditsDepleted" error on the free/basic tier). Chrome MCP browser automation against a logged-in session is the free-tools-only path. Same mechanism networking-agent uses successfully for LinkedIn; zero ban risk because clicks look identical to human use.

---

## Cross-cutting (legal / regulatory — fold into the bucket each affects)

| Source | How to query | Bucket(s) |
|---|---|---|
| Federal Register API | `https://www.federalregister.gov/api/v1/articles?conditions[publication_date][gte]=<yesterday>&conditions[publication_date][lte]=<yesterday>&conditions[agencies][]=<agency>` per relevant agency | maps to bucket per categories.md law-flags |
| Congress.gov | `https://api.congress.gov/v3/bill/?fromDateTime=<yesterday>` (free tier) | founders, investors-general, big-tech |
| SEC EDGAR | `https://efts.sec.gov/LATEST/search-index?q=&dateRange=custom&startdt=<yesterday>&enddt=<yesterday>&forms=D` | investors-general |
| CourtListener | per-court RSS where useful | real-estate, big-tech |

These three (Federal Register, Congress.gov, SEC EDGAR) are the only formal APIs that proved reliable in the v1 run. Keep them.

---

## 1. consulting

### Query templates

```
("McKinsey" OR "Bain" OR "BCG" OR "Deloitte") (partner OR principal OR director) (promoted OR named OR appointed OR departed OR joined) after:<yesterday>
site:mckinsey.com OR site:bain.com OR site:bcg.com after:<yesterday>
"McKinsey Insights" OR "Bain Insights" OR "BCG Henderson Institute" published:<yesterday>
"FTC" OR "antitrust" consulting OR "non-compete" after:<yesterday>
"strategy&" OR "Deloitte Consulting" report OR study published:<yesterday>
```

### Twitter handles to monitor (firm + senior content)

- @McKinsey, @BainAlerts, @BCG, @DeloitteUS
- @QuantumBlack (McKinsey AI arm)
- @hbr (cross-reference for consulting takes)
- Curated partner-level handles to add: TBD — start with @ericschmidt-style names that frequently appear (operators turned advisors)

### Chrome MCP X scraping pattern

For each handle in the list above, drive Chrome MCP to `https://x.com/<handle>` and extract recent tweets per the standard pattern in `01-fetch/CONTEXT.md`. Skip pinned tweets and pure quote-RTs.

---

## 2. real-estate

### Query templates

```
"REIT" OR "commercial real estate" OR "CRE" earnings OR M&A OR acquisition after:<yesterday>
("CBRE" OR "JLL" OR "Cushman & Wakefield" OR "Newmark") (SVP OR partner OR managing director) (joined OR appointed OR closed OR brokered) after:<yesterday>
"opportunity zone" OR "1031 exchange" OR "REIT taxation" after:<yesterday>
"commercial lease" OR "office vacancy" OR "industrial absorption" after:<yesterday>
site:bisnow.com OR site:globest.com OR site:therealdeal.com OR site:commercialobserver.com after:<yesterday>
```

### Twitter handles

- @CBRE, @JLL, @cushwake, @newmark
- @Bisnow, @TheRealDeal, @CoStarNews, @CommercialObserver
- @REIT (Nareit)
- @KleimanRE (curated broker-personality), @adamneumann (post-WeWork commentary), @scottrechler (RXR Realty)

### Chrome MCP X scraping

For each handle above, navigate to `https://x.com/<handle>` and extract recent tweets per `01-fetch/CONTEXT.md`. Skip pinned + quote-RTs.

---

## 3. founders

### Query templates

```
("seed round" OR "Series A" OR "Series B") "$" million after:<yesterday>
"announced today" startup funding after:<yesterday>
site:techcrunch.com OR site:theinformation.com after:<yesterday>
("launched" OR "debuted") ("startup" OR "company") "founder" after:<yesterday>
```

### HN Algolia API (this worked in v1, keep)

```
https://hn.algolia.com/api/v1/search?tags=show_hn,launch&numericFilters=created_at_i><yesterday-epoch-start>,created_at_i<<yesterday-epoch-end>
```

### Twitter handles

- @TechCrunch, @Crunchbase, @Forbes, @Strictly_VC
- @paulg, @sama, @patrickc, @collisionconf
- @levie (Aaron Levie / Box-style operator-founders)
- Founder-circle: @balajis, @naval, @rabois, @gokulrajaram

### Chrome MCP X scraping

For each handle above, navigate to `https://x.com/<handle>` and extract recent tweets per `01-fetch/CONTEXT.md`. Skip pinned + quote-RTs.

---

## 4. investors-general

### Query templates

```
("VC" OR "venture capital" OR "fund") "raised" OR "closed" OR "launching" "$" million after:<yesterday>
site:fortune.com OR site:axios.com pro-rata OR term-sheet after:<yesterday>
"emerging manager" OR "solo capital" OR "scout fund" after:<yesterday>
"new fund" announced after:<yesterday>
```

### SEC EDGAR Form D (worked in v1, keep)

```
https://efts.sec.gov/LATEST/search-index?q=&dateRange=custom&startdt=<yesterday>&enddt=<yesterday>&forms=D
```

### Twitter handles

- @stridevc, @hunterwalk, @msuster, @semilshah, @jasonlk
- @StrictlyVC, @TermSheet, @AxiosProRata, @newcomer
- @PitchBook, @CBinsights
- @fredwilson (USV), @bilalfazlani (LP-side), @michaelseibel (operator+investor)

### Chrome MCP X scraping

For each handle above, navigate to `https://x.com/<handle>` and extract recent tweets per `01-fetch/CONTEXT.md`. Skip pinned + quote-RTs.

---

## 5. yc

### Query templates

```
"Y Combinator" partner OR "group partner" OR "Demo Day" after:<yesterday>
site:ycombinator.com OR site:news.ycombinator.com after:<yesterday>
"YC" batch OR "YC W" OR "YC S" announcement after:<yesterday>
"Garry Tan" after:<yesterday>
```

### HN Algolia (yc-specific)

```
https://hn.algolia.com/api/v1/search?query=Y%20Combinator%20partner&numericFilters=created_at_i><yesterday-epoch-start>,created_at_i<<yesterday-epoch-end>
```

### Twitter handles

- @ycombinator, @paulg, @garrytan, @sama, @jaltma
- @nikitabier (alum-side), @amjadmasad (Replit, YC alum-flavor)
- Partner accounts: @aaronkharris, @ericmigi, @timbresnik, @gustaf

### Chrome MCP X scraping

For each handle above, navigate to `https://x.com/<handle>` and extract recent tweets per `01-fetch/CONTEXT.md`. Skip pinned + quote-RTs.

---

## 6. a16z

### Query templates

```
"Andreessen Horowitz" OR "a16z" partner OR podcast OR portfolio after:<yesterday>
site:a16z.com OR site:future.com after:<yesterday>
"Marc Andreessen" OR "Chris Dixon" OR "Ben Horowitz" essay OR post after:<yesterday>
```

### Twitter handles (this is where a16z actually posts now)

- @a16z, @pmarca (Marc Andreessen), @cdixon (Chris Dixon), @bhorowitz (Ben Horowitz)
- @ConnieChan, @kevinakwok, @kim_milosevich, @smc90 (host of a16z podcast)
- @smattfauer, @ScottKupor, @anish_acharya
- @vijayoptionally (consumer GP)

### Chrome MCP X scraping

For each handle above, navigate to `https://x.com/<handle>` and extract recent tweets per `01-fetch/CONTEXT.md`. Skip pinned + quote-RTs. **Twitter is the PRIMARY signal for this bucket** — a16z partners post fresh thinking on X that doesn't make it onto firm sites for weeks.

---

## 7. tier1-vcs

### Query templates (firm-level)

```
"Sequoia Capital" OR "Greylock" OR "Benchmark Capital" OR "Founders Fund" OR "Index Ventures" OR "Accel" partner OR investment OR portfolio after:<yesterday>
site:sequoiacap.com OR site:greylock.com OR site:foundersfund.com OR site:indexventures.com OR site:accel.com after:<yesterday>
"led the" Series ("Sequoia" OR "Benchmark" OR "Greylock") after:<yesterday>
```

### Twitter handles (where tier-1 partners actually post)

- Sequoia: @roeloff (Roelof Botha), @stewart (Stewart Butterfield, partner), @ravi_gupta
- Greylock: @reidhoffman, @sarahtavel, @sridharrama, @asabet (Asheem Chandna)
- Benchmark: @bgurley (Bill Gurley, retired but still influential), @peterf (Peter Fenton), @sarahatavel-style
- Founders Fund: @keithrabois, @thielcap (Peter Thiel via fund), @brianspaly
- Index: @mikevolpi, @daniellevine, @jandowest
- Accel: @rich_wong, @philip_collins-style

### Chrome MCP X scraping

For each handle above, navigate to `https://x.com/<handle>` and extract recent tweets per `01-fetch/CONTEXT.md`. Skip pinned + quote-RTs. **Twitter is the PRIMARY signal for this bucket** — Tier-1 VC partners post on X what they used to post on dead firm blogs.

---

## 8. big-tech

### Query templates

```
("VP" OR "Vice President" OR "Distinguished Engineer" OR "Sr Director") (Meta OR Apple OR Google OR Amazon OR Microsoft OR Netflix) (joins OR departs OR appointed OR promoted) after:<yesterday>
site:theinformation.com OR site:theverge.com OR site:bloomberg.com tech executive after:<yesterday>
"executive order" AI after:<yesterday>
"DOJ" OR "FTC" antitrust (Apple OR Google OR Amazon OR Meta OR Microsoft) after:<yesterday>
"DMA" OR "Digital Services Act" OR "AI Act" after:<yesterday>
```

### Federal Register / DOJ for regulatory items

```
https://www.federalregister.gov/api/v1/articles?conditions[publication_date][gte]=<yesterday>&conditions[agencies][]=federal-trade-commission
https://www.federalregister.gov/api/v1/articles?conditions[publication_date][gte]=<yesterday>&conditions[agencies][]=federal-communications-commission
```

### Twitter handles

- Reporters: @CaseyNewton, @karaswisher, @nilaypatel, @arstechnica, @ina, @NSilverChannel
- Execs: @sundarpichai (Google), @tim_cook (Apple), @satyanadella (Microsoft), @elonmusk (X but cross-relevant), @chamath (operator-investor)
- Trackers: @TechMeme, @theverge, @bloombergtech

### Twitter API query

```
(from:CaseyNewton OR from:karaswisher OR from:nilaypatel OR from:TechMeme OR from:bloombergtech) -is:retweet
```

---

## Operational notes

**Rate limits:**
- WebSearch: no hard rate limit at our usage scale
- WebFetch: ~1/sec courteous; some sites geo-block or auth-wall (skip and log, don't retry hard)
- Twitter API v2 free tier: 1500 tweets / 15-min window across all queries — plenty for this use
- Federal Register: 1000 req/hr free
- SEC EDGAR: 10/sec
- Congress.gov: 5000/hr with key
- HN Algolia: ~10000/hr unofficial

**Failure handling:**
- A single search/fetch failure logs a row in `../log/<date>.md` and continues
- A whole-bucket failure produces an empty briefing per the v1 rule

**De-duplication:** same story may appear via multiple search queries or via Twitter + WebSearch. Use the article URL as the de-dup key. Prefer the original publisher over an aggregator.

**Date filtering:** "yesterday" is the prior calendar day in user's timezone. For Monday runs, fetch Friday + Saturday + Sunday (3 days). The query templates use `<yesterday>` as a placeholder — stage 01 substitutes the actual date.

**Twitter handles need maintenance.** Unlike RSS URLs, handles rarely 404 — but accounts get renamed, locked, or change posting cadence. Audit the handle lists every 90 days. Add new partner accounts as they show up in actual outreach (when networking-agent identifies a partner during enrichment, they're worth monitoring).

---

## What changed from v1

- ❌ Per-firm RSS endpoints (most 404'd or auth-walled)
- ✅ WebSearch with date-filtered Google dorks
- ✅ Twitter API v2 with curated handle lists per bucket
- ✅ Federal Register / Congress.gov / SEC EDGAR (kept — these worked)
- ✅ HN Algolia (kept — worked for founders + yc)

Net effect: the brittle "is the firm's blog feed alive?" problem becomes the much-less-brittle "do partners still post on Twitter?" — and the answer for senior people is yes.
