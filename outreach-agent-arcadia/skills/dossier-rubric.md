# Dossier Rubric

The "good enough" specification for stage 03 (enrichment). Defines what
must be captured per qualified lead, with stop criteria so enrichment
doesn't expand into perfect-paralyze.

---

## Time budget

**45-75 min agent runtime + 10 min user gap-fill per lead.**

If you hit 75 min and the dossier still has gaps, ship it with `unknown`
fields and write a `human_checks.md` listing what the user needs to
verify.

---

## Required sections (must be present, even if marked `unknown`)

Use the schema from `memory/templates/person.md`. The full dossier is written to
`memory/people/<name>.md` (canonical) AND to
`stages/03-enrichment/output/<lead>.md` (operational copy with frontmatter
linking back).

### 1. Profile

- Real name (if discoverable beyond handle)
- Location + timezone (critical for send-protocol quiet hours)
- Background pre-creator (LinkedIn / About page)
- Current company / brand name(s)

### 2. Business

- Core offering - course / community / coaching / agency / mix
- Pricing of each product (course price, community tier, coaching
  package)
- Audience size (followers/subscribers/paid members) per platform
- Estimated MRR with **evidence link** (don't fabricate; cite source)

### 3. Stack

- Where their community lives (Discord/Skool/Circle/Slack/Telegram)
- Course platform (Teachable/Thinkific/Kajabi/Podia/Skool/Maven)
- Email tool (ConvertKit/Substack/Beehiiv/Mailchimp)
- Payment (Stripe direct/Lemonsqueezy/Gumroad)
- Site builder (custom/Webflow/Carrd/Substack)
- Notion / Airtable / other docs

### 4. Voice

- Tone (academic/bro/indie/educational/casual/formal)
- Recent content themes (last 30 days, 3-5 themes)
- Their hook style - capture 2-3 actual hooks they've used
- Words/phrases they use a lot - for mirroring

### 5. Channels (every reachable surface)

Fill the audience-metrics table from `memory/templates/person.md`:

| Platform | Followers/Subs | Posts/wk | Avg engagement |
|---|---|---|---|
| Twitter | | | |
| YouTube | | | |
| Skool | | | |
| Instagram | | | |
| TikTok | | | |
| LinkedIn | | | |
| Newsletter | | | |
| Discord | | | |

Plus: public email if findable, public Discord invite, personal site URL.

### 6. Community engagement signals

- Posts in own community: frequency (daily / weekly / monthly / dormant)
- Reply ratio: broadcast vs conversational (do they reply to members?)
- Member-to-creator activity ratio (healthy = lots of member-led
  discussion)
- Last activity date in community
- Moderation: solo show or team

### 7. Fit assessment (Arcadia-specific)

- Audience demographic match (18-45, gaming-comfortable)? Y/N + evidence
- Community size in 100-5,000 sweet spot? Y/N + count
- Current bottleneck visible (e.g., "complains about Discord notifications
  weekly")? Y/N + quote
- Spatial / interactive interest expressed? Y/N + evidence
- Niche match: strong / medium / weak

### 8. Momentum

- Growth trajectory (follower velocity, member growth) - direction
- Recent launches / press / partnerships - list 1-3
- Sentiment in last 30d posts - energetic / steady / burnt out

### 9. Loom hooks (THE personalization payload)

**3 specific things to reference in the 30-second Loom intro.** These
must be *recent and specific*, not generic praise.

Good Loom hook:
> "Saw your video last week on community burnout - the part about
> 'pretending to enjoy a Discord channel you'd unsubscribe from if you
> could' got me."

Bad Loom hook:
> "Love your content."

Capture 3 hooks. Personalization stage picks the strongest for the actual
Loom.

### 10. Pitch justification

One paragraph in their language: *why this specific person* would benefit
from Arcadia. Not generic. References their specific stack and pain.

### 11. Disqualifiers

Surface any:
- Spatial competitor already in use
- Anti-metaverse public stance
- Member base too small / too large
- Niche outside ICP

If any disqualifier appears here, **kick the lead back to stage 02 with a
note**. Don't push to stage 04.

---

## Data collection - what's easy vs hard

| Easy (free APIs / Playwright MCP) | Hard (anti-scraping / login walls) |
|---|---|
| YouTube subs + views (Data API free tier) | Instagram engagement |
| Twitter follower count + recent tweets | Twitter avg engagement at scale |
| Public Skool community page (member count, posts) | LinkedIn detail beyond what's shown logged-out |
| Public Discord invite member count | Substack paid subscriber count |
| Personal site, newsletter signup pages | Skool paid vs free split |
| Reddit user history | Patreon supporter count |

For "hard" items, mark as `unknown` and add to `human_checks.md` rather
than spending agent time fighting anti-scraping.

---

## human_checks.md template

Written next to the dossier file. Lists 3-5 specific manual verifications
the user does in 5-10 minutes.

```markdown
# Human checks for [name]

Things I (the agent) couldn't reliably verify. Please check and update
`memory/people/<name>.md` directly.

- [ ] Open their Skool community page logged in - confirm tier price and
      whether community is paid (couldn't see logged out)
- [ ] Check Instagram follower count manually - IG anti-scraping blocked
      automated check (link: https://instagram.com/...)
- [ ] Verify whether they're currently on Whop - saw a 2024 mention but
      can't confirm 2026 status (link: tweet URL)
- [ ] Confirm their location (Twitter bio says "🌎" - need actual TZ for
      send-protocol quiet hours)
```

---

## Stop conditions

Ship the dossier when ANY of these are true:

1. All 11 sections have content (even if marked `unknown` for hard items)
2. Agent has spent 75 min and at least 7/11 sections are filled
3. A disqualifier is found (kick back to stage 02 immediately, no need
   to complete the rest)
4. Lead is clearly worse than scored (e.g., revenue evidence collapses
   on inspection) - kick back to stage 02 for re-score

---

## Output

- `memory/people/<name>.md` - comprehensive dossier with all 11 sections, status
  `enriched`
- `stages/03-enrichment/output/<lead>.md` - engagement record with
  frontmatter `dossier_ref: '[[memory/people/<name>]]'` and `status:
  enriched`
- `stages/03-enrichment/output/<lead>-human_checks.md` (if any unknowns
  remain)
- `logs/daily/YYYY-MM-DD.md` block:
  `## HH:MM - outreach-agent - enriched [[memory/people/x]] (45 min, 9/11 sections, 2 human checks queued)`
