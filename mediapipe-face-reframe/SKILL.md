---
name: mediapipe-face-reframe
description: Vision-based face work for clips: locate a streamer's facecam automatically, measure its box tightly, score facial-expression intensity over time from Face Landmarker blendshapes (jawOpen, mouthSmile, brow raise, eye widen) to find kaget/ngakak/marah moments by face instead of audio, and track the face for reframing. Use when starting a clip job on a new creator layout (to measure the cam box), when audio signals cannot find the moment, or when a clip needs the face tracked rather than a fixed crop. OpenCV is the companion for frame sampling and fallback face detection.
---

# MediaPipe Face Reframe

The house clipper finds moments by audio and chat, then measures the facecam
box by hand from stills. MediaPipe (github.com/google-ai-edge/mediapipe,
Apache-2.0) adds the missing vision signal:

- **Face detection** (BlazeFace): where is a face, in which frames. Run over
  sampled frames of a new source to find the persistent facecam location
  before anyone guesses a crop.
- **Face Landmarker** (Tasks API): 468 landmarks + 52 blendshape scores per
  frame. Blendshapes are an expression meter: `jawOpen` + `mouthSmileLeft/
  Right` spike on laughter and shouting, `browInnerUp` + `eyeWideLeft/Right`
  on surprise, `browDownLeft/Right` on anger. A time series of these scores
  over a VOD is a moment-finding signal that matches how Rangga judges clips
  (expression first), which loudness alone cannot see: a silent shocked face
  is invisible to audio scans.
- **OpenCV** (github.com/opencv/opencv, Apache-2.0): frame extraction at
  fixed fps, Haar/DNN fallback detection, and the crop/resize plumbing
  around the MediaPipe results. Heavy image work still belongs to ffmpeg;
  OpenCV is for analysis frames only.

## Setup on this VM

- Per-job venv: `pip install mediapipe opencv-python-headless`. All inference
  is local; nothing is uploaded anywhere.
- Models come only from Google's official MediaPipe storage
  (storage.googleapis.com/mediapipe-models/...): `face_landmarker.task`
  (includes blendshapes) and the BlazeFace `.tflite`. Do not fetch model
  files from third-party mirrors.
- Cost profile that works here: scan a low-res copy (360p) at 1 fps for the
  expression time series, then confirm the winning seconds at full res.
  Facecam regions in a 360p frame are small; blendshape scores get noisy, so
  rank by sustained peaks (1-3 s windows), not single frames.

## Workflow

1. Sample frames (1 fps) from the scan copy; run face detection on a spread
   of timestamps and cluster the boxes: the stable cluster is the facecam.
2. Crop the facecam region (with margin), upscale 2x, run the Face
   Landmarker over the region's frames; record blendshapes per second.
3. Score expression intensity (start: jawOpen + mouthSmile mean for ngakak,
   browInnerUp + eyeWide for kaget, browDown + mouthPress for marah), smooth
   over 2 s, list the top peaks with timestamps.
4. Verify each peak with real stills (face must match the on-screen event in
   the same seconds; flat or occluded face = discard, per house rule), then
   hand the window to clipper-pipeline for cutting. The measured face cluster
   also gives the tight cam box the fullcam layout needs.

## Status

UNTESTED on a live target at install time (20 Nov 2026, from the eigen X-post
repo roundup; security-reviewed by reading). A first trial on the Windah
Motion Klip job was scheduled the same day; see that job's trial report for
the outcome. Source note: original house playbook for the public MediaPipe
and OpenCV projects; no upstream code copied.
