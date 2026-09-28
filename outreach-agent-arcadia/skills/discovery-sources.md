# Discovery Sources - Search Recipes

Concrete queries and source-traversal patterns for stage 01 (discovery).
Used to surface candidates earning ~$20k+/month from creator-economy work
across **all community platforms**, not just Skool.

**Volume target: 50 candidates/day.**

---

## Source priority (work top-to-bottom, stop at 50)

| Priority | Source | Expected yield/day | Effort |
|---|---|---|---|
| 1 | Skool leaderboards + discover | 10-15 | Low |
| 2 | Community directories (Hive Index, Community Club) | 10-15 | Low |
| 3 | Twitter/X revenue signals (Google site: queries) | 5-10 | Medium |
| 4 | YouTube creator funnels | 5-10 | Medium |
| 5 | Patreon / Teachable / Kajabi / Circle directories | 5-10 | Medium |
| 6 | Reddit / HN / GitHub | 3-5 | Low |
| 7 | Podcast guest lists + newsletter directories | 3-5 | Low |

---

## 1. Skool

**Discovery surface:** `https://www.skool.com/discover`

**Process:**
1. Open Skool Discover page (Playwright MCP or WebSearch)
2. Filter by category: Business, Personal Development, Money, Education,
   Health & Fitness
3. Sort by member count or trending
4. For each visible community:
   - Capture: community URL, owner name, member count, tier price
   - Estimate MRR = members × tier price
5. Skip communities under ~400 paid members at $50/mo (~$20k/mo floor)
6. Dedup against `memory/people/`

**Revenue heuristic:** most paid Skools price at $39-$199/mo. Use visible
price if shown; otherwise assume $49 median.

**Additional Skool sources:**
- Skool Games leaderboard (top communities by revenue)
- Skool Stories (featured community owners)
- eLearning Harbor / CommuniPass Skool rankings
- Google: `site:skool.com "members" "$" community`

---

## 2. Community Directories

**The Hive Index** - `https://thehiveindex.com`
- Browse by category: Business, Marketing, Tech, Education, Health
- Filters: paid communities, platform (Discord, Slack, Circle, Skool)
- Each listing shows member count + platform + pricing

**Community Club** - `https://www.community.club/`
- Directory of community professionals and their communities
- Search by niche, platform, size

**Mighty Networks Discover** - `https://www.mightynetworks.com/discover`
- Paid communities on Mighty Networks
- Visible pricing and member count

**Circle Communities** - search Google for `site:circle.so` + niche keywords
- Circle communities have public-facing landing pages
- Pricing often visible on join page

**Google queries for community directories:**
```
"paid community" "members" "$" -free site:thehiveindex.com
"paid community" "$99" OR "$149" OR "$199" OR "$299" per month
"join my community" "$" members 2026
best paid communities [niche] 2026
top online communities for [niche] earning
```

---

## 3. Twitter / X (via Google site: queries)

Twitter search is gated. Use Google `site:` queries to surface tweets
with revenue signals.

**High-signal queries (rotate daily):**
```
site:twitter.com "made $20k" OR "made $30k" OR "made $50k" OR "made $100k" community
site:twitter.com "monthly recurring" course OR community -ad -hiring
site:twitter.com "100k month" creator OR community -hiring
site:twitter.com "members" "($" community OR course
site:twitter.com "course launch" "($" 2026
site:twitter.com "my discord" "members" -giveaway
site:twitter.com "stripe" screenshot creator OR community
site:twitter.com "paid community" members "$"
site:twitter.com "skool" OR "circle" OR "discord" "revenue" OR "MRR"
site:twitter.com "community business" "$" month
```

**Profile inspection checklist:**
- Bio mentions community / course / coach / creator
- Link in bio → course landing page or community signup
- Pinned tweet sells an offer
- Follower count ≥ 5,000
- Active in last 30 days

---

## 4. YouTube Creator Funnels

**YouTube Data API (free tier, 10k requests/day)**

**Search queries:**
```
"how I built my community" revenue
"course launch" "i made $"
"my paid community" members
"how I make $" "per month" community OR course
"skool" OR "circle" OR "discord" community revenue
"online course business" revenue 2026
```

**Process:**
1. Search for high-signal terms
2. For channels with 20k+ subscribers, check:
   - Description for linked community/course
   - Recent video titles for launch/revenue mentions
