# 01-sources — Lead source configs (flat, post-2026-05-01)

The discover stage reads from this folder. **One `searches.md` per category, flat.** Drop your LinkedIn saved-search URLs (or other source URLs) into the matching category's `searches.md` file.

```
01-sources/
├── consulting/searches.md
├── real-estate/searches.md
├── founders/searches.md
├── investors-general/searches.md
├── yc/searches.md
├── a16z/searches.md
├── tier1-vcs/searches.md
├── big-tech-execs/searches.md
└── inbox/                 # drop unsorted CSVs / seed lists here
```

Each `searches.md` accepts:
- LinkedIn saved-search URLs (one per line, or grouped under sub-headings)
- Direct URLs to public team pages (e.g. ycombinator.com/people, a16z.com/people)
- Free-text seed lists ("Name @ Firm" lines that the agent enriches)

## Why no rotation anymore

Earlier versions had W01–W04 subfolders inside each category that rotated weekly. Removed 2026-05-01 because it added more complexity than it earned. Variety happens naturally — the discover stage walks all sources fresh each morning, dedup against `06-send/output/` ensures we don't re-contact anyone.

The W-week subfolders are now empty vestiges. Their content was merged into the parent category's `searches.md` with sub-headings preserving the original sub-segment context. Safe to delete from Finder.

## Adding new sources

Open the category's `searches.md`, paste the URL, save. Next morning's run picks it up.
