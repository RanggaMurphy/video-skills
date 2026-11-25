#!/usr/bin/env python3
"""Jedag-jedug template v2 (TikTok/CapCut style).

What makes it jedag-jedug:
- HARD jump cuts on every beat, hopping around the source timeline
- Snap zoom: instant punch-in on the beat head, fast decay (not a slow zoom)
- Shake: position jitter for the first frames after each beat hit
- Flash + saturation pulse on every beat head
- Punchy distorted kick / bass track when no --music is given

Usage:
  python3 jedag.py --input VIDEO --output OUT.mp4 [--bpm 130] [--dur 8]
                   [--music SONG] [--w 720] [--h 1280]
"""
import argparse, subprocess, sys, wave
import numpy as np


def synth_beat(path, bpm, dur, sr=44100):
    n = int(sr * dur)
    beat = 60.0 / bpm
    mix = np.zeros(n)
    rng = np.random.default_rng(11)
    # distorted kick: sine sweep with tanh drive
    klen = int(sr * 0.16)
    kt = np.arange(klen) / sr
    freq = 42 + 110 * np.exp(-kt * 34)
    phase = np.cumsum(freq) / sr * 2 * np.pi
    kick = np.tanh(np.sin(phase) * np.exp(-kt * 18) * 2.4)
    # clap: filtered noise burst, beats 2 and 4 of each bar
    clen = int(sr * 0.09)
    ct = np.arange(clen) / sr
    clap = rng.standard_normal(clen) * np.exp(-ct * 46) * (0.6 + 0.4 * np.sin(2 * np.pi * 1700 * ct))
    # bass boom notes A1 A1 C2 G1
    notes = [55.0, 55.0, 65.41, 49.0]
    blen = int(sr * 0.24)
    bt = np.arange(blen) / sr
    # hat offbeats
    hlen = int(sr * 0.03)
    hat = rng.standard_normal(hlen) * np.exp(-np.arange(hlen) / sr * 170)
    nbeats = int(dur / beat)
    for i in range(nbeats):
        s = int(i * beat * sr)
        mix[s:s + klen] += kick * 1.0
        if i % 4 in (1, 3):
            mix[s:s + clen] += clap * 0.5
        bass = np.sin(2 * np.pi * notes[i % 4] * bt) * np.exp(-bt * 8)
        mix[s:s + blen] += bass * 0.6
        hs = s + int(beat / 2 * sr)
        if hs + hlen < n:
            mix[hs:hs + hlen] += hat * 0.35
    mix = np.tanh(mix * 1.15)
    mix = mix / max(1e-6, np.max(np.abs(mix))) * 0.92
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def build_filter(bpm, dur, w, h, src_dur, fps=30):
    beat = 60.0 / bpm
    frames = int(round(beat * fps))
    nseg = int(dur / beat)
    parts, labels = [], []
    for i in range(nseg):
        # hop around the source: golden-ratio jumps keep cuts energetic
        st = (i * 2.618) % max(1.0, src_dur - beat - 0.1)
        seed = i * 7 + 3
        parts.append(
            f"[0:v]trim=start={st:.3f}:duration={beat:.4f},setpts=PTS-STARTPTS,"
            f"fps={fps},scale={int(w*1.6)}:{int(h*1.6)},"
            f"zoompan=z='1.07+0.24*exp(-on*0.85)':"
            f"x='iw/2-(iw/zoom/2)+lt(on,4)*sin(on*36+{seed})*9':"
            f"y='ih/2-(ih/zoom/2)+lt(on,4)*cos(on*31+{seed})*9':"
            f"d={frames}:s={w}x{h}:fps={fps}[s{i}]")
        labels.append(f"[s{i}]")
    parts.append("".join(labels) + f"concat=n={nseg}:v=1:a=0[cc]")
    parts.append(
        f"[cc]eq=brightness='0.26*exp(-18*mod(t,{beat:.4f}))'"
        f":saturation='1.3+0.5*exp(-18*mod(t,{beat:.4f}))'[v]")
    return ";".join(parts)


def probe_dur(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration', '-of', 'csv=p=0', path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--bpm', type=float, default=130.0)
    ap.add_argument('--dur', type=float, default=8.0)
    ap.add_argument('--music', default=None)
    ap.add_argument('--w', type=int, default=720)
    ap.add_argument('--h', type=int, default=1280)
    a = ap.parse_args()

    audio = a.music if a.music else '/tmp/jedag_beat2.wav'
    if not a.music:
        synth_beat(audio, a.bpm, a.dur + 0.5)

    fc = build_filter(a.bpm, a.dur, a.w, a.h, probe_dur(a.input))
    cmd = ['ffmpeg', '-y', '-v', 'error',
           '-i', a.input, '-i', audio,
           '-filter_complex', fc,
           '-map', '[v]', '-map', '1:a',
           '-t', f'{a.dur:.2f}',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest',
           a.output]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:]); sys.exit(1)
    print('OK ->', a.output)


if __name__ == '__main__':
    main()
