# Workflow: Edit X/Twitter Profile

## What it does
Updates profile fields (name, bio, location, website) on X/Twitter.

## Prerequisites
- Logged into x.com in Playwright browser

## Steps

1. `browser_navigate` to `https://x.com/settings/profile`
2. `browser_snapshot` - the Edit Profile dialog should open automatically
3. If dialog doesn't open, look for "Edit profile" button and click it
4. `browser_snapshot` - find the Name, Bio, Location, Website textboxes
5. For each field to update:
   a. `browser_click` the field
   b. Select all (Meta+a) to clear existing text
   c. `browser_type` the new value
6. `browser_snapshot` - verify all fields look correct, proofread grammar
7. `browser_click` the "Save" button
8. Verify the dialog closes (page returns to home or profile)

## Current profile values (as of 2026-04-26)
- Name: Ibi
- Bio: Founder of Arcadia. Building the future of online communities.
- Location: (empty)
- Website: (empty)

## Notes
- No em dashes in any field
- Capitalize proper nouns (Arcadia)
- Bio limit: 160 characters
- Always proofread before clicking Save
