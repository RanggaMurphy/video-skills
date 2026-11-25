---
name: what-if-animation
description: '"What If" animated episodes from one topic line: a seven-beat script formula, ElevenLabs voice with word timings, a fast-cut shot list, a self-checked storyboard, then every frame drawn in code (SVG + Remotion) with the cast on a single code rig so characters cannot drift between shots. Use when the user wants a What If episode or cartoon, or wants the code-rig character-consistency method applied to Buggy Before Sleep. Upstream: https://github.com/kelano86/what-if-animation (MIT, by FreshStack), installed locally at ~/workspace/tools/what-if-animation. Status: banked 21 Nov 2026 on the user''s order, UNTESTED here; the pipeline needs an ElevenLabs API key we do not currently hold, so do not promise an episode until that is resolved and one example render has been proven.'
---

# What If Animation — code-drawn "What If" episodes (kelano86)

One topic line in ("What if you could rewind 10 seconds?"), a finished
15-25 second episode out, in the dusk-lit stick-figure style of the
"What If" channels. No image model, no video model: the AI writes the
scenes as SVG and Remotion renders them; voice and sound effects come
from ElevenLabs.

## Where things live

- Local checkout: `~/workspace/tools/what-if-animation`
  (upstream: github.com/kelano86/what-if-animation, MIT).
- The repo IS a skill: read its own `SKILL.md` first and follow it over
  this wrapper. Then `references/formula.md` (script formula),
  `references/look.md` (measured look, pace, checklists),
  `references/kit.md` (engine/cast/sets catalogue), `references/sound.md`,
  `references/traps.md`.
- `studio/` is the Remotion project (copy it out per the upstream setup;
  never build a deliverable inside the tools checkout). Two finished
  example episodes ship in `studio/src/episodes/`: `rewind` and
  `copy-paste`.
- Pipeline scripts in `scripts/`: voice, plan, stills, board, sfx,
  mixcheck, motiongrid, master.

## The pipeline (upstream SKILL.md, in order)

1. Script on the seven-beat formula (below) into `episode.json`,
   45-65 words, every fact worked out and sourced in its `science`
   field before it is voiced.
2. Voice: one ElevenLabs take with character timestamps; pauses
   tightened to genre pace; word timings drive everything after.
3. Shot list on the words: about 27+ cuts a minute in the opening, no
   static shot over ~3 s, shot size/angle varied every cut.
4. Storyboard: one still per shot at its key frame.
5. Self-check the stills against an 11-point checklist; fix and
   re-render failing shots before any animation.
6. Animate from the key poses (`poseAt`, `faceAt`, camera `kf`); check
   motion with frame grids against the motion checklist.
7. Sound: an effect on every visible action, ambience per place, music
   bed, mix checked so effects stay clear of the voice.
8. Master to -14 LUFS, peaks under -1 dBTP; report length, pace and
   the ElevenLabs credits the run used.

## Character consistency: the rig (the part that matters most for us)

The characters are never generated images. Each character is a **rig**:
one drawing function in code (SVG) that renders the character in every
shot, parameterised by pose and expression (`poseAt` / `faceAt`). The
hero Pip, his friend Mo, and the sister, mum and the suit are all looks
on that one rig. Because the same function draws the character
everywhere, there is nothing to drift: consistency is structural, not
something checked after the fact. New looks are approved on a cast
sheet render (`npx remotion still src/index.ts Cast out/cast.png`)
before use. Sets are code too: rooms in real perspective, lit by their
own lamps and windows, added to a shared library so later episodes
reuse them.

Contrast with our house pipeline: our flat-face cast is image sprites
over painted plates, so consistency is maintained by locked sheets and
frame inspection. This repo's answer is to remove the image step for
characters entirely. Its own honest limit: walk cycles and acting stay
simple; the look carries it, and painted/textured styles are NOT
realistic in pure code (they need an image model).

## Story patterns: the seven-beat What If formula

Decoded upstream from five scripts across four channels (Ifverse,
FunNotSoFun, IFinity, Could've Been Tales):

1. Cold open in the middle of the action: three or four quick demos of
   the power; the power's word is said every time.
2. The premise and its rules, as the title card ("WHAT IF YOU COULD"
   + the power in four words or fewer).
3. The fun part: escalating everyday wins.
4. The not-so-fun part: the cost, built on ONE real, checked fact with
   a number, followed by "That's real."
5. Someone powerful notices (a man in a suit, robbers, a government).
6. A moral choice with family at stake (usually a little sister).
7. Cliffhanger: a question for the comments, "Part 1 of 2".

The 15-25 s episode is the cold open of that arc: beats 1-4 in full,
5-7 folded into the last line. A 40-60 s cut adds beats 4-6 properly
and ends on "Part 1". Writing rules: second person, present tense,
sentences of three to eight words; every line must be a picture that
reads in one shot with no caption; demos escalate small and selfish,
then useful, then a little uncanny; the power has a word, a sound and
a look; end on a question or a threat, never a resolution; never
remake an existing channel episode (search the premise first).

Note for Buggy Before Sleep: our house format is different (calm
bedtime narration, ~30 s segments, one word/phrase captions, frozen
house voices). The transferable assets here are the rig idea and the
formula, not the fast-cut pacing or the ElevenLabs voice.

## Requirements and blockers

- Node 18+ (this VM: v24, OK), ffmpeg + ffprobe (OK), Python 3.9+
  with numpy and Pillow (OK).
- **ElevenLabs API key: NOT held here. This is the hard blocker.**
  Upstream measured ~150-250 credits per episode; the free plan
  (~10,000 credits/month when checked Oct 2026) covers ~40 episodes
  but is non-commercial and asks for an ElevenLabs credit, so check
  its terms before monetising. The key is the user's decision.
- Remotion itself is free for individuals and companies of up to
  three people (upstream README); larger use needs a company licence.

## Fit and limits

- UNTESTED here as of banking (21 Nov 2026). To test: (1) the user
  supplies an ElevenLabs key; (2) copy `studio/` to a project folder
  and `npm install`; (3) render one shipped example episode end to
  end and verify the output personally; only then offer a real
  episode. Budget the first run as a pipeline proof, not a deliverable.
- Choose this when the user wants a true What If-format episode or
  wants to explore the code-rig approach. For Buggy Before Sleep
  productions as currently locked (flat-face painted style, house
  voices), the house pipeline stays the default.
