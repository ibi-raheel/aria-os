# Stage 03 — Anchor Generation

## Job

Take stage 02's bucketed items and produce candidate **anchor questions** — pre-written hooks that downstream agents (networking-agent, outreach-agent-arcadia) can use directly when composing connection notes or outreach messages. Write per-category anchor lists. Then write the final consumable briefings.

## Inputs

| File | Why |
|---|---|
| All files in `../02-categorize/output/<date>/` | The bucketed items |
| `../../outreach-agent-arcadia/_config/voice.md` | Voice rules for anchors targeting outreach |
| `../../networking-agent/_config/message-templates.md` | Per-category 300-char templates so anchors fit slot patterns |

## Process

For each of the 8 category files in `02-categorize/output/<date>/`:

1. Read every kept item.
2. For each item, generate 1-3 candidate anchors. An anchor is a specific question or observation a future networking-agent can drop into a connection note. Constraints:
   - **Grounded in the item.** The anchor must reference the actual story — its specific framing, named people, or specific data point. If you can swap the item for a different story and the anchor still works, it's not specific enough.
   - **Curiosity-led, not pitch-led.** Anchors should open conversations, not pitch products. Voice guidance lives in `../../outreach-agent-arcadia/_config/voice.md` — anchors should pass the same checks.
   - **Source-traceable.** Each anchor records the briefing-item URL it derives from, and a one-line "why this anchor" explanation referencing the excerpt.
   - **Short.** Anchor body should be ≤200 chars (the slot it fills in templates is small).

3. Within each category, rank anchors by quality. Quality criteria:
   - Specificity (highest priority — generic-sounding anchors get dropped)
   - Recency of underlying news (matches the item's signal score)
   - Voice fit (passes the 12-item voice checklist roughly)

4. Write per-category anchor file:
   ```
   ../briefings/<date>/<category>-anchors.md
   ```

5. File format:
   ```markdown
   ---
   category: consulting
   date: 2026-04-29
   anchors_count: 4
   ---
   
   # consulting anchors — 2026-04-29
   
   ## Anchor 1
   - **for:** items #1 and #3 in `briefings/2026-04-29/consulting.md`
   - **derived from:** "Jordan Example panel on agentic commerce at Google Cloud Next, 2026-04-27"
   - **source_url:** https://www.linkedin.com/in/jordan-example/...
   - **anchor body:**
     > Your Google Cloud Next post on agentic commerce landed. Most retailers still treat agents as search front-ends. Curious what use cases convinced you the shift is structural, not seasonal?
   - **char_count:** 195
   - **best_for_template:** consulting-partner
   
   ## Anchor 2
   ...
   ```

6. **Then write the consumable briefings** at `../briefings/<date>/<category>.md`. The briefing is what humans and downstream agents actually read. It combines stage 02's items (with summaries) and stage 03's anchors into one digestible file:
   ```markdown
   ---
   category: consulting
   date: 2026-04-29
   item_count: 5
   anchor_count: 4
   ---
   
   # consulting — 2026-04-29
   
   ## Top items
   
   ### 1. Jordan Example on Agentic Commerce — McKinsey
   - **source:** https://www.linkedin.com/in/jordan-example/...
   - **published:** 2026-04-28
   - **excerpt:** "It was great to share our views on the fast-changing #AgenticCommerce landscape at #GoogleCloudNext..."
   - **summary:** <2-paragraph distillation>
   - **anchor candidates:** see `consulting-anchors.md` Anchor 1, Anchor 2
   
   ### 2. ...
   
   ## Cross-references
   - Item 1 also relevant to: a16z (see `a16z.md` item 3)
   ```

7. Append final per-category anchor counts to `../log/<date>.md`.

## Output

| Artifact | Location | Format |
|---|---|---|
| Per-category anchors | `../briefings/<date>/<category>-anchors.md` | YAML frontmatter + per-anchor blocks |
| Per-category briefings | `../briefings/<date>/<category>.md` | YAML frontmatter + items + cross-refs + anchor pointers |
| Log update | `../log/<date>.md` | anchor counts per category |
| OS daily log | `../../logs/daily/<date>.md` | timestamped block summarizing the run |

## What good looks like

- Every kept item produces at least 1 candidate anchor.
- Every anchor has a source URL, a derived-from line, and a body that passes voice rules.
- Anchors are tight — every word earns its place. No filler, no "Hope this email finds you well" energy.
- Cross-references are accurate (if item appears in 2 buckets, both files reference each other).
- A reader can scan one briefing in ≤5 minutes and feel caught up on that bucket.

## What to avoid

- **Anchors that fail the name-swap test.** If you can swap the named person and the anchor still works, it's too generic. Drop and regenerate.
- **Anchors that pitch.** "Want to chat about X?" with X being a product is a pitch, not an anchor. Anchors are observational + curious.
- **Inventing context that wasn't in the item.** If the item said "panel on agentic commerce" don't anchor as if you know specific takeaways unless the item quoted them.
- **Skipping the cross-reference write.** If item 1 in consulting cross-refers a16z, the a16z briefing must mention item 1 too.

## Tools used

- LLM only — read stage 02 files + voice config, write stage 03 anchor files + final briefings. No external calls.

## Tier check

Reads stage 02 + downstream agent configs. Writes to `../briefings/<date>/` and `../log/`. Appends to `../../logs/daily/<date>.md`. No vault writes to people/companies/decisions, no outreach actions.

## Hand-off to downstream agents

After this stage completes, `briefings/<date>/` contains 8 briefings + 8 anchor files. Networking-agent's 05:00 run reads these. Outreach-agent-arcadia reads as needed for stages 03/04. The two consumers don't know or care about the 01-fetch and 02-categorize intermediates — they only read final briefings.

---

## Validate writes (final step before declaring stage complete)

Run `/validate-writes <output-dir-of-this-stage>`. Read the resulting verdict at `hygiene-agent/integrity/validate-<timestamp>.md`.

- **If PASS:** declare stage complete.
- **If FAIL:** fix every hard fail (apply auto-fixes where the validator marks them available; manual repair otherwise). Re-run `/validate-writes`. Repeat until PASS.
- **Do NOT declare stage complete until you have a PASS verdict file.**

This is the prevention layer — no bad data should propagate to the next stage. See `hygiene-agent/03-validate/CONTEXT.md` for what the validator checks.
