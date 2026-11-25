---
name: chase-animate
description: 'Procedural canvas animation in any style (Chase AI''s Animate skill for Claude Code): short single-file canvas videos, drawn and scored entirely in code, with story, look and storyboard approval gates before building. Seven built-in styles (cut paper, crosshatch ink, riso, sketchbook, math, pixel, isometric) plus new looks matched from the user''s own references. Use when the user wants a code-drawn animated short or explainer in a distinct graphic style, or a style matched from reference images. Upstream: https://github.com/cth9191/animate (MIT), installed locally at ~/workspace/tools/animate. Status: banked 21 Nov 2026 on the user''s order, UNTESTED here; Playwright/Chromium availability on this VM is unverified, so prove one demo build before promising output.'
---

# Animate — procedural animation in any style (Chase AI / cth9191)

A Claude Code skill that makes short animated videos entirely in code:
one HTML canvas, drawn and scored procedurally, deterministic frame by
frame, rendered to MP4 with a headless browser and ffmpeg. Explainers,
histories and little stories in a chosen graphic style.

## Where things live

- Local checkout: `~/workspace/tools/animate`
  (upstream: github.com/cth9191/animate, MIT).
- The skill itself lives in the checkout at
  `plugins/animate/skills/animate/` — read its `SKILL.md`, `craft.md`,
  `grammar/` and `intake.md` there before use; they are the operating
  manual and override this wrapper.
- `plugins/animate/skills/animate/styles/` holds the style plug-ins
  (each with STYLE.md rules, a kit.js, a sample and a demo),
  `kit/` the shared engine (seeded randomness, cameras, shape-morph
  renderer, storyboard, synth), `tools/` the build/test/export/review
  scripts, and `examples/history-of-ai/` a complete 60 s demo piece.

## How it works

Approval gates come before any expensive build:

0. Intake: a few questions (subject, formats, voice, look, hero,
   music, product) and the style gallery.
1. Story check: the picked format plus a numbered beat table, facts
   web-checked. User approves or changes beats.
2. Look check: 2-4 full-size style frames (for a new look, side-by-side
   against the user's references). Thumbs up per frame.
3. Storyboard: every beat as a key frame with sound and transitions.
   Thumbs up/down per panel.
4. Build: animate the approved panels, render, review.
5. Delivery with measured checks: cuts on the beat grid, loudness arc,
   hero anchoring, narration pace.

Styles are plug-ins: grammar, timing, sound, renderer and tools stay
constant; a style supplies the drawing kit. Built in: cut paper,
crosshatch ink, riso print, sketchbook, math (manim-style), pixel,
isometric. An eighth option matches a NEW look from user references:
measure palette, line weight, texture, motion and cut rhythm, draw
comparison frames, get approval, save as `styles/<name>/` for reuse.

Also baked in: a story grammar of 8 short-form formats; voice-over
with word timing measured locally via faster-whisper (ElevenLabs
connector or the user's own recording); the user's own music
beat-mapped so cuts land on the song; real product screenshots
animated inside the style; one piece laid out natively for 9:16, 1:1,
4:5 and 16:9; closed-form spring motion and optional motion blur.

## Requirements and blockers

- Node 18+ (this VM: v24, OK) and ffmpeg (OK).
- Playwright with Chromium: required for rendering; **not verified
  installed on this VM**. Installing it is a sizable download and a
  separate decision, not part of this banking pass.
- Voice-over extras (optional): Python with faster-whisper for word
  timing; ElevenLabs connector only if the user wants that voice.

## Fit and limits

- UNTESTED here as of banking (21 Nov 2026). To test: install
  Playwright + Chromium, build the shipped example
  (`examples/history-of-ai`) with the checkout's own tools, export one
  format, and verify frames and loudness personally before offering
  it for a real job.
- Choose this for a graphic, code-drawn look (paper, ink, riso,
  pixel) or when a client style must be matched from references and
  reused. It does not do painted/illustrated character work; for the
  channel's locked flat-face painted style the house pipeline stays
  the default, and for hand-painted cartoons see
  `claude-animation-base`.
