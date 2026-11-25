---
name: remotion-best-practices
description: 'Companion reference of Remotion API best practices that the house remotion skill does not cover: interpolate/easing discipline, TransitionSeries, sequencing, the captions pipeline, calculateMetadata, media embedding, render gotchas, map techniques, and how to look up current Remotion docs. Use ALONGSIDE the house remotion skill (which owns VM environment and workflow) whenever writing or debugging Remotion compositions. Adapted in-house from the official Remotion skills pack: https://github.com/remotion-dev/skills (no licence file in that repo; Remotion framework licensing itself is covered by the upstream remotion-license skill topic — free for individuals and small teams, paid licence for larger companies).'
---

# Remotion best practices — companion to the house `remotion` skill

The house `remotion` skill owns environment, scaffolding, and render
workflow on this VM. This companion carries the API-level rules from
Remotion's official agent-skills pack, digested in our own words. It
does not replace or overwrite the house skill.

## Looking up current docs (do this instead of guessing APIs)

- Any Remotion docs URL returns clean Markdown if you append `.md`
  (e.g. `https://www.remotion.dev/docs/sequence.md`). Fetch that
  instead of relying on memory for exact prop names.
- The official docs are also searchable through Remotion's Algolia
  index (a public search-only key ships in the upstream skill); a
  web search restricted to remotion.dev usually finds the same page.

## Timing and animation

- Drive all motion from `interpolate()` over an explicit frame range,
  or from `spring()` for physical settle. Customise with
  `Easing.bezier(...)` / `Easing.spring` rather than hand-rolled math.
- `interpolate()` does NOT clamp by default — values overshoot past
  the output range. Pass `extrapolateLeft/Right: 'clamp'` whenever
  overshoot would break layout or opacity.
- Keep animations Studio-editable: put the `interpolate()` call
  directly in the `style` prop and prefer individual CSS transform
  properties (translate/scale/rotate) over a combined `transform`
  string.
- Apply the house `motion-design` skill for choosing durations,
  easing families, and choreography — this file is about API shape,
  that one is about feel.

## Structure: compositions, sequencing, transitions

- Multi-scene videos: use `<TransitionSeries>` — a Transition
  (crossfade, slide, wipe) plays both scenes at once and shortens
  the timeline; an Overlay (e.g. a light leak at the cut) renders on
  top without shortening it. Children are absolutely positioned.
- Use `calculateMetadata` on a composition when its duration or
  dimensions depend on fetched data (media lengths, remote props) —
  never hard-code a duration that the data should decide.
- Connected compositions and per-composition timing props keep one
  render producing many variants; prefer props over duplicating
  components.

## Captions pipeline

Three stages, each with its own tooling in `@remotion/captions`:
1. **Transcribe** audio to the Remotion `Caption` JSON format (the
   upstream pack documents Whisper-based flows; on this VM the house
   `whisperx-word-timing` skill already produces word timings —
   convert its output to the Caption shape rather than adding a
   second transcription stack).
2. **Import SRT** when captions already exist as .srt — fetch the
   file (local `staticFile()` or a remote URL) and parse it into
   Caption objects.
3. **Display** with the captions element; group words into pages
   sized for the frame instead of rendering one word per frame by
   hand.

## Media handling

- Embedding existing video/audio: use Remotion's media components so
  playback stays frame-accurate; trim with start/end props rather
  than pre-cutting files when the cut is composition-level.
- When a standalone trimmed file IS needed (upload, external use),
  re-encode with ffmpeg — stream-copy trims can freeze the first
  frames. (House `ffmpeg-skill` owns the commands.)
- Metadata helpers exist for probing media in the browser context:
  video duration, audio duration, video dimensions — use them inside
  `calculateMetadata` instead of shelling out mid-render.
- Silence detection, audio visualisation, text measuring, and DOM
  measuring all have dedicated upstream guides; measure text with
  the provided utilities rather than estimating widths, or captions
  and titles will overflow unpredictably.
- Fonts: prefer local fonts for render reproducibility; Google Fonts
  via `@remotion/google-fonts` is fine but adds a network dependency
  at render time.

## Maps in Remotion

Upstream techniques exist for static maps, MapLibre/Mapbox/MapTiler
vector maps, and Cesium 3D flyovers. House rules still win:

- Never load map tile libraries from a CDN inside a Muse web
  artifact (they render blank in preview) — that ban is about
  artifacts; inside a Remotion project, bundled packages are fine.
- Map techniques need the user's own API keys (MapTiler/Mapbox/
  Google 3D Tiles). Render-stability is the known trap: tiles must
  be fully loaded before the frame is captured or the video flickers
  — upstream ships per-provider render-stability notes for this.
- The Cesium camera-path generator (a small local script that turns
  a GeoJSON centerline into a smoothed, continuously-curving flight
  path) is a good pattern to reuse: resample evenly, moving-average
  smooth, damp lateral deviation toward the chord. No network use.

## Rendering and delivery

- Transparent video (alpha) is supported — pick the codec/container
  for alpha deliberately instead of discovering at delivery time
  that the default dropped it.
- Remotion's framework has its own telemetry and licence-key
  mechanics for commercial renders (`licenseKey` on render calls;
  `"free-license"` if the user qualifies). This is upstream framework
  behaviour, documented openly — surface it, don't hide it, when a
  render is for a company.
- OpenTimeline export exists for handing a Remotion timeline to
  editors; the house `card-carousel-promo` edit-pack idea is the
  same spirit for template promos.

## SaaS / Studio / interactivity (awareness only)

- The upstream pack also covers Remotion Player embedding, rendering
  as a service (Lambda/server), and Studio interactivity (markup
  written so Studio can edit it: animations inline in style props,
  timeline structure kept visible). We rarely need these; consult
  the upstream repo if a project grows in that direction.
