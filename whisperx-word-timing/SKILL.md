---
name: whisperx-word-timing
description: Word-level caption timing upgrade: WhisperX forced alignment on top of Whisper transcription, giving per-word timestamps and optional speaker diarization. Use when faster-whisper word timestamps are visibly drifting in a clip's captions, when captions must be frame-tight for fast speech, or when a multi-speaker video needs speaker labels before clipping. The house default stays faster-whisper inside clipper-pipeline; reach for this only when timing quality or diarization is the actual bottleneck.
---

# WhisperX Word Timing

faster-whisper (house default, already in the clipper venv) produces segment
and word timestamps directly. WhisperX (github.com/m-bain/whisperX,
BSD-2-Clause) adds a phoneme-based forced-alignment pass (wav2vec2) that
re-times every word, plus optional pyannote speaker diarization. The output
is the same shape the clipper caption builder consumes: words with start/end.

## When it earns its keep

- Caption drift: words landing early/late against the audio in fast or noisy
  speech (game audio under the voice, shouting, laughter over words).
- Multi-speaker sources (podcast panels, collab streams) where captions or
  moment picking need to know who is speaking.
- Not worth it for clean single-speaker speech: faster-whisper is faster,
  lighter, and already wired into clipper-pipeline.

## Setup on this VM

- Per-job venv only, never global. `pip install whisperx` pulls PyTorch:
  install torch from the CPU wheel index first
  (`--index-url https://download.pytorch.org/whl/cpu`). Heavy stack (torch +
  pyannote); the VM has ~8 GB shared RAM, so align bounded excerpts, not
  whole multi-hour VODs.
- Alignment models download from Hugging Face on first use per language
  (Indonesian alignment model availability is uneven; if none loads, WhisperX
  falls back to unaligned timestamps, at which point faster-whisper is the
  better tool anyway).
- Diarization needs a Hugging Face account token AND accepting the pyannote
  model terms on their site. That token is a credential: it goes through the
  secure credential flow, never into a skill file, job file, or chat, and
  diarization only runs if Rangga has approved setting that up. Without the
  token, alignment alone still works.

## Workflow

1. Transcribe the excerpt (faster-whisper output can be reused as the base
   transcript; WhisperX can also transcribe itself).
2. Run alignment for the excerpt's language; export word-level JSON.
3. Feed the word timings into the clipper-pipeline caption step in place of
   the faster-whisper timings for that clip.
4. Spot-check three caption boundaries against the audio before rendering the
   full clip; if alignment made anything worse, revert to the default.

## Status

UNTESTED on a live target (installed 20 Nov 2026 from the eigen X-post repo
roundup; security-reviewed by reading). Source note: original house playbook
for the public WhisperX project; no upstream code copied.
