# Workflow: Send Twitter DM

## What it does
Sends a direct message to a specific user on X/Twitter.

## Prerequisites
- Logged into x.com in Playwright browser
- Target's @handle known
- Message text ready

## Steps

1. `browser_navigate` to `https://x.com/{handle}` (the target's profile)
2. `browser_snapshot` - find the **"Message"** button on their profile
3. `browser_click` the Message button (test ID: `sendDMFromProfile`)
4. `browser_snapshot` - the DM conversation opens with a textbox labeled
   "Unencrypted message" (test ID: `dm-composer-textarea`)
5. `browser_type` the message text into the textbox
6. `browser_snapshot` - verify the text looks correct, proofread grammar
7. `browser_click` the Send button next to the textbox (test ID:
   `dm-composer-send-button`)
8. `browser_snapshot` - verify message appears as a blue bubble with a
   timestamp. If "Failed, Try Again" appears, click it once to retry.

9. `browser_navigate` back to `https://x.com/{handle}` (their profile)
10. `browser_snapshot` - find the **"Follow"** button
11. `browser_click` the Follow button (if not already following)

That's it. Navigate, Message, type, Send, Follow.

## If X shows a "Create Passcode" or encrypted chat dialog
Press `Escape` to dismiss it, then proceed from step 1.

## Verification
- The sent message appears as a blue bubble with a timestamp
- The conversation shows in the Chat sidebar on the left

## Rate limits
- Max 20 DMs per day on Twitter
- Wait 30-60 seconds between DMs in a batch

## Notes
- No em dashes in message text
- Capitalize proper nouns (Arcadia, etc.)
- Keep outreach DMs under 300 chars
- If the user has DMs closed, the Message button won't appear on their
  profile. Log and skip, try a different channel.
