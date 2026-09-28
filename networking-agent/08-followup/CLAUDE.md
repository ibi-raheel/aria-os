# 08-followup — coffee-chat ask stage

Sends DMs to LinkedIn connections you've already accepted, asking for a 20-minute coffee chat. Runs Tue/Thu at 09:00 (the off-days from the MWF networking pipeline). Caps at 5-10 sends per run.

This stage is about **converting accepted invites into actual conversations.** The original networking-agent gets the connection. This stage gets the meeting.

## What this stage does

1. **Sweep.** Drive Chrome to `linkedin.com/mynetwork/invite-connect/connections/` (sorted "Recently added"). Snapshot the visible connections. Diff against the prior sweep snapshot to identify net-new acceptees + previously-unmessaged backlog.
2. **Classify.** For each candidate, apply the value-pass rules (`_config/valuable-person-rules.md`) and the exclusion list (`_config/excluded-roles.md`). Output `value-pass` or `value-skip` with reason.
3. **Anchor.** For each value-pass person, pick the right anchor source:
   - **Shape 1 (recent accept, original anchor still hot):** reuse the original connect-note anchor and pivot the question forward.
   - **Shape 2 (old accept, fresh activity):** fetch their recent post / panel / piece as a NEW anchor.
   - **Shape 3 (old accept, no fresh activity):** drop for this cycle. Try again next sweep.
4. **Draft.** Apply the right template from `_config/coffee-ask-templates.md` based on category × shape. Run the voice checklist. If any rule fails, revise once; if it still fails, drop.
5. **Review (opt-in only).** Default is live send. If the operator wants to inspect drafts before they ship, they pass `dry-run-only` to that run; drafts then stop at `05-review/<date>/` for manual approval.
6. **Send.** Open LinkedIn message thread for the person, paste the DM, send. Atomic per-action writes to the engagement record (same convention as `06-send/`).

## Source of acceptee data

LinkedIn doesn't expose a per-person "accepted my invite" event. The agent infers it by:
- Reading the Connections page (sortable by Recently added) and diffing against `01-sweep/_snapshots/<date>.md`
- For each candidate, opening their messaging thread to check whether they replied to the original connect-note
  - **State A (replied):** thread shows their message after our connect-note. Use Shape 1 path with continuity.
  - **State B (silent accept):** thread shows only our connect-note (or no thread at all). Use Shape 2 path with new anchor.

## Two run modes

**Default (recurring):** the Tue/Thu scheduled task processes the diff since last sweep. Picks the top 5-10 value-pass candidates, drafts, ships (or stages for review).

**Backlog (manual, on-demand):** `/networking-followup-backlog` processes the historical connections list (people who accepted before this stage existed). Filtered to value-pass only, prioritized by seniority + target-firm match + recent activity. Capped at 20 candidates per run; operator approves which subset to actually message.

**Backlog-on-empty fallback (automatic):** if the regular Tue/Thu sweep returns 0 net-new acceptees, the orchestrator falls through to the historical Connections list and ships up to 5 backlog candidates that day instead of ending the run with 0 sends. This guarantees the off-day still produces volume even when no fresh acceptances have arrived. See orchestrator's Stage 1.5 for mechanics.

## Category gates (do-not-message buckets)

Some categories are gated from the follow-up stage until a different message structure is drafted:

| Category | Status | Reason |
|---|---|---|
| `real-estate` | **GATED** | Real-estate principals + advisors need a different message structure than the consulting/founder/investor template family. Coffee-ask template pending operator review. Skipped with `value-skip / real-estate-template-pending` until lifted. |

To lift a category gate: remove the row + add a Shape 1/2 template variant in `_config/coffee-ask-templates.md` for that category.

## Stage folders

```
08-followup/
  _config/
    coffee-ask-templates.md         # templates per category × state
    valuable-person-rules.md        # filter rules
    excluded-roles.md               # student / intern / junior list

  01-sweep/
    _snapshots/<date>.md            # connections-page snapshot per run
    output/<date>/
      _sweep-summary.md             # net-new, backlog-eligible, backlog-stale counts
      new-acceptees.md              # candidates this run

  02-classify/output/<date>/
    _classify-summary.md            # value-pass / value-skip + reasons
    skipped/<slug>.md               # one file per skip with reason

  03-anchor/output/<slug>.md        # anchor pick (shape 1/2/3) + source URL

  04-draft/output/<slug>.md         # drafted DM + voice checklist

  05-review/<date>/                 # dry-run gate (operator opt-in only via `dry-run-only` flag)
    <slug>.md                       # one file per drafted DM awaiting OK

  06-send/output/<slug>.md          # DM sent, engagement record updated
```

