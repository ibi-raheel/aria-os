---
title: Target filters per category
updated: 2026-04-28
---

# Target filters

The discovery and qualify stages read this file to decide who counts as a valid target. Each category has explicit inclusion criteria and shared exclusions.

## Universal exclusions (apply to every category)

- Anyone in `exclusions.md`
- Anyone with a canonical file in `06-send/output/` (already contacted)
- Anyone marked as a 1st-degree connection on LinkedIn (use a different flow for existing connections)
- Profiles with no public anchor (no recent post, no notable bio, no public work) — fail the scoring threshold
- Accounts that look fake or dormant (no photo, <10 connections, last activity >2 years)

---

## 1. Consulting (4/day) — JOB TARGET

**Sub-allocation:** 3 partners + 1 recruiter per day.

**Partners — include:**
- Title contains: Partner, Senior Partner, Principal, Associate Partner, Director (only at consulting firms)
- Firm in: McKinsey & Company, Bain & Company, Boston Consulting Group, BCG, Deloitte (S&O practice only), PwC (Strategy& only), Oliver Wyman, Kearney, L.E.K., Roland Berger
- Tenure at firm ≥ 2 years (no recent transfers — they're still ramping)

**Recruiters — include:**
- Title contains: Talent Acquisition, Recruiter, People & Talent, Recruiting Lead, Campus Recruiter, Experienced Hire Recruiter
- Firm in MBB list (consulting recruiters specifically — not generic agency recruiters)

**Exclude:**
- Junior staff (Associate, Consultant, Senior Consultant) — partners only on the partner side
- Big-4 audit / tax (Deloitte tax, PwC audit, EY, KPMG outside their strategy practices)

---

## 2. Real estate (3/day) — LEASE DUE DILIGENCE

**Mix:** ~2 principals + 1 advisor per day on average.

**Principals — include:**
- REIT executives at VP+ level (Boston Properties, SL Green, Vornado, Simon Property Group, Kimco, Federal Realty, Prologis, Rexford, Equity Residential, AvalonBay, Host Hotels, etc.)
- Real estate private equity: Partner, Principal, Managing Director at Blackstone Real Estate, Brookfield, Starwood, KKR Real Estate, Carlyle Real Estate, Tishman Speyer, Related Companies
- Family-office heads with disclosed RE focus
- Developer-owners: Founders / Owners / Presidents of mid-to-large CRE development firms

**Advisors — include:**
- Senior tenant-rep brokers at CBRE, JLL, Cushman & Wakefield, Newmark, Savills, Colliers — title SVP, EVP, Vice Chairman, or Senior Director equivalent
- Real estate attorneys: Partner level at firms with strong CRE practice (Skadden, Latham, Gibson Dunn, Goodwin, Greenberg Traurig, DLA Piper, Fried Frank)
- Lease consultants and tenant advocacy specialists

---

## 3. Founders (2/day)

- Founders / Co-founders / CEOs of post-product startups
- Stage mix: pre-seed/seed, Series A, Series B+, second-time founders (group your `searches.md` URLs by stage if you want)
- Company size 5–500 employees
- Excluded: solo founders pre-product (less to anchor on), public-company CEOs (different tier of game)
- Sectors: weighted toward creator tooling, fintech, SaaS B2B, prop-tech, consumer mobile (adjust based on user's interest)

---

## 4. Investors — general (2/day)

Investors NOT covered by the YC, a16z, or Tier-1 VC buckets below.

- VCs (GP, Partner, Principal) at funds <$2B AUM
- Angel investors with disclosed track record (≥5 portfolio companies)
- Family offices with venture allocations
- Solo capital / scout-program leads
- Excluded: corporate venture (different dynamic), investor-relations staff

---

## 5. YC (firm) (2/day)

- Y Combinator partners, group partners, visiting partners
- YC operations / program staff (recruiting partners, alumni network leads, Demo Day team)
- Excluded: YC-funded founders (those go in the Founders bucket)

---

## 6. a16z (2/day)

- General Partners, Partners, Principals at Andreessen Horowitz
- Operating partners and platform team leads
- Excluded: a16z-funded founders (Founders bucket)

---

## 7. Tier-1 VC firms (2/day)

Investment roles at: Sequoia Capital, Greylock, Benchmark, Founders Fund, Index Ventures, Accel.

- General Partners, Partners, Principals (any vintage)
- Operating partners and platform staff
- Excluded: portfolio company founders

---

## 8. Big Tech (6/day) — FUNCTION-BROAD, ACTIVE-POSTER

**Rebalanced 2026-05-06** (decision: 2026-05-06-networking-agent-15-floor-bigtech-expansion). Was eng-execs-only; now function-broad to act as a wide-pool absorber alongside consulting. Folder name `big-tech-execs` preserved for continuity but contents are no longer execs-only.

**Title scope (any function):**
- Engineering: VP/Senior Director Engineering, Distinguished Engineer, Staff Engineer (creator-leaning), Engineering Manager
- Product: Senior PM, Group PM, Principal PM, Director/VP Product
- Design: Senior/Staff/Principal Designer, Design Manager, Director/VP Design
- People: Technical Recruiter, Engineering Recruiter, Senior Recruiter, Head of Talent, People Operations, VP People
- GTM: VP Sales, Director Sales, VP Marketing, Head of Brand, Director Communications
- Finance/Strategy/Ops: Head of Strategy, Strategy & Operations, Business Operations, VP/Head of Finance
- AI-lab specific: Member of Technical Staff, Research Engineer, Developer Relations / DevRel

**Firms:** FAANG (Meta, Apple, Google/Alphabet incl. DeepMind/Waymo/YouTube, Amazon incl. AWS, Netflix), Microsoft (incl. GitHub, LinkedIn), plus the new wider tier: Nvidia, Stripe, OpenAI, Anthropic, Databricks, Snowflake, Coinbase, Airbnb, Uber, Shopify, Notion, Figma, Linear, Vercel, Salesforce, ServiceNow, Atlassian, Tesla, Block.

**Required gate (replaces the old seniority filter):**
- **Posted on LinkedIn within the last 30 days.** This is what makes the function-broad scope safe. A "VP Marketing at Stripe" who hasn't posted in 6 months drops at qualify; a "Sr Engineering Manager at Vercel" who posts weekly ranks high.

**Excluded:**
- Anyone outside the listed firms
- Recently joined (<6 months at current title) — wait until they settle
- Anyone failing the active-poster gate (regardless of seniority)
- Anyone whose recent posts are exclusively job-pitch / hiring spam without genuine commentary

---

## Scoring (applied at 03-qualify stage)

Each candidate gets a score; only top-N per bucket move forward.

| Signal | Weight |
|--------|-------:|
| Concrete public anchor (recent post, deal, panel, paper, podcast, talk) | +3 |
| Mutual connections (per mutual, capped) | +1 each, max +3 |
| Role specificity match to bucket | +2 |
| Public writing or speaking history | +2 |
| Recent activity within 30 days | +1 |
| **Red flags** | |
| Profile looks dormant | -2 |
| Generic bio / no specifics to anchor on | -2 |
| Recently job-hunting or in transition (avoid burdening) | -1 |

Minimum score to enter the daily 20: **5**. Below that, the lead is parked in `02-discovery/` with a note for re-evaluation later.
