---
name: clipper-pipeline
description: End-to-end clipping pipeline for paid per-view campaigns (ContentRewards and similar): record a campaign's real rules, find trending videos and live streams, rank clip moments, cut 1080x1920 vertical clips with captions and hooks, check each clip against the campaign rules, and keep a per-campaign scoreboard. Use when Rangga mentions a clipping campaign, clipping a creator or streamer, making shorts/reels from a stream or VOD, hooks for clips, or checking a clip before posting. Adapted from the open-source gtavi-claudecode plugin (MIT), generalized to any creator, game, or topic. Nothing is ever posted automatically; Rangga approves and posts every clip himself.
---

# Clipper Pipeline

One pipeline, six steps: campaign intake, source finding, moment finding, cutting,
hooks, rule check, then the learning loop. It works for any creator, game, or topic,
not just one game.

Low-level ffmpeg work (probing, loudness measurement, format checks) follows the
house `ffmpeg-skill`; this skill covers the campaign workflow and its own scripts.

## Setup on this VM

- Scripts live in `scripts/` next to this file. Run them with the venv python:
  `~/workspace/clipper-adapt/venv/bin/python scripts/<name>.py ...`
  The venv has yt-dlp, faster-whisper, numpy, requests, truststore. System
  python does not. (truststore matters here: this VM's HTTPS proxy CA is in the
  system trust store but not in certifi's bundle; common.py routes yt-dlp
  through it and defaults YouTube to the android player client, which is the
  one this VM's IP is allowed to use. Both are already wired in; nothing to
  configure.)
- ffmpeg/ffprobe are on PATH (8.x, with libass for burned captions).
- Work root: set `CLIPPER_HOME` to the campaign folder (below). Jobs land in
  `$CLIPPER_HOME/jobs/`, finished clips in `jobs/<id>/edits/`.
- YouTube access from this VM is flaky: bot checks fire intermittently and
  downloads can be cut mid-stream. yt-dlp resumes partial downloads, and
  moments.py reuses a job's saved metadata and source file, so re-running the
  same command is the normal recovery. Expect a retry or two; do not treat a
  single failed fetch as "the video is unavailable".
- Transcription is optional (CPU only here). Measured on this VM in the
  adaptation test: a full moments scan of a 90 s video, including the first
  whisper-model download (~605 MB cache) and transcription, took about 19 s —
  but that video has very little speech (27 words). Speech-dense or long
  videos will take much longer; for long sources use `--model tiny` or
  `--no-transcribe` and lean on loudness + heatmap. See step 3.
- Rendering is the slow step: about 4 s of render per 1 s of clip at
  1080x1920 (x264 medium) on this VM. A 23 s clip took ~95 s. Budget for it.

## Campaign folders

One folder per campaign, created at intake:

```
~/workspace/clipping/<campaign-slug>/
  campaign.md     the rules, exactly as published or pasted (template below)
  scoreboard.csv  one row per posted clip (scripts/scoreboard.py)
  payouts.csv     real payout numbers only (scripts/payouts.py)
  jobs/           moment scans and edits (created by the scripts)
```

## Step 1: Campaign intake

Read the campaign page live, or use the rules text Rangga pastes. Record in
`campaign.md`:

- name, creator/brand, platform(s) accepted, link, date checked
- rate per 1K views, any cap per clip or per person, budget left — **only numbers
  shown on the page itself. If a number is not visible, write `unknown`. Never
  estimate, never carry a rate over from another campaign.**
- rules in the machine-checkable lines `check.py` understands, plus the full
  rules in plain text under them:

```
min_seconds: 15
max_seconds: 60
required_hashtags: #example #campaign
required_mention: @creator
```

- Rules behind a login: ask Rangga to paste them. Do not sign in, join, or
  accept campaign terms for him; he joins campaigns himself.
- Skip any campaign that asks for leaks, "play early", piracy, game-currency
  glitches, AFK bots, or fake engagement. Say why in one line and stop.

## Step 2: Source finding

Trending videos on a topic (YouTube, no account or key needed):

```
CLIPPER_HOME=<campaign dir> ~/workspace/clipper-adapt/venv/bin/python scripts/trends.py \
  --query "<topic or creator>" --hours 24 --limit 30 --out <campaign dir>/trends.md
```

Ranks by views per hour and flags which videos carry "most replayed" data.
Show the top 10 (title, channel, views, views/hour, age, link), pick up to 3 that
fit the campaign's allowed sources, and drop anything that looks like a leak or
"play early" post. Caveat from this VM: the android player client returns no
exact publish time, so ages fall back to the upload date and are marked `~` in
the output; those views/hour figures are approximate.

Live streams right now:

```
~/workspace/clipper-adapt/venv/bin/python scripts/streams.py --query "<topic or game>" --out <campaign dir>/streams.md
```

