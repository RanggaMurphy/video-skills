---
name: remotion
description: 'Create videos programmatically with Remotion (React components rendered to MP4): title cards, product promos, captioned templates, data-driven and batch-variant videos, map animations. Use when the user wants a video GENERATED from code, text, or data — as opposed to editing existing footage, which is ffmpeg-skill. Needs Node 20+, ffmpeg, and a headless Chromium.'
---

# Remotion — programmatic video

Remotion renders React components frame-by-frame in a headless browser
and encodes the result with ffmpeg. The video is code: change a prop,
re-render, get a new video. That makes it the right tool for templated
and data-driven output — Shopee product promos with per-product props,
captioned shorts, animated title cards, route/map explainers, and
batch variants of one design. For cutting, joining, reframing, or
fixing footage that already exists, use `ffmpeg-skill` instead; the
two skills are complements, not substitutes.

## Environment on this VM (verified live 2026-11-15, Round 7 vet)

- Node v24.22.1, npm 10.9.4 — fine (Remotion 4.x wants Node 18+;
  20+ recommended).
- ffmpeg 8.1.2 at `/usr/bin/ffmpeg` — fine.
- Headless browser: use Remotion's own Chrome Headless Shell — it
  downloads into the project's `node_modules` on first render and
  works (smoke-verified 2026-11-15). Do NOT point Remotion at
  `/opt/meta-chromium/chrome` (the Muse browser build): it is
  policy-locked and refuses to start under Remotion ("Hatch WebGL
  domain policy is required for browser startup").
- VM swaps wipe global installs: re-verify `node`, `ffmpeg`, and the
  chrome path before promising a render. Project `node_modules` are
  per-project and survive in the workspace.

## Workflow

1. **Scaffold** a throwaway or project directory (official packages
   only):
   `npx create-video@latest --yes --blank --no-tailwind <dir>`
   (add `--tailwind` if the design needs it). `npm i` inside if the
   scaffolder's install step errored.
2. **Write the composition** in React: a `<Composition>` with
   `durationInFrames`, `fps`, `width`, `height`; animate with
   `useCurrentFrame()` + `interpolate()`/`spring()` — never CSS
   transitions or timers, they do not render deterministically.
   Parameterise content with input props (`--props='{...}'` or a
   JSON file) so one composition serves many products/videos.
3. **Preview a frame before a full render:**
   `npx remotion still <comp-id> out/frame.png --frame=30`
4. **Render:** `npx remotion render <comp-id> out/video.mp4`
   For 9:16 social output set the composition to 1080×1920.
5. **Verify the output** (effective results, not exit codes):
   `ffprobe` the MP4 for duration/dimensions/codec and check the
   file size is sane before reporting success.

Captions: generate or import SRT, render them as part of the
composition (word-by-word highlight styles live in the upstream
`remotion-captions` reference). Maps: static-map and animated-route
techniques live in the upstream `remotion-maps` reference; the Cesium
3D flyover and Mapbox/MapTiler techniques need the **user's own** API
keys passed via environment variables (`REMOTION_MAPBOX_TOKEN`,
`REMOTION_MAPTILER_KEY`, `REMOTION_GOOGLE_MAPS_API_KEY`) — never
hardcode a key into a composition and never use a third party's key.

## Reference material (vetted clone, read-only)

The full upstream skill set — 13 skills: best-practices (bundle),
create, markup, render, captions, maps, interactivity, studio, docs,
multimedia, saas, upgrade, license — was statically audited in
Round 7 and is kept as reference at:

`~/workspace/skill-vet-round7/remotion-skills/skills/`

Read the relevant upstream `SKILL.md` / `REFERENCE.md` there when a
job needs depth (markup patterns, timing, effects, transitions,
render options). Official docs: https://www.remotion.dev/docs/ai/skills
and appending `.md` to any remotion.dev docs URL returns its Markdown
source.

## Cautions

- **Remotion's own license is not MIT.** The framework is free for
  individuals and companies of up to 3 people; larger companies and
  some automation-for-others uses need a paid license
  (https://www.remotion.dev/docs/license). At Rangga's current scale
  (individual creator) rendering is free — recheck before any
  commercial/team scale-up. The skills repo itself ships **no LICENSE
  file**, which is why this skill is house prose over a reference
  clone rather than an as-is install (ADOPTIONS.md Round 7).
- **No self-update.** The upstream `remotion-upgrade` skill prescribes
  `npx skills update … --yes`; that route is NOT adopted here. Skill
  updates go through a fresh vet round, like every other adoption.
  Upgrading the Remotion *packages inside a project* (`npx remotion
  upgrade`) is ordinary project work and is fine.
- Renders are CPU-heavy on this VM (1.5 shared CPUs): keep smoke
  renders short, prefer stills for iteration, and do not promise
  render times.
