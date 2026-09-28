---
title: Image / graph generation for Slot 2 (and other visual posts)
updated: 2026-05-02
---

# Image generation

Slot 2 (insight / critique) requires a visual on most posts. Two paths depending on what kind of visual.

## Path 1 — Charts / graphs / comparison tables (no external API)

For data visualizations — pricing comparisons, feature matrices, member-flow diagrams, growth curves, etc. — the agent generates HTML + Chart.js (or pure SVG) and screenshots it via Playwright MCP.

**Pipeline:**

1. `/twitter-draft` flags slot 2 as `needs_chart: true` with a `chart_spec:` block (data + type)
2. `/twitter-screenshot` writes a temp HTML file at `twitter-agent/screenshots/<date>/_chart-source-<slot>.html` rendering the chart
3. Navigates Playwright MCP to `file://` URL via `mcp__playwright__browser_navigate`, screenshots the chart region (specific viewport size for Twitter — 1200x675 for landscape, or 1080x1080 for square)
4. Saves PNG to `twitter-agent/screenshots/<date>/slot-2-<slug>.png`

**Chart libraries available offline (no CDN, no API key):**
- Chart.js (already in `Arcadia/node_modules/`)
- D3 (if needed for custom data viz)
- Pure SVG with hand-drawn paths for simple comparison diagrams

**Chart styling rules:**
- Match Arcadia palette where it makes sense (oxblood / wax-red / gilt / verdigris / vellum). Reference: `Arcadia/design/kit/colors_and_type.css`.
- No legend chart-junk. Single-purpose visual that the tweet's text labels.
- Title in the chart only if it's not redundant with the tweet's opening line.
- Mobile-first sizing — Twitter feed renders the image at thumbnail size first; the visual must read at 600px wide.

## Path 2 — Illustrations / scenes / non-data images (Gemini API)

For non-data visuals — a stylized illustration of "the doorway opening," an isometric scene of "the four-stall market," a metaphor image — the agent calls Gemini's image generation API.

**Gating:** Gemini API key must be configured before this path is usable. Until then, fall back to:
- Hand-curated SVG assets in `Arcadia/design/kit/assets/` (lantern, medallion, wax-seal, ornaments, logo-arcadia, vellum-texture, oak-texture)
- Existing screenshot-able pages from `Arcadia/design/kit/ui_kits/` (tavern, tent, academy, dashboard, market)

**Gemini API config (when ready):**

```yaml
provider: google-gemini
model: gemini-2.5-image       # or whatever the current image-gen model is
api_key_env: GEMINI_API_KEY   # operator drops key in OS-level .env, agent reads from env, never written to disk in this folder
api_endpoint: https://generativelanguage.googleapis.com/v1/models/{model}:generateContent
output_format: png
default_size: 1200x675        # Twitter landscape
```

**Prompt conventions for Gemini calls:**

Every image prompt must include:
- The specific scene / metaphor (concrete, not abstract)
- The Arcadia visual style ("medieval scriptorium aesthetic, parchment textures, wax-seal motifs, oxblood + gilt + vellum palette")
- The format requirement ("flat illustration, no text, no logos, no watermarks")
- Aspect ratio matching the slot's canvas

**Example prompts:**

```
"A stylized isometric illustration of four wooden market stalls under canvas awnings, medieval-fair feel, parchment-toned palette with oxblood and gilt accents. No text. No logos. Landscape 1200x675."

"A hand-drawn diagram showing four community platforms (boxed labels: Skool, Circle, Discord, Notion) connected to a single creator silhouette by tangled lines, then a single clean line from one box (Arcadia) to the same creator. Minimalist sketch style, vellum background, oxblood line weight."
```

**Cost / volume:**
- Gemini image gen ≈ $0.03–0.04/image (as of 2026, verify current)
- Slot 2 runs once per weekday → ~22 images/month → ~$0.70/month at full volume
- Negligible cost; not a budget concern

## Path 3 — Existing Arcadia design assets (free, always available)

When the post is about a specific UI element or world-fragment that already exists in `Arcadia/design/kit/`, prefer screenshotting the actual asset over generating something new.

**Quick reference:**

| Asset | Path | Best for |
|---|---|---|
| Logo | `Arcadia/design/kit/assets/logo-arcadia.svg` | Brand reveal, hero |
| Wax seal | `Arcadia/design/kit/assets/wax-seal.svg` | "Seal it" submit moments |
| Medallion | `Arcadia/design/kit/assets/medallion.svg` | Achievements, level badges |
| Lantern | `Arcadia/design/kit/assets/lantern.svg` | Ambient / atmospheric posts |
| Inkwell + quill | `Arcadia/design/kit/assets/inkwell-quill.svg` | Writing / posting / scribe content |
| Ornaments | `Arcadia/design/kit/assets/ornaments.svg` | Dividers, decorative breaks |
| Vellum texture | `Arcadia/design/kit/assets/texture-vellum.svg` | Backgrounds |
| Oak texture | `Arcadia/design/kit/assets/texture-oak.svg` | Surface backgrounds |

UI kits (full HTML pages — best for screenshots showing real UI):

| Kit | Path |
|---|---|
| Tavern | `Arcadia/design/kit/ui_kits/tavern/index.html` |
| Tent | `Arcadia/design/kit/ui_kits/tent/index.html` |
| Academy | `Arcadia/design/kit/ui_kits/academy/index.html` |
| Dashboard | `Arcadia/design/kit/ui_kits/dashboard/index.html` |
| Market | `Arcadia/design/kit/ui_kits/market/index.html` |

Preview pages (for individual UI elements):

```
Arcadia/design/kit/preview/01-colors-primary.html
Arcadia/design/kit/preview/02-colors-paper.html
Arcadia/design/kit/preview/03-colors-semantic.html
Arcadia/design/kit/preview/04-type-display.html
Arcadia/design/kit/preview/05-type-caps.html
Arcadia/design/kit/preview/06-type-body.html
Arcadia/design/kit/preview/09-spacing.html
Arcadia/design/kit/preview/11-elevation.html
Arcadia/design/kit/preview/12-buttons.html
Arcadia/design/kit/preview/15-medallions.html
Arcadia/design/kit/preview/16-hardware.html
Arcadia/design/kit/preview/17-drop-caps.html
Arcadia/design/kit/preview/18-logo.html
Arcadia/design/kit/preview/19-ornaments.html
Arcadia/design/kit/preview/20-divider.html
```

## Selection logic (which path?)

```
if slot_2 is a chart / data viz / comparison:
    → Path 1 (Chart.js HTML + screenshot)
elif slot_2 is a UI reveal / world-fragment / specific Arcadia element:
    → Path 3 (screenshot existing asset / preview page)
elif slot_2 is a metaphor / scene / illustration:
    → Path 2 (Gemini API) — fall back to Path 3 if key not configured
else:
    → text-only is acceptable on slot 2 if a strong visual genuinely doesn't exist
```

Don't generate filler images. A weak image is worse than no image.
