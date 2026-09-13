# README — China Tax Advisory static rebuild (handoff for future AI)

Read this first before changing anything. Short, load-bearing facts only.

## What this is

Independent static site for https://www.chinataxadvisory.com (originally rebuilt
off Squarespace 7.1 in Sept 2026; the site has had zero runtime dependency on
Squarespace since — all pages, images, and assets are local files in this repo).
Stack: **plain HTML + CSS + JS, no framework, no build step**. Deploy: **GitHub → Cloudflare Workers Static Assets** (new unified Workers & Pages flow, Framework: Static).

Positioning: a high-end boutique China tax advisory practice. The site should feel refined, discreet, and expensive in the sense of quality — not flashy, templated, or corporate-generic.

## Key locations

- Site repo (local): `C:\Users\Huang\Desktop\Futong\Web Migration\` (moved from `Desktop\Web Migration` on 2026-09-07; if still at old path, same contents)
- Legacy archive, not required for operation: `C:\Users\Huang\Desktop\Futong\Squarespace\` — Credentials/OIG1-21, Photo 2025/AZ.jpg + Office.png, Logo & Banner/. Nothing on the live site reads from it.
- GitHub: `https://github.com/GDSJJC/chinataxadvisory` (user GDSJJC, email abe.zhao@outlook.com), branch `main`
- Preview: `https://chinataxadvisory.abe-zhao.workers.dev` (production branch `main`)
- Live: `https://www.chinataxadvisory.com` via Cloudflare Workers custom domain (DNS on Cloudflare since Sept 2026). Domain registration vendor holds the name only (Squarespace Domains, renewal Jan 2027) — the website makes no runtime use of it. Never delete Zoho MX/TXT mail records in Cloudflare DNS.

## Architecture / conventions

- Clean-URL folders: `about/index.html` → `/about/`, `client-cases/index.html` → `/client-cases/`, `contact/index.html` → `/contact/`, `contact/thank-you/index.html` → `/contact/thank-you/`, `blog/<slug>/index.html` → `/blog/<slug>/`. Homepage `index.html` doubles as the Insights listing (featured post + 4-row list).
- Shared: `css/style.css` (tokens: navy `#0f2340`, gold `#c5a880`/`#a9885e`, warm paper `#f7f4ef`; fonts **Cormorant Garamond** display + **Source Sans 3** body/UI via Google Fonts), `js/main.js` (mobile nav + credentials lightbox).
- Config: `wrangler.jsonc` (name chinataxadvisory, assets.directory ".", not_found_handling "404-page"), `_redirects` (legacy hash-slug → clean-slug redirects kept for SEO continuity — a static file, no live external connection), `sitemap.xml`, `robots.txt`, `blog/rss.xml`, `404.html`, `.gitignore` (excludes `.git/`, `.wrangler/`, `Web Dev.txt`).
- Publishing: `tools/publish-insight.py` (one-command post publisher, no design changes), `tools/IMAGE_GUIDE.md` (hero sourcing), `POSTING_GUIDE.md` (end-to-end: alert → website → LinkedIn), `HOW-TO-POST-A-BLOG.md` (quick reference).
- `Web Dev.txt` (prior hosting/AI-model analysis) is **intentionally untracked** — never commit it.
- Images, all local: office→`/images/office.png`, cases→`/images/credentials/case-01..21.jpg`. Portrait `/images/about.jpg` **removed Sept 2026** for firm-first branding — do not re-add personal photos. Blog heroes live under `/images/<slug>.jpg` with the license note shielded at `tools/licenses/<slug>.source.txt` (last remote CDN hero localized Sept 2026). Article pages carry no in-body hero by design; the homepage shows the featured image only.

## Current pages

| URL | File | Notes |
|---|---|---|
| `/` | `index.html` | Insights. Featured post (`.insight-feature`) + four rows (`.insight-list` / `.insight-row`). Not a card grid. |
| `/about/` | `about/index.html` | Firm page. H1 is a statement, **not** the words “China Tax Advisory” (that already sits in the wordmark). |
| `/client-cases/` | `client-cases/index.html` | Credentials. 21 case **images** in a 2-col grid; click opens lightbox. |
| `/contact/` | `contact/index.html` | FormSubmit form + office photograph. |
| `/contact/thank-you/` | `contact/thank-you/index.html` | Post-submit page. `noindex`. **Not** in nav or `sitemap.xml`. |
| `/blog/<slug>/` | `blog/<slug>/index.html` | Insight articles. Copy an existing post as the template. |

## What was done

**2026-09-07** — Static rebuild, GitHub + Cloudflare, 5 insights migrated, credentials images localized, firm-first voice, FormSubmit contact form, old hosted website replaced (DNS on Cloudflare; registration vendor holds the name only).

**2026-09-13** — Visual redesign now live: warm paper ground, Cormorant Garamond + Source Sans 3, hairline nav (no pills), Insights as featured + list (no 6-card grid, no navy gradient hero), About restyled without repeating the firm name as H1, Credentials 2-col + lightbox (images uncropped and unedited), Contact form redirects to `/contact/thank-you/` instead of FormSubmit’s generic thanks page. Reply copy is “as soon as we can” — **no SLA / no “one business day.”**

**2026-09-14** — Independence + publishing pipeline: last remote CDN hero localized to `/images/` (zero remote image dependencies), one-command publisher `tools/publish-insight.py` with dry-run validation, hero sourcing guide `tools/IMAGE_GUIDE.md`, end-to-end `POSTING_GUIDE.md` (alert → website → LinkedIn kit). Design frozen.

