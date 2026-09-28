# Workflow: LinkedIn Outreach (Connection + Message)

## What it does
Sends a connection request and/or message to a specific user on LinkedIn.
Three modes depending on what the profile allows.

## Prerequisites
- Logged into linkedin.com in Playwright browser with Premium
- Target's LinkedIn profile URL known
- Connection note and message text ready

## Decision tree

For each profile, check two things:

### 1. Check Message
1. `browser_navigate` to `https://www.linkedin.com/in/{username}/`
2. Click the **Message** link/button
3. Look at the compose overlay:
   - **"Free message"** visible = type full "quick question" message (subject + body), send it
   - **"Use 1 of X InMail credits"** = close the compose, do NOT send (save credits)

### 2. Check Connect
1. Click the **More** button (aria-label="More") on the profile
2. Click **Connect** in the dropdown
3. Look at the dialog:
   - **Normal "Add a note" dialog** (no email field) = click "Add a note", type short note (~80-100 chars), send
   - **"Enter their email to connect"** = cancel, just **Follow** instead

## Message send steps (Free message only)

1. Click Message on profile
2. Verify "Free message" label
3. Type subject (specific to person's situation, not generic)
4. Type full personalized message in body (use `pressSequentially` with delay)
5. Click the blue send arrow (use `page.mouse.click()` at button position if locator fails)
6. Verify: URL changes to `/messaging/thread/`, message appears in conversation

## Connection request steps (no email gate)

1. Click More > Connect
2. Click "Add a note"
3. Type short note (~80-100 chars, one sentence)
4. Click Send
5. Verify: "Invitation sent" toast, button changes to "Pending"

## Short connection note format

One sentence, ~80-100 chars. Reference one specific thing about them.
No pitch, no Arcadia, no question, no time ask.

Examples:
- "Amy, love what you've built with Calibrae Collective. Building in the community space - would love to connect."
- "Pat, big fan of SPI. Building in the community space myself - would love to connect."

## Follow-only (email-gated connect)

1. Click the Follow button on profile
2. If an overlay intercepts clicks, use `page.evaluate()` to click via DOM

## After each person

Update the canonical file immediately:
- `sent_channel`: add `linkedin-dm` (one value for all LinkedIn actions)
- Outreach log: add separate rows for each specific action (free message, connection request, follow, etc.) with detail in the Action column
- Do NOT put `linkedin-connect`, `linkedin-follow`, `linkedin-message`, or `linkedin-inmail` in `sent_channel` or `failed_channels` - these distinctions belong in the outreach log only

## Rate limits
- Max 20 messages per day on LinkedIn
- Wait 60 seconds between messages in a batch
- LinkedIn is aggressive about rate limiting - slow down if any warnings appear
- Connection requests: ~20-30 per day safe

## Notes
- No em dashes in message text
- Capitalize proper nouns
- Use `slowly: true` or `pressSequentially` for message body
- LinkedIn's compose URL can be extracted from the Message link's href
- If an overlay div intercepts Playwright clicks, use `page.evaluate()` to click via DOM directly
