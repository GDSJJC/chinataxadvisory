# README — China Tax Advisory static rebuild (handoff for future AI)

Read this first before changing anything. Short, load-bearing facts only.

## What this is

Premium static rebuild of https://www.chinataxadvisory.com (Squarespace 7.1), to eliminate Squarespace hosting cost.
Stack: **plain HTML + CSS + JS, no framework, no build step**. Deploy: **GitHub → Cloudflare Workers Static Assets** (new unified Workers & Pages flow, Framework: Static).

Positioning: a high-end boutique China tax advisory practice. The site should feel refined, discreet, and expensive in the sense of quality — not flashy, templated, or corporate-generic.

## Key locations

- Site repo (local): `C:\Users\Huang\Desktop\Futong\Web Migration\` (moved from `Desktop\Web Migration` on 2026-09-07; if still at old path, same contents)
- Originals: `C:\Users\Huang\Desktop\Futong\Squarespace\` — Credentials/OIG1-21, Photo 2025/AZ.jpg + Office.png, Logo & Banner/
- GitHub: `https://github.com/GDSJJC/chinataxadvisory` (user GDSJJC, email abe.zhao@outlook.com), branch `main`
- Preview: `https://chinataxadvisory.abe-zhao.workers.dev` (production branch `main`)
- Live: `https://www.chinataxadvisory.com` via Cloudflare Workers custom domain (DNS moved from Squarespace Domains to Cloudflare, Sept 2026). Domain registration stays at Squarespace Domains (renewal Jan 2027) — cancel the Squarespace **Website** only, never the domain.

## Architecture / conventions

- Clean-URL folders: `about/index.html` → `/about/`, `client-cases/index.html` → `/client-cases/`, `contact/index.html` → `/contact/`, `contact/thank-you/index.html` → `/contact/thank-you/`, `blog/<slug>/index.html` → `/blog/<slug>/`. Homepage `index.html` doubles as Insights listing (matches Squarespace where `/` is the blog list).
- Shared: `css/style.css` (tokens: navy `#0f2340`, gold `#c5a880`/`#a9885e`, warm paper `#f7f4ef`; fonts **Cormorant Garamond** display + **Source Sans 3** body/UI via Google Fonts), `js/main.js` (mobile nav + credentials lightbox).
- Config: `wrangler.jsonc` (name chinataxadvisory, assets.directory ".", not_found_handling "404-page"), `_redirects` (old Squarespace hash slug → clean slug + .html aliases), `sitemap.xml`, `robots.txt`, `blog/rss.xml`, `404.html`, `.gitignore` (excludes `.git/`, `.wrangler/`, `Web Dev.txt`).
- `Web Dev.txt` (prior hosting/AI-model analysis) is **intentionally untracked** — never commit it.
- Images: office→`/images/office.png`, cases→`/images/credentials/case-01..21.jpg` (from OIG1..21). Portrait `/images/about.jpg` (from AZ.jpg) **removed Sept 2026** for firm-first branding — do not re-add personal photos. Blog heroes still remote Unsplash-via-Squarespace CDN — localize on next pass if desired.

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

**2026-09-07** — Static rebuild, GitHub + Cloudflare, 5 insights migrated, credentials images localized, firm-first voice, FormSubmit contact form, Squarespace Website replaced (domain registration stays at Squarespace Domains).

**2026-09-13** — Visual redesign now live: warm paper ground, Cormorant Garamond + Source Sans 3, hairline nav (no pills), Insights as featured + list (no 6-card grid, no navy gradient hero), About restyled without repeating the firm name as H1, Credentials 2-col + lightbox (images uncropped and unedited), Contact form redirects to `/contact/thank-you/` instead of FormSubmit’s generic thanks page. Reply copy is “as soon as we can” — **no SLA / no “one business day.”**

Rollback of the pre-redesign site: git tag `pre-redesign-2026-09-13` and branch `archive/pre-redesign-2026-09-13` (commit `a78b381`). Restore only if the owner asks: `git reset --hard pre-redesign-2026-09-13` then push. Do not revert the redesign on your own.

## What is left / TODO for future AI

- [x] **Contact form**: FormSubmit (`https://formsubmit.co/info@chinataxadvisory.com`, no account; Formspree signup was blocked in China by reCAPTCHA CSP). First submit triggers one activation mail to info@ — click Activate once. `_next` → `https://www.chinataxadvisory.com/contact/thank-you/` (never leave the visitor on formsubmit.co). `_autoresponse` confirms receipt. MailerLite was considered and rejected for contact (it subscribes inquirers to audience).
- [x] **Go-live (Sept 2026)**: domain onboarded to Cloudflare (Free), nameservers Squarespace Domains → Cloudflare, `www` as Workers custom domain.
- [x] **Visual redesign (Sept 2026)**: owner reviewed locally, then published to `main`.
- [ ] Optional: localize 5 blog hero images to `/images/`; add favicon polish; verify OG tags; add apex→www redirect if desired (only `www` is connected today).
- [ ] Blog workflow: see `HOW-TO-POST-A-BLOG.md`. Keep `sitemap.xml` + `blog/rss.xml` in sync on every post.

## Rules for future edits

- Domain registration stays at Squarespace Domains (do not transfer/cancel before Jan 2027 renewal). Squarespace Website may be cancelled now that Cloudflare is live. Never delete Zoho MX/TXT mail records in Cloudflare DNS.
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
- Full posting steps: `HOW-TO-POST-A-BLOG.md`.
