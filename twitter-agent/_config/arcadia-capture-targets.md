---
title: Arcadia capture targets — route catalog for the screenshot stage
updated: 2026-05-10
production_url: https://arcadia-web-swart.vercel.app
notes: |
  This is the source of truth for "where to point Playwright MCP when slot 1 needs a visual."
  The draft stage proposes a `capture_intent` keyword in the slot frontmatter; the
  screenshot stage looks it up here, executes the recipe, saves PNG, attaches to slot.
---

# Arcadia capture targets

The agent has three capture surfaces in Arcadia:

1. **Direct dashboard routes** — fast, full-bleed captures of studio screens
2. **Modal-tab captures** — for tabs without direct routes (members / billing / settings)
3. **In-world captures** — pixel-art top-down view; character can be walked to specific areas

## Hard preconditions for every capture (run BEFORE any screenshot)

These two preconditions are mandatory. If either cannot be confirmed, abort the capture and ship the slot text-only.

### 1. Browser viewport must be sized correctly

Playwright MCP renders in a headless Chromium viewport. No OS window chrome to worry about.

**How to apply:**
- Call `mcp__playwright__browser_resize` with `width=1280, height=720`.
- Playwright screenshots capture only the viewport content (no desktop bleed).

### 2. Arcadia "Simulation" toggle must be ON

The dashboard header has a `SIMULATION · OFF/ON` toggle. With simulation OFF, every metric renders as `$0 / 0 sales / 0% / $0 MRR` — the studio looks empty and the post lands flat. With simulation ON, dashboards render demo numbers that look like a real, used product.

**How to apply:**
- After loading any `/dashboard*` route, run `mcp__playwright__browser_snapshot` and check for `simulation · on` (case-insensitive).
- If the toggle reads `simulation · off`, click the toggle via `mcp__playwright__browser_click`.
- After clicking, wait 1.5s (`mcp__playwright__browser_wait_for`) and re-verify it now reads `simulation · on` AND that the metric tiles have populated with non-zero numbers.
- If the toggle can't be flipped or the metrics don't populate, abort the capture for this slot and post text-only.

This precondition does NOT apply to in-world (`/world`) captures — the toggle has no effect on the Phaser scene. World captures are exempt.

### 3. Content-safety scan (post-capture, pre-attach)

After a clean capture, run `mcp__playwright__browser_snapshot` once more and grep visible text against a deny-list before the image attaches to any tweet. This is a separate gate from the two above, but it lives in the same recipe.

**Deny-list to scan against:**
- Slurs and profanity (operator maintains list separately; never inline here).
- Test-data signals: `Example`, `Smoke test`, `lorem`, `TODO`, `test-` handle prefix, two-letter or one-word course titles like `dd`, `aaa`, `xxx`.
- Anything starting with `[INTERNAL]`, `[STAGING]`, `[DRAFT]`.

If any match, the screenshot is **quarantined** to `twitter-agent/screenshots/<date>/_quarantine/<slug>.png` with a sidecar listing what tripped the gate. Slot 1 (the anchor) does NOT fall back to text-only — instead, the agent pulls from the evergreen Arcadia visual rotation (per marketing-brain.md Gate 3). Slot 1 always ships with an Arcadia image; only the specific captured frame gets quarantined. Operator gets a Slack ping in `#twitter-arcadia` flagging the quarantine reason so the test data can be cleaned and the fresh capture re-attempted next run.

Independent of the deny-list: the run summary in `#twitter-arcadia` includes the captured image inline, and the post step waits for operator thumbs-up before attaching. Manual visual approval is the backstop the deny-list can't replace.

---

## Capture formats — PNG vs GIF

