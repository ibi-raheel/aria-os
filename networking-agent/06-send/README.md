# 06-send — Stage 06: Sent (engagement records live in output/)

`output/<slug>.md` is the **engagement record** for each contacted person. Source of truth for the anchor (with source URL + date + verbatim excerpt), the note that was sent, send timestamp, and the per-person outreach log. Files arrive here only after a successful LinkedIn send. These records carry `dossier_ref: '[[memory/people/<slug>]]'` pointing to the shared dossier.

The reconcile stage checks acceptance status 14+ days post-send and sorts copies into `../07-track/`.
