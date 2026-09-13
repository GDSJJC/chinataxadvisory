# How to post a new blog (independent static site)

Read `README.md` first (voice, footer Disclaimer, fonts, no personal bylines),
then follow **`POSTING_GUIDE.md`** — it covers the whole pipeline from tax
alert to website to LinkedIn.

## Recommended path (from a reviewed tax alert, ~10 min + image)

1. Finish the alert to `final_ready` in the China Tax Alert workstation
   (Model Two `approve`/`approve_with_changes`, with `web-package.json` +
   `web-article.html`).
2. Save the hero per `tools/IMAGE_GUIDE.md` as `images/<slug>.jpg`.
3. Stage the post with one command (from the China Tax Alert folder):
   `python .\orchestrator.py publish-web --alert-id <alert-id>`
   (or from here: `python tools\publish-insight.py --package <pkg> --article <html>`).
4. Verify locally, commit + push (`blog/<slug>`, `index.html`, `sitemap.xml`,
   `blog/rss.xml`, hero). Cloudflare deploys in ~1 min.
5. Post the generated LinkedIn kit manually (attach the hero file).

Full steps, verification checklist, and rules: `POSTING_GUIDE.md`.

## Standalone path (no tax-alert package, AI-assisted)

Tell the AI in this repo folder:

> "Add this as a new Insight post. Title: [...] Date: [e.g. 2026-10-15]
> Category: [reuse an existing site category] Slug: [short-lowercase]
> Body: [paste full text] Hero: [images/<slug>.jpg or 'find one per
> tools/IMAGE_GUIDE.md'].
> Use tools/publish-insight.py (build a web-package.json + web-article.html
> first, then run it). No design changes — copy header/footer/fonts verbatim,
> byline 'China Tax Advisory', unified footer Disclaimer. Commit and push."

The AI must use the script, not hand-edit the homepage chain, sitemap, or RSS.

## Manual fallback (no AI)

1. Build `web-package.json` + `web-article.html` by hand (schema and fragment
   rules are documented in `POSTING_GUIDE.md` step 1).
2. Run `python tools\publish-insight.py --package <pkg> --article <html> --dry-run`,
   review, then rerun without `--dry-run`.
3. Verify, commit, push as above.

Do not hand-edit `index.html` rows, `sitemap.xml`, `blog/rss.xml`, or prev/next
links — the script keeps them consistent.

## Images

Local files only: image at `images/<slug>.jpg`, license note shielded at
`tools/licenses/<slug>.source.txt`. Never hotlink any CDN. How to find a
proper one: `tools/IMAGE_GUIDE.md`. Homepage shows an image for the featured
post only; list rows are typographic.

## LinkedIn

Manual 60-second post from the generated `linkedin-<slug>.txt` kit (hook + 2
lines + link + ≤3 hashtags, hero attached). Details and the semi-auto RSS →
Buffer/Typefully option: `POSTING_GUIDE.md` step 4.