YouTube live search plus Twitch by category name (keyless public endpoint) plus
a best-effort Kick lookup. Viewer counts are what the platform returned at that
moment; report them as-is, never rounded up.

## Step 3: Moment finding

```
CLIPPER_HOME=<campaign dir> ~/workspace/clipper-adapt/venv/bin/python scripts/moments.py <url-or-file> --top 8
```

Writes `jobs/<id>/candidates.md` and `candidates.json`. Signals, each used only
when it actually exists:

- **Loudness spikes** (ffmpeg, always available): per-second loudness jumps above
  the local level.
- **YouTube "most replayed" heatmap**: when yt-dlp returns heatmap data for the
  video. Weighted highest.
- **Chat spikes**: YouTube VOD chat replay (downloaded automatically for videos
  that were live) or a TwitchDownloader `chat.json` passed with `--chat`.
  Twitch VOD chat cannot be fetched keylessly; live Twitch chat only via step 6.
- **Hype words in the transcript**: needs transcription (below).

Candidates are 15–40 s windows (`--min`/`--max`), non-overlapping, snapped to
word boundaries when a transcript exists. Present each candidate with its time
range, why it scored, and its transcript line; recommend the best 3 with a hook
angle each. Drop spoilers, nudity, and anything leak-like before recommending.

### Transcription (optional, slow here)

faster-whisper runs on CPU in the venv. Default model `small`; override with
`--model tiny|base|small` or the `CLIPPER_WHISPER_MODEL` env var. The tiny
model is far faster and good enough for hype-word spotting, rougher for
captions. Measured numbers from the adaptation test are in
`~/workspace/clipper-adapt/ADAPTATION-NOTES.md`; as a rule, the more speech a
video has, the longer transcription takes, so long VODs should be scanned
with `--max-minutes`, a smaller model, or no transcription.

- `--no-transcribe` skips whisper entirely: loudness + heatmap + chat only.
  Candidates then have no transcript text, and cut.py will warn and cut without
  captions unless captions are supplied another way.
- If faster-whisper or the model download fails, moments.py says so and
  continues without the transcript signal. It never invents transcript text.

## Step 4: Cutting

```
CLIPPER_HOME=<campaign dir> ~/workspace/clipper-adapt/venv/bin/python scripts/cut.py jobs/<id> --pick <n> \
  --layout fill --hook "Hook text here"
```

Output: `jobs/<id>/edits/clip_<n>.mp4` plus a `clip_<n>.json` sidecar (source
URL, channel, hook) that check.py and the scoreboard use.

- 1080x1920, 30 fps, H.264 + AAC, loudness normalized to about -14 LUFS
  (single-pass loudnorm), faststart on.
- Layouts: `fill` (crop to fill the frame; default for gameplay), `blur` (full
  frame centered over a blurred copy; use when a crop would cut the action),
  `facecam` and `react` (cam panel on top, content below; `react` adds the big
  title on the seam via `--title`, box or outline style).
- `facecam`/`react` need `--cam x:y:w:h` as fractions of the source frame.
  There is **no automatic webcam detection in this version** (the original used
  OpenCV face tracking; unvalidated here, see the notes). Get the box once from
  a frame grab of the source and reuse it for that creator.
- Captions: `--captions word` (word-by-word, current word highlighted, groups of
  3), `bubble` (one speech-bubble line per group), or `none`. Slurs are always
  masked in burned captions; hard swears are masked unless `--allow-profanity`.
  Captions come only from the job's transcript; no transcript, no captions.
- Hook: `--hook "TEXT"` burns a hook box for the first ~2.6 s. Write hooks with
  step 5 first, then cut. Target length 7–30 s unless the campaign says
  otherwise; end on the payoff, trim dead air at the start.
- Verify the result before showing it: 1080x1920, hook visible in the first
  seconds, captions readable, audio present. Use ffprobe or ffmpeg-skill's
  check. Never overwrite the source video.

## Step 5: Hooks

Write 3 options per clip, mark your pick. Sentence case, 3–9 words for the hook
box. The clip must deliver what the hook promises; no clickbait.

Patterns that work:

- Number promise: "3 things you missed in this trailer" / "3 momen yang kamu lewatkan"
- Shock fact: "This car was hidden in plain sight" / "Mobil ini sembunyi di depan mata"
- Situation: "When the cops chase the wrong player" / "Pas polisi salah kejar orang"
- Negation: "You can't do this in the old game" / "Ini nggak bisa di game lamanya"
- Question: "Would you survive this chase?" / "Kamu bakal selamat nggak dari kejaran ini?"
- Name the creator when known: "Even [name] didn't see this coming" /
  "[Name] aja nggak nyangka bagian ini"

