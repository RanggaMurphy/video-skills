# Jedag-Jedug Template — Beat-Synced TikTok Edit

Turn any clip into a jedag-jedug edit: hard jump cuts on every beat,
snap punch-zoom with shake on each beat head, flash + saturation pulse,
and a punchy kick/bass track when no music is supplied.

## Requirements

- ffmpeg + ffprobe on PATH
- python3 with numpy
- The `jedag.py` script from this folder

## Run it

```bash
python3 jedag.py --input VIDEO.mp4 --output OUT.mp4 --bpm 130 --dur 8
```

Options:

- `--bpm` beat grid of the song (default 130). Match the actual song BPM
  or the punches drift off the beat.
- `--dur` output length in seconds (default 8).
- `--music SONG.mp3` use a real song instead of the synthesized beat
  track. The edit grid still follows `--bpm`, so set it to the song's BPM.
- `--w / --h` output size (default 720x1280, vertical 9:16).

## How it works

1. The source is chopped into one segment per beat. Segments hop around
   the source timeline (golden-ratio jumps) so every beat is a hard cut
   to a different moment. Do NOT use smooth continuous zooms, they read
   as a slideshow, not jedag-jedug.
2. Each segment gets a snap zoom: scale starts at ~1.31 on the beat head
   and decays exponentially to ~1.07 (zoompan, `z='1.07+0.24*exp(-on*0.85)'`).
3. Shake: x/y jitter for the first 4 frames after each hit
   (`lt(on,4)*sin(on*36+seed)*9`), seed varies per segment.
4. One global pass adds a brightness flash and saturation pulse at every
   beat head: `eq=brightness='0.26*exp(-18*mod(t,BEAT))'`.
5. Without `--music`, a beat track is synthesized with numpy: distorted
   kick (sine sweep 152->42 Hz through tanh), clap on beats 2 and 4,
   bass boom pattern A1 A1 C2 G1, hats on offbeats.

## Tuning notes

- Source footage matters more than effects: action, explosions, gameplay,
  or fast movement works. Calm/slow footage makes the edit feel dead no
  matter how strong the effects are.
- If cuts feel chaotic, lower the hop distance in `build_filter`
  (the `2.618` multiplier) or raise it for more chaos.
- Punch strength is the `0.24` in the zoom expression; shake amplitude
  is the `*9` terms; flash strength is `0.26`.
- ffmpeg expressions inside zoompan cannot use `on<4`; write `lt(on,4)`.
