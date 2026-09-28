# 04-draft

Drafts the coffee-ask DM by filling the matched template from `_config/coffee-ask-templates.md` against the anchor data in `03-anchor/output/<slug>.md`.

## Layout

```
04-draft/
  output/
    <slug>.md              # one file per drafted DM
```

## Template selection

`template_path` from `03-anchor` selects the variant: `<category>-shape<1|2>`. Examples:
- `consulting-partner-shape1`
- `founder-shape2`
- `tier1-vc-shape2`

Inbound-connection variant: if the dossier has `connect_direction: inbound`, swap the opener from "thanks for connecting" to "appreciate the invite from your end."

## Slot fills

| Slot | Source |
|---|---|
| `[first_name]` | dossier name (first part) |
| `[original_question_topic]` | `03-anchor.original_question` (Shape 1 only) |
| `[recent_anchor: ...]` | `03-anchor.anchor.type` + `.source` + `.topic` |
| `[contrast / extension]` | computed at draft time — operator-curated or LLM-generated continuation |
| `[sharp question]` | computed at draft time — must pass voice checklist |
| `[honest frame]` | from category template + dossier (e.g., "I'm exploring strategy roles at MBB") |
| `[day1]`, `[day2]` | computed: next two off-days that are not skipped (default Tuesday + Thursday) |

## Voice checklist

Run the 13-item checklist from `_config/coffee-ask-templates.md` on every draft. Failure → revise once. Second failure → drop candidate, log reason.

## File shape

```yaml
---
slug: <slug>
template: <category>-shape<1|2>
shape: 1 | 2
char_count: <int>
voice_checklist_passed: true | false
voice_checklist_failures: [list of failed items, if any]
draft_at: <ISO>
days_offered:
  - <day1 ISO date>
  - <day2 ISO date>
duration_minutes: 20
dm_text: |
  <full DM text, ready to send>
---

# <Name> — coffee-ask draft

## Drafted DM

> <full DM text>

## Source data

- Anchor: [[../03-anchor/output/<slug>|03-anchor/<slug>.md]]
- Original engagement: [[../../06-send/output/<slug>|06-send/<slug>.md]]
- Dossier: [[../../../memory/people/<slug>|<Name>]]
```

## Cap enforcement

Drafts are produced for ALL value-pass candidates. The cap (5-10/day) is applied here: rank by score (highest first) and only the top N proceed to `05-review/`. Overflow drafts stay in `04-draft/output/` for next-run consideration; they're re-evaluated for freshness.
