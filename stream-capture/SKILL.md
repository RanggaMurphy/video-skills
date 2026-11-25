---
name: stream-capture
description: Capture sources the house downloader does not cover: TwitchDownloader downloads Twitch VODs/clips and downloads + renders the chat replay (chat spikes are a moment signal and chat can be composited), Streamlink records streams from Twitch, YouTube Live, and 1000+ other sites while they are live. Use when a clipping target is on Twitch, when a moment hunt needs the chat replay alongside the video, or when a stream must be recorded live because no VOD will exist. YouTube VOD downloads stay with yt-dlp inside clipper-pipeline.
---

# Stream Capture

clipper-pipeline's capture step is yt-dlp, which is the right tool for
YouTube and most VOD sites. Two gaps remain, both filled from the public
toolkit:

- **Twitch**: yt-dlp handles basic Twitch VODs, but **TwitchDownloader**
  (github.com/lay295/TwitchDownloader, MIT) is the specialist: VOD and clip
  download, and crucially chat download in JSON plus chat *rendering* back
  to video. Chat data is also an analysis signal: message-rate and emote
  spikes over a VOD are a moment-finding input on par with loudness
  (clipper-pipeline lists chat density as a signal but had no fetcher for
  Twitch chat until now).
- **Live**: **Streamlink** (github.com/streamlink/streamlink, BSD-2-Clause)
  resolves and records live streams (Twitch, YouTube Live, many others)
  while they air, for creators who delete VODs or where the campaign window
  is the live itself. Recording a live stream is a long-running foreground
  commitment: only start one on Rangga's explicit order for a named stream
  and time window.

## Setup on this VM

- Streamlink: per-job venv, `pip install streamlink`. Use only the plugins
  bundled in the installed package. Never sideload third-party plugin files:
  streamlink plugins are executable Python, and an unreviewed plugin is
  unreviewed code.
- TwitchDownloader: use the TwitchDownloaderCLI build from the official
  repo's GitHub releases only (it is a .NET binary; check the release page
  for the Linux build), or build from source if no suitable binary exists.
  Do not fetch it from mirrors or package sites.
- OBS Studio (github.com/obsproject/obs-studio, GPL-2.0) appears in the same
  toolkit lists as the capture tool, but it is a desktop GUI recorder: on
  this headless VM it adds nothing over Streamlink + ffmpeg screen sources.
  Noted here so nobody installs it expecting a headless recorder; skip it.

## Workflow

1. Twitch VOD job: TwitchDownloaderCLI for the video part and the chat JSON
   in one pass; store both in the job's sources/ next to the yt-dlp
   artefacts so moment finding can join chat spikes with loudness.
2. Chat render only when a deliverable actually shows chat (most campaign
   clips do not); the JSON alone is enough for signal work.
3. Live job: confirm the exact stream URL and stop condition with Rangga,
   record with Streamlink to the job folder, then treat the recording as a
   normal source for clipper-pipeline.

## Status

UNTESTED on a live target (installed 20 Nov 2026 from the eigen X-post repo
roundup; security-reviewed by reading). Source note: original house playbook
for the public projects named above; no upstream code copied.
