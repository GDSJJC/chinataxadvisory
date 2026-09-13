#!/usr/bin/env python3
"""Publish a reviewed tax-alert web package as a new Insight post.

Independent static-site publisher. No design changes: the new article copies
the live template's header/nav/footer/fonts verbatim, and the homepage keeps
the featured + 4-row structure. No Squarespace or remote-CDN dependencies:
hero images must live under /images/.

Usage:
    python tools/publish-insight.py --package <web-package.json> --article <web-article.html>
    python tools/publish-insight.py --package ... --article ... --dry-run
    python tools/publish-insight.py --package ... --article ... --allow-no-image

Inputs (produced by the China Tax Alert workstation, Model Two final):
    web-package.json  per China Tax Alert 01_Work_Flow/system/schemas/web-package.schema.json
    web-article.html  body fragment: <h2>/<p>/<ul>/<li> (+ <strong>, <a>) only.

Effects:
    1. blog/<slug>/index.html          (new article, template-copied chrome)
    2. index.html                      (new post -> featured; old featured -> top row; keep 5)
    3. sitemap.xml                     (new <url>)
    4. blog/rss.xml                    (new <item>, newest first)
    5. LinkedIn kit printed to stdout + saved next to the package file.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

WEB_ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = WEB_ROOT / "blog"
IMAGES_DIR = WEB_ROOT / "images"
HOMEPAGE = WEB_ROOT / "index.html"
SITEMAP = WEB_ROOT / "sitemap.xml"
RSS = BLOG_DIR / "rss.xml"
SITE = "https://www.chinataxadvisory.com"
DISCLAIMER = (
    "Insights on this site are for general information only and do not "
    "constitute professional advice. Tax law and enforcement practice change "
    "\u2014 please seek tailored advice before acting."
)
FONTS_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400"
    "&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;1,400&display=swap"
)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN = ("squarespace", "squarespace-cdn")


class PublishError(RuntimeError):
    pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def fmt_meta_date(iso: str) -> str:
    dt = datetime.strptime(iso, "%Y-%m-%d")
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def rfc822_gmt(iso: str) -> str:
    dt = datetime.strptime(iso, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(dt, usegmt=True)


def short_label(title: str, explicit: str = "") -> str:
    if explicit.strip():
        return explicit.strip()
    if len(title) <= 52:
        return title
    cut = title[:52].rsplit(" ", 1)[0]
    return cut + "\u2026"


def pick_template() -> Path:
    """Newest article template: prefer one that already has a canonical tag."""
    posts = sorted(
        (p for p in BLOG_DIR.iterdir() if p.is_dir() and (p / "index.html").is_file()),
        key=lambda p: (p / "index.html").stat().st_mtime,
    )
    if not posts:
        raise PublishError("No existing blog posts to copy the template from")
    for post in reversed(posts):
        if 'rel="canonical"' in read_text(post / "index.html"):
            return post / "index.html"
    return posts[-1] / "index.html"


def existing_posts() -> list[dict]:
    """Parse rss.xml (newest first) for slug/title/date ordering."""
    items = []
    if RSS.is_file():
        for m in re.finditer(
            r"<item>\s*<title>(.*?)</title>\s*<link>(.*?)</link>\s*<pubDate>(.*?)</pubDate>",
            read_text(RSS),
            re.DOTALL,
        ):
            link = m.group(2).strip()
            slug = link.rstrip("/").rsplit("/", 1)[-1]
            try:
                dt = datetime.strptime(m.group(3).strip(), "%a, %d %b %Y %H:%M:%S GMT")
            except ValueError:
                continue
            items.append({"slug": slug, "title": html.unescape(m.group(1).strip()), "date": dt})
    return items


def h1_of(slug: str) -> str:
    page = BLOG_DIR / slug / "index.html"
    if not page.is_file():
        return slug
    m = re.search(r"<h1>(.*?)</h1>", read_text(page), re.DOTALL)
    return html.unescape(m.group(1).strip()) if m else slug


def build_article(template_html: str, pkg: dict, body_html: str, prevnext: str) -> str:
    title = pkg["title"].strip()
    seo_title = pkg.get("seo_title", "").strip() or title
    meta_desc = pkg["meta_description"].strip()
    slug = pkg["slug"]
    meta_line = (
        f'<div class="meta">China Tax Advisory <span class="dot"></span> '
        f"{fmt_meta_date(pkg['publish_date'])}"
        f' <span class="dot"></span> {html.escape(pkg["category"].strip())}</div>'
    )
    out = template_html
    out = re.sub(r"<title>.*?</title>", f"<title>{html.escape(seo_title)} \u2014 China Tax Advisory</title>", out, count=1)
    out = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{html.escape(meta_desc, quote=True)}">',
        out,
        count=1,
    )
    canon = f'<link rel="canonical" href="{SITE}/blog/{slug}/">'
    if 'rel="canonical"' in out:
        out = re.sub(r'<link rel="canonical" href=".*?">', canon, out, count=1)
    else:
        out = out.replace("</title>", "</title>\n" + canon, 1)
    out = re.sub(r'<div class="meta">.*?</div>', meta_line, out, count=1)
    out = re.sub(r"<h1>.*?</h1>", f"<h1>{html.escape(title)}</h1>", out, count=1, flags=re.DOTALL)
    out = re.sub(
        r'<p class="standfirst">.*?</p>',
        f'<p class="standfirst">{html.escape(pkg["standfirst"].strip())}</p>',
        out,
        count=1,
        flags=re.DOTALL,
    )
    out = re.sub(
        r'(?s)<p class="standfirst">.*?</p>\n.*?<div class="prevnext">',
        f'<p class="standfirst">{html.escape(pkg["standfirst"].strip())}</p>\n{body_html.strip()}\n<div class="prevnext">',
        out,
        count=1,
    )
    out = re.sub(r'(?s)<div class="prevnext">.*?</div>\s*</article>', prevnext + "\n</article>", out, count=1)
    return out


def update_homepage(homepage_html: str, pkg: dict, hero_src: str | None) -> str:
    slug = pkg["slug"]
    feat_m = re.search(r'(?s)<article class="insight-feature">.*?</article>', homepage_html)
    if not feat_m:
        raise PublishError("Homepage featured block not found")
    old_feat = feat_m.group(0)

    def field(pat: str, default: str = "") -> str:
        m = re.search(pat, old_feat, re.DOTALL)
        return html.unescape(m.group(1).strip()) if m else default

    old_href = field(r'<h2><a href="(.*?)">')
    old_title = field(r"<h2><a .*?>(.*?)</a></h2>")
    old_meta = field(r'<div class="meta">(.*?)</div>')
    old_excerpt = field(r"</h2>\s*<p>(.*?)</p>")
    old_meta_text = re.sub(r"<.*?>", "", old_meta).replace("\u00b7", "|")
    parts = [p.strip() for p in old_meta_text.split("|")]
    old_date = parts[0] if parts else ""
    old_cat = parts[1] if len(parts) > 1 else ""
    demoted_row = (
        f'<article class="insight-row">\n'
        f'<div class="meta">{html.escape(old_date)} <span class="dot"></span> {html.escape(old_cat)}</div>\n'
        f'<h3><a href="{html.escape(old_href, quote=True)}">{html.escape(old_title)}</a></h3>\n'
        f"<p>{html.escape(old_excerpt)}</p>\n"
        f"</article>"
    )
    img_block = (
        f'<a class="insight-feature-img" href="/blog/{slug}/">'
        f'<img src="{html.escape(hero_src, quote=True)}" '
        f'alt="{html.escape((pkg.get("hero_image") or {}).get("alt", "Insight illustration"), quote=True)}" '
        f'loading="eager"></a>\n' if hero_src else ""
    )
    new_feat = (
        f'<article class="insight-feature">\n'
        f"{img_block}"
        f"<div>\n"
        f'<div class="meta">{html.escape(fmt_meta_date(pkg["publish_date"]))} '
        f'<span class="dot"></span> {html.escape(pkg["category"].strip())}</div>\n'
        f'<h2><a href="/blog/{slug}/">{html.escape(pkg["title"].strip())}</a></h2>\n'
        f"<p>{html.escape(pkg['homepage_excerpt'].strip())}</p>\n"
        f'<a class="text-link" href="/blog/{slug}/">Read analysis</a>\n'
        f"</div>\n"
        f"</article>"
    )
    out = homepage_html.replace(old_feat, new_feat, 1)
    marker = '<div class="insight-list">'
    if marker not in out:
        raise PublishError("Homepage insight-list block not found")
    out = out.replace(marker, marker + "\n" + demoted_row, 1)
    rows = re.findall(r'(?s)<article class="insight-row">.*?</article>', out)
    if len(rows) > 4:
        out = out.replace(rows[-1], "", 1)
    return out


def linkedin_kit(pkg: dict, slug: str) -> str:
    li = pkg.get("linkedin") or {}
    hook = (li.get("hook") or pkg["homepage_excerpt"]).strip()
    body = (li.get("body") or pkg["standfirst"]).strip()
    tags = [t if t.startswith("#") else "#" + t for t in (li.get("hashtags") or [])][:3]
    hero = (pkg.get("hero_image") or {}).get("local_path", "")
    lines = [
        hook,
        "",
        body,
        "",
        f"Full analysis: {SITE}/blog/{slug}/",
        " ".join(tags) if tags else "",
        "",
        f"Image: {hero} (attach the local hero file to the LinkedIn post; do not hotlink).",
        "Post within 24h of publishing for best reach; first 2 lines show before 'see more'.",
    ]
    return "\n".join(lines).strip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Publish a web package as a new Insight post (no design changes)")
    ap.add_argument("--package", required=True, help="Path to web-package.json")
    ap.add_argument("--article", required=True, help="Path to web-article.html fragment")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-no-image", action="store_true")
    ap.add_argument("--linkedin-out", default="")
    args = ap.parse_args(argv)

    try:
        pkg = json.loads(Path(args.package).read_text(encoding="utf-8-sig"))
        body_html = Path(args.article).read_text(encoding="utf-8-sig").strip()
        slug = str(pkg.get("slug", "")).strip()
        if not SLUG_RE.fullmatch(slug):
            raise PublishError(f"slug must be lowercase kebab-case: {slug!r}")
        for field in ("title", "publish_date", "category", "standfirst", "homepage_excerpt", "meta_description"):
            if not str(pkg.get(field, "")).strip():
                raise PublishError(f"web-package is missing required field: {field}")
        datetime.strptime(pkg["publish_date"], "%Y-%m-%d")
        blob = (json.dumps(pkg, ensure_ascii=False) + body_html).lower()
        for bad in FORBIDDEN:
            if bad in blob:
                raise PublishError("Package must not reference Squarespace; use independent local assets")
        if re.search(r"<(html|head|body|header|footer|style|script|img)\b", body_html, re.IGNORECASE):
            raise PublishError("web-article.html must be a body fragment (<h2>/<p>/<ul>/<li> only); no page chrome, styles, scripts, or images")
        target = BLOG_DIR / slug
        if target.exists():
            raise PublishError(f"Release post already exists: blog/{slug}/")
        hero_src = None
        hero = pkg.get("hero_image") or {}
        if hero.get("local_path"):
            hero_file = WEB_ROOT / str(hero["local_path"]).lstrip("/")
            if hero_file.is_file():
                hero_src = "/" + str(hero["local_path"]).lstrip("/")
            elif not args.allow_no_image:
                raise PublishError(
                    f"Hero image not found in website repo: {hero['local_path']} "
                    f"(save it under images/ per tools/IMAGE_GUIDE.md, or rerun with --allow-no-image)"
                )
        posts = existing_posts()
        posts = [p for p in posts if p["slug"] != slug]
        new_date = datetime.strptime(pkg["publish_date"], "%Y-%m-%d")
        older = next((p for p in posts if p["date"] <= new_date), None)
        newer = None
        for p in reversed(posts):
            if p["date"] > new_date:
                newer = p
                break
        my_short = short_label(pkg["title"], str(pkg.get("short_label", "")))
        # Convention: newest post -> [Next (older, full H1), All insights];
        # middle -> [Previous (newer short), Next (older short)]; oldest -> [Previous, All].
        if older is None and newer is None:
            prevnext = (
                f'<div class="prevnext">\n'
                f'<a href="/"><small>\u2190 All insights</small><strong>Back to Insights</strong></a>\n'
                f"</div>"
            )
        elif newer is None:
            prevnext = (
                f'<div class="prevnext">\n'
                f'<a href="/blog/{older["slug"]}/"><small>Next \u2192</small><strong>{html.escape(h1_of(older["slug"]))}</strong></a>\n'
                f'<a href="/"><small>\u2190 All insights</small><strong>Back to Insights</strong></a>\n'
                f"</div>"
            )
        else:
            links = f'<a href="/blog/{newer["slug"]}/"><small>\u2190 Previous</small><strong>{html.escape(short_label(h1_of(newer["slug"])))}</strong></a>\n'
            links += (
                f'<a href="/blog/{older["slug"]}/"><small>Next \u2192</small><strong>{html.escape(short_label(h1_of(older["slug"])))}</strong></a>\n'
                if older
                else f'<a href="/"><small>All insights \u2192</small><strong>Back to Insights</strong></a>\n'
            )
            prevnext = f'<div class="prevnext">\n{links}</div>'

        template_html = read_text(pick_template())
        for token, name in ((DISCLAIMER, "unified footer Disclaimer"), (FONTS_HREF, "Google Fonts link")):
            if token not in template_html:
                raise PublishError(f"Template is missing {name}; refusing to publish from a stale template")
        article_page = build_article(template_html, pkg, body_html, prevnext)
        homepage_new = update_homepage(read_text(HOMEPAGE), pkg, hero_src)
        sitemap_new = read_text(SITEMAP).replace(
            "</urlset>",
            f"<url><loc>{SITE}/blog/{slug}/</loc><changefreq>yearly</changefreq><priority>0.9</priority></url>\n</urlset>",
        )
        rss_new = read_text(RSS).replace(
            "</channel>",
            f"<item><title>{html.escape(pkg['title'].strip())}</title>"
            f"<link>{SITE}/blog/{slug}/</link>"
            f"<pubDate>{rfc822_gmt(pkg['publish_date'])}</pubDate></item>\n</channel>",
        )
        kit = linkedin_kit(pkg, slug)
        if args.dry_run:
            print(f"DRY RUN ok: blog/{slug}/ + homepage + sitemap + rss; no files written.")
            print("--- LinkedIn kit ---")
            print(kit)
            return 0
        (target).mkdir(parents=True)
        (target / "index.html").write_text(article_page, encoding="utf-8")
        HOMEPAGE.write_text(homepage_new, encoding="utf-8")
        SITEMAP.write_text(sitemap_new, encoding="utf-8")
        RSS.write_text(rss_new, encoding="utf-8")
        # Repair the prev/next chain. Existing link labels are preserved; only the
        # link that must point at the new post is rewritten (href + label).
        def repoint(page_slug: str, link_index: int, new_href: str, new_small: str, new_label: str) -> None:
            page = BLOG_DIR / page_slug / "index.html"
            phtml = read_text(page)
            m = re.search(r'(?s)<div class="prevnext">.*?</div>', phtml)
            if not m:
                raise PublishError(f"Neighbour {page_slug} has no prevnext block")
            links = re.findall(r'(?s)<a href=".*?">.*?</a>', m.group(0))
            if link_index >= len(links):
                raise PublishError(f"Neighbour {page_slug} prevnext has no link #{link_index}")
            links[link_index] = (
                f'<a href="{html.escape(new_href, quote=True)}">'
                f"<small>{new_small}</small><strong>{html.escape(new_label)}</strong></a>"
            )
            new_block = '<div class="prevnext">\n' + "\n".join(links) + "\n</div>"
            page.write_text(phtml.replace(m.group(0), new_block, 1), encoding="utf-8")

        def set_first_link(page_slug: str, small: str, href: str, label: str) -> None:
            repoint(page_slug, 0, href, small, label)

        if newer is None and older is not None and len(posts) == 1:
            # Second post ever: previously-newest was [Next, All]; becomes [Previous(new), All].
            page = BLOG_DIR / older["slug"] / "index.html"
            phtml = read_text(page)
            m = re.search(r'(?s)<div class="prevnext">.*?</div>', phtml)
            if not m:
                raise PublishError(f"Neighbour {older['slug']} has no prevnext block")
            links = re.findall(r'(?s)<a href=".*?">.*?</a>', m.group(0))
            first = (
                f'<a href="/blog/{slug}/">'
                f"<small>\u2190 Previous</small><strong>{html.escape(my_short)}</strong></a>"
            )
            rest = links[1:] if len(links) > 1 else [
                f'<a href="/"><small>All insights \u2192</small><strong>Back to Insights</strong></a>'
            ]
            new_block = '<div class="prevnext">\n' + "\n".join([first] + rest) + "\n</div>"
            page.write_text(phtml.replace(m.group(0), new_block, 1), encoding="utf-8")
        elif newer is None and older is not None:
            # Normal newest insert: previously-newest was [Next(second, kept), All(dropped)].
            page = BLOG_DIR / older["slug"] / "index.html"
            phtml = read_text(page)
            m = re.search(r'(?s)<div class="prevnext">.*?</div>', phtml)
            if not m:
                raise PublishError(f"Neighbour {older['slug']} has no prevnext block")
            links = re.findall(r'(?s)<a href=".*?">.*?</a>', m.group(0))
            first = (
                f'<a href="/blog/{slug}/">'
                f"<small>\u2190 Previous</small><strong>{html.escape(my_short)}</strong></a>"
            )
            kept = links[0] if links else (
                f'<a href="/"><small>All insights \u2192</small><strong>Back to Insights</strong></a>'
            )
            new_block = '<div class="prevnext">\n' + "\n".join([first, kept]) + "\n</div>"
            page.write_text(phtml.replace(m.group(0), new_block, 1), encoding="utf-8")
        else:
            # Middle or oldest insert: repoint the adjacent links, preserving labels elsewhere.
            if older is not None:
                set_first_link(older["slug"], "\u2190 Previous", f"/blog/{slug}/", my_short)
            if newer is not None:
                nhtml = read_text(BLOG_DIR / newer["slug"] / "index.html")
                nm = re.search(r'(?s)<div class="prevnext">.*?</div>', nhtml)
                nlinks = re.findall(r'(?s)<a href=".*?">.*?</a>', nm.group(0)) if nm else []
                if len(nlinks) >= 2:
                    repoint(newer["slug"], 1, f"/blog/{slug}/", "Next \u2192", my_short)
                elif len(nlinks) == 1:
                    page = BLOG_DIR / newer["slug"] / "index.html"
                    phtml = read_text(page)
                    new_block = (
                        '<div class="prevnext">\n' + nlinks[0] + "\n"
                        f'<a href="/blog/{slug}/"><small>Next \u2192</small>'
                        f"<strong>{html.escape(my_short)}</strong></a>\n</div>"
                    )
                    page.write_text(phtml.replace(nm.group(0), new_block, 1), encoding="utf-8")
        out_path = Path(args.linkedin_out) if args.linkedin_out else Path(args.package).parent / f"linkedin-{slug}.txt"
        out_path.write_text(kit, encoding="utf-8")
        print(f"Created blog/{slug}/index.html")
        print("Updated index.html (featured + list, kept 5), sitemap.xml, blog/rss.xml")
        print(f"Wrote LinkedIn kit to {out_path}")
        print("--- LinkedIn kit ---")
        print(kit)
        print("Next: verify locally, then: git add blog/<slug> index.html sitemap.xml blog/rss.xml images/<hero> tools/licenses/<slug>.source.txt; git commit; git push origin main")
        return 0
    except PublishError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
