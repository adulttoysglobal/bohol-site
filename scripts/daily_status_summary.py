#!/usr/bin/env python3
"""Read-only status aggregator for BOHOL daily SEO & GEO morning report."""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
JOURNAL_DIR = ROOT_DIR / "src" / "data" / "journal"
GSC_CACHE = ROOT_DIR / "src" / "data" / "gsc_live_cache.json"
PUBLISHER_SCRIPT = ROOT_DIR / "scripts" / "auto_seo_publisher.py"
DAILY_PUSH_LOG = ROOT_DIR / "scripts" / "daily_push.log"
AUTO_PUB_LOG = ROOT_DIR / "scripts" / "auto_publisher.log"


def run_cmd(args, encoding="utf-8"):
    try:
        res = subprocess.run(
            args,
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            encoding=encoding,
            errors="replace",
            timeout=15,
        )
        return res.stdout.strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def tail_file(path: Path, lines: int = 25) -> str:
    if not path.exists():
        return "(file not found)"
    content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(content[-lines:])


def main():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"REPORT_TIME_LOCAL: {now_str} (Asia/Shanghai)")

    # 1. Journal articles & remaining topics
    md_files = sorted(JOURNAL_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    existing_slugs = {p.stem for p in md_files}
    print(f"\n=== JOURNAL SUMMARY ===")
    print(f"TOTAL_ARTICLES: {len(md_files)}")
    print("LATEST_5_FILES:")
    for p in md_files[:5]:
        ts = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  - {ts} | {p.stem}")

    pool = []
    if PUBLISHER_SCRIPT.exists():
        src = PUBLISHER_SCRIPT.read_text(encoding="utf-8", errors="replace")
        slugs = re.findall(r'"slug"\s*:\s*"([^"]+)"', src)
        titles = re.findall(r'"title"\s*:\s*"([^"]+)"', src)
        pool.extend(list(zip(slugs, titles)))
    for pack_name in ("keyword_gap_topics_part1.json", "keyword_gap_topics_part2.json"):
        pack_path = ROOT_DIR / "scripts" / pack_name
        if pack_path.exists():
            try:
                items = json.loads(pack_path.read_text(encoding="utf-8"))
                for it in items:
                    pool.append((it.get("slug", ""), it.get("title", "")))
            except Exception:
                pass
    if pool:
        remaining = [(s, t) for s, t in pool if s and s not in existing_slugs]
        print(f"TOPIC_POOL_TOTAL: {len(pool)}")
        print(f"TOPIC_POOL_REMAINING: {len(remaining)}")
        for s, t in remaining[:5]:
            print(f"  - [PENDING] {s} | {t}")
        if len(remaining) > 5:
            print(f"  ... (+{len(remaining) - 5} more queued topics)")

    # 2. GSC Live Cache
    print("\n=== GSC LIVE CACHE ===")
    if GSC_CACHE.exists():
        data = json.loads(GSC_CACHE.read_text(encoding="utf-8", errors="replace"))
        auto_push = data.get("autoPushStatus", {})
        sa = data.get("searchAnalytics", {})
        print(f"LAST_PUSHED: {data.get('lastPushedDisplay')}")
        print(f"STATUS: {data.get('status')}")
        print(f"TOTAL_URLS_PUSHED: {auto_push.get('totalUrlsPushed')}")
        print(f"SITEMAPS_SUBMITTED: {auto_push.get('googleSitemapsSubmitted')}")
        print(f"INDEXING_API: {auto_push.get('googleIndexingApi', {}).get('status')}")
        print(f"DATE_RANGE: {sa.get('dateRange')}")
        print(f"IMPRESSIONS: {sa.get('totalImpressions')}")
        print(f"CLICKS: {sa.get('totalClicks')}")
        print(f"AVG_CTR: {sa.get('avgCtr')}%")
        print(f"AVG_POSITION: #{sa.get('avgPosition')}")
        print("TOP_PAGES:")
        for row in sa.get("pages", [])[:8]:
            key = row.get("keys", [""])[0]
            print(
                f"  - {key} | clicks={row.get('clicks')} | imp={row.get('impressions')} | pos=#{row.get('position', 0):.1f}"
            )
        print("TOP_QUERIES:")
        for row in sa.get("queries", [])[:8]:
            key = row.get("keys", [""])[0]
            print(
                f"  - {key} | clicks={row.get('clicks')} | imp={row.get('impressions')} | pos=#{row.get('position', 0):.1f}"
            )
    else:
        print("GSC cache missing.")

    # 3. Git log
    print("\n=== RECENT GIT COMMITS ===")
    print(run_cmd(["git", "log", "-n", "5", "--format=%cd | %h | %s", "--date=format:%Y-%m-%d %H:%M:%S"]))

    # 4. Windows Scheduled Tasks
    print("\n=== WINDOWS SCHEDULED TASKS ===")
    for task in ["BOHOL_Daily_Google_SEO_Push", "BOHOL_Auto_SEO_Publisher"]:
        out = run_cmd(["schtasks", "/query", "/tn", task, "/fo", "csv", "/v"], encoding="gbk")
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if len(lines) >= 2:
            vals = [v.strip('"') for v in lines[1].split('","')]
            labels = {2: "NextRun", 3: "Status", 5: "LastRun", 6: "LastResult"}
            print(f"Task: {task}")
            for idx, lbl in labels.items():
                if idx < len(vals):
                    print(f"  {lbl}: {vals[idx]}")
        else:
            print(f"Task: {task} -> {out}")

    # 5. Recent log tails
    print("\n=== DAILY_PUSH_LOG TAIL ===")
    print(tail_file(DAILY_PUSH_LOG, 15))
    print("\n=== AUTO_PUBLISHER_LOG TAIL ===")
    print(tail_file(AUTO_PUB_LOG, 22))


if __name__ == "__main__":
    main()
