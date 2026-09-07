# How to post a new blog (static site, no Squarespace)

You have 2 ways. AI-assisted is fastest and recommended.

## Option A — AI-assisted (recommended, 5 min)

1. In this repo folder, tell the AI (Spark or any coding AI):
   > "Here's my new article. Add it to my website.
   > Title: [paste title]
   > Date: [e.g. 2026-10-15]
   > Category: [e.g. Transfer pricing / VAT / Treaty / FDI]
   > Body: [paste full text, Markdown or Word is fine]
   > Slug: [short-lowercase-with-dashes, e.g. sta-clarifies-xy-rule]"
2. The AI will:
   - create `blog/<slug>/index.html` (copy of existing article template),
   - add a card to the top of `index.html` → Latest insights,
   - add the URL to `sitemap.xml` and an `<item>` to `blog/rss.xml`,
   - commit + push → Cloudflare auto-deploys in ~1 min.
3. Check `https://chinataxadvisory.abe-zhao.workers.dev/blog/<slug>/` and the homepage card.

Prompt template you can reuse:
```
Add this as a new Insight post.
Title: ...
Date: ...
Category: ...
Slug: ...
Body:
---
[paste]
---
Update homepage Latest insights (newest first, keep 5 posts + 1 contact CTA card),
sitemap.xml, blog/rss.xml. Commit and push.
```

## Option B — Manual (no AI)

1. Copy an existing post folder, e.g. `blog/china-2025-encouraged-catalogue-tax-incentives/` → `blog/<new-slug>/`.
2. Open `blog/<new-slug>/index.html`, replace `<title>`, `<h1>`, date/category line, `.standfirst`, and body sections. Keep header/footer/nav identical.
3. Homepage `index.html`: duplicate one `<article class="card">`, put newest first, update image (reuse an existing Unsplash URL or add `/images/<new>.jpg`), title, excerpt, link.
4. `sitemap.xml`: duplicate a `<url>` block with the new loc.
5. `blog/rss.xml`: duplicate an `<item>` block (title/link/pubDate).
6. Commit + push:
   ```
   git add blog/<new-slug> index.html sitemap.xml blog/rss.xml
   git commit -m "New insight: <title>"
   git push origin main
   ```
7. Wait 1 min, verify preview URL.

## Images for new posts

- Put new files in `images/` (e.g. `images/my-topic.jpg`), reference as `/images/my-topic.jpg`.
- Blog hero images currently reuse remote Unsplash-via-Squarespace URLs — OK short-term. For longevity, save the image locally under `images/`.

## LinkedIn — blurb + link (manual recommended)

There is **no free fully-automatic** static-site → LinkedIn-personal-profile sync (LinkedIn restricts personal API posting; company pages allow more).

Recommended: 60-second manual post with this template:
```
[Hook — 1 line outcome, e.g. "RMB 24M assessed on a RMB 240M offshore sale."]
[1-2 lines: what rule, why it matters.]
Full analysis: https://chinataxadvisory.abe-zhao.workers.dev/blog/<slug>/
#ChinaTax #TransferPricing (pick 3 max)
```
Tips: first 2 lines show before "see more" — put the hook there. Paste link at end (LinkedIn unfurls the card from our OG tags). Post within 24h of publishing for best reach.

Semi-auto option (if you post often):
- **RSS → Buffer/Typefully → LinkedIn**: connect `https://chinataxadvisory.abe-zhao.workers.dev/blog/rss.xml` (or the final domain `/blog/rss.xml`) to Buffer/Make/Zapier → draft LinkedIn post on new RSS item → you approve with one click. Free tiers cover ~5 posts/mo.
- **Zapier/Make RSS → LinkedIn Company Page** can auto-post, but Personal profiles usually require manual approval step. Do not grant LinkedIn credentials to unreliable tools.
- Until volume justifies it, manual is faster and higher quality (you tailor the hook).

After custom domain goes live (post-January), replace `workers.dev` links with `https://www.chinataxadvisory.com/blog/<slug>/`.
