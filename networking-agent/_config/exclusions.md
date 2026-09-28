---
title: Never-contact list
updated: 2026-04-28
---

# Exclusions

Anyone listed here will never appear in the daily 20, regardless of category or score. The qualify stage filters these out first.

## Format

One person per entry. Match by LinkedIn URL slug when available, otherwise by name + firm.

```yaml
exclusions:
  # - linkedin: example-name
  #   name: Example Name
  #   firm: Example Firm
  #   reason: existing colleague | already connected | competitor | personal | other
```

## Categories of exclusion

- **Existing colleagues** — anyone currently working with the user at Arcadia or close orbit
- **Already connected (1st degree)** — handled separately, but list here if there's a specific reason to never re-contact
- **Existing investors** — current cap-table relationships
- **Family / personal contacts** — don't industrialize personal relationships
- **Competitors / hostile** — anyone the user has explicit reason to avoid
- **Burnt bridges** — past failed conversations that shouldn't be reopened by the agent

## Firm-level exclusions

Sometimes a whole firm should be skipped. Use this section for that.

```yaml
firm_exclusions:
  # - firm: Example Firm
  #   reason: ongoing legal matter | personal preference | other
```

## How to add

When the user says "never contact X" or "remove Y from outreach," update this file directly and write a short note in `../memory/decisions/YYYY-MM-DD-exclude-<slug>.md` explaining why.
