# networking-agent

Automated LinkedIn networking pipeline. Sends 20 personalized connection requests per run on a **Mon/Wed/Fri 05:00 cadence** (decision: 2026-05-04), distributed across 8 categories tied to specific personal goals (job at MBB, lease due diligence, ecosystem density). On the off-days (Tue/Thu) the `08-followup/` stage ships 5-10 coffee-chat-ask DMs to connections who already accepted.

> **Operating mode:** runs autonomously via four scheduled tasks (discovery 02:30, qualify 02:50, send 05:00 on Mon/Wed/Fri; follow-up 09:00 on Tue/Thu). The user can run any stage manually with the `/networking-*` slash commands.

## Quick reference

| | |
|---|---|
| Send target (per run) | Up to 23 connection requests, **15 hard floor**, 300-char personalized notes |
| Send schedule | 05:00 local, **Mon/Wed/Fri** (weekend + holidays skip) |
| Follow-up target (per run) | 5-10 coffee-chat-ask DMs, 200-400 chars |
| Follow-up schedule | 09:00 local, **Tue/Thu** (off-days from the send pipeline) |
| Channel | LinkedIn connect + note → LinkedIn DM thread continuation |
| Send mechanism | Claude-in-Chrome MCP on user's logged-in session |
| State model | File location in stage folder = state. Plain markdown only. |
| Source of truth | `06-send/output/<slug>.md` — single canonical file per person, accreted by both send and follow-up stages |

## Per-run split (send stage, rebalanced 2026-05-06)

Spec total 23, hard floor 15. If projected ranked < 15 the agent halts and pings `#linkedin-networking` rather than ship a thin run. Decision: 2026-05-06-networking-agent-15-floor-bigtech-expansion.

| Slots | Category | Role | Goal |
|------:|----------|------|------|
| 4 | Consulting | Wide-pool absorber | Job at McKinsey / Bain / BCG |
| 3 | Real estate | Weak-pool, gated for follow-up | Lease due diligence |
| 2 | Founders | Weak-pool | Peer learning |
| 2 | Investors (general) | Weak-pool | Long-term ecosystem |
| 2 | YC (firm) | Premier — never accept cascade | Pipeline access |
| 2 | a16z | Premier — never accept cascade | Pipeline density |
| 2 | Tier-1 VCs | Premier — never accept cascade | Sequoia, Greylock, Benchmark, Founders Fund, Index, Accel |
| 6 | Big Tech | Wide-pool absorber, function-broad | HR/PM/EM/design/GTM/finance/ops at FAANG/MSFT/Nvidia/Stripe-tier |

When weak-pool buckets undersupply, slots cascade into the wide-pool absorbers (consulting + Big Tech). Premier slots stay empty rather than burn anchors.

## How to run

**Automatic.** Four scheduled tasks: `networking-agent-discovery` (02:30 MWF), `networking-agent-qualify` (02:50 MWF), `networking-agent-daily-run` (05:00 MWF — sends), and `networking-agent-followup-run` (09:00 Tue/Thu — coffee-ask DMs).

**Manual.** From any folder in the OS:
- `/networking-discover`, `/networking-qualify`, `/networking-send` — individual MWF stages
- `/networking-followup-run` — Tue/Thu coffee-ask loop (sweep → classify → anchor → draft → review or send)
- `/networking-followup-backlog` — manual one-shot for historical Connections backlog
- `/networking-reconcile` — check acceptances + transitions, move 06 → 07-track/<state>/
- `/networking-status` — read-only pipeline state
- `/networking-run` — DEPRECATED all-in-one (use individual commands)

## Folder structure (post 2026-04-28 refactor + 2026-05-04 follow-up addition)

```
networking-agent/
├── README.md                ← you are here
├── CLAUDE.md                ← agent-specific instructions for Claude sessions
├── _config/                 ← targets, templates, quota, exclusions, holidays
├── 01-sources/              ← saved searches, CSVs, inbox by category
├── 02-discovery/            ← MWF discovery output (vetted candidate pools)
├── 03-qualify/              ← MWF qualify output (ranked send queue)
├── 06-send/output/          ← canonical files — source of truth, accreted by send + follow-up
├── 07-track/                ← post-send routing (accepted / ignored / declined / job-pipeline)
├── 08-followup/             ← Tue/Thu coffee-chat-ask stage (sweep → classify → anchor → draft → review → send)
└── log/                     ← run summaries (counts + anomalies)
```

The previous `04-enrich/` and `05-personalize/` stages were collapsed into `/networking-send`'s per-person loop. The follow-up stage `08-followup/` was added 2026-05-04 to convert accepted invites into actual conversations — see `08-followup/CLAUDE.md` for the stage spec.

## Setup tasks before first run

1. Confirm Premium tier (Career / Business / Sales Nav) and update `weekly_cap` in `_config/daily-quota.md`.
2. Populate `01-sources/<category>/W01-<segment>/` with at least one LinkedIn saved-search URL or seed list per category.
3. Add personal exclusions to `_config/exclusions.md` (current colleagues, existing investors, anyone you've already connected with).
4. Run `/networking-discover` once manually to verify lead ingestion before the first scheduled run.

## See also

- `PLAN.md` — full design rationale and rotation schedule
- `../CLAUDE.md` — OS-level routing rules
- `../DESIGN.md` — ICM architectural canon
- `../outreach-agent-arcadia/` — sibling agent (different goal, same scaffold)