Reaction titles (react layout, shown the whole clip): creator name + reaction
verb + what happened, CAPS on 2–3 key words ("Rangga LOST IT at the final
play"). Describe what is on screen. Never invent a quote or an opinion for the
creator.

Avoid: bare labels ("Funny moment"), "wait for it", "you won't believe this",
fake urgency, CAPS everywhere, spoilers in the hook, and the word "official"
for fan or campaign content. One emoji at most. Do not reuse a hook within a
week; check the scoreboard.

## Step 6: Live mode (manual-assisted, unvalidated)

```
CLIPPER_HOME=<campaign dir> ~/workspace/clipper-adapt/venv/bin/python scripts/live.py <live-url> --minutes 60
```

Records a YouTube or Twitch live stream in 60 s segments and auto-cuts a clip
around each chat spike (YouTube chat via yt-dlp; Twitch chat via anonymous IRC,
no account). Spike clips land in `jobs/<id>/live/`; run moments/cut on them
afterwards.

Status: **the script is ported but has not been run against a live stream in
this setup yet.** Treat it as manual-assisted: confirm the stream is public and
not a leak or pirated copy before starting, note the creator for credit, watch
the output while it runs, and review every spike clip yourself. Do not promise
Rangga hands-free live clipping until a real run has been checked.

## Step 7: Rule check (before anything is shown as ready)

```
~/workspace/clipper-adapt/venv/bin/python scripts/check.py jobs/<id>/edits/clip_<n>.mp4 \
  --campaign <campaign dir>/campaign.md --caption "the exact caption text Rangga will post"
```

Checks, PASS/FAIL each: 1080x1920, ~30 fps, audio present, duration inside the
campaign's min/max, required hashtags and mention present in the caption, and
no banned terms (leak, play early, free download, crack, mod menu, money
glitch, AFK bot, and similar) in the hook or caption. Exit code 1 on any FAIL.

- On FAIL: fix the cause (re-cut, fix the caption) and re-run. Do not argue
  with a failed check.
- With no campaign file, check.py uses 7–60 s defaults and says plainly that no
  real rules check happened. A clip is not "checked" until it has passed
  against the actual campaign.md.
- Read the caption yourself too: it must credit the original creator, contain
  no invented facts, and not read as official. The script cannot judge that.

Only after every check passes: show Rangga the clip file, the caption, and the
credit line, and wait for his yes. **He posts it himself. Nothing in this skill
uploads or posts anything, ever.**

## Step 8: Learning loop

Per campaign, in its folder:

- Log every post when it goes out:
  `scripts/scoreboard.py --file <campaign dir>/scoreboard.csv add --clip clip_1 --platform tiktok --hook "..." --length 24 --credit "@creator" --test "hook-question"`
- Fill real numbers at the reads:
  `... read --clip clip_1 --at 24h --views 12000` and `--at 72h`. Payout only
  when the campaign actually shows one: `--payout 6.00`, or log it in
  `payouts.csv` with `scripts/payouts.py add ...` using the rate from
  campaign.md. **Real numbers only; a missing read stays blank, never guessed.**
- One test at a time: change one variable (hook style, length, posting time,
  caption length) and name it in `--test`. No verdict before 24 h; prefer the
  72 h read. Weekly: compare medians by hook style, length, and time slot;
  double down on what is above median, rework or drop what stayed below for a
  full week.

## Hard rules

1. Nothing is uploaded, posted, or submitted automatically. Rangga approves
   every clip and posts it himself.
2. Always credit the original creator, in the post caption (not burned into
   the video).
3. Campaign rates, budgets, and rules come only from the campaign page or from
   text Rangga pastes. Unknown stays `unknown`. No invented numbers, no
   earnings promises or projections presented as fact.
4. No leaks, no "play early", no piracy, no game-currency glitches or bots,
   no fake news, no invented quotes. Clip a creator only inside their campaign
   or with permission.
5. Never present the page or a clip as official or affiliated with the game
   publisher or the creator.
6. A missing signal (no heatmap, no chat, no transcript) is reported as
   missing, never faked.

## Not in this version

- GTA-specific databases from the original plugin (cheat-code lists, secrets
  maps) and its questions-to-posts and page playbook: dropped, they were
  content features for one game's fan page, not pipeline.
- The 5-language multilang pack (translated captions, stock-voice hooks):
  possible later add-on, not built.
- Automatic webcam detection for facecam/react layouts: the original's OpenCV
  face tracking was not ported; pass `--cam` fractions manually.
- Twitch VOD chat download: not possible keylessly (needs a persisted-query
  hash); use a TwitchDownloader chat.json via `--chat`, or live mode.
- Live mode: ported, unvalidated (step 6).

## Provenance

Adapted 2026-11-19 from Bodila51/gtavi-claudecode (MIT license, unofficial fan
project) — source kept at `~/workspace/clipper-adapt/source-repo/`. What was
ported, changed, dropped, and the end-to-end test evidence:
`~/workspace/clipper-adapt/ADAPTATION-NOTES.md`.
