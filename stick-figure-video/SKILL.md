---
name: stick-figure-video
description: 'Direct and produce stick-figure story/explainer videos end to end: one-line brief -> storyboard proposal -> scene-by-scene production with a frozen character anchor, narration, captions, music and a local render. Use when the user wants a stickman/stick-figure video, or a cheap faceless animated story format (e.g. the Buggy Story Night channel). Method adapted in-house from stickman-video-director (MIT): fork https://github.com/CryptoYuyyy02/stickman-video-director, upstream https://github.com/kaomei/stickman-video-director — the repos are text-only method packs (no code ships in the fork) and are NOT installed here; this skill carries the workflow in our own words. IMPORTANT: video-generation models are unavailable on this machine (media.generate_video is region-blocked), so only the local code-render route in this skill is executable here.'
---

# Stick-figure video — director workflow with a local render engine

A stick-figure video stays watchable when three things never drift:
the character, the narrator, and the beat structure. Everything else
is a per-scene variable. This skill freezes the first three in
writing before any frame is drawn, then produces the film scene by
scene and stitches it.

There are two production engines in the source method. Only one
works here:

- **Model engine (NOT available here):** per-scene prompts fed to a
  video-generation model (upstream assumes Google Flow / Gemini
  Omni). Smooth motion, but costs generation quota and drifts
  without a reference image. `media.generate_video` is region-
  blocked on this account, so do not plan around it.
- **Code engine (our route):** layered drawings animated frame by
  frame with Python/PIL and piped to ffmpeg. Zero generation cost,
  fully deterministic, character cannot drift because the same
  drawing code draws every frame. Smoothness is capped by how much
  per-frame motion we author. Remotion (house `remotion` skill) is
  an acceptable alternative renderer for the same scene plan.

## Workflow

### 1. Setup gate — settle these before planning

- Source: a topic line, an article, or a finished script.
- Ratio: `16:9` or `9:16` (native staging for each; never crop one
  into the other).
- Duration: in ~10-second scene units (30s = 3 scenes, 60s = 6).
- Style: pick one drawing grammar from the style notes below and
  freeze it.
- Voice: one narrator for the whole video, chosen up front.

If ratio or style is missing, ask once, in one message. Never pick
a ratio silently.

### 2. Director's proposal (Phase A) — then stop for approval

Produce a proposal, not prompts or frames:

- Title, core message, and the opening hook.
- The narration script, rewritten as natural spoken text at
  **20–25 words per 10 seconds** of runtime (~120–150 words for
  60s). Preserve the source's facts, names and numbers; never
  invent statistics, quotes or claims to fill time.
- A storyboard table with exactly one row per scene: time range,
  narrative job, what the figure does, camera/transition, the
  narration lines for that scene, music/SFX notes.
- The frozen character anchor (below) and the frozen voice profile,
  written out in full.
- At most three saturated accent colours, each given a meaning
  (danger, discovery, success...). Name colours in plain words in
  creative text, never hex/RGB.

End the proposal by asking for approval or named revisions. A
global change (ratio, duration, style, voice) invalidates the
approval and needs a revised proposal.

### 3. Beat structure — the five-stage arc

Shape the script so a viewer has a reason to stay:

1. **Hook (first 2–5s):** a counter-intuitive question or visual
   paradox. No throat-clearing, no title card, narration starts at
   second 0.
2. **Broken assumption:** state what everyone believes, then break
   it in one sentence.
3. **Hidden mechanism:** reveal the inside detail or friction that
   explains the situation.
4. **Payoff truth:** the underlying mechanism or human truth, stated
   plainly — the "aha".
5. **Elevation:** a memorable closing line; for explainer formats, a
   genuine discussion question. For story formats, the emotional
   resolution replaces the question.

Inside each ~10s scene, stage three beats (establish → escalate →
land the beat and hand off to the next scene), with a perceptible
visual change every 2–3 seconds. The figure must act — run, grab,
build, fall, point — never idle while the camera drifts. End each
scene on something the next scene inherits: a pose, a moving prop,
a direction of travel, a shape.

For narrative story shorts (our channel use), a simpler arc is
fine — setup → escalation → twist/payoff — but keep the hook-first,
no-silent-opener and scene-handoff rules.

### 4. The character anchor — the consistency technique

