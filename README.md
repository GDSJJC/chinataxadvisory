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
- Live (old): Squarespace at `www.chinataxadvisory.com` via Zoho domain — **DO NOT TOUCH Squarespace, its content, or Zoho DNS**. Only read public pages. Squarespace subscription runs to Jan (next year); DNS move is a January-only decision by owner.

## Architecture / conventions

- Clean-URL folders: `about/index.html` → `/about/`, `client-cases/index.html` → `/client-cases/`, `contact/index.html` → `/contact/`, `blog/<slug>/index.html` → `/blog/<slug>/`. Homepage `index.html` doubles as Insights listing (matches Squarespace where `/` is the blog list).
- Shared: `css/style.css` (tokens: navy #0f2340, gold #c5a880/#a9885e; fonts Alice + Almarai via Google Fonts), `js/main.js` (mobile nav only).
- Config: `wrangler.jsonc` (name chinataxadvisory, assets.directory ".", not_found_handling "404-page"), `_redirects` (old Squarespace hash slug → clean slug + .html aliases), `sitemap.xml`, `robots.txt`, `blog/rss.xml`, `404.html`, `.gitignore` (excludes `.git/`, `.wrangler/`, `Web Dev.txt`).
- `Web Dev.txt` (568 lines, prior hosting/AI-model analysis) is **intentionally untracked** — never commit it.
- Images: about→`/images/about.jpg` (from AZ.jpg), office→`/images/office.png`, cases→`/images/credentials/case-01..21.jpg` (from OIG1..21). Blog heroes still remote Unsplash-via-Squarespace CDN — localize on next pass if desired.

## What was done (2026-09-07)

1. Audited public site: nav About/Insights(`/`)/Credentials(`/client-cases`, 21 text-in-image cases, zero captions)/Contact (Office.png + Formspree-needed form + info@chinataxadvisory.com); 5 posts migrated full-text (condensed faithfully).
2. Built premium refresh (not pixel-match): bigger 30px two-tone brand (navy + bronze-gold, intentional), hero + 5 cards + about teaser + credentials teaser + contact CTA.
3. Decisions applied: credentials keep image grid uncropped (`height:auto; object-fit:contain` — never crop or text is lost); free form services; premium refresh; newsletter removed (replaced with contact CTA card); contact has compact bio + link to full `/about/` (no URL merge, 4 nav items kept for SEO).
4. GitHub + Cloudflare wired: empty repo → commit 16 files → push → Connect GitHub (note: user first authorized All repos; tightened to Only `chinataxadvisory` via github.com/settings/installations) → Create application → Framework Static, no build cmd, output `/` → Build #f2f3c529 Success.
5. Fixes pushed: brand 22→30px, credentials uncropped, `.git/` excluded from deploy, 404-page handling, newsletter removal, contact bio, image localization.

## What is left / TODO for future AI

- [ ] **Formspree wiring**: `contact/index.html` has `https://formspree.io/f/YOUR_FORM_ID` + `_subject`/`_replyto`/`_gotcha`. Owner creates free form at formspree.io (recipient info@chinataxadvisory.com), pastes real id — one-line edit, commit, push. MailerLite was considered and rejected for contact (it subscribes inquirers to audience; keep MailerLite only if newsletter returns).
- [ ] Visual QA on preview (desktop/tablet/phone) vs old site; owner gives fix list.
- [ ] Optional: localize 5 blog hero images to `/images/`; add favicon polish; verify OG tags.
- [ ] Blog workflow: see `HOW-TO-POST-A-BLOG.md` (AI prompt template + manual steps + LinkedIn blurb template + RSS→Buffer semi-auto option). Keep `sitemap.xml` + `blog/rss.xml` in sync on every post.
- [ ] **January only**: if owner approves, move Zoho DNS to Cloudflare + set custom domain + update canonicals/sitemap/RSS from `workers.dev` to `www.chinataxadvisory.com`. Do not do earlier.

## Rules for future edits

- Never log into, edit, or break Squarespace/Zoho. New site runs in parallel until owner says cut over.
- Never crop credential images. Keep `height:auto`.
- Keep stack dependency-free. No React/Next, no DB, no server.
- Every push to `main` auto-deploys — verify at the workers.dev URL after ~1 min.
- Commit messages short; include updated `sitemap.xml`/`rss.xml` when adding posts.
