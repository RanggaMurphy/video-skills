"""Cut one candidate into a finished vertical clip.

1080x1920, 30 fps, word-by-word burned captions (slurs and swears masked), hook box in the first seconds,
loudness normalised to -14 LUFS. Writes jobs/<id>/edits/clip_<n>.mp4 + .json (metadata for check.py).

usage: python cut.py jobs/<id> --pick 1 [--layout fill|blur|facecam|react] [--hook "TEXT"]
                     [--cam x:y:w:h] [--title "TEXT" --title-style box|outline --title-secs 0]
                     [--captions word|bubble|none] [--start S --end S]

Layouts:
  fill     crop the video to fill the 9:16 frame (default for gameplay)
  blur     full video centered over a blurred copy of itself
  facecam  the cam region (given with --cam as fractions x:y:w:h) on top, game below
  react    face on top (730 px panel), game below, big title on the seam (--title)

Adapted from Bodila51/gtavi-claudecode (MIT). Changes for this environment:
- Fonts: Liberation Sans (installed here) instead of Arial Black / Arial.
- --cam auto (OpenCV face detection) is NOT in this version; pass the cam box
  as fractions. Auto-detection is listed as unvalidated in the skill notes.
- The OpenCV game-crop offset picker was dropped (cv2 dependency).
- Captions are skipped with a warning when the job has no transcript.json
  (moments.py run with --no-transcribe); the clip is still cut.
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import load_json, run, save_json, tool

W, H = 1080, 1920
FONT = "Liberation Sans"


def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


import re as _re
_SLURS = _re.compile(r"\b(nigg\w*|n[i1]gg?a\w*|f[a@]gg?\w*|retard\w*|tranny\w*|chink\w*|spic\w*|kike\w*)\b", _re.I)


_SWEARS = _re.compile(r"\b(fuck\w*|motherfuck\w*|shit\w*|bitch\w*|cunt\w*|dick\w*|pussy\w*|asshole\w*|bastard\w*|whore\w*|slut\w*)\b", _re.I)


def _mask(m):
    w = m.group(0)
    return w[0] + '*' * (len(w) - 1)


def clean(s, profanity=False):
    """Slurs are always masked (n-word -> n****); hard swears too unless profanity=True."""
    s = _SLURS.sub(_mask, s)
    return s if profanity else _SWEARS.sub(_mask, s)


def esc(s):
    return s.replace("\\", "").replace("{", "(").replace("}", ")").replace("\n", " ")


def wrap(text, width):
    lines, cur = [], ''
    for wd in text.split():
        if cur and len(cur) + 1 + len(wd) > width:
            lines.append(cur); cur = wd
        else:
            cur = (cur + ' ' + wd).strip()
    return lines + ([cur] if cur else [])


def build_ass(words, s0, e0, hook, cap_y, title=None, caps='word', profanity=False):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},92,&H00FFFFFF,&H0000E5FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1
Style: Hook,{FONT},68,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,18,0,8,70,70,170,1
Style: TitleBox,{FONT},66,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1
Style: TitleOut,{FONT},80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,9,2,8,50,50,0,1
Style: Bubble,{FONT},58,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,16,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    ws = [dict(w, w=clean(w["w"], profanity)) for w in words if s0 <= w["s"] < e0 and w["w"]]
    # groups of up to 3 words, break on punctuation or pauses
    groups, cur = [], []
    for w in ws:
        if cur and (len(cur) == 3 or w["s"] - cur[-1]["e"] > 0.6 or cur[-1]["w"][-1:] in ".?!,"):
            groups.append(cur); cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    hook_end = 2.6 if hook else 0
    for gi, g in enumerate(groups):
        g_end = groups[gi + 1][0]["s"] if gi + 1 < len(groups) else g[-1]["e"] + 0.4
        g_end = min(g_end, g[-1]["e"] + 0.8)
        for k, w in enumerate(g):
            a = w["s"] - s0; b = (g[k + 1]["s"] - s0) if k + 1 < len(g) else g_end - s0
            if b <= a:
                continue
            parts = []
            for j, x in enumerate(g):
                t = esc(x["w"].upper())
                parts.append("{\\c&H0000E5FF&}" + t + "{\\c&H00FFFFFF&}" if j == k else t)
            pop = "{\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)}" if k == 0 else ""
            if caps == 'bubble':
                if k == 0:
                    txt = esc(' '.join(x['w'] for x in g)).strip()
                    txt = txt[:1].upper() + txt[1:]
                    ev.append(f"Dialogue: 0,{ts(a)},{ts(g_end - s0)},Bubble,,0,0,0,,{{\\pos({W // 2},{cap_y})}}{pop}{txt}")
                continue
            ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\pos({W // 2},{cap_y})}}{pop}{' '.join(parts)}")
    if title:  # reaction title: (style, text, y, seconds)
        st, text, ty, secs = title
        end = (e0 - s0) if secs <= 0 else secs
        lines = wrap(esc(text), 26 if st == 'box' else 24)
        body = '\\N'.join(lines)
        if st == 'box':
            ev.append(f"Dialogue: 2,{ts(0)},{ts(end)},TitleBox,,0,0,0,,{{\\pos({W // 2},{ty})}}{body}")
        else:
            ev.append(f"Dialogue: 2,{ts(0)},{ts(end)},TitleOut,,0,0,0,,{{\\pos({W // 2},{ty})\\an8}}{body}")
        hook = ''
    if hook:
        ev.append(f"Dialogue: 1,{ts(0)},{ts(hook_end)},Hook,,0,0,0,,{{\\fad(0,180)\\fscx92\\fscy92\\t(0,120,\\fscx100\\fscy100)}}{esc(hook)}")
    return hdr + "\n".join(ev) + "\n"


CAP_Y = {"fill": 1380, "blur": 1460, "facecam": 1120, "react": 1560}
TOP = 730  # react layout: face panel height = seam y (even)
GAME_H = H - TOP  # 1190


def even(n):
    return int(n) // 2 * 2


def video_filter(layout, cam, ass, band=None, cam_side='right', src=None):
    """Layout + burned-caption filter graph ending in [vo]."""
    if layout == "fill":
        v = f"[0:v]scale=-2:{H},crop={W}:{H}[v]"
    elif layout == "blur":
        v = (f"[0:v]split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=24:2,eq=brightness=-0.08[bg];"
             f"[b]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-80[v]")
    elif layout == 'react':
        sw, sh = src
        x, y, w, h = map(float, cam.split(':'))
        cw, chh = even(sw * w), even(sh * h)
        top = f"crop={cw}:{chh}:{even(sw * x)}:{even(sh * y)}"
        gw = even(sw * GAME_H / sh) if sw * GAME_H / sh >= W else W
        gx = (gw - W) if cam_side == 'left' else 0  # keep the side opposite the cam in frame
        v = (f"[0:v]split[a][b];[a]{top},scale={W}:{TOP}:force_original_aspect_ratio=increase,crop={W}:{TOP},setsar=1[cam];"
             f"[b]scale={gw}:{GAME_H},crop={W}:{GAME_H}:{even(gx)}:0,setsar=1[game];[cam][game]vstack[v]")
        if band:
            y0, bh, secs = band
            en = f":enable='lte(t,{secs})'" if secs > 0 else ''
            v = v[:-3] + f"[v0];[v0]drawbox=x=0:y={y0}:w=iw:h={bh}:color=white@1:t=fill{en}[v]"
    else:  # facecam (panel heights must be even, or the stack comes out 1080x1918)
        x, y, w, h = map(float, cam.split(":"))
        cam_h = even(H * 0.38)
        v = (f"[0:v]split[a][b];[a]crop=iw*{w}:ih*{h}:iw*{x}:ih*{y},scale={W}:{cam_h}:force_original_aspect_ratio=increase,"
             f"crop={W}:{cam_h}[cam];[b]scale=-2:{H - cam_h},crop={W}:{H - cam_h}[game];[cam][game]vstack[v]")
    sub = str(ass).replace("\\", "/").replace(":", "\\:")
    return v + f";[v]fps=30,subtitles='{sub}'[vo]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job"); ap.add_argument("--pick", type=int, default=1)
    ap.add_argument("--layout", choices=["fill", "blur", "facecam", "react"], default="blur")
    ap.add_argument("--title", default="", help="reaction title, e.g. 'Rangga LOST IT at the final play'")
    ap.add_argument("--title-style", choices=["box", "outline"], default="box")
    ap.add_argument("--title-secs", type=float, default=0, help="0 = whole clip")
    ap.add_argument("--captions", choices=["word", "bubble", "none"], default="word")
    ap.add_argument("--hook", default="")
    ap.add_argument("--allow-profanity", action="store_true", help="keep swear words in captions (slurs are always masked)")
    ap.add_argument("--cam", default="", help="cam region as fractions x:y:w:h (required for facecam/react; auto-detection not in v1)")
    ap.add_argument("--start", type=float); ap.add_argument("--end", type=float)
    a = ap.parse_args()
    d = Path(a.job); c = load_json(d / "candidates.json")
    pick = next(x for x in c["candidates"] if x["n"] == a.pick)
    s0 = a.start if a.start is not None else pick["start"]; e0 = a.end if a.end is not None else pick["end"]
    tpath = d / "transcript.json"
    words = load_json(tpath) if tpath.exists() else []
    out = d / "edits"; out.mkdir(exist_ok=True)
    layout, cam, side = a.layout, a.cam, 'right'
    if layout in ('react', 'facecam'):
        if not cam:
            sys.exit(f"layout {layout} needs --cam x:y:w:h (fractions of the source frame). "
                     "Auto-detection is not in this version; find the cam box once from a frame grab.")
        side = 'left' if float(cam.split(':')[0]) + float(cam.split(':')[2]) / 2 < 0.5 else 'right'
    cap_y = CAP_Y[layout]
    title, band = None, None
    if a.title and layout == 'react':
        n = len(wrap(a.title, 26 if a.title_style == 'box' else 24))
        if a.title_style == 'box':
            bh = n * 78 + 44
            band = (TOP - bh // 2, bh, a.title_secs)
            title = ('box', a.title, TOP, a.title_secs)
        else:
            title = ('outline', a.title, TOP + 40, a.title_secs)
    ass = out / f"clip_{a.pick}.ass"
    caps = a.captions
    if caps != 'none' and not words:
        print("warning: no transcript for this job, cutting without captions", file=sys.stderr)
        caps = 'none'
    cap_words = words if caps != 'none' else []
    ass.write_text(build_ass(cap_words, s0, e0, a.hook, cap_y, title=title, caps=caps, profanity=a.allow_profanity), encoding="utf-8")
    src = None
    if layout == 'react':
        from common import ffprobe
        vs = [x for x in ffprobe(c['source'])['streams'] if x.get('codec_type') == 'video'][0]
        src = (int(vs['width']), int(vs['height']))
    v = video_filter(layout, cam, ass, band=band, cam_side=side, src=src)
    mp4 = out / f"clip_{a.pick}.mp4"
    run([tool("ffmpeg"), "-y", "-v", "error", "-ss", f"{s0:.2f}", "-to", f"{e0:.2f}", "-i", c["source"],
         "-filter_complex", v, "-map", "[vo]", "-map", "0:a?", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
         "-ar", "48000", "-movflags", "+faststart", str(mp4)])
    info = c.get("info", {})
    save_json(out / f"clip_{a.pick}.json", {"file": str(mp4), "start": s0, "end": e0, "layout": layout, "hook": a.hook or a.title, "title": a.title, "cam": cam,
                                            "source_url": info.get("webpage_url"), "source_title": info.get("title"),
                                            "source_channel": info.get("channel") or info.get("uploader")})
    print(mp4)


if __name__ == "__main__":
    main()
