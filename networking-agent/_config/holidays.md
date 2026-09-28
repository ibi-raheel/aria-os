---
title: Holiday skip days
updated: 2026-04-28
locale: US
---

# Holidays — agent skips these days

The agent does not run on these dates. If the 05:00 scheduled task fires on a holiday, the run logs a "skipped — holiday" line in `log/YYYY-MM-DD.md` and exits without sending.

## 2026

```yaml
holidays_2026:
  - 2026-01-01  # New Year's Day
  - 2026-01-19  # MLK Day
  - 2026-02-16  # Presidents' Day
  - 2026-05-25  # Memorial Day
  - 2026-06-19  # Juneteenth
  - 2026-07-03  # Independence Day (observed, July 4 is Saturday)
  - 2026-09-07  # Labor Day
  - 2026-10-12  # Columbus Day
  - 2026-11-11  # Veterans Day
  - 2026-11-26  # Thanksgiving
  - 2026-11-27  # Day after Thanksgiving
  - 2026-12-24  # Christmas Eve
  - 2026-12-25  # Christmas Day
  - 2026-12-31  # New Year's Eve
```

## 2027

```yaml
holidays_2027:
  - 2027-01-01
  - 2027-01-18
  - 2027-02-15
  - 2027-05-31
  - 2027-06-18  # Juneteenth observed (June 19 is Saturday)
  - 2027-07-05  # Independence Day observed (July 4 is Sunday)
  - 2027-09-06
  - 2027-10-11
  - 2027-11-11
  - 2027-11-25
  - 2027-11-26
  - 2027-12-23
  - 2027-12-24
  - 2027-12-31
```

## Personal blackout dates

Add specific dates here when the user is on vacation, traveling, or otherwise wants the agent dark.

```yaml
personal_blackouts:
  # - 2026-MM-DD  # description (e.g. vacation in Spain)
```

## Why these dates

LinkedIn acceptance rates drop sharply on US federal holidays and around major holidays even for international targets. Skipping preserves the daily quota for days when targets are actually checking LinkedIn. Adjust the list if user is based outside the US or targets non-US heavy.
