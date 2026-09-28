# engagement-cohorts/

One file per ISO week: `<YYYY-WW>.md`. Operator curates the 5 cohort members for the upcoming week. Agent reads it Monday 09:00 to start engaging.

If the next-week file is missing, the agent drops a flag at `twitter-agent/_pending-cohort.md` and skips the engagement step until the cohort is set.

Old cohort files are kept as a record — useful for spotting which past members responded to engagement, who's worth re-adding, who isn't.
