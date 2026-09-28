# Workflow: Send Instagram DM

## What it does
Sends a direct message to a specific user on Instagram.

## Prerequisites
- Logged into instagram.com in Playwright browser
- Target's @username known
- Message text ready

## Steps

1. `browser_navigate` to `https://www.instagram.com/{username}/` (the target's profile)
2. `browser_snapshot` - find the **"Message"** button on their profile
3. `browser_click` the Message button
4. `browser_snapshot` - the DM conversation opens in a side panel with a
   textbox labeled "Message"
5. `browser_type` the message text into the textbox (use `slowly: true`)
6. `browser_snapshot` - verify the text looks correct, proofread grammar
7. `browser_click` the **Send** button next to the textbox
8. `browser_snapshot` - verify message appears as a sent bubble with a
   timestamp. An alert "Message sent" confirms delivery.

9. `browser_navigate` back to `https://www.instagram.com/{username}/`
10. `browser_snapshot` - find the **"Follow"** button on their profile
11. `browser_click` the Follow button (if not already following)

That's it. Navigate, Message, type, Send, Follow.

## If the profile is private
The Message button won't appear. Log and skip, try a different channel.

## Verification
- The sent message appears as a bubble with a timestamp
- An alert element says "Message sent"
- The conversation shows the full message text

## Rate limits
- Max 15 DMs per day on Instagram
- Wait 45-90 seconds between DMs in a batch
- New accounts are rate-limited more aggressively

## Notes
- No em dashes in message text
- Capitalize proper nouns (Arcadia, etc.)
- Keep outreach DMs under 300 chars
- Use `slowly: true` on `browser_type` - Instagram's input field needs
  character-by-character typing to register properly
- Instagram may show a "not everyone can message this account" notice
  for some users - log and skip
