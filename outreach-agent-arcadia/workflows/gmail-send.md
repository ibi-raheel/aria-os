# Workflow: Send Email via Gmail

## What it does
Composes and sends an email from you@example.com via Gmail in browser.

## Prerequisites
- Logged into mail.google.com in Playwright browser
- Recipient email address known
- Subject line and body text ready

## Steps

1. `browser_navigate` to `https://mail.google.com/`
2. `browser_snapshot` - find the Compose button
3. `browser_click` the Compose button
4. `browser_snapshot` - find the To, Subject, and Body fields in the compose window
5. `browser_type` the recipient email into the "To" field
6. `browser_click` the Subject field
7. `browser_type` the subject line
8. `browser_click` the body/message area
9. `browser_type` the email body text
10. `browser_snapshot` - verify all fields are correct, proofread
11. `browser_click` the Send button
12. `browser_wait_for` "Message sent" confirmation toast

## Fallback: Gmail MCP draft
If Playwright can't send (browser not logged in, etc.):
1. Use `mcp__claude_ai_Gmail__create_draft` to create a draft
2. Notify user that a draft was created instead of sent
3. User can review and send manually from Gmail

## Verification
- "Message sent" toast appears after clicking Send
- If "Message sent" doesn't appear within 5 seconds, take a snapshot to diagnose

## Rate limits
- Max 50 emails per day
- Wait 15-30 seconds between emails in a batch
- Gmail may flag high-volume sending - if captcha appears, stop and notify user

## Notes
- No em dashes in subject or body
- Capitalize proper nouns
- Sign off as "- ibi"
- Subject lines: lowercase, 1-3 words, curiosity-driven (per voice.md)
