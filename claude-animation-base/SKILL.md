---
name: claude-animation-base
description: 'Hand-painted cartoon animation from code: a p5.js + p5.brush starter kit with a ready character (Clawd), 31 acted emotions, and a model-facing animation guide. Use when the user wants a hand-drawn, painted-look cartoon short or character animation rather than stick figures or 3D. Upstream: https://github.com/JohnHeibel/ClaudeAnimationBase (MIT), installed locally at ~/workspace/tools/claude-animation-base. Status: banked 21 Nov 2026 on the user''s order, UNTESTED in a real production here; verify the render pipeline end to end before promising a deliverable.'
---

# Claude Animation Base — hand-painted cartoons from code

A starter kit for animating hand-painted cartoons: p5.js with the
p5.brush engine, a ready-made character, 31 acted emotions, and an
ANIMATION_GUIDE.md written for the model driving it.

## Where things live

- Local checkout: `~/workspace/tools/claude-animation-base`
  (upstream: github.com/JohnHeibel/ClaudeAnimationBase, MIT).
- Read first, in the checkout: `README.md`, then `ANIMATION_GUIDE.md`.
  The guide is the operating manual; follow it over this wrapper.
- Entry points in the checkout: `studio.html` (interactive studio),
  `render.mjs` (headless render), `src/` (scenes and character code).

## How to work

1. Copy the checkout to the project's own folder before editing;
   never build a deliverable inside the tools checkout.
2. Direct the scene with the `motion-design` skill first (timing,
   easing, emotion-to-motion), then write the scene code.
3. Render with the checkout's own pipeline; verify the output frames
   personally before delivering (house artefact-verification rule).
4. Mix and finish audio with the house `ffmpeg-skill` pipeline.

## Fit and limits

- Choose this over `stick-figure-video` when the user wants a painted,
  hand-drawn look or an expressive recurring character. Choose
  `stick-figure-video` for fast stick-figure story shorts (that
  pipeline is proven here; this one is not yet).
- UNTESTED here as of banking (21 Nov 2026): the first real job must
  budget time to prove install, render, and export before any
  deadline is promised to the user.
