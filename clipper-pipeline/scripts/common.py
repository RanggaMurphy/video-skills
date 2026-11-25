"""Shared helpers: paths, tool lookup, yt-dlp and ffmpeg wrappers.

Adapted from Bodila51/gtavi-claudecode (MIT). Changes: the work root env var is
CLIPPER_HOME (was CLIP_DESK_HOME); everything else is the original logic.
Run these scripts with the venv python: ~/workspace/clipper-adapt/venv/bin/python
"""
import hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(os.environ.get("CLIPPER_HOME", Path.cwd()))
JOBS = ROOT / "jobs"


def tool(name):
    p = shutil.which(name)
    if not p:
        sys.exit(f"{name} not found. ffmpeg/ffprobe must be on PATH.")
    return p


def run(cmd, check=True, capture=False):
    r = subprocess.run(cmd, check=False, text=True, encoding="utf-8", errors="replace",
                       stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)
    if check and r.returncode != 0:
        msg = (r.stderr or "")[-1500:] if capture else ""
        sys.exit(f"command failed ({r.returncode}): {' '.join(map(str, cmd))[:200]}\n{msg}")
    return r


_YTDLP_WRAP = ("import truststore; truststore.inject_into_ssl(); import sys; "
               "sys.argv = ['yt-dlp'] + sys.argv[1:]; from yt_dlp import main; main()")


def ytdlp_base():
    """yt-dlp command prefix, adapted to this VM (found in the 2026-11-19 test):
    - The VM's HTTPS proxy CA is in the system trust store but not in certifi's
      bundle, so plain yt-dlp fails with CERTIFICATE_VERIFY_FAILED. When the
      truststore package is available, yt-dlp is started through a wrapper that
      injects the system store (the same trick the source repo used in-process).
    - YouTube bot-blocks this VM's IP for the default player client; the
      android client is allowed through, so it is set as the default. The
      extractor-arg only affects the youtube extractor.
    """
    import importlib.util
    if importlib.util.find_spec("yt_dlp"):
        if importlib.util.find_spec("truststore"):
            exe = [sys.executable, "-c", _YTDLP_WRAP]
        else:
            exe = [sys.executable, "-m", "yt_dlp"]
    else:
        exe = [tool("yt-dlp")]
    base = exe + ["--no-warnings", "--no-progress",
                  "--extractor-args", "youtube:player_client=android"]
    if sys.platform == "win32":
        base += ["--compat-options", "no-certifi"]  # use the Windows certificate store
    return base


def ytdlp_json(url, extra=()):
    r = run(ytdlp_base() + ["-J", *extra, url], capture=True)
    return json.loads(r.stdout)


def is_url(s):
    return bool(re.match(r"https?://", s))


def job_dir(src):
    key = hashlib.sha1(src.encode()).hexdigest()[:8]
    stem = re.sub(r"[^a-z0-9]+", "-", Path(src).stem.lower() if not is_url(src) else src.split("v=")[-1].split("/")[-1].lower())[:24].strip("-")
    d = JOBS / f"{stem or 'job'}-{key}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ffprobe(path):
    r = run([tool("ffprobe"), "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
             "-of", "json", str(path)], capture=True)
    return json.loads(r.stdout)


def save_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
