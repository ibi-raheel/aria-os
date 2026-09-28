# Workflow: Post on X/Twitter

## What it does
Composes and publishes a tweet from @IbiRaheel.

## Prerequisites
- Logged into x.com in Playwright browser
- Tweet text provided by user (or generated from context)

## Steps

1. `browser_navigate` to `https://x.com/compose/post`
2. `browser_snapshot` - find the tweet compose textbox
3. `browser_type` the tweet text into the compose box
4. `browser_snapshot` - verify text appears correctly, proofread for grammar
5. `browser_click` the "Post" button
6. `browser_wait_for` the compose dialog to close (confirms post went through)

## Verification
- Take a snapshot after posting to confirm the tweet appears in the timeline
- If the post button is disabled, check character count (280 max)

## Notes
- No em dashes in tweet text
- Capitalize proper nouns (Arcadia, etc.)
- If attaching media: use `browser_file_upload` before clicking Post