AI and code both drift when told "same character". What works is a
**frozen textual drawing specification**, written once, then reused
verbatim for every scene (as a prompt block for a model, or as the
drawing constants in the render code). Rules for a good anchor:

- Describe the figure as literal drawing instructions: head shape
  and fill, whether there is a face, exact limb count, line weight,
  proportions (e.g. about 4–4.5 heads tall for a slender figure),
  and what must never appear (no clothing, no filled torso, no
  extra limbs).
- State the replacement rule: a limb exists only in its current
  pose — raising an arm replaces the old arm line, it never leaves
  a resting arm underneath. This single rule prevents the classic
  extra-hand failure.
- Freeze the palette and background treatment with the figure.

Our default anchor for minimal story work (write variants per
character when a story needs a cast; each character gets their own
frozen block, repeated wherever they appear):

```text
One stick figure drawn in clean black line on a flat off-white
background. Hollow circular head, no face, no hair, no clothing,
no filled body. Single uniform line weight for head, spine, arms
and legs. Exactly two arms and two legs; each limb is drawn only
in its current pose. Stable proportions, about four heads tall.
Accent colour appears on props and effects only, never on the
figure.
```

A second proven grammar from the source method, for a warmer
1930s-cartoon feel: thin ink-line figure with a flat white round
face, two small hair tufts, single-stroke spine and limbs, bare
line body, performing inside hand-drawn period scenery in a muted
palette (sage gray-green, pearl gray, gray-taupe, ivory, tiny
faded brick-red accents), even diffuse light, no sepia, no CGI
shading. Same rule: freeze the character block and the style block;
vary only scene and timed action.

### 5. Local render (code engine) — how a film gets made here

