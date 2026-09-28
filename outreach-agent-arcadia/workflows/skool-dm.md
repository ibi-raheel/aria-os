# Workflow: Send Skool DM

## What it does
Sends a direct message to a user on Skool.

## Prerequisites
- Logged into skool.com in Playwright browser
- Target's Skool profile name known
- Must be in the same Skool community as the target to DM them
- Message text ready

## Steps

1. `browser_navigate` to `https://www.skool.com/messages`
2. `browser_snapshot` - find the new message / compose button
3. `browser_click` the new message button
4. `browser_snapshot` - find the recipient search field
5. `browser_type` the target's name
6. `browser_snapshot` - wait for search results
7. `browser_click` the correct user
8. `browser_snapshot` - find the message input
9. `browser_type` the message text
10. `browser_click` Send (or press Enter)
11. `browser_snapshot` - verify message appears
12. Navigate to target's profile and follow them if not already following

## Alternative: message from community member list
1. `browser_navigate` to the target's community page
2. Find and click "Members" tab
3. Search for the target user
4. Click their profile, then "Message"
5. Continue from step 8 above

## Verification
- Message appears in the chat thread
- If Skool shows an error (not in same community), log and skip

## Rate limits
- Max 30 DMs per day on Skool
- Wait 30 seconds between DMs in a batch

## Notes
- No em dashes in message text
- Keep DMs under 250 chars for outreach
- Skool DMs are the most casual channel - match that energy
