# Video Skills for Muse

A pack of custom Muse skills for YouTube and short-form video
production: clipping, editing, animation, motion design, subtitles.

## Install

Clone this repo, then copy the skill folders you want into your Muse
custom-skills directory (`~/workspace/custom-skills/`). Each folder's
`SKILL.md` explains when the skill applies and how it works. Most skills
need ffmpeg on PATH; some need python3 (see each SKILL.md).

```bash
git clone https://github.com/RanggaMurphy/video-skills.git
cp -r video-skills/* ~/workspace/custom-skills/
```

## Contents

- **clipper-pipeline** — stream clipping pipeline (facecam layout, word captions, QC)
- **clipsai-highlights** — highlight extraction from long videos
- **auto-editor-tighten** — tighten cuts and silence with auto-editor
- **ffmpeg-skill** — ffmpeg recipes and patterns
- **jedag-jedug** — beat-synced TikTok edits (hard cuts, snap zoom, shake, flash)
- **remotion** + **remotion-best-practices** — programmatic video with Remotion
- **chase-animate** — procedural animation in any style
- **claude-animation-base** — hand-painted cartoon style from code
- **lemo-opuscar** — 99 film styles in code (skill instructions only; the engine itself is the open-source project https://github.com/lemomo-ai/lemo-opuscar, clone it separately)
- **what-if-animation** — code-drawn What If episodes
- **stick-figure-video**, **stickman-story-remotion**, **stickman-video-director** — stickman video workflows
- **motion-design**, **motion-prompt** — motion direction and motion library
- **card-carousel-promo** — 15-second beat-mapped card carousel promo
- **mediapipe-face-reframe** — face-aware reframing
- **stream-capture** — stream capture workflow
- **whisperx-word-timing** — word-level subtitle timing with WhisperX
