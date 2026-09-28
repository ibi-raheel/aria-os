# 07-track — Stage 07: Connection lifecycle tracking

Subfolders sort post-send state:
- `accepted/` — connection accepted, follow-up plan in file body
- `ignored/` — pending > 60 days, presumed dropped
- `declined/` — explicitly declined or profile gone
- `job-pipeline/` — copies (not moves) of accepted consulting-category leads, on a slower job-aware follow-up cadence
