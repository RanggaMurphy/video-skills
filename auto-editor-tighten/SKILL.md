---
name: auto-editor-tighten
description: Tighten a cut by removing dead air automatically and map a long video's scene boundaries: Auto-Editor cuts silence/low-motion stretches by loudness and motion analysis (and can export an edit decision list or a trimmed file), PySceneDetect finds scene cuts and transitions. Use when a drafted clip still drags (pauses, loading screens, quiet gameplay between beats), or when a long VOD needs a scene map before moment hunting. The house ffmpeg-skill silence tool covers simple cases; use this when motion-aware cutting or a real scene list is needed.
---

# Auto-Editor Tighten

Two analysis tools that sit between moment finding and final render:

- **Auto-Editor** (github.com/WyattBlue/auto-editor, source under the
  Unlicense) analyses audio loudness (and optionally frame motion) and cuts
  the stretches below threshold: dead air, pauses, quiet wandering between
  the beats a clip is actually about. It can write the trimmed video
  directly, or export the edit (Premiere/Resolve/Shotcut XML, or its own
  timeline JSON) so the cut list can be inspected before anything renders.
  Prefer the export-and-inspect route on campaign clips: never let a
  threshold silently eat the setup of a joke or the breath before a scream.
- **PySceneDetect** (github.com/Breakthrough/PySceneDetect, BSD-3-Clause)
  detects scene boundaries (content-aware and threshold detectors) and can
  split or list scenes with timestamps. On stream VODs the scene list maps
  game/menu/loading structure and gives moment hunting clean segment edges
  to snap clip boundaries to.

## Setup on this VM

- PySceneDetect is a clean pip package: per-job venv,
  `pip install scenedetect[headless]`.
- Auto-Editor: the source is public domain (Unlicense) but the project moved
  to a "FOSSIL" model: some release builds gate features behind the author's
  paid license keys, and the separate GUI app is proprietary. House rules:
  install from PyPI/source (`pip install auto-editor`, noting PyPI can lag
  the newest major) or pin a specific GitHub release binary from the
  official repo only; NEVER buy or enter a license key without Rangga's
  explicit decision, and do not use the proprietary GUI. The free CLI
  features (loudness/motion cutting, timeline export) are all this skill
  needs.
- Both tools are local-only; neither needs an account or network at run time.

## Workflow

1. PySceneDetect first on long sources: `scenedetect -i in.mp4 list-scenes`
   (ContentDetector default) -> scene table into the job folder.
2. After a clip's moment is locked and roughly cut, run Auto-Editor in
   export mode on the draft, review the cut list against the transcript,
   restore any wrongly-cut beats by hand, then render via ffmpeg-skill.
3. Keep thresholds conservative for gameplay: game audio dips are content,
   not dead air. When in doubt, do not tighten; pacing problems are fixed by
   choosing a better window, not by shredding the one you have.

## Status

UNTESTED on a live target (installed 20 Nov 2026 from the eigen X-post repo
roundup; security-reviewed by reading). Source note: original house playbook
for the two public projects; no upstream code copied.
