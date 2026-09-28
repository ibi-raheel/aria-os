# Categories — what each bucket covers

The 8 buckets news-agent tracks daily. These mirror networking-agent's category split exactly so briefings drop straight into networking-agent's per-person send loop without a translation layer.

For each bucket: **what counts**, **what doesn't**, **what to flag specially** (often regulatory/legal items relevant to that audience).

---

## 1. consulting

**Counts:**
- Hiring/promotion announcements at McKinsey, Bain, BCG, Deloitte S&O, Strategy&, PwC Strategy
- Partner/Principal-authored research, podcasts, panels, op-eds
- Firm-level news: new practice areas, geographic expansion, leadership changes
- Major client engagement disclosures (when public)
- Industry pieces these firms publish (HBR partnerships, FT consulting beat)

**Doesn't count:**
- Generic "consulting tips" content from non-firm consultants
- Lower-tier firms unless they hired from MBB

**Law/regulation flags (folded into this bucket):**
- FTC actions touching consulting (e.g., non-compete rulings affecting firm hiring)
- DOJ investigations into MBB clients (when consulting work is mentioned)
- Federal procurement rule changes (affects gov-consulting practices)

---

## 2. real-estate

**Counts:**
- REIT execs (CEO/CFO/COO + division presidents): hires, departures, M&A, earnings beats/misses
- CRE deals over $50M (acquisitions, dispositions, refis)
- Tenant-rep brokers at CBRE / JLL / Cushman / Newmark: SVP+ activity
- Real-estate attorneys: published thought-leadership, panel appearances
- Family-office heads + RE PE partners
- Sub-segment by current week's rotation: office/mixed-use, retail, industrial, multifamily, hospitality

**Law/regulation flags:**
- Federal Register: SEC real-estate adviser rules, EPA/OSHA building rules, IRS opportunity-zone changes
- Congress.gov: tax-law changes affecting depreciation, 1031 exchanges, REIT taxation
- State-level zoning, lease, or rent-control changes (limit to top metros: NYC, LA, SF/Bay, Boston, Miami, Austin, Seattle, DC)
- Court opinions on commercial-lease disputes (CourtListener)

**Doesn't count:**
- Residential mortgage news (off-target — outreach targets are commercial)
- Single-family flipping content
- Generic "real estate market" forecasts without named operators

---

## 3. founders

**Counts:**
- Funding rounds (seed → Series B) with named founder + named investor
- Product launches by named founders in the same vertical orbit as Arcadia (community, creator tools, vertical SaaS)
- Founder-authored Substack/Twitter/LinkedIn posts that go beyond "growth hack" content
- Hiring rounds at peer-level startups (CTO/Head-of-Eng moves)

**Law/regulation flags:**
- SEC startup rules (Reg CF, Reg A+, accredited-investor changes)
- FTC startup-related rulings
- State employment law changes affecting equity comp / non-competes
- AI Act / state AI regulation (impacts a lot of founders)

**Doesn't count:**
- Series C+ unless founder is peer/network-relevant
- Public-company founders (those go in big-tech)
- Generic "startup advice" content

---

## 4. investors-general

**Counts:**
- VC/angel announcements: new funds, fund closes, GP departures from major firms (sub-$2B AUM, since Tier-1 VCs are their own bucket)
- Solo capital + family-office moves
- Scout-program changes
- Strictly VC, Term Sheet (Fortune), Axios Pro Rata content
- Deal news where investor is the focus (not the founder)

**Law/regulation flags:**
- SEC Form D filings (newly-formed funds): pull daily from EDGAR
- SEC marketing rule + adviser rule updates
- Congress.gov: changes to carried-interest taxation, Reg D changes
- ERISA / Dept of Labor rules affecting LP investing
- Antitrust action against major LPs (pension funds, endowments)

**Doesn't count:**
- Tier-1 VCs (own bucket)
- a16z (own bucket)
- YC (own bucket)
- Private-equity buyouts >$100M (different audience)

---

## 5. yc

**Counts:**
- Y Combinator partner news: hires, departures, podcast/panel appearances
- Batch announcements (W26, S26 — when applicable)
- Demo Day coverage
- Notable alumni events relevant to current partners
- ycombinator.com/blog new posts, partner-authored Substacks
- Garry Tan public statements

**Doesn't count:**
- Individual YC company news (those are founders bucket)
- YC company funding rounds (founders bucket)

---

## 6. a16z

**Counts:**
- a16z GP/Partner news: hires, role changes, thought-leadership
- a16z portfolio company news (when partner is named)
- a16z.com / future.com new posts
- Partner Substacks (Marc Andreessen's blog, Chris Dixon's, Ben Horowitz's, etc.)
- Podcast episodes (a16z podcast)

**Doesn't count:**
- a16z portfolio company news without partner involvement (founders bucket)

---

## 7. tier1-vcs

**Counts:**
- Sequoia Capital: investments, partner hires, "Perspectives" blog posts, podcast (Crucible)
- Greylock: investments, partner content
- Benchmark: investments, partner content
- Founders Fund: investments, partner content (Peter Thiel public statements)
- Index Ventures: investments, partner content
- Accel: investments, partner content

**Doesn't count:**
- Their portfolio companies' news without partner involvement (founders bucket)

**Law/regulation flags:**
- Antitrust action mentioning these firms or their portfolio companies
- SEC scrutiny of late-stage rounds these firms led

---

## 8. big-tech

**Counts ONLY senior moves and substantive items:**
- VP+, Distinguished Engineer, GM, Sr Director at Meta, Apple, Google/Alphabet, Amazon, Microsoft, Netflix
- New hires, departures, internal moves at this level (use sources like The Information, CNBC, Reuters, Bloomberg)
- Senior-authored papers, talks at major conferences (NeurIPS, RSA, Strange Loop, Code Conference)
- Promotion announcements
- Major product/platform launches under named senior leadership

**Law/regulation flags:**
- DOJ/FTC antitrust actions against big tech (these often touch named execs)
- EU DMA/DSA actions
- Congressional hearings featuring named execs
- AI Executive Orders, AI Act implementation
- State data-privacy / kids' online safety laws (CA AB 2273, etc.)
- Ongoing antitrust cases (Google search trial, Apple App Store, etc.)

**Doesn't count:**
- IC engineers
- First-line managers
- Generic "Big Tech earnings preview" content unless named exec is quoted

---

## How to handle items that fit multiple buckets

If a news item legitimately belongs to 2+ buckets (e.g., "a16z partner publishes thought-leadership on real-estate tech"), include it in the most-specific bucket only and add a one-line cross-reference note in the others:

```
> See also: this item appears in [[news-agent/briefings/2026-04-29/a16z]]
```

The agent should NOT duplicate the full item across files. Single source of truth, references in others.

---

## Bucket sizing guidance for the operator

Realistic items-per-day per category, after categorization filters:

| Category | Typical items/day | Edge cases |
|---|---|---|
| consulting | 2–5 | Can be 0 some days; 10+ during major firm news cycles |
| real-estate | 3–8 | Higher on Fed announcement days |
| founders | 5–15 | Higher on Tuesdays (most rounds announced) |
| investors-general | 3–8 | Higher around fund-formation dates (quarter-end) |
| yc | 0–3 | Spikes during Demo Day weeks (twice per year) |
| a16z | 1–5 | Steady, occasional thought-leadership bursts |
| tier1-vcs | 1–5 | Sequoia + Benchmark dominate volume |
| big-tech | 3–10 | Depends on regulatory cycle |

If a bucket has 20+ items on a given day, the categorize stage should rank by signal score (recency × source-authority × specificity) and keep the top 10–15.
