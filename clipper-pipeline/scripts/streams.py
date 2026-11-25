"""Find live streams about a topic, ranked by concurrent viewers.

usage: python streams.py --query "topic or game" --limit 20 --out streams.md
YouTube always. Twitch: keyless public GQL by category name (the --query is used
as the Twitch category; for a creator name, search YouTube or open the channel
directly). Kick is tried once, skipped silently on failure.
Viewer counts are exactly what the platform returned at run time.

Adapted from Bodila51/gtavi-claudecode (MIT). Changes: the Twitch lookup no
longer hardcodes one game; the optional Helix path (needs TWITCH_CLIENT_ID and
TWITCH_TOKEN) was dropped because this setup uses no API keys.
"""
import argparse, json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote_plus
sys.path.insert(0, str(Path(__file__).parent))
from common import ytdlp_base, ytdlp_json, run

try:  # this VM's proxy CA lives in the system store, not in certifi's bundle
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass


def fmt_dur(sec):
    if not sec or sec < 0:
        return ""
    sec = int(sec)
    return f"{sec // 3600}h{sec % 3600 // 60:02d}m"


def youtube(query, limit):
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}&sp=EgJAAQ%253D%253D"
    r = run(ytdlp_base() + ["--flat-playlist", "-J", "--playlist-end", str(limit), url], capture=True, check=False)
    if r.returncode != 0 or not r.stdout.strip():
        print(f"youtube search failed: {(r.stderr or '')[-300:]}", file=sys.stderr)
        return []
    ids = []
    for e in json.loads(r.stdout).get("entries") or []:
        if e and e.get("id"):
            ids.append(e.get("url") or f"https://www.youtube.com/watch?v={e['id']}")

    def one(u):
        try:
            return ytdlp_json(u)
        except BaseException:  # run() calls sys.exit on failure
            return None

    with ThreadPoolExecutor(max_workers=8) as ex:
        infos = list(ex.map(one, ids))
    now = time.time(); out = []
    for i in infos:
        if not i or not i.get("is_live"):
            continue
        start = i.get("release_timestamp") or i.get("timestamp")
        out.append({"platform": "YouTube", "channel": i.get("channel") or i.get("uploader") or "",
                    "title": i.get("title") or "", "url": i.get("webpage_url") or "",
                    "viewers": i.get("concurrent_view_count"), "live_for": fmt_dur(now - start) if start else ""})
    return out


def twitch_nokey(game, limit=20):
    """No account/API key: Twitch public web GQL (see twitch.py)."""
    import twitch as tw
    try:
        rows = tw.top_streams(game, limit)
    except Exception as e:
        print(f"twitch (no key) failed: {e}", file=sys.stderr)
        return []
    now = time.time()
    return [{"platform": "Twitch", "channel": r["login"], "title": r["title"], "url": r["url"], "viewers": r["viewers"],
             "live_for": fmt_dur(now - tw.started_ts(r["created_at"])) if tw.started_ts(r["created_at"]) else ""} for r in rows]


def kick(query):
    """Public API is often blocked; one try, silent on any failure."""
    try:
        import requests
        r = requests.get("https://kick.com/api/v2/channels", params={"query": query}, timeout=8,
                         headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return []
        data = r.json()
        items = data if isinstance(data, list) else data.get("data", [])
        return [{"platform": "Kick", "channel": c.get("slug", ""), "title": (c.get("livestream") or {}).get("session_title", ""),
                 "url": f"https://kick.com/{c.get('slug', '')}", "viewers": (c.get("livestream") or {}).get("viewer_count"),
                 "live_for": ""} for c in items if isinstance(c, dict) and c.get("livestream")]
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True); ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--out", default="streams.md")
    a = ap.parse_args()
    sections = [("YouTube", youtube(a.query, a.limit))]
    t = twitch_nokey(a.query, a.limit)
    if t:
        sections.append(("Twitch", sorted(t, key=lambda r: r["viewers"] or -1, reverse=True)[:a.limit]))
    k = kick(a.query)
    if k:
        sections.append(("Kick", k))
    stamp = time.strftime("%Y-%m-%d %H:%M")
    md = [f"# Live streams: {a.query}", f"Checked {stamp}. Viewer counts are as returned at that moment.", ""]
    for name, rows in sections:
        rows = sorted(rows, key=lambda r: r["viewers"] or -1, reverse=True)
        md += [f"## {name}", ""]
        if not rows:
            md += ["No live streams found.", ""]
            continue
        md += ["| # | Channel | Title | Viewers | Live for | URL |", "|---|---|---|---|---|---|"]
        for n, r in enumerate(rows, 1):
            v = "" if r["viewers"] is None else r["viewers"]
            md.append(f"| {n} | {r['channel']} | {r['title'].replace('|', '/')} | {v} | {r['live_for']} | {r['url']} |")
            print(f"{name:8} {str(v):>7}  {r['channel'][:24]:24} {r['title'][:50]:50} {r['url']}")
        md.append("")
    Path(a.out).write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
