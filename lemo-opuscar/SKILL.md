---
name: lemo-opuscar
description: 'A library of 99 film styles made entirely in code (Lemo-Opuscar by Lemomo): pick a style, bring a story, and the agent directs and produces a short narrated film in that style, with no video model. Use when the user wants a short film in a specific ready-made visual style (watercolor, blueprint, risograph, pixel RPG, news package and 93 more) or wants to save a style of their own. Upstream: https://github.com/lemomo-ai/lemo-opuscar (mixed licensing, see below), installed locally at ~/workspace/tools/lemo-opuscar. Status: banked 21 Nov 2026 on the user''s order, UNTESTED here; per-film renders are heavy (30-60 minutes on a normal machine per the source article) and this VM is far weaker, so treat it as documentation-only until a small test film has been proven.'
---

# Lemo-Opuscar — 99 film styles in code (Lemomo / lemomo-ai)

A toolbox of film styles made in code. Each style is a style prompt
(`styles/<slug>/STYLE.md`: look, colour, type, motion, camera grammar,
sound palette, pitfalls) plus a demo film made entirely in code. Pick
a style, bring your own story, and the agent writes a treatment,
directs and produces the film: voice, score, animation, mix, render.
Theo's article counted 66 styles; the library has since grown to 99
in 15 categories (documentary, painting, sketch, crafts, print,
graphic/type, diagrams, cartoons, games, film/tape, interfaces,
light, 3D miniature, instruments, data/maps).

## Where things live

- Local checkout: `~/workspace/tools/lemo-opuscar` (253 MB; `styles/`
  alone is ~104 MB of style definitions and demo assets)
  (upstream: github.com/lemomo-ai/lemo-opuscar).
- Operating manuals in the checkout, in this order: `AGENTS.md`
  (workflow and house rules), `DIRECTOR.md` (story, sound, rhythm,
  camera, checks, delivery), `TECHNIQUE.md` (install, voice, music,
  mix), `core/README.md` (tool commands). Follow them over this
  wrapper.
- The installable skill source is `plugin/skills/lemo-opuscar/` in
  the checkout (upstream install is via the Claude plugin
  marketplace `lemolab`). On first real use the skill downloads its
  library to `~/lemo-opuscar`; that first download is the >1 GB one
  the article warns about. It has NOT been run here.
- House rules from upstream AGENTS.md that bind any use: never build
  a film inside `styles/` (copy what you need into the film's project
  folder); never edit `core/` or `styles/` for a user's film; write
  your own TREATMENT.md before opening a style's demo, and use the
  demo only to learn techniques, never its story.

## How a film is made (upstream workflow)

1. Brief: style + topic confirmed, own material (voice, music,
   photos, logos) inventoried, missing system tools checked with the
   shipped `setup.sh`, storyboard preference asked once.
2. Treatment: three candidate structures in TREATMENT.md, one chosen.
3. Look: style frames rendered with the real drawing code and checked
   against STYLE.md.
4. Storyboard only if the user asked for one (then stop for approval).
5. Produce: voice (Kokoro offline TTS, or edge-tts; speech checked
   with faster-whisper), score, animation, mix, render via `core/`
   tools.
6. Self-check against DIRECTOR.md and deliver.

Three styles (marked with a diamond in the upstream list) draw with
an image generator and cannot start without one.

## Licensing: mixed, check before commercial use

There is no single licence (GitHub reports NOASSERTION). The
checkout's `LICENSE` is an index; `REUSE.toml` states the terms file
by file, and `LICENSES/` holds CC-BY 2.0/3.0/4.0, **CC-BY-NC-4.0**,
CC0, ISC and several custom references. Practical rule: before using
a style or asset commercially, check its entry in `REUSE.toml`;
some components are non-commercial. Films made with the library
carry no LemoLab credit or watermark requirement per upstream
AGENTS.md.

## Requirements and blockers on this VM

- The deps tiers are NOT installed: core tools, the voice tier
  (kokoro-onnx, edge-tts, faster-whisper) and the music tier all
  come from the skill's `setup.sh deps` flow, which is a real
  install (and the first-use library download is >1 GB). None of
  that was run in this banking pass.
- Compute: the source article measured 30-60 minutes per film plus
  heavy model tokens on a normal machine. This VM has ~1.5 shared
  CPUs and ~8 GB RAM, so expect far longer renders; long films are
  not realistic here until proven otherwise.

## Fit and limits

- UNTESTED here as of banking (21 Nov 2026). To test: run the
  checkout's `setup.sh` check, install only the core deps tier,
  and make one very short film (under ~20 s) in a simple 2D style,
  verifying frames, loudness and total wall-clock time before
  offering it for real work.
- Choose this when the user wants a finished short in a distinct
  ready-made style and can accept a long render. For the channel's
  locked flat-face story work, the house pipeline stays the default.