1. **Narration first.** Generate the voice track via the house
   spoken-audio route, one segment per scene. Check every segment:
   run silence detection — TTS occasionally returns a take with
   multi-second pauses baked in or a wildly wrong duration. If a
   segment's duration is an outlier for its word count, split it by
   sentence and re-generate the pieces, then concatenate; do not
   just re-roll the same text (caches can return the same bad take).
   **Bedtime voice standard (standing — Rangga's ruling, 21 Nov
   2026, after hearing the EN story-new-1 narration as too fast):**
   Buggy Before Sleep is a BEDTIME channel, so the voice-over must
   be unhurried and relaxed, calm and soft ("halus") — like someone
   telling a story to help you fall asleep, never a brisk read.
   The voice is FROZEN per channel for consistency across
   episodes. EN channel (Buggy Before Sleep): always
   `avocado_v2:MAI_03` (the house TTS default) at speed **~85**
   (working range 80–88; favour the calmest takes, never the old
   95–105 pilot speeds, and never repair pace with a speed-up pass
   afterwards). ID channel (Buggy Before Sleep ID): always
   a native Indonesian voice at rate **−15%** — Rangga's ruling,
   21 Nov 2026, after hearing `avocado_v2:MAI_03`'s foreign
   accent carry into the Indonesian narration; a language's
   channel uses a native voice of that language. NOTE:
   `id-ID-ArdiNeural` was tried in story-new-1-id v2 and
   REJECTED by Rangga (21 Nov 01:43) as too generic
   ("pasaran") and off-theme for a night channel — the ID
   house voice is now FROZEN as
   **`avocado_v2:vd2_r8_rep1k_0363_v068_28k_g5k` ("Musing
   Mirror")** — a native-Indonesian-accent voice from the
   same avocado_v2 library as MAI_03, velvety-soft timbre —
   picked by Rangga himself from audition samples on 21 Nov
   2026 (speed 85 via the house `tts` CLI). (Edge-tts operational note: run it with the
   proxy env vars unset — the egress proxy breaks its WSS
   handshake; direct egress works.) Inter-line gaps breathe:
   ~0.8s at scene breaks, ~0.5s inside a scene, ~1.1s of quiet
   before the CTA. Keep
   the music gentle and WELL under the voice: the v2 recipe
   (bed −5 dB + sidechain ducking) measured only ~1 dB under
   the narration mean and Rangga judged it covering the
   voice-over (21 Nov 2026) — target the bed mean ≥ ~10 dB
   below the narration mean in measured windows. Runtime is whatever
   the calm pace needs — calm beats hitting a duration target;
   if a video must get shorter, cut script words, not pace. The
   same voice and delivery on every episode is the point: viewers
   should recognise the storyteller.
   **Write scripts for the ear, not the eye (standing —
   Rangga's ruling, 21 Nov 2026):** narration scripts use
   MINIMAL COMMAS — at most one per line, prefer none — and no
   ellipses. TTS pauses at every comma, so comma-chained prose
   comes out chopped with flat intonation. Split chained
   clauses into short, clean spoken sentences instead; the
   story beats and meaning stay, the punctuation goes.
   **Hook without pause (standing — Rangga's ruling, 21 Nov
   2026, corrected 01:43):** Buggy Before Sleep videos DO open
   with the "Bagaimana Jika.." / "What if.." hook line — but
   with NO curiosity pause after it. The narration flows
   straight from the hook into the premise with only the normal
   short intra-scene gap (~0.5s or less); never hold a beat on
   the hook word.
2. **Draw per scene.** Python + Pillow: draw background, props and
   the figure from the anchor constants; animate by interpolating
   poses between authored key poses (plant feet, show contact —
   hands touch the object they hold). Stream frames straight into
   ffmpeg (rawvideo pipe) instead of writing thousands of PNGs.
   A 15–20s 720p sample renders in well under a minute on CPU.
3. **Fit picture to voice.** The narration is the timeline master.
   Stretch or compress each scene's animation to its narration
   segment's length (plus ~0.15s) so scenes join head-to-tail with
   zero silent gaps and no dead air.
4. **Captions.** Burn in or sidecar, segmented by meaning and real
   speech pauses, one line at a time for minimal styles. For word-
   level timing use the house `whisperx-word-timing` skill.
   **Word-by-word is the channel standard (standing — Rangga's
   ruling on pilot v2c, 21 Nov 2026: subtitles appear word by word
   "jadi orang ga baca duluan" — so viewers cannot read ahead of
   the narration).** Mechanics: forced-align the known script text
   against the narration stem (WhisperX alignment; keep the
   script's words verbatim, take only timings — never let ASR
   rewrite the text). Reveal is SINGLE-WORD REPLACEMENT
   (owner ruling, 21 Nov 2026 — this supersedes the progressive-
   accumulation rule set during pilot v2c earlier the same day):
   exactly ONE word is on screen at a time; each word appears at
   its spoken timestamp and is then erased and replaced by the
   next word, for the whole video. One caption event per word,
   timed to that word's spoken window — a word holds until the
   next word starts, so the last word of a sentence holds through
   the micro-gap, and a hook word (e.g. "if…") can hold alone
   through a deliberate narration pause. One line only (it is a
   single word), centred horizontally in the same safe-zone
   position as the block rule below. No accent tinting: the word
   is plain bold white throughout. Watch for the TTS lead-in trap: WhisperX
   pins each segment's first word to the segment start, but TTS
   clips carry ~0.2s of baked-in silence — correct first-word
   starts against the stem's actual energy onset. Note libass
   renders ~0.735× PIL's measured width for this font stack —
   calibrate once with a test render before trusting PIL metrics.
   Generated/drawn scenes themselves carry no incidental text,
   logos or watermarks; any word art is added deliberately here.
   **Vertical / Shorts caption rule (standing — Rangga's ruling on
   pilot v2, 21 Nov 2026: "jangan terlalu bawah subtitle-nya"):**
   for 9:16 output headed to YouTube Shorts, never use an opaque
   background box behind captions, and never park them at the
   bottom of the frame — the Shorts player UI (title, channel
   name, action buttons) covers roughly the bottom 25%. Style:
   bold white sans with a thick dark outline and a soft shadow,
   no box (ASS `BorderStyle 1`). Position the block in the
   lower-middle: baseline around 65–70% of frame height, i.e.
   bottom margin ≈ 25–30% of frame height (ASS `MarginV` ≈
   390–450 at 1280 height; pilot v2b used 420). Centre
   horizontally, max 2 lines per caption — choose font and size
   so the longest caption fits 2 lines (pilot v2b: Noto Sans
   SemiCondensed, size 44 at 720 wide, side margins 36). In QC,
   draw the 75%-height line on the check frames and confirm every
   caption sits fully above it.
   **Watermark (standing — Rangga's ruling on pilot v2c, 21 Nov
   2026: "tambahin watermark di setiap video").** Every episode
   carries the channel handle as a watermark for the full duration:
   small semi-transparent white text with a soft shadow in the
   TOP-LEFT area (inset ≈ 28px at 720×1280; pilot v2c: Noto Sans
   SemiCondensed 24, alpha &H55, thin outline, ASS alignment 7 on
   its own layer). Never the bottom (captions + Shorts UI live
   there), never centre. It must be readable when looked for but
   not compete with the art or captions. The handle text is
   confirmed at render time — if the channel handle changes, the
   upload master is re-rendered with the new text.
5. **Music and mix.** If no music tool is available, a simple local
   synthesis (e.g. numpy-generated tones/music-box style motifs)
   can score a short film: suspense register before the turn, warm
   register after, with the change aligned to the story's reveal.
   Keep music clearly under the voice; final loudness around
   **−14 LUFS**. **Mix balance (standing — Rangga's ruling on
   pilot v2c, 21 Nov 2026: the backsound "nabrak sama voice
   overnya"):** build the mix from stems, never by re-processing a
   combined mix. Bed sits ≈ 5 dB lower relative to the voice than
   feels "equal", PLUS gentle sidechain ducking keyed on the
   narration (≈ 4 dB more dip while she speaks). Pilot v2c
   reference numbers (stem domain): music went from ≈ +2 dB ABOVE
   voice RMS under speech to ≈ 7 dB BELOW it; in the gaps it
   stays audible. Prove the balance with measurements (music level
   in narration-free gaps vs under narration, before/after), not
   by ear alone.
6. **Assemble** scenes with ffmpeg, then verify (next section).

Output specs: 1280×720 (16:9) or 720×1280 / 1080×1920 (9:16),
H.264 + AAC. A vertical version is a re-staged render with
depth/stacked composition, not a centre crop of the landscape one.

### 6. Acceptance — judge the actual film, never the plan

A correct storyboard does not certify the output. Before calling a
video done:

- **ffprobe the final file:** dimensions, ratio, duration, both
  streams present, duration matches the plan.
- **Extract frames from every scene** and inspect: character
  matches the anchor in all scenes (limb count, head, line weight,
  no filled torso appearing mid-film), beat order is the planned
  order, hands/feet make believable contact, no stray text.
- **Watch/listen once at normal speed** if the environment allows;
  if it does not, record the check as `not_checked` — never invent
  a pass. Sampled frames are labelled sampled, not a full viewing.
- Use explicit gate states: `pass`, `fail`, `not_checked`,
  `not_applicable` (with a reason). Any failed or unchecked
  required gate means "not accepted yet", and the repair loop
  fixes only the offending scene, preserving accepted scenes and
  audio, then re-checks the repaired scene and its neighbours.
- Known failure modes to hunt: character drift between scenes
  (worst in close-ups and final scenes), beats landing out of
  order, a scene whose style flattens compared to the rest, TTS
  segments with baked-in silence, captions drifting from speech.

## House integration

- **Narration:** house spoken-audio/TTS route only. The source
  method's provider bindings (specific hosted voice services and
  fixed voice IDs) are deliberately not carried over; the voice is
  chosen per production and frozen in the proposal.
- **Captions:** house `whisperx-word-timing` for word-level timing.
  Channel standard is word-by-word SINGLE-WORD REPLACEMENT —
  one word on screen at a time (§5 step 4; owner ruling
  21 Nov 2026, superseding the v2c progressive-accumulation
  rule). Vertical output follows the Shorts caption rule in §5
  step 4 (no opaque box; safe-zone placement above the bottom
  quarter), and every episode carries the handle watermark
  (§5 step 4, top-left).
- **Motion quality:** apply the house `motion-design` skill's
  principles (anticipation, follow-through, easing) to key poses —
  stick figures read through body acting, not facial detail.
- **Channel use:** this is the pilot format candidate for the
  faceless story channel (Buggy Story Night, EN + ID editions).
  Production cost per video on the code engine is agent time only:
  script + storyboard, one render pass per scene, one QC pass.
  Standing channel rules still apply: Rangga reviews and approves
  before any upload, and uploads happen live at publish time —
  never via YouTube scheduling.

## What was deliberately excluded from the source

- Video-model production routes and their provider setup/onboarding
  guidance (unavailable and unnecessary here).
- Fixed third-party voice/service requirements baked into some
  upstream style contracts.
- The fork author's own production diary: file paths, sample
  verdicts and rulings from their machine. Their field lessons that
  generalise (TTS silence defects, scene-splitting, speed-fitting
  picture to voice, frame-based acceptance) are folded in above in
  our own words.
