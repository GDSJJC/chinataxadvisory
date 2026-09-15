#!/usr/bin/env python3
"""Queue a validated web package for future release.

Usage:
    python tools/schedule-insight.py --package <web-package.json> --article <web-article.html> --release-date YYYY-MM-DD

Validates with publish-insight.py --dry-run, then copies into
scheduled/<date>-<slug>/, updates scheduled/manifest.json, appends scheduled/LOG.md.
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
    def today_shanghai() -> str:
        return datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
except Exception:
    def today_shanghai() -> str:
        return datetime.utcnow().date().isoformat()

WEB_ROOT = Path(__file__).resolve().parent.parent
SCHED_DIR = WEB_ROOT / "scheduled"
MANIFEST = SCHED_DIR / "manifest.json"
LOG = SCHED_DIR / "LOG.md"


def load_manifest() -> dict:
    if MANIFEST.is_file():
        return json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    return {"queue": []}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Queue a post for scheduled release")
    ap.add_argument("--package", required=True)
    ap.add_argument("--article", required=True)
    ap.add_argument("--release-date", required=True, help="YYYY-MM-DD (Asia/Shanghai)")
    args = ap.parse_args(argv)

    try:
        datetime.strptime(args.release_date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: release-date must be YYYY-MM-DD: {args.release_date!r}")
        return 1
    if args.release_date < today_shanghai():
        print(f"ERROR: release-date {args.release_date} is in the past (today {today_shanghai()} Shanghai)")
        return 1

    pkg = json.loads(Path(args.package).read_text(encoding="utf-8-sig"))
    slug = str(pkg.get("slug", "")).strip()
    if not slug:
        print("ERROR: web-package is missing slug")
        return 1
    if str(pkg.get("publish_date", "")).strip() != args.release_date:
        print(f"ERROR: package publish_date {pkg.get('publish_date')!r} must equal --release-date {args.release_date!r}")
        return 1

    # Validate with the live publisher (dry-run). Fails if slug exists, hero missing, etc.
    r = subprocess.run(
        [sys.executable, str(WEB_ROOT / "tools" / "publish-insight.py"),
         "--package", args.package, "--article", args.article, "--dry-run"],
        capture_output=True, text=True,
    )
    print(r.stdout, end="")
    if r.returncode != 0:
        print(r.stderr, end="")
        print("ERROR: package failed validation; not queued")
        return 1

    dirname = f"{args.release_date}-{slug}"
    dest = SCHED_DIR / dirname
    if dest.exists():
        print(f"ERROR: queue entry already exists: scheduled/{dirname}/")
        return 1
    if (WEB_ROOT / "blog" / slug).exists():
        print(f"ERROR: blog/{slug}/ already live; unpublish first or pick another slug")
        return 1

    dest.mkdir(parents=True)
    shutil.copy2(args.package, dest / "web-package.json")
    shutil.copy2(args.article, dest / "web-article.html")

    man = load_manifest()
    man.setdefault("queue", [])
    if any(e.get("slug") == slug and e.get("status") == "queued" for e in man["queue"]):
        print(f"ERROR: slug already queued: {slug}")
        shutil.rmtree(dest)
        return 1
    man["queue"].append({
        "dir": dirname,
        "slug": slug,
        "release_date": args.release_date,
        "status": "queued",
        "added_at": today_shanghai(),
        "title": str(pkg.get("title", "")).strip(),
    })
    man["queue"].sort(key=lambda e: (e.get("release_date", ""), e.get("slug", "")))
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"| {today_shanghai()} | {slug} | {args.release_date} | queued |\n")

    print(f"Queued scheduled/{dirname}/ for {args.release_date} (Shanghai).")
    print("Daily Action will publish it automatically; no further action needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
