---
name: motion-prompt
description: 'A numbered library of 240 named motions (motion graphics, camera moves, UI, web effects, photo looks, art styles, diagrams), each with a moving sample, a timing/easing spec and dependency-free Canvas 2D code, made to be picked by number and ported into a project with its motion numbers intact. Use when a scene needs a specific named move (a camera push-in, a title entrance, an easing), when our own animation reads stiff and needs a proven motion reference, or when the user wants to browse or name motions. Upstream: https://github.com/showheyohtaki/motion-prompt (MIT), installed locally at ~/workspace/tools/motion-prompt. Status: banked 21 Nov 2026 on the user''s order, UNTESTED here; no element has been ported into a house production yet.'
---

# Motion Prompt — a numbered library of motions (showheyohtaki)

A "common language" for asking an AI for movement: 240 named elements
in 10 packs of 24 (`motion`, `camera`, `ui`, `lp`, `photo`, `motion2`,
`lp2`, `camera2`, `artstyle`, `diagram`). Theo's article described 120
samples; the repo has since doubled. Every element has a three-digit
ID (`#012`), a name (English, Japanese, Spanish, Chinese), a one-line
meaning, a spec of its timings and easing, a live demo, and
dependency-free Canvas 2D code written as a pure function of time.

## Where things live

- Local checkout: `~/workspace/tools/motion-prompt`
  (upstream: github.com/showheyohtaki/motion-prompt, MIT).
- The repo's own skill is at `skills/motion-prompt/` in the checkout;
  read its `SKILL.md` and `references/porting.md` before porting
  anything — they override this wrapper.
- The catalogue data also ships in the clone under `api/v1/`
  (catalog, per-element spec+code files, pack kits), so the CLI can
  read everything locally with
  `MOTION_PROMPT_BASE=~/workspace/tools/motion-prompt/api/v1` and no
  network.
- Pack name lists (number, name, meaning, example ask) are readable
  directly in `packs/<pack>/README.md` inside the checkout.

## How samples are picked

Four routes, per the upstream skill:

1. **Gallery pick (the main route upstream).** The CLI
   (`node skills/motion-prompt/scripts/motion-prompt.mjs pick`,
   optionally `--pack camera,camera2`) opens the web gallery; the
   user ticks samples, adds an optional note, presses "Send to AI",
   and the picks (numbers, in order, plus the note) return to the
   agent. On this VM there is no browser hand-off to the user's
   phone, so use this only if the user is at a browser; otherwise
   route 2 or 4.
2. **By number.** The user (or we) names IDs directly: `get <id...>`
   prints each element's spec followed by its code (max 8 per call);
   `kit <pack>` prints the shared constants/helpers a pack's elements
   need. Numbers are final: never substitute a different element.
3. **Pasted picks.** The gallery's "Copy picks" text (or a
   `?pick=012,045` link) pasted into chat counts as the same picks.
4. **Search.** `search <words...>` ranks elements against a few words
   describing one scene's motion (English or Japanese). Use it when
   nobody can browse the gallery and we are choosing.

Fetch narrowly: `search`/`list` to find candidates, `get` only for
the few that will actually be ported.

## How a picked motion is applied

Port the element into the project's own stack (Canvas, Remotion,
CSS/SVG, or our PIL/ffmpeg compositor) following
`references/porting.md`. The motion's numbers are the product: keep
durations, delays, easing curves, overshoot, distances and angles
exactly as specced; replace only the content (words, images) and the
palette. For a swap ("replace this title with #005"), keep the scene's
length, content and hand-overs and replace only the motion. Every
element and kit file starts with a `// Motion Prompt #ID · MIT
License` line: carry that attribution line into the file where the
ported code ends up. For video-generation models, do not pass code:
`prompt <id>` gives a prose prompt built from the name and spec.

For our house pipeline specifically: we do not run Canvas, so what
transfers is the spec (the timing/easing/path numbers) into our
compositor's motion code, and the demo as the visual reference for
what the move should read as.

## Why it is banked (relevance to current work)

Rangga's standing note on the flat-style Story 7 build is that the
walking still reads less smooth than he wants ("kurang alus"). This
library is a catalogue of proven motion recipes, including the
`camera`/`camera2` packs (push-ins, pull-backs, hand-overs like our
segment 1 shot 4 pull-back) and the `motion` packs (entrances, easing
vocabulary). It is reference material for motion polish across all
house animation work, not a renderer.

## Fit and limits

- UNTESTED here as of banking (21 Nov 2026). To test: pick two or
  three elements (for example one camera move and one entrance),
  port one into a house shot with the spec numbers intact, render
  both versions, and compare frame strips before adopting it as a
  standard reference.
- The `ui`, `lp`, `photo`, `artstyle` and `diagram` packs name web,
  photo, image-style and slide things rather than video motion; use
  them by name and spec in prompts, not as code.
- If a number does not exist in the catalogue, say so; never invent
  an element from its name alone (upstream rule).