**2026-09-14 (shielding)** — Beneath-surface files blocked from the public web: `_redirects` 302s `tools/*`, guides, `wrangler.jsonc`, `.gitignore` to the 404 page (true 404 rewrites are not permitted on this platform, so 302-to-404 is the maximum shielding available; 302 chosen so a reverted rule never sticks in browsers). `_headers` adds `X-Robots-Tag: noindex` insurance on the same paths. License notes live shielded at `tools/licenses/`. `_redirects`/`_headers` are consumed at deploy and never served.

Rollback of the pre-redesign site: git tag `pre-redesign-2026-09-13` and branch `archive/pre-redesign-2026-09-13` (commit `a78b381`). Restore only if the owner asks: `git reset --hard pre-redesign-2026-09-13` then push. Do not revert the redesign on your own.

## What is left / TODO for future AI

- [x] **Contact form**: FormSubmit (`https://formsubmit.co/info@chinataxadvisory.com`, no account; Formspree signup was blocked in China by reCAPTCHA CSP). First submit triggers one activation mail to info@ — click Activate once. `_next` → `https://www.chinataxadvisory.com/contact/thank-you/` (never leave the visitor on formsubmit.co). `_autoresponse` confirms receipt. MailerLite was considered and rejected for contact (it subscribes inquirers to audience).
- [x] **Go-live (Sept 2026)**: domain onboarded to Cloudflare (Free), nameservers Squarespace Domains → Cloudflare, `www` as Workers custom domain.
- [x] **Visual redesign (Sept 2026)**: owner reviewed locally, then published to `main`.
- [ ] Optional: favicon polish; verify OG tags; add apex→www redirect if desired (only `www` is connected today).
- [ ] Blog workflow: see `POSTING_GUIDE.md` (end-to-end) and `HOW-TO-POST-A-BLOG.md` (quick ref). Always publish via `tools/publish-insight.py` so `sitemap.xml` + `blog/rss.xml` + prev/next stay in sync — never hand-edit them.

## Rules for future edits

- **Design freeze**: no changes to `css/`, `js/`, layout, fonts, header/nav/footer markup, or the Disclaimer wording without the owner's explicit approval. Adapt post content to the template, never the reverse.
- **Independence**: no remote page-builder, CDN, or image-proxy dependencies. All assets are local files in this repo. Do not reintroduce Squarespace (or any builder) URLs, embeds, or hotlinks.
- **Shielding**: nothing beneath the surface is public. `tools/`, guides, `wrangler.jsonc`, `.gitignore` 302 to the 404 page via `_redirects` (+ noindex insurance in `_headers`). Never link to them from any page, never store public-bound files under `tools/`, and never remove a shield rule without owner approval.
- Registration vendor holds the domain name only (do not transfer/cancel before Jan 2027 renewal). Never delete Zoho MX/TXT mail records in Cloudflare DNS.
- Keep stack dependency-free. No React/Next, no DB, no server.
- Every push to `main` auto-deploys — verify at `https://www.chinataxadvisory.com` after ~1 min (workers.dev preview works too).
- Commit messages short; include updated `sitemap.xml`/`rss.xml` when adding posts.

**Voice and branding**
- Firm-first voice everywhere: no personal names or portraits; blog bylines read “China Tax Advisory”.
- Do not put “China Tax Advisory” as the About H1 — the wordmark already says it. About H1 is a positioning statement.
- Footer is unified: heading `Disclaimer`, text `Insights on this site are for general information only and do not constitute professional advice. Tax law and enforcement practice change — please seek tailored advice before acting.`, fine line `© <year> China Tax Advisory · All rights reserved · RSS`. Keep identical on every page (including thank-you).
- Brand wordmark stays 30px desktop (24px mobile); do not enlarge. “China Tax” navy, “Advisory” gold (`#a9885e`).

**Design**
- Aesthetic: boutique, understated, high quality. Do not reintroduce rounded pill nav, card-lift hover, navy gradient heroes, or Alice/Almarai.
- Fonts stay Cormorant Garamond + Source Sans 3. New pages must use the same Google Fonts link as existing pages.
- Do not make the site flashier or more “modern for its own sake.” Prefer restraint.

**Credentials**
- Never crop, rewrite, replace, or otherwise alter the 21 case images or the text embedded in them. Keep `height:auto; object-fit:contain`.
- Presentation only: 2-col desktop / 1-col phone, gold numerals, lightbox in `js/main.js`. Do not add “Case 01” captions that duplicate the images.

**Contact / thank-you**
- Keep FormSubmit hidden fields: `_subject`, `_honey`, `_captcha=false`, `_template=table`, `_next` (full `https://` URL to `/contact/thank-you/`), `_autoresponse`.
- Reply language is sincere and prompt **without a time commitment**. Current wording: “We reply as soon as we can.” / “We will reply as soon as we can.” Do not restore “one business day” or any other SLA.
- Thank-you page stays `noindex`, out of the sitemap, out of primary nav. FormSubmit’s own thanks page is generic — do not send visitors there.

**Insights**
- Newest post is `.insight-feature` on the homepage; the previous featured item moves to the top of `.insight-list` as an `.insight-row`. Keep five posts. Do not add a dummy contact card to fill a grid.
- Full posting steps: `POSTING_GUIDE.md`. Hero images: `tools/IMAGE_GUIDE.md`. Categories: reuse an existing site category (see homepage `.meta` lines); do not invent new labels without owner approval.
