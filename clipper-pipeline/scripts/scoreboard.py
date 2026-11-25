"""Campaign scoreboard: one row per posted clip, views filled in at 24h / 72h reads.

Only real numbers Rangga reports go in. Blank means "not read yet", never zero-fill a guess.

usage: python scoreboard.py --file CAMPAIGN_DIR/scoreboard.csv add --clip clip_1 --platform tiktok --hook "TEXT" --length 24 [--credit "@creator"] [--test "hook-style-a"]
       python scoreboard.py --file CAMPAIGN_DIR/scoreboard.csv read --clip clip_1 --at 24h --views 12000 [--payout 6.00]
       python scoreboard.py --file CAMPAIGN_DIR/scoreboard.csv show

New file for this adaptation (the source repo kept the scoreboard as a manual CSV).
"""
import argparse, csv, sys
from datetime import date
from pathlib import Path

FIELDS = ["date", "clip", "platform", "hook", "length_sec", "credit", "test_name",
          "views_24h", "views_72h", "payout", "notes"]


def rows(path):
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, rs):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerows(rs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("add")
    a_.add_argument("--clip", required=True); a_.add_argument("--platform", required=True)
    a_.add_argument("--hook", default=""); a_.add_argument("--length", type=float, default=0)
    a_.add_argument("--credit", default=""); a_.add_argument("--test", default=""); a_.add_argument("--notes", default="")
    r_ = sub.add_parser("read")
    r_.add_argument("--clip", required=True); r_.add_argument("--at", choices=["24h", "72h"], required=True)
    r_.add_argument("--views", type=int, required=True); r_.add_argument("--payout", default="")
    sub.add_parser("show")
    a = ap.parse_args()

    rs = rows(a.file)
    if a.cmd == "add":
        rs.append({"date": date.today().isoformat(), "clip": a.clip, "platform": a.platform, "hook": a.hook,
                   "length_sec": f"{a.length:g}", "credit": a.credit, "test_name": a.test,
                   "views_24h": "", "views_72h": "", "payout": "", "notes": a.notes})
        write(a.file, rs)
        print(f"added {a.clip} ({a.platform})")
    elif a.cmd == "read":
        hit = [r for r in rs if r["clip"] == a.clip]
        if not hit:
            sys.exit(f"no row for clip {a.clip}")
        for r in hit:
            r["views_" + a.at] = str(a.views)
            if a.payout:
                r["payout"] = a.payout
        write(a.file, rs)
        print(f"{a.clip}: views_{a.at} = {a.views}")
    else:
        if not rs:
            print("scoreboard is empty"); return
        for r in rs:
            print(f"{r['date']}  {r['clip']:10} {r['platform']:10} 24h={r['views_24h'] or '-':>8} 72h={r['views_72h'] or '-':>8} "
                  f"payout={r['payout'] or '-':>8}  test={r['test_name'] or '-'}  hook={r['hook'][:40]}")


if __name__ == "__main__":
    main()