## Atomic-write rule (same as 06-send)

Every observable action writes to the engagement record before the next browser action starts:
- `coffee-ask-drafted` → write
- `opened-message-thread` → write
- `pasted-dm` → write
- `clicked-send` → write
- `confirmed-sent` → write
- `failed` → write with reason

Resume mode: if the loop crashes, the next run reads the engagement record and picks up exactly where it stopped.

## Engagement-record extension + file-update contract

The follow-up DM updates the same `06-send/output/<slug>.md` file (do NOT create a parallel record) by adding new outreach_log rows + setting status. The follow-up doesn't get its own engagement file because it's a continuation of the same relationship, not a separate one.

**Canonical file-update contract.** The orchestrator command at `../../.claude/commands/networking-followup-run.md` carries the full per-stage file-update contract (which md files get touched, what changes in each, in what order). Read it before any send action. The contract covers:

- Per-person, per-stage write targets (sweep snapshot, classify decision, anchor pick, draft, review, send loop)
- Atomic-write rule: every observable browser action completes its file write BEFORE the next action starts
- Dossier `## Engagements` row update on every status transition (one row per agent — update in place, do not append a second row)
- Daily log atomic per-action rows in `../../logs/daily/<date>.md` (single networking-agent table, send rows + follow-up rows interleaved)
- Auto-correction of stale `unverified-failure` records when state-detection finds the original message delivered in-thread

New status transitions (added to the canonical enum in `../../conventions.md`):

```
sent → accepted → coffee-asked → coffee-scheduled → coffee-completed
                              ↘ coffee-declined
                              ↘ coffee-ignored (after 14d no reply)
                              ↘ coffee-failed (send error)
```

State transitions:
- `accepted` is set by the sweep when state-detection sees the connection delivered in-thread
- `coffee-asked` is set when the DM is sent (atomic with `confirmed_sent`)
- `replied` is set on the next sweep when state-detection sees a new message from them in the thread
- `coffee-scheduled` / `coffee-declined` are operator-driven OR `/networking-reconcile`-driven from thread parsing
- `coffee-ignored` is set by `/networking-reconcile` 14 days after `coffee-asked` if no reply
- `coffee-failed` is set on send-time error (profile gone, thread locked, cap exceeded)

Each state change MUST update the dossier `## Engagements` row in the same atomic write so the dossier and engagement record never diverge.

## Hard rules

1. **Never DM a person without a value-pass classification.** No exceptions.
2. **Never DM a real-estate-bucket candidate via this stage** until the gate is lifted (see Category gates above). Discovery + send pipelines for real-estate continue normally; only the follow-up coffee-ask is gated.
2. **Never send the same coffee-ask twice.** Once `coffee-asked` is set, this stage skips that person forever (the next conversational turn is operator-led).
3. **Never restate the original question verbatim.** State A path pivots forward; State B path uses a new anchor entirely.
4. **Never use a calendar link / Calendly / scheduling page in the DM.** Plain "can I have 20 minutes of your time next Tue or Thu?" — they pick a slot themselves in their reply.
5. **Never offer more than 2 days.** "Tuesday or Thursday" — not "this week sometime."
6. **Never ask for more than 20 minutes by default.** 15 for the most senior; 30 only if the operator explicitly overrides.
8. **No format menu.** No "phone, video, or async voice" — let them choose in their reply, or default to whatever they suggest.
9. **Atomic writes.** Same rule as 06-send. Crashes mid-loop must be recoverable.

## Voice rules (apply to every DM)

The DM is governed by `_config/coffee-ask-templates.md`, which inherits voice rules from `../../outreach-agent-arcadia/_config/voice.md`. Hard gates:

- Zero em-dashes (2026 AI tell — replace with comma + parallel construction, period + new sentence, or colon)
- Zero filler ("quick question," "just wanted to," "hope this finds you well")
- Zero stock closers ("would value the connection," "look forward to your response")
- 200-400 chars (LinkedIn DM cap is 8000 but anything over 400 reads as a wall)
- Name swap test: would the DM fail if you swapped the recipient's name? It must.


## Slack channel — `#linkedin-networking`

End-of-run summary posts to **`#linkedin-networking`** (channel ID `C0B1R95QVM1`) — shared with the parent networking-agent's MWF send-run channel, so all LinkedIn-related runs land in one stream.

Routing source-of-truth: `../../_config/slack-channels.md`. Scheduled-task prompt at `networking-agent-followup-run` includes the formatting template.

Slack post failure does NOT halt the run — atomic-write rule still applies for the engagement-record updates; Slack is the notification layer only.
