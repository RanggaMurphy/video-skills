---
name: stickman-video-director
description: 'Stickman story-video directing method: two engines (A = per-scene video-model generation from frozen four-block prompts; B = local code render), a 13-style catalog with verbatim character DNA locks, tested pacing rules (voiceover from 0s, per-scene speed-fit to narration, zero-silence joins), a TTS failure playbook, and actual-film acceptance checks. Use when planning a stickman/story short and for its pacing, prompt-contract and repair discipline; our house stick-figure-video skill remains the production engine for Buggy Before Sleep. Upstream: https://github.com/CryptoYuyyy02/stickman-video-director (MIT), itself an adaptation of https://github.com/kaomei/stickman-video-director (MIT). Installed locally at ~/workspace/tools/stickman-video-director. Status: banked 21 Nov 2026 on the user''s order, UNTESTED here; this checkout is documentation only (the upstream B-mode executable runtime is NOT included), and the A route assumes a video model we cannot currently use, so do not promise productions from this install alone.'
---

# Stickman Video Director — directing method, two engines (kaomei, via CryptoYuyyy02)

A director's playbook for stickman story videos: split the story into
scenes, keep the character and style blocks frozen verbatim across every
scene, fit each scene's picture to its narration, and accept or repair
based on the actual rendered film, never on the prompts looking right.
The shipped example is a 58-second horror-to-warm story (an office
elevator that stops nightly at a floor sealed for six years): 6 scenes
generated separately, Chinese voiceover, code-synthesized BGM that turns
from suspense to warm at the reveal, ffmpeg stitch with burned captions
and loudness normalization.

## Where things live

- Local checkout: `~/workspace/tools/stickman-video-director`
  (464K, 13 files; upstream fork github.com/CryptoYuyyy02/stickman-video-director,
  MIT; original upstream github.com/kaomei/stickman-video-director, MIT,
  ~6.6K stars; the full upstream repo is ~658MB, mostly preview media,
  and was NOT cloned).
- `SKILL.md` in the checkout is the adapted edition (dated 2026-11-17)
  with the adapter's own production records and locked pacing rules.
  Read it first; it is the operational summary.
- `UPSTREAM-SKILL.md` is kaomei's full original skill text (skill name
  `directing-stickman-videos`): the complete A/B contracts.
- `references/` holds only 10 of the upstream reference files:
  `a7-prompt-contract.md` (the four-block frozen prompt contract),
  `a7-acceptance.md`, `rubber-hose.md`, `b1-minimal-handdrawn.md`,
  `style-catalog.md` (Style 1-5 character DNA locks), `examples.md`,
  `storyboard-template.md`, `getting-started.md`,
  `mode-execution-boundaries.md`, and `a7-kitchen-ref.jpg` (the A7
  rubber-hose identity reference image).

## The gap to know before promising anything

The upstream skill's B · Autopilot mode runs on an executable runtime
(`scripts/autopilot.mjs`, per-style renderers, an `assets/` tree with
prompt-lock JSONs and validated sample films, and roughly 40 further
reference files: autopilot, B2-B6, voice-continuity, cozy-storytelling,
and more). **None of that is in this checkout.** The adapter kept the
core documents and states that missing references are to be pulled from
upstream raw on demand. Treat any such future fetch as an untrusted
download: inspect before use, never execute blindly. What we actually
banked is the method, not a runnable pipeline.

## The two engines

- **A · Director / model engine.** The skill writes an approved
  storyboard plus standalone ~10-second clip prompts (N = duration / 10)
  for a video model (upstream route: Gemini Omni Flash via Google
  Flow). Consistency comes from frozen blocks repeated verbatim in
  every prompt: Block 1 fixed character, Block 2 fixed style/palette,
  Block 3 scene, Block 4 timed action/camera. Styles: 1 Classic
  Minimalist (light/dark), 2/2A/2B Modern Beanie, 3 Prehistoric,
  4 Cozy Storytelling, 5 Historical Cartoon, A6 Amber Noir,
  A7 Rubber Hose (1930s ink-and-paint, thin-line hero, muted palette;
  full contract in `references/a7-prompt-contract.md`). Smooth and
  rich, but burns video-model quota and needs frame-level acceptance
  and repairs.
