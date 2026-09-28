# 06-send (follow-up)

Sends the coffee-ask DM via LinkedIn message thread. Updates the existing engagement record at `../../06-send/output/<slug>.md` (no parallel record).

## Layout

This stage doesn't have its own `output/` folder. Instead it appends to the existing engagement record from the original send stage. The reason: the follow-up is a continuation of the same relationship, not a separate one.

```
(no files in 08-followup/06-send/output/)
The send action writes to:
../../06-send/output/<slug>.md   ← existing engagement record gets new outreach_log rows + status update
```

## Canonical file-update contract

The full per-stage file-update contract lives in `../../../.claude/commands/networking-followup-run.md` under the "File update contract" heading. **Read it before executing any send action.** The contract specifies:

- Every md file touched, when, and what changes
- Atomic-write rule (write before next browser action — no batching)
- Dossier `## Engagements` row update on every status transition
- Daily log atomic per-action row format (one row per observable action)
- Auto-correction of stale `unverified-failure` records

Local-to-this-stage summary appears below.

## Per-person send loop (atomic)

For each `review_status: approved` draft from `05-review/`:

1. Open `../../06-send/output/<slug>.md` (must exist — they were originally invited via the send stage). If missing, abort with error.
2. Open Chrome to the candidate's LinkedIn profile.
3. Click "Message" to open the thread.
4. Wait for thread to render. Detect state:
   - **State A:** thread shows their post-accept reply → use Shape 1 DM
   - **State B:** thread shows only our connect-note (or empty) → use Shape 1 or 2 DM as drafted
5. Paste the drafted `dm_text` into the message composer. Atomic write `pasted-dm`.
6. Click Send. Atomic write `clicked-send`.
7. Confirm send (toast / message appears in thread). Atomic write `confirmed-sent` with status `coffee-asked`.
8. Move the review file from `05-review/<date>/<slug>.md` to `_archive/<date>/<slug>.md` so it doesn't appear in the next review queue.
9. Append a row to `../../../logs/daily/<date>.md`: `Time | Person | Category | coffee-ask | sent`.
10. Move to the next person.

## Atomic-write rule

Same as the original send stage. Every observable action writes to the engagement record before the next browser action. Resume mode if the loop crashes.

## Engagement-record updates

The `06-send/output/<slug>.md` frontmatter gets new fields:

```yaml
# Existing (from original send):
status: sent → accepted → coffee-asked
sent_at: <original ISO>
sent_note: <original connect-note>

# New (from follow-up):
coffee_asked_at: <ISO>
coffee_ask_text: <full DM text>
coffee_ask_shape: 1 | 2
coffee_ask_template: <category>-shape<1|2>
coffee_ask_days_offered: [<day1>, <day2>]
coffee_ask_duration_minutes: 20
```

And new `outreach_log` rows:

```yaml
outreach_log:
  # ... existing rows from original send ...
  - timestamp: <ISO>
    action: opened_message_thread
    result: success
    state_detected: a | b
  - timestamp: <ISO>
    action: pasted_dm
    result: success
    char_count: <int>
  - timestamp: <ISO>
    action: clicked_send
    result: success
  - timestamp: <ISO>
    action: confirmed_sent
    result: success
    new_status: coffee-asked
```

## Failure modes

| Failure | Action |
|---|---|
| Profile gone (deleted/blocked) | Set status `coffee-failed: profile-gone`, log, skip |
| Message thread won't open | Retry once with different click pattern; if still fails, log `coffee-failed: thread-locked` |
| Send button greyed out (LinkedIn DM cap or premium-feature gate) | Log `coffee-failed: send-disabled`, halt the run, alert operator |
| Tab/Chrome crashes mid-loop | Resume from last atomic write on next run |

## Reconcile

`/networking-reconcile` (existing command) is responsible for transitioning `coffee-asked → coffee-scheduled` (manually after they reply with a time) and `coffee-asked → coffee-ignored` (after 14d no reply). The follow-up agent itself does not handle replies — that's a separate conversation surface.
