---
name: clipsai-highlights
description: Find highlight moments in long videos by transcript semantics instead of loudness: ClipsAI (Whisper transcription + embedding-based clip ranking that returns ready clip boundaries) and FunClip (FunASR/Paraformer transcription with LLM-assisted or manual line-pick clipping) as the alternative. Use when a long VOD or podcast needs candidate moments and the audio-energy signals (loudness, most-replayed heatmap) are weak, flat, or misleading, or when Rangga asks to try AI highlight detection. Pairs with clipper-pipeline, which still owns campaign rules, cutting, captions, and delivery.
---

# ClipsAI Highlights

Semantic moment finding: transcribe the video, embed the transcript segments,
rank them as "highlight-worthy", and take the top segments as clip candidates.
This is a different signal from the house defaults in `clipper-pipeline`
(loudness clusters, most-replayed heatmap, chat spikes). Use it as a second
opinion or when the energy signals fail, then verify every candidate against
the actual frames before cutting. A ranked segment is a lead, not a moment:
the expression-on-face check from clipper-pipeline still decides.

## The two tools

- **ClipsAI** (github.com/ClipsAI/clipsai, MIT, Python). Fully automatic:
  `Transcriber` (Whisper) -> `ClipFinder` ranks segments and returns clip
  start/end times; `resize_video()` can reframe to 9:16 using its own face /
  object detection. Caveat: the upstream code has been stale since Jan 2024;
  pin versions and expect dependency friction. Its reframe is a fallback only;
  the house fullcam layout (facecam full-width on top) stays the standard.
- **FunClip** (github.com/modelscope/FunClip, MIT, Python, actively
  maintained). FunASR Paraformer ASR (strong for Chinese, works for English;
  Indonesian quality unproven) + optional LLM-assisted segment picking, or
  manual pick-by-transcript-line. Ships a Gradio UI; on this VM call its
  Python functions headlessly instead of serving the UI.

## Setup on this VM

- Never install globally. Create a per-job venv and install there:
  `python3 -m venv venv && ./venv/bin/pip install clipsai` (FunClip: clone the
  repo into the job folder and install its requirements into the same venv).
- PyTorch must come from the CPU wheel index on this VM
  (`--index-url https://download.pytorch.org/whl/cpu`); the default PyPI wheel
  drags in multi-GB CUDA packages. The VM has ~8 GB RAM shared with other
  work: run transcription on bounded excerpts (10-30 min), never a multi-hour
  VOD in one pass, and watch free RAM before starting.
- Both tools download ASR/embedding models from Hugging Face / ModelScope on
  first run. That is expected behaviour for these tools; verify the model
  names match the repos' documentation before the first download, and never
  pass either tool any credential or API key (FunClip's optional LLM step
  takes an OpenAI-style key: leave it unset unless Rangga explicitly approves
  a key for it).

## Workflow

1. Take the excerpt or full audio the job already has (clipper-pipeline
   downloads and loudness data can be reused; do not re-download).
2. Transcribe, run the clip ranking, keep the top 5-10 candidate windows.
3. Cross-check candidates against the house signals and, decisively, against
   sampled stills of the creator's face at those timestamps.
4. Hand surviving windows to clipper-pipeline's normal cutting/caption/rules
   flow. Record in the job report that the moment came from semantic ranking
   so results can be compared against loudness-picked clips later.

## Status

UNTESTED on a live target (installed 20 Nov 2026 from the eigen X-post repo
roundup; security-reviewed by reading, no upstream code was copied into this
skill). Source note: tool selection and workflow adapted from the public repos
linked above; this file is an original house playbook, not a copy of either
repo's docs.