3. Cross-reference handle on Twitter / Skool / other platforms

---

## 5. Platform-Specific Directories

### Patreon
- Google: `site:patreon.com [niche] "per month"` - shows public earnings
- Graphtreon.com - Patreon earnings leaderboards by category
- Filter: creators earning $20k+/mo with community elements (Discord, etc.)

### Teachable / Thinkific / Kajabi
- Google: `site:teachable.com [niche] course` OR `"powered by teachable"`
- Google: `site:thinkific.com [niche]` OR `"powered by thinkific"`
- Google: `site:kajabi.com [niche]` - Kajabi creators often have landing pages
- Look for: pricing visible, community tab, member areas

### Maven
- `https://maven.com/courses` - browse by category
- Cohort-based courses with visible pricing ($500-$2000+)
- Instructors with large followings are candidates

### Podia / Gumroad
- Google: `site:podia.com [niche]` - creator storefronts
- Google: `site:gumroad.com [niche]` with revenue signals
- Gumroad shows public sales data for some creators

### Mighty Networks
- `https://www.mightynetworks.com/discover` - browse paid communities
- Filter by category, pricing visible

---

## 6. Reddit / HN / GitHub

### Reddit (JSON API, no auth)
**Subreddits:**
- /r/Entrepreneur, /r/SideProject, /r/IMadeThis
- /r/CreatorEconomy, /r/passive_income, /r/digital_marketing
- /r/OnlineBusiness, /r/WorkOnline
- /r/coursecreation, /r/teachingonline

**Queries:**
```
"my community" members revenue
"i launched" course "$"
"made $20k" OR "made $30k" OR "made $50k" month
"paid discord" members revenue
"paid community" revenue month
```

### Hacker News (Algolia API)
- Show HN posts about creator tools/courses
- "Ask HN: how I made $X teaching" threads

### GitHub
- Search users by bio: "creator" / "educator" / "course"
- Dev educators with paid Discord/Slack communities

---

## 7. Podcast Guest Lists + Newsletter Directories

### Podcasts featuring community builders
- Search podcast directories for recent guests on:
  - "The Startup Ideas Podcast" (Greg Isenberg's guests)
  - "Creator Science" (Jay Clouse)
  - "Community-Led Growth" podcast
  - "My First Million" (SaaS + community founders)
- Each guest is a potential lead - cross-reference their community

### Newsletter directories
- Substack Leaderboard - `https://substack.com/leaderboard`
  - Top newsletters by category, many have paid communities
- Beehiiv Creator Directory
- ConvertKit Creator Network

### Google queries for lists
```
"top paid communities" 2026
"best online communities" for [niche] 2026
"community builders to follow" 2026
"creators making $" per month community
"course creators" earning "$" list
```

---

## Per-batch process (daily, starts 6 AM)

1. **Skool scan** (30 min) - Discover page + leaderboards. Target: 10-15.
2. **Community directories** (30 min) - Hive Index, Community Club,
   Mighty Networks. Target: 10-15.
3. **Twitter queries** (30 min) - rotate 3-5 queries from the list above.
   Target: 5-10.
4. **YouTube search** (20 min) - 2-3 queries, check top results. Target: 5-10.
5. **Platform directories** (20 min) - Patreon leaderboards, Teachable/Kajabi
   pages. Target: 5-10.
6. **Reddit/HN/podcast/newsletter** (10 min) - quick sweep. Target: 3-5.
7. **Dedup** - cross-check all candidates against `memory/people/`.
8. **Write lead files** - `stages/01-discovery/output/<slug>.md` per capture.
9. **Create vault stubs** - `memory/people/<slug>.md` per new lead.
10. **Daily log** - append batch summary to `logs/daily/YYYY-MM-DD.md`.

Total runtime target: ~2.5 hours for 50 candidates.

---

## Capture template (per lead)

```markdown
---
name:
handle:
source: skool | twitter | youtube | reddit | patreon | teachable | kajabi | circle | mighty | maven | discord | hn | github | directory
discovered: YYYY-MM-DD
revenue_evidence: "one-line evidence string"
source_url:
follower_count:
community_platform:
community_size:
community_price:
estimated_mrr:
stage_status: discovered
vault_ref: '[[memory/people/<slug>]]'
---

# Why this person

One paragraph: what surfaced them, what makes them ICP-shaped, what
specific signal triggered the capture.
```
