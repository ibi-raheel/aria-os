# 01-sweep

Reads the LinkedIn Connections page, snapshots the visible list, and identifies new acceptees by diffing against the prior sweep snapshot.

## Layout

```
01-sweep/
  _snapshots/
    YYYY-MM-DD.md           # one snapshot per run; full Connections list as captured
  output/
    YYYY-MM-DD/
      _sweep-summary.md     # counts: net-new, total connections, backlog-eligible
      new-acceptees.md      # list of slugs to feed into 02-classify
```

## How the diff works

1. Open `linkedin.com/mynetwork/invite-connect/connections/` (sorted "Recently added").
2. Scroll until the visible "Connected on [date]" timestamps cross the previous run's most-recent timestamp.
3. Capture each new entry: name, headline, profile URL, "Connected on" date.
4. Compute slug from name + LinkedIn URL.
5. Diff against `_snapshots/<previous-run>.md`. New entries → `new-acceptees.md`.
6. Re-snapshot the full visible list to `_snapshots/<today>.md` for the next run's diff.

## Backlog-eligible

A "backlog-eligible" entry is one already in the snapshot history but never followed-up with (no `coffee-asked` in their engagement record). The backlog mode (`/networking-followup-backlog`) processes these on operator demand.

## Edge cases

- **First run (no prior snapshot):** the entire Connections list becomes the initial snapshot; no entries flow to `02-classify`. Operator runs `/networking-followup-backlog` separately to seed the historical pool.
- **Connection removed/blocked between runs:** silently dropped from the new snapshot. Their engagement record is left as-is.
- **Operator manually accepts an invite mid-day:** picked up on the next sweep run.
