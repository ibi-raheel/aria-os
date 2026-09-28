# Stage 02 — Categorize

## Job

Take stage 01's per-source output, assign each item to one of the 8 categories from `../_config/categories.md`, drop items that don't fit any category, rank by signal score within each category, write per-category bucketed files. **No anchor generation yet** — that's stage 03.

## Inputs

| File | Why |
|---|---|
| All files in `../01-fetch/output/<date>/` | The raw items to categorize |
| `../_config/categories.md` | Bucket definitions and law-source mappings |
| `../_config/source-authority.md` | Tier classification, denylist, corroboration rules |

## Process

1. Read every file in `01-fetch/output/<date>/`. Each yields a list of items with `url`, `published`, `excerpt`, `raw_body`.

2. **Apply source-authority gating per `../_config/source-authority.md`** (this happens BEFORE category assignment — denylisted or sole-Tier-4 items shouldn't even reach bucket scoring):
   - **Drop denylist items.** If the item's `source_url` domain matches the denylist, drop it. Log the drop with reason `denylisted: <domain>`.
   - **Tag each surviving item with `source_tier: 1 | 2 | 3 | 4`** based on its publisher domain per the tier definitions.
   - **For items making factual claims about named people, deals, or laws** (promotions, hires, departures, deals led, statements attributed, awards, etc.):
     - Tier 1 single source → keep, mark `corroboration: not_required`. The source IS the news (SEC filing, Federal Register notice, firm-official press release).
     - Tier 2 single source → keep, mark `corroboration: single_tier_2`. Anchors allowed but flagged.
     - Tier 2 + 1 corroborating Tier 1/2/3 source → keep, mark `corroboration: corroborated`. Anchors allowed without flag.
     - Tier 3 single source → keep but mark `confirmation_status: unconfirmed`. Drop from anchor generation. Operator can manually upgrade if they verify.
     - Tier 4 single source → drop unless the self-report exception applies (the named person posting about themselves on X/LinkedIn). Self-report items keep with `tier: 4_self_report` and anchors must phrase as "saw your post that…" not "the news that…".
   - **For non-factual-claim items** (analysis, thought-leadership, market commentary): no corroboration required, but Tier 4-only items still mark as opinion (`type: opinion`) so anchors phrase appropriately.
   - **Verify date.** The item's `published_date` must be within the date window. If WebFetch captured a date from the article body or `<meta>` tags, mark `date_confidence: high`. If only the search-result snippet's claimed date is available, mark `date_confidence: low` — and if low-confidence AND outside window, drop.

3. For each surviving item, determine its category:
   - Check against bucket definitions in `_config/categories.md` ("Counts" rules per bucket).
   - If the item is a legal/regulatory item (Federal Register, Congress.gov, SEC EDGAR, etc.), match it to the bucket whose audience is most affected per the law-source mappings.
   - If the item fits 2+ buckets, assign to the most-specific one and add a cross-reference note for the others (per `categories.md` § "How to handle items that fit multiple buckets").
   - If the item fits 0 buckets, drop it. Log the drop reason in the run log.

4. Score each kept item on a 0-10 signal score:
   - **Recency** (0-3): same-day = 3, yesterday = 2, 2 days ago = 1, older = 0.
   - **Source authority** (0-3): now derived from `source_tier` rather than guessed — Tier 1 = 3, Tier 2 = 2, Tier 3 = 1, Tier 4 = 0.
   - **Specificity** (0-2): names a specific person or firm in our target lists = 2; sector-level relevance = 1; general industry = 0.
   - **Action-relevance** (0-2): item lends itself to a connection-note hook = 2; informative but hook-light = 1; pure background = 0.

5. Within each bucket, keep the top items by signal score:
   - If bucket has ≤10 items: keep all.
   - If bucket has 11-20 items: keep top 10.
   - If bucket has 20+ items: keep top 12 + log how many were dropped.

6. Write one file per bucket:
   ```
   output/<date>/<category>.md
   ```
   Example: `output/2026-04-29/consulting.md`, `output/2026-04-29/real-estate.md`, ..., `output/2026-04-29/big-tech.md`.

7. File format (each kept item carries the source-authority fields from step 2):
   ```markdown
   ---
   category: consulting
   date: 2026-04-29
   items_kept: 5
   items_dropped: 0
   items_dropped_denylist: 0
   items_dropped_unconfirmed: 0
   ---
   
   ## 1. <title> — score 9
   - **source_url:** <URL>
   - **source_tier:** 1 | 2 | 3 | 4
   - **corroboration:** not_required | single_tier_2 | corroborated | unconfirmed | self_report
   - **corroborated_by:** [URLs of additional sources, if any]
   - **published:** 2026-04-28
   - **date_confidence:** high | low
   - **excerpt:** "<verbatim>"
   - **verbatim_match:** true
   - **signal_score:** 9 (recency 3 + authority 3 + specificity 2 + action-relevance 1)
   - **summary (2 paragraphs):**
     <agent-written distillation, ~100-150 words>
   - **cross_references:** [if any]
   
   ## 2. ...
   ```

8. Empty buckets get a single-line file:
   ```markdown
   ---
   category: yc
   date: 2026-04-29
   items_kept: 0
   ---
   
   No notable items in this category for 2026-04-29.
   ```

9. Append per-category counts to `../log/<date>.md`, INCLUDING drop reasons (denylisted, tier-4-only, unconfirmed-tier-3, date-confidence-low):
   ```markdown
   ## consulting — categorize
   - Items in: 12
   - Denylisted drops: 1 (theonion.com)
   - Tier-4-only drops: 2 (sole-source tweets without corroboration)
   - Tier-3-unconfirmed drops from anchors: 1 (kept in briefing flagged)
   - Date-confidence-low drops: 0
   - Items kept: 8
   ```

## Output

| Artifact | Location | Format |
|---|---|---|
| Bucketed items per category | `02-categorize/output/<date>/<category>.md` | YAML frontmatter + per-item blocks |
| Log entry | `../log/<date>.md` | Markdown table updated with per-category counts |

## What good looks like

- All 8 categories produce a file every weekday (some may be empty — fine).
- Every kept item has a complete signal score breakdown — you can see WHY it scored 9 vs 6.
- Summaries are fact-grounded — they reference the excerpt verbatim, never paraphrase the URL.
- Cross-references are bidirectional (if item X in consulting cross-references a16z, item X also appears as a one-liner in a16z's file).
- Total run time: under 15 minutes (LLM-bound for the summaries, not network-bound).

## What to avoid

- **Inventing summaries.** Every summary must be derivable from the excerpt + raw_body in the source file. If those don't say something, don't summarize as if they did.
- **Inflating signal scores.** A score of 8+ should be rare and meaningful. Don't grade-inflate.
- **Cross-referencing for the sake of it.** Cross-reference only when the item has GENUINE interest to a second bucket. "Mentions a16z in passing" doesn't qualify.
- **Re-fetching.** This stage reads stage 01's output only. If something looks missing in 01's output, log it and continue — don't fetch live.

## Tools used

- LLM only — read stage 01 files, write stage 02 files. No external calls.

## Tier check

Reads `01-fetch/output/`. Writes to `02-categorize/output/` and appends to `../log/`. No vault writes, no outreach actions.

## One-way reference rule

This stage reads stage 01. Never reads stage 03 or briefings/. (Stage 03 reads stage 02; briefings/ writes from stage 03's output.)

---

## Validate writes (final step before declaring stage complete)

Run `/validate-writes <output-dir-of-this-stage>`. Read the resulting verdict at `hygiene-agent/integrity/validate-<timestamp>.md`.

- **If PASS:** declare stage complete.
- **If FAIL:** fix every hard fail (apply auto-fixes where the validator marks them available; manual repair otherwise). Re-run `/validate-writes`. Repeat until PASS.
- **Do NOT declare stage complete until you have a PASS verdict file.**

This is the prevention layer — no bad data should propagate to the next stage. See `hygiene-agent/03-validate/CONTEXT.md` for what the validator checks.
