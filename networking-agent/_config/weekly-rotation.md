---
title: Weekly rotation — DEPRECATED 2026-05-01
status: deprecated
updated: 2026-05-01
---

# Weekly rotation — DEPRECATED

The W01–W04 sub-segment rotation was removed on 2026-05-01 because it added more friction than value. All source URLs now live in flat per-category `searches.md` files (see `01-sources/README.md`).

The discover stage walks all sources every morning. Dedup against `06-send/output/` prevents re-contacting anyone. Variety happens naturally because the searches return different people each time.

This file is kept only as a record of the prior architecture. The discover stage no longer reads from it.

If you want to re-introduce sub-segment targeting later, the right answer is probably **tags within the flat searches.md** (e.g. group URLs under `## McKinsey`, `## Bain`, etc. and have the agent rotate which sub-heading it prioritizes). Not separate folders.