- **B · Code engine.** Layered assets animated per frame locally
  (the adapter's route: Python PIL streamed to ffmpeg, or Remotion),
  zero video quota, consistency structural, smoothness capped by frame
  density. Styles B1-B6 in the upstream text (minimal line, colorful
  hand-drawn, retro TV, survival thriller, character explainer,
  dynamic meme). On this VM the executable B runtime is the part that
  is missing (see the gap above); our house engine already covers this
  role.

## Tested production rules worth porting (not yet ported)

From the adapted SKILL.md's own dated production records:

1. **Pacing lock.** No silent title card (title burned into scene 1's
   picture), voiceover starts at 0s, copy written full (about 55-60
   Chinese chars per 10s scene; upstream Director scales English VO to
   ~20-25 words per 10s clip), each scene's picture speed-fitted with
   setpts to its narration duration +0.15s, narration segments joined
   back-to-back with zero silence.
2. **TTS failure playbook.** A take whose duration is an outlier for
   its text length is a bad take: check with silencedetect (long
   intra-take silences are the tell), and fix by splitting the line
   into sentence-level takes and concatenating locally, which beat
   rewording; a poisoned cached take can also be broken by changing a
   few characters before regenerating.
3. **Repair with your own frames.** For a scene that drifts in style,
   re-generate using the film's own already-accepted frames as the
   reference, not an external reference image; it matched the film's
   look better.
4. **Synthesized BGM structure.** With no music tool, numpy synthesis:
   suspense act (low drone, sparse piano, music-box overtones) switching
   key/mode at the story's reveal point (D minor to F major in the
   example), BGM bed about -21 LUFS under narration, final mix about
   -14.3 LUFS.
5. **Acceptance on the actual film.** Extract frames per scene and
   check character consistency, beat order, and contact relations;
   a correct prompt does not certify the output. (Same rule as our
   house verify-the-delivered-artefact discipline, independently
   arrived at.)

## VM fit and blockers

- Nothing to install: the checkout is Markdown plus one JPEG. No
  package.json, no scripts, no binaries.
- A route is prompt-only for us: it assumes Google Flow / a video
  model; we hold no Flow account and the media video tool here is
  region-blocked (403, confirmed 21 Nov 2026). Bank the four-block
  contract for if/when a video model becomes available.
- B route ingredients we DO have: Python PIL 10.2, numpy 1.26,
  ffmpeg 8.1, Node v24. The upstream autopilot runtime itself is
  absent, so our house PIL/ffmpeg engine stays the B implementation.
- TTS assumptions do not transfer: upstream names Gemini voices (and
  ElevenLabs "Brian" locked for B4). Our channels keep their frozen
  house voices; do not adopt these.
- Security: this checkout contains zero executable files, so there was
  nothing to run and nothing that phones home. Inspection was
  read-only text viewing; an execution-risk check fired on the clone
  result during install, and no repo content was executed, imported,
  or installed beyond the plain clone and reading.

## Overlap with our existing video skills

- **House `stick-figure-video`** remains the production engine for
  Buggy Before Sleep / What If Tonight flat-face films (locked cast
  sheets, painted plates, frozen voices, caption and loudness rules).
  This repo adds no engine over it. Its genuinely new value for us is
  the method layer above: the pacing lock, the TTS playbook, and the
  four-block prompt contract.
- **`stickman-story-remotion`** (ahmadaryanto skeleton): the adapted
  SKILL.md independently audited this same skeleton and reached a
  division of labour we share: code skeleton for cheap explainer and
  office shorts; atmospheric narrative (horror, mood) belongs to the
  model engine or to our painted-plate pipeline, not the skeleton.
  No new code for us here.
- **`what-if-animation`**: that repo ships a real code rig plus a
  Remotion studio (executable, currently blocked on an ElevenLabs
  key). This repo is method documents whose executable half is
  missing; the two complement rather than duplicate: rig mechanics
  there, directing/pacing discipline here.
- **`claude-animation-base`**: p5 hand-painted cartoons; different
  family, no overlap beyond "drawn in code".
- **`motion-prompt`**: a motion-element library; complementary.
  Motion-prompt supplies movement vocabulary, this supplies scene,
  pacing and acceptance structure.
- Its "modern story style" (big-head character, detailed illustrated
  backgrounds, cinematic lighting) is the closest upstream cousin of
  our locked flat-face look, with a full worked production and repair
  record; worth reading before the next flat-face film's shot plan.
