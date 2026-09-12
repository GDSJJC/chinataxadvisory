# README — China Tax Advisory static rebuild (handoff for future AI)

Read this first before changing anything. Short, load-bearing facts only.

## What this is

Premium static rebuild of https://www.chinataxadvisory.com (Squarespace 7.1), to eliminate Squarespace hosting cost.
Stack: **plain HTML + CSS + JS, no framework, no build step**. Deploy: **GitHub → Cloudflare Workers Static Assets** (new unified Workers & Pages flow, Framework: Static).

## Key locations (after planned move)

- Site repo (local): `C:\Users\Huang\Desktop\Futong\Web Migration\` (moved from `Desktop\Web Migration` on 2026-09-07; if still at old path, same contents)
- Originals: `C:\Users\Huang\Desktop\Futong\Squarespace\` — Credentials/OIG1-21, Photo 2025/AZ.jpg + Office.png, Logo & Banner/
- GitHub: `https://github.com/GDSJJC/chinataxadvisory` (user GDSJJC, email abe.zhao@outlook.com), branch `main`
- Preview: `https://chinataxadvisory.abe-zhao.workers.dev` (production branch `main`)
- Live: `https://www.chinataxadvisory.com` via Cloudflare Workers custom domain (DNS moved from Squarespace Domains to Cloudflare, Sept 2026). Domain registration stays at Squarespace Domains (renewal Jan 2027) — cancel the Squarespace **Website** only, never the domain.

## Architecture / conventions

- Clean-URL folders: `about/index.html` → `/about/`, `client-cases/index.html` → `/client-cases/`, `contact/index.html` → `/contact/`, `blog/<slug>/index.html` → `/blog/<slug>/`. Homepage `index.html` doubles as Insights listing (matches Squarespace where `/` is the blog list).
- Shared: `css/style.css` (tokens: navy #0f2340, gold #c5a880/#a9885e; fonts Cormorant Garamond + Source Sans 3 via Google Fonts), `js/main.js` (mobile nav + credentials lightbox).
- Rollback of the 2026-09-13 visual redesign: git tag `pre-redesign-2026-09-13` and branch `archive/pre-redesign-2026-09-13` (commit `a78b381`). Restore with `git switch archive/pre-redesign-2026-09-13`, or put the old site back on `main` with `git reset --hard pre-redesign-2026-09-13` then push. Do not push a reset until the owner confirms.
- Config: `wrangler.jsonc` (name chinataxadvisory, assets.directory ".", not_found_handling "404-page"), `_redirects` (old Squarespace hash slug → clean slug + .html aliases), `sitemap.xml`, `robots.txt`, `blog/rss.xml`, `404.html`, `.gitignore` (excludes `.git/`, `.wrangler/`, `Web Dev.txt`).
- `Web Dev.txt` (568 lines, prior hosting/AI-model analysis) is **intentionally untracked** — never commit it.
- Images: office→`/images/office.png`, cases→`/images/credentials/case-01..21.jpg` (from OIG1..21). Portrait `/images/about.jpg` (from AZ.jpg) **removed Sept 2026** for firm-first branding — do not re-add personal photos. Blog heroes still remote Unsplash-via-Squarespace CDN — localize on next pass if desired.

## What was done (2026-09-07)

1. Audited public site: nav About/Insights(`/`)/Credentials(`/client-cases`, 21 text-in-image cases, zero captions)/Contact (Office.png + form + info@chinataxadvisory.com); 5 posts migrated full-text (condensed faithfully).
2. Built premium refresh (not pixel-match): 30px two-tone brand (navy + bronze-gold, intentional — do not enlarge), hero + 5 cards + about teaser + credentials teaser + contact CTA.
3. Decisions applied: credentials keep image grid uncropped (`height:auto; object-fit:contain` — never crop or text is lost); free form services; premium refresh; newsletter removed (replaced with contact CTA card); firm-first branding, no personal names/photos, bylines read "China Tax Advisory".
4. GitHub + Cloudflare wired: empty repo → commit 16 files → push → Connect GitHub (note: user first authorized All repos; tightened to Only `chinataxadvisory` via github.com/settings/installations) → Create application → Framework Static, no build cmd, output `/` → Build #f2f3c529 Success.
5. Fixes pushed: brand 22→30px, credentials uncropped, `.git/` excluded from deploy, 404-page handling, newsletter removal, contact bio, image localization.

## What is left / TODO for future AI

- [x] **Contact form**: `contact/index.html` uses **FormSubmit** (`https://formsubmit.co/info@chinataxadvisory.com`, no account; Formspree signup was blocked in China by reCAPTCHA CSP). First submit triggers one activation mail to info@ — click Activate once. MailerLite was considered and rejected for contact (it subscribes inquirers to audience; keep MailerLite only if newsletter returns).
- [x] **Go-live (Sept 2026)**: domain onboarded to Cloudflare (Free), Squarespace A/CNAME records deleted, nameservers switched Squarespace Domains → Cloudflare, `www` added as Workers custom domain. Canonicals/sitemap/RSS already pointed at `www.chinataxadvisory.com` — no code change needed.
- [ ] Visual QA on live `www` URL (desktop/tablet/phone); owner gives fix list.
- [ ] Optional: localize 5 blog hero images to `/images/`; add favicon polish; verify OG tags; add apex→www redirect if desired (only `www` is connected today).
- [ ] Blog workflow: see `HOW-TO-POST-A-BLOG.md` (AI prompt template + manual steps + LinkedIn blurb template + RSS→Buffer semi-auto option). Keep `sitemap.xml` + `blog/rss.xml` in sync on every post. New posts use byline "China Tax Advisory", unified footer Disclaimer (see Rules).

## Rules for future edits

- Domain registration stays at Squarespace Domains (do not transfer/cancel before Jan 2027 renewal). Squarespace Website may be cancelled now that Cloudflare is live. Never delete Zoho MX/TXT mail records in Cloudflare DNS.
- Never crop credential images. Keep `height:auto`.
- Firm-first voice everywhere: no personal names or portraits; blog bylines read "China Tax Advisory".
- Footer is unified: heading `Disclaimer`, text `Insights on this site are for general information only and do not constitute professional advice. Tax law and enforcement practice change — please seek tailored advice before acting.`, fine line `© <year> China Tax Advisory · All rights reserved · RSS`. Keep identical on every page.
- Brand wordmark stays 30px desktop (24px mobile); do not enlarge.
- Keep stack dependency-free. No React/Next, no DB, no server.
- Every push to `main` auto-deploys — verify at `https://www.chinataxadvisory.com` after ~1 min (workers.dev preview works too).
- Commit messages short; include updated `sitemap.xml`/`rss.xml` when adding posts.
