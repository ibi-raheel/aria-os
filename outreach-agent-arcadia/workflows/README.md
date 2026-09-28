# Workflows

Each file is a repeatable browser-based task the agent can execute autonomously
via Playwright MCP. The user says "do X" and the agent reads the workflow file
and runs it. No manual steps, no re-explaining.

## How to add a new workflow

1. Create `workflow-name.md` in this folder
2. Include: what it does, prerequisites, step-by-step Playwright instructions,
   verification
3. Add it to the index below

## Index

| Workflow | File | What it does |
|---|---|---|
| Post on X/Twitter | `twitter-post.md` | Compose and publish a tweet |
| Send Twitter DM | `twitter-dm.md` | Send a direct message on X |
| Send Instagram DM | `instagram-dm.md` | Send a direct message on Instagram |
| Send LinkedIn DM | `linkedin-dm.md` | Send a direct message on LinkedIn |
| Send Skool DM | `skool-dm.md` | Send a direct message on Skool |
| Send email (Gmail) | `gmail-send.md` | Compose and send an email via Gmail |
| Edit X profile | `x-profile-edit.md` | Update name, bio, location, website on X |
