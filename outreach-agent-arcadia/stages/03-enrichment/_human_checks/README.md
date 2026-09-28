# 03-enrichment/_human_checks — non-canonical helper files

Per audit finding #6 (2026-04-30): files like `<firstname>-<handle>-skool-human_checks.md` were living in `stages/03-enrichment/output/` alongside actual engagement records. They:

- aren't engagement records (no `dossier_ref`, no canonical structure)
- use a slug pattern (`firstname-handle-platform`) that doesn't map to canonical dossier slugs
- aren't graph-linked

They're *helpers* for the enrichment process — questions or facts that need human verification before the engagement record is finalized. This folder is their proper home: outside `output/`, prefixed `_` so it sorts to the top and signals "not part of the canonical pipeline."

## What lives here

`<firstname>-<handle>-<platform>-human_checks.md` files surfaced by the enrichment stage when something can't be verified mechanically and needs operator review.

## When to act on them

When the operator is doing dossier-cleanup work, scan this folder. Resolved items should either be (a) merged into the corresponding canonical dossier and the file deleted, or (b) moved to `_resolved/` if the agent's stage spec defines that subfolder.

## Why not in output/

`output/` is reserved for canonical engagement records. Mixing helpers there creates schema drift and breaks the "every output file is a graph node" invariant that hygiene-agent enforces.
