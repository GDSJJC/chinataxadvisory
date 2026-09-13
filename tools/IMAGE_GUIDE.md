# Image guide — Insight posts (independent, no Squarespace)

Rule: every image on this site is a local file. Never hotlink a CDN, image
proxy, or page-builder asset host. The last remote hero
(`images.squarespace-cdn.com`) was localized in Sept 2026 to
`/images/shenzhen-offshore-share-sale.jpg`; do not reintroduce remote URLs.

## Where images live

- Heroes: `/images/<slug>.jpg` (e.g. `/images/sta-clarifies-xy-rule.jpg`) —
  public by design (homepage featured slot).
- License proof lives shielded from the public web at
  `/tools/licenses/<slug>.source.txt` (one line: source URL + license +
  date). The `/tools/*` shield rule keeps it off the site; never store it
  beside the image.
- Homepage: only the featured post shows an image (`.insight-feature-img`,
  16/10 crop via CSS). List rows are typographic — no per-row images.
- Article pages: no in-body hero by design. The publisher only wires the
  homepage featured image.

## What fits a boutique tax practice

Prefer restrained, architectural, documentary images: city skylines at dusk,
office towers, courthouse/ministry facades, port and factory exteriors,
abstract paper/stone texture. Requirements:

- No text, logos, watermarks, or recognizable people in frame.
- No gavel/scales/calculator clichés unless the article is about disputes.
- Muted tones that sit well on warm paper (`#f7f4ef`); avoid neon or heavy HDR.
- Landscape, ≥1600px wide, JPG quality ~80, target ≤600KB.

## Finding one (per post, ~10 min)

1. Search a free-license library: Unsplash (`unsplash.com`), Pexels
   (`pexels.com`), or Pixabay (`pixabay.com`). Keywords that work for tax
   analysis: `shanghai skyline dusk`, `shenzhen architecture`, `beijing
   business district`, `container port aerial`, `modern office facade`,
   `abstract concrete texture`.
2. Confirm the license page allows free commercial use without attribution
   (Unsplash License, Pexels License, Pixabay Content License all do as of
   2026 — recheck at download time; screenshot or save the license line).
3. Download the `Large`/`Original` JPG, resize to 1600px wide if larger
   (any editor or `ffmpeg -i in.jpg -vf scale=1600:-1 out.jpg`), save as
   `/images/<slug>.jpg`.
4. Write `tools/licenses/<slug>.source.txt`: photographer, page URL, license
   name, download date. Example:
   `Photo by X (https://unsplash.com/photos/...) — Unsplash License — 2026-09-20`.
5. Alt text: one neutral clause, e.g. `City business district skyline at
   sunset`. Never leave `alt=""` on a featured image.
6. Record the same four fields in the tax-alert `web-package.json`
   `hero_image` (`local_path`, `alt`, `source`, `license`).

If no suitable photo exists (e.g. highly technical topic), generate an
abstract one instead: ask the AI for a `1600x1000 muted architectural
abstraction, no text, no people, warm gray and navy tones` image, save it
the same way, and set `source` to `AI-generated for this article` with the
tool and date. Do not present AI images as photographs of real places.

## Asking the AI to find one

> "Find a suitable hero image for my new Insight post `<slug>` about
> `<one-line topic>`. Restrained, professional, no text or people,
> landscape ≥1600px, free commercial license. Save it as
> `images/<slug>.jpg` with the license note at
> `tools/licenses/<slug>.source.txt`, and give me the `alt` text plus the
> `hero_image` block for `web-package.json`."

The AI must not change any CSS, layout, or fonts — image wiring only.
