# Posting guide — from tax alert to website to LinkedIn

The full pipeline. Website design is frozen: no CSS, layout, font, or
header/footer changes without the owner's explicit approval. This guide only
adds content through the existing template.

## Overview

```
China Tax Alert workstation          Website repo (this folder)          LinkedIn
(Model One drafts,                  tools/publish-insight.py            manual 60-sec
 Model Two reviews + approves,       generates article + homepage +      post with the
 writes final.md +                   sitemap + rss from the live         generated kit
 web-package.json +
 web-article.html)
        |                                      |                            |
        +-- orchestrator.py publish-web --------+--> git push --> live      +--> paste kit
```

## Step 1 — Finish the alert (China Tax Alert folder)

1. Run the two-model workflow to `final_ready` with an `approve` or
   `approve_with_changes` Model Two decision, per that repo's `README.md`.
2. Model Two's final must include, besides `final.md`:
   - `model_two/final/web-package.json` (see `01_Work_Flow/system/schemas/web-package.schema.json`):
     `slug`, `title`, optional `short_label`, `publish_date` (YYYY-MM-DD),
     `category` (use an existing site category: `Indirect transfer`,
     `Treaty / BO`, `Transfer pricing`, `VAT Law`, `FDI incentives` —
     check the homepage `.meta` lines), `standfirst`, `homepage_excerpt`,
     `seo_title` (≤60ch), `meta_description` (≤155ch), `hero_image`
     (`local_path` like `/images/<slug>.jpg`, `alt`, `source`, `license`),
     `tags`, `linkedin` (`hook`, `body`, ≤3 `hashtags`).
   - `model_two/final/web-article.html`: body fragment only —
     `<h2>`, `<p>`, `<ul>/<li>`, sparing `<strong>`, links to official
     sources. No page chrome, styles, scripts, images, personal names,
     Squarespace URLs, or time-commitment language.
3. Get the hero image per `tools/IMAGE_GUIDE.md`: save the image as
   `images/<slug>.jpg` and its license note as
   `tools/licenses/<slug>.source.txt` (shielded, never public) in this repo.

## Step 2 — Stage the post (one command)

From the China Tax Alert folder:

```powershell
python .\orchestrator.py publish-web --alert-id <alert-id>
```

This validates the package (slug format, required fields, no Squarespace
references, `final_ready` + approving decision, hero present) and runs this
repo's `tools/publish-insight.py`, which:

- creates `blog/<slug>/index.html` from the live template (header, fonts,
  footer Disclaimer byte-identical),
- moves the current homepage featured post to the top row, puts the new
  post in the featured slot, keeps 5 posts,
- appends `sitemap.xml` and prepends `blog/rss.xml`,
- repairs the prev/next chain (existing labels preserved),
- prints + saves a LinkedIn kit next to the package file.

Direct use (same thing, from this folder):

```powershell
python tools\publish-insight.py --package <path\web-package.json> --article <path\web-article.html>
```

Add `--dry-run` to validate without writing anything. If the hero is not
ready yet, the command stops with instructions; bypass only with
`--allow-no-image` (featured slot goes text-only — add the image later).

## Step 3 — Verify locally, then publish

1. Open `blog/<slug>/index.html` in a browser: title, date/category line,
   standfirst, sections, prev/next links, footer Disclaimer identical.
2. Open `index.html`: new featured on top, previous featured as first row,
   5 posts total.
3. Commit and push (auto-deploys in ~1 min via Cloudflare):

```
git add blog/<slug> index.html sitemap.xml blog/rss.xml images/<slug>.jpg tools/licenses/<slug>.source.txt
git commit -m "New insight: <title>"
git push origin main
```

4. Check `https://www.chinataxadvisory.com/blog/<slug>/` and the homepage.

## Step 4 — LinkedIn (optional, manual recommended)

Fully automatic posting is not available for personal profiles (LinkedIn API
limits). Use the generated kit (`linkedin-<slug>.txt`):

```
[Hook — 1 line outcome]
[1-2 lines: what rule, why it matters.]
Full analysis: https://www.chinataxadvisory.com/blog/<slug>/
#ChinaTax #... (max 3)
```

Attach the local hero file to the LinkedIn post (do not hotlink). Post
within 24h; the first 2 lines show before "see more".

Higher volume option: connect `https://www.chinataxadvisory.com/blog/rss.xml`
to Buffer/Typefully/Make/Zapier to draft posts on each new RSS item, then
approve with one click. Do not grant LinkedIn credentials to unreliable tools.

## Rules that always apply

- Design freeze: never edit `css/`, `js/`, header/nav/footer markup, fonts,
  or the Disclaimer wording to "fit" a post. Adapt the content instead.
- Firm-first voice: byline is always `China Tax Advisory`; no personal names
  or portraits.
- Independence: no Squarespace URLs, CDN links, or builder dependencies
  anywhere. All images and assets are local files in this repo.
- Shielding: repo internals (`tools/`, guides, `wrangler.jsonc`,
  `.gitignore`) are blocked from the public web via `_redirects` (+
  `X-Robots-Tag` insurance in `_headers`). Never link to them from any
  page, and never store public-bound files under `tools/`.
- No time commitments in reply language ("as soon as we can", never
  "one business day").
- `contact/thank-you/` stays `noindex`, out of nav and sitemap.
