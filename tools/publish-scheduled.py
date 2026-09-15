#!/usr/bin/env python3
"""Publish due scheduled posts (release_date <= today Shanghai).

Usage:
    python tools/publish-scheduled.py [--today YYYY-MM-DD] [--dry-run]

Default today is Asia/Shanghai. Due items run through
tools/publish-insight.py, then their scheduled/ folder is removed,
manifest.json marked live, and scheduled/LOG.md appended.
LinkedIn kits are preserved under scheduled/_published/.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    def shanghai_today() -> str:
        return datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
except Exception:
    def shanghai_today() -> str:
        return datetime.utcnow().date().isoformat()

WEB_ROOT = Path(__file__).resolve().parent.parent
SCHED_DIR = WEB_ROOT / "scheduled"
MANIFEST = SCHED_DIR / "manifest.json"
LOG = SCHED_DIR / "LOG.md"
PUBLISHED = SCHED_DIR / "_published"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Publish due scheduled posts")
    ap.add_argument("--today", default="", help="Override today (YYYY-MM-DD, Shanghai)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    today = args.today.strip() or shanghai_today()
    try:
        datetime.strptime(today, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: --today must be YYYY-MM-DD: {today!r}")
        return 1

    if not MANIFEST.is_file():
        print("No manifest; nothing due.")
        return 0
    man = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    queue = man.get("queue", [])
    due = sorted(
        (e for e in queue if e.get("status") == "queued" and e.get("release_date", "") <= today),
        key=lambda e: (e.get("release_date", ""), e.get("slug", "")),
    )
    if not due:
        print(f"No due posts for {today} (Shanghai).")
        return 0

    print(f"Due for {today} (Shanghai): {len(due)}")
    for e in due:
        print(f" - {e.get('release_date')} {e.get('slug')}")

    if args.dry_run:
        for e in due:
            d = SCHED_DIR / e["dir"]
            r = subprocess.run(
                [sys.executable, str(WEB_ROOT / "tools" / "publish-insight.py"),
                 "--package", str(d / "web-package.json"),
                 "--article", str(d / "web-article.html"), "--dry-run"],
                capture_output=True, text=True,
            )
            print(r.stdout, end="")
            if r.returncode != 0:
                print(r.stderr, end="")
                print(f"ERROR: dry-run failed for {e.get('slug')}; fix before release")
                return 1
        print("DRY RUN ok: all due items validate.")
        return 0

    PUBLISHED.mkdir(parents=True, exist_ok=True)
    published: list[str] = []
    for e in due:
        slug = e["slug"]
        d = SCHED_DIR / e["dir"]
        if (WEB_ROOT / "blog" / slug).exists():
            print(f"ERROR: blog/{slug}/ already exists; leaving queued for manual review")
            continue
        kit_out = PUBLISHED / f"linkedin-{slug}.txt"
        r = subprocess.run(
            [sys.executable, str(WEB_ROOT / "tools" / "publish-insight.py"),
             "--package", str(d / "web-package.json"),
             "--article", str(d / "web-article.html"),
             "--linkedin-out", str(kit_out)],
            capture_output=True, text=True,
        )
        print(r.stdout, end="")
        if r.returncode != 0:
            print(r.stderr, end="")
            print(f"ERROR: publish failed for {slug}; leaving queued")
            return 1
        # Default kit location is next to the package (inside queue dir);
        # if --linkedin-out was honoured the file is already preserved.
        default_kit = d / f"linkedin-{slug}.txt"
        if default_kit.is_file() and not kit_out.is_file():
            shutil.move(str(default_kit), str(kit_out))
        shutil.rmtree(d)
        e["status"] = "live"
        e["published_at"] = today
        published.append(slug)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"| {today} | {slug} | {e.get('release_date')} | published |\n")
        print(f"Published {slug}; removed scheduled/{e['dir']}/")

    man["queue"] = [e for e in queue if e.get("status") == "queued"] + \
                   [e for e in queue if e.get("status") != "queued"]
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Done: {len(published)} published.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