Each entry in the catalog has a `capture_format` field:
- `png` (default) — single still image. Fast, small, the right choice for any frame where the meaning is in the layout/copy/numbers.
- `gif` — animated browser-action recording. **DEFERRED** — Playwright MCP has no built-in GIF recorder (Chrome MCP's `gif_creator` is retired). GIF intents fall back to their PNG equivalents for now.

**When to choose GIF.**
- The story requires motion (`/world` walks, the day-cycle sweep, character idle animations)
- The frame has more than one beat (scrolling past four course tiles in sequence > a static screenshot of all four at once)
- The atmosphere of Arcadia is the post's emotional anchor (ambient music + torch light + character sprite — lost in a still)

**When to stay on PNG.**
- The post is anchored on a specific number, headline, or copy line ("the kiln · publish what's finished")
- Twitter feed thumbnail at 600px wide will read fine without motion
- File size matters (PNGs are ~50-200KB; comparable GIFs run 1.5-4MB)

**Format limitations.**
- GIFs are GIF-only — no MP4. Twitter accepts GIFs natively but compresses them; quality 10 (default) is usually fine, drop to 8 for higher-motion clips.
- File-size cap: Twitter accepts media up to 15MB. Most 4-6 second Arcadia captures land 2-4MB.
- Browser tab only — anything outside Chrome (Finder, native apps) cannot be captured this way.

---

## GIF recipe — DEFERRED

GIF capture is deferred. Playwright MCP does not have a built-in GIF recorder equivalent to Chrome MCP's `gif_creator`. All GIF intents (`world-stroll`, `the-kiln-scroll`) fall back to their PNG equivalents until a GIF solution is implemented.

---

## Critical Phaser keyboard input note

Arcadia's `/world` view runs on Phaser. The canvas has `tabIndex: -1` and Phaser's keyboard manager listens at the `window` level. To move the character, dispatch synthetic `KeyboardEvent`s via `mcp__playwright__browser_evaluate`:

```javascript
window.dispatchEvent(new KeyboardEvent('keydown', {
  key: 'ArrowRight', code: 'ArrowRight', keyCode: 39, which: 39, bubbles: true
}));
await new Promise(r => setTimeout(r, 1000));
window.dispatchEvent(new KeyboardEvent('keyup', {
  key: 'ArrowRight', code: 'ArrowRight', keyCode: 39, which: 39, bubbles: true
}));
```

For diagonal movement: dispatch two keys at once (don't release the first before pressing the second). For longer walks: extend the keydown→keyup interval. Arrow keys + WASD both work via this dispatch path.

---

## Direct dashboard routes (full-bleed captures)

| `capture_intent` | `capture_format` | Route | What it shows | Brand-voice anchors visible | Best for posts about |
|---|---|---|---|---|---|
| `world-spawn` | `png` | `/world` | Top-down pixel-art, character at "The Square" portal | "ibi.raheel" + level shield · "The Square (1 wandering)" · ambient torch lighting | Build-in-public posts about the world / ambient music / atmosphere |
| `world-stroll` | `gif` | `/world` | 4-second character walk through The Square — captures motion + torchlight + ambient feel | Same as `world-spawn` but with character sprite animating | When the post's emotional beat is *atmosphere*, not a number |
| `studio-overview` | `png` | `/dashboard` | Keeper's studio greeting + 30d revenue / MRR / one-time / paying subscribers / return-on-spend | "good evening, ibi.raheel." · "five numbers kept on ledgers, one coin jar on the desk, an envelope of folk who haven't left, and the doings of the day in a margin" | Shipped a metric or simulator feature; "look at the dashboard" posts |
| `the-kiln` | `png` | `/dashboard/courses` | Courses dashboard ("the kiln") with course count, published, revenue 30d, recurring MRR, avg finish | "the kiln · publish what's finished, keep what's drying" · "ink a new course →" · "✦ resume the scribe" · "in the satchel" | Course-related posts, content publishing flow |
| `the-kiln-scroll` | `gif` | `/dashboard/courses` | Scroll from KPI tiles down through the four-tile published-courses grid | Same as `the-kiln`, but the scroll reveals the grid as an arc of motion | Posts about *publishing* as a verb, not metrics — when scroll = the beat |
| `the-stage` | `png` | `/dashboard/events` | Events dashboard ("the stage") with live now / upcoming 7d / scheduled / past timeline | "the stage · the weekly Q&A, the kickoff, the office hour" · "ink the calendar" · "+ new event" | Live-event posts, weekly Q&A spotlights |

---

## Modal-tab captures (tabs without direct routes)

These tabs (`members`, `billing`, `settings`) return 404 when accessed as direct URLs. They only exist as in-modal state. To capture, navigate to any working dashboard route, then click the tab button.

| `capture_intent` | Route load | Tab to click | What it shows |
|---|---|---|---|
| `members-roll` | `/dashboard` | `button[aria-label="Members"]` (or text "members") | TBD — captured manually first time |
| `billing-ledger` | `/dashboard` | `button[aria-label="Billing"]` (or text "billing") | TBD |
| `settings` | `/dashboard` | `button[aria-label="Settings"]` (or text "settings") | TBD (probably keep low-priority for posting) |

**Recipe for modal-tab capture:**

```
0a. PRECONDITION: Browser viewport sized to 1280x720 via mcp__playwright__browser_resize
0b. PRECONDITION: Simulation toggle ON (flip if currently OFF; verify metrics populate)
1. Navigate to /dashboard via mcp__playwright__browser_navigate
2. Wait 2s for studio to render (mcp__playwright__browser_wait_for)
3. Click tab button via mcp__playwright__browser_click
4. Wait 1.5s for tab content to animate in
5. Screenshot via mcp__playwright__browser_take_screenshot
6. POST-CAPTURE: content-safety scan (deny-list via mcp__playwright__browser_snapshot) — quarantine if any hit
7. Save to twitter-agent/screenshots/<date>/<slug>.png (or _quarantine/ if step 6 failed)
```

The first time the agent captures one of these, it should also record the brand-voice anchor strings visible on that tab and update this catalog (a one-time bootstrap; subsequent runs just use the catalog).

---

## In-world captures (Phaser, character-positioned)

The character spawns at "The Square" (the portal). To capture other in-world areas, walk the character there via JS keyboard dispatch, wait for the camera to settle, then screenshot.

| `capture_intent` | `capture_format` | Path from spawn | Brand-voice anchor visible | Best for posts about |
|---|---|---|---|---|
| `the-square-portal` | `png` | (no movement) | "The Square (1 wandering)" + glowing portal | World openings, daily anchors |
| `world-stroll` | `gif` | Walk character right (`d` × 4s) from spawn through The Square | Character animation + ambient torchlight + "wandering" counter | Atmosphere, daily anchors, Day-N posts where motion lands |
| `the-tavern` | `png` | TBD — walk N? walk W? | TBD | Community gathering, music, "hosts" |
| `the-market` | `png` | TBD | TBD — "four-stall market" referenced in earlier specs | Commerce, monetization, paying-tier sales |
| `the-academy` | `png` | TBD | TBD | Learning, courses ("the kiln" linked product surface) |
| `the-tent` | `png` | TBD | TBD | Onboarding / new-arrival framing |

**Recipe for in-world capture:**

```
0. PRECONDITION: Browser viewport sized to 1280x720 via mcp__playwright__browser_resize
   (Simulation toggle does NOT apply to /world — Phaser scene is independent)
1. Navigate to /world via mcp__playwright__browser_navigate
2. Wait 5s for game + assets + character to render (mcp__playwright__browser_wait_for)
3. Dispatch keyboard events to walk character to target via mcp__playwright__browser_evaluate
4. Wait 1.5s after final key release for camera + character idle settle
5. Screenshot via mcp__playwright__browser_take_screenshot
6. Save to twitter-agent/screenshots/<date>/<slug>.png
```

**Bootstrapping the path map.** The first time the agent (or operator manually) captures each in-world area, record:
- The exact key sequence + durations to reach the area from spawn
- A reference screenshot
- The visible brand-voice anchor strings

After bootstrapping, the catalog has tested paths. Subsequent runs just replay them.

---

## Mapping post topics → capture intents

This is the lookup the **draft stage** uses to pick a `capture_intent` for slot 1. Drafts that don't match any keyword ship text-only.

| Draft topic / signal | Best capture intent | Format | Fallback |
|---|---|---|---|
| "shipped a course/lesson/syllabus" | `the-kiln` | `png` | `studio-overview` |
| "publishing as a verb / building courses in motion" | `the-kiln-scroll` | `gif` | `the-kiln` |
| "set up an event / weekly Q&A / office hour" | `the-stage` | `png` | `studio-overview` |
| "ambient music / world atmosphere / day cycle / lonely-but-warm" | `world-stroll` | `gif` | `world-spawn` |
| "the world is a place, not a feed" | `world-stroll` | `gif` | (none — text-only) |
| "MRR / pricing / monetization" | `studio-overview` | `png` | `the-kiln` |
| "members / churn / retention" | `members-roll` (modal-tab) | `png` | `studio-overview` |
| "the four-stall market / commerce" | `the-market` (in-world) | `png` | `studio-overview` |
| "onboarding / new arrivals" | `the-tent` (in-world) | `png` | `world-spawn` |
| "loneliness problem / belonging" (the core belief) | `world-stroll` | `gif` | `world-spawn` (png if GIF unavailable) |
| (no match) | (text-only — slot 1 ships words alone, no image) | — | — |

If the operator updates the post-topic semantic map, both this section and the draft stage's prompt reference it.

---

## Output format

Each successful capture writes:

```
twitter-agent/screenshots/<date>/<slug>.png             # PNG captures
twitter-agent/screenshots/<date>/<slug>.gif             # GIF captures (motion intents)
twitter-agent/screenshots/<date>/<slug>.md              # metadata sidecar (same shape regardless of format)
```

Sidecar shape:

```yaml
---
slug: <slug>
capture_intent: <intent from catalog>
capture_format: png | gif
route: <URL the capture was taken from>
viewport: 1280x720      # or whatever was set
captured_at: <ISO timestamp>
duration_seconds: <only for gifs>
frame_count: <only for gifs — reported by gif export>
brand_voice_anchors_visible:
  - <copy text 1>
  - <copy text 2>
---
```

The slot 1 draft references the capture via `attached_visual: screenshots/<date>/<slug>.<ext>` and the post step uploads it to Twitter alongside the tweet text.

---

## Bootstrap status (as of 2026-05-06)

| Target | Status |
|---|---|
| `world-spawn` (png) | ✓ tested — character + portal visible, voice anchors confirmed |
| `world-stroll` (gif) | ⛔ DEFERRED — GIF pipeline not available in Playwright MCP. Falls back to `world-spawn` (png). |
| `studio-overview` (png) | ✓ tested — all 5 metric tiles + brand voice landed |
| `the-kiln` (png) | ✓ tested — courses dashboard + 4 published + voice landed (NOTE: live test data contains offensive course title; quarantine until operator cleans it) |
| `the-kiln-scroll` (gif) | ⛔ DEFERRED — GIF pipeline not available in Playwright MCP. Falls back to `the-kiln` (png). |
| `the-stage` (png) | ✓ tested — events timeline + "ink the calendar" voice landed |
| `members-roll` (png) | ⏳ pending — needs first capture via modal-tab click |
| `billing-ledger` (png) | ⏳ pending — same |
| `settings` (png) | ⏳ pending — same; low-priority for posting |
| `the-tavern` (png) | ⏳ pending — needs walk-path bootstrap |
| `the-market` (png) | ⏳ pending — same |
| `the-academy` (png) | ⏳ pending — same |
| `the-tent` (png) | ⏳ pending — same |

Bootstrap the in-world paths next time the operator + agent are paired with Playwright (operator can drive the character to each area, agent records the key sequences).

---

## Auth + dev-server gotchas

- **No auth challenge** observed on `/world` or `/dashboard/*` — all routes load with operator's persisted session.
- **Production URL only** for now. If a staging URL is added later, update `production_url` in the frontmatter.
- **Mobile viewport** — Twitter renders feed images at small thumbnails. Agent should screenshot at 1280×720 (Twitter landscape) and ensure key UI elements read at the 600px-wide thumbnail size.
