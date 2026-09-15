# Scheduled queue — publishing plan

One article per month. Drafts wait here until their release date, then the
daily Action publishes them automatically.

## How it works

1. Queue: `python tools/schedule-insight.py --package <web-package.json> --article <web-article.html> --release-date YYYY-MM-DD`
   (validates with `publish-insight.py --dry-run`, copies into
   `scheduled/<date>-<slug>/`, updates `manifest.json`, appends `LOG.md`).
2. Release: `.github/workflows/scheduled-publish.yml` runs daily at
   22:00 UTC (06:00 Beijing). `tools/publish-scheduled.py` publishes every
   queued item with `release_date <= today (Asia/Shanghai)`, then removes its
   folder, marks it `live` in `manifest.json`, and appends to `LOG.md`.
   The push to `main` auto-deploys via Cloudflare (~1 min).
3. Manual run: Actions → Scheduled publish → Run workflow (optional `today`
   override `YYYY-MM-DD` for testing; use with `--dry-run` behaviour by
   running `python tools/publish-scheduled.py --today <date> --dry-run` locally).

## Rules

- `scheduled/*` is shielded from the public web (`_redirects` + `_headers`).
  Never link to it from any page. Queue contents are still visible in git
  history; for true embargo use a private holding repo instead.
- `web-package.json` `publish_date` must equal the queue `release_date`.
- Hero image must already exist under `images/` at schedule time
  (shared `insight-hero.jpg` is the current default).
- Do not hand-edit `manifest.json` rows; use the scripts.
