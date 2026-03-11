#!/usr/bin/env python3
"""使用 Playwright 抓取 https://mrxn.net/jswz 技术文章，导出 Markdown + 图片。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as html2md
from playwright.sync_api import BrowserContext, Page, sync_playwright

BASE_URL = "https://mrxn.net"
START_PATH = "/jswz"
SKIP_PATH_PREFIXES = (
    "/jswz/tag/",
    "/jswz/category/",
    "/jswz/author/",
    "/jswz/wp-",
)
SKIP_PATH_CONTAINS = ("/feed", "/comment")
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)


@dataclass
class CrawlConfig:
    timeout: int = 35
    max_retries: int = 5
    base_backoff: float = 2.0
    min_interval: float = 1.5
    delay: float = 0.8


@dataclass
class CrawlResult:
    success: list[dict[str, str]]
    failed: list[dict[str, str]]
    discovered_pages: list[str]
    candidate_urls: list[str]


def normalize_url(url: str) -> str:
    normalized, _ = urldefrag(url)
    return normalized.rstrip("/") or normalized


def sanitize_filename(text: str) -> str:
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"[\\/:*?\"<>|]+", "", text)
    text = re.sub(r"-+", "-", text).strip(".-_")
    return (text[:120] or "untitled").lower()


def is_within_jswz(url: str) -> bool:
    p = urlparse(url)
    return p.netloc == urlparse(BASE_URL).netloc and p.path.startswith(START_PATH)


def article_url_reason(url: str) -> tuple[bool, str]:
    p = urlparse(url)
    path = p.path
    if not path.startswith(START_PATH):
        return False, "out_of_scope"
    if any(path.startswith(prefix) for prefix in SKIP_PATH_PREFIXES):
        return False, "taxonomy_or_system_path"
    if any(k in path for k in SKIP_PATH_CONTAINS):
        return False, "feed_or_comment_path"
    if path in {START_PATH, START_PATH + "/"}:
        return False, "root_path"
    if re.search(r"/page/\d+/?$", path):
        return False, "pagination_path"
    parts = [seg for seg in path.split("/") if seg]
    if len(parts) < 2:
        return False, "path_too_short"
    # 过滤纯数字分页/索引页，例如 /jswz/21.html
    stem = Path(parts[-1]).stem
    if stem.isdigit():
        return False, "numeric_slug"
    return True, "ok"


def likely_article_url(url: str) -> bool:
    ok, _ = article_url_reason(url)
    return ok


def safe_page_title(page: Page, fallback_url: str) -> str:
    # 不使用会等待 30s 的 locator.text_content，避免无 h1 页面导致超时崩溃
    try:
        h1 = page.eval_on_selector("h1", "el => el.textContent")
        if isinstance(h1, str) and h1.strip():
            return h1.strip()
    except Exception:
        pass

    try:
        og = page.eval_on_selector('meta[property="og:title"]', "el => el.getAttribute('content')")
        if isinstance(og, str) and og.strip():
            return og.strip()
    except Exception:
        pass

    try:
        t = page.title() or ""
        if t.strip():
            return t.strip()
    except Exception:
        pass

    return Path(urlparse(fallback_url).path).name or "untitled"


def is_challenge_page(page: Page) -> bool:
    t = (page.title() or "").lower()
    html = (page.content() or "").lower()
    return "just a moment" in t or "enable javascript and cookies to continue" in html


def goto_with_retry(page: Page, url: str, cfg: CrawlConfig) -> bool:
    for attempt in range(1, cfg.max_retries + 1):
        try:
            print(f"[DEBUG] goto attempt={attempt} url={url}")
            page.goto(url, wait_until="domcontentloaded", timeout=cfg.timeout * 1000)
            page.wait_for_timeout(2500)
            if is_challenge_page(page):
                wait_s = cfg.base_backoff * (2 ** (attempt - 1))
                print(f"[WARN] challenge page detected: {url}, wait {wait_s:.1f}s")
                page.wait_for_timeout(int(wait_s * 1000))
                continue
            return True
        except Exception as exc:  # noqa: BLE001
            wait_s = cfg.base_backoff * (2 ** (attempt - 1))
            print(f"[WARN] goto failed attempt={attempt} url={url}: {exc}")
            if attempt == cfg.max_retries:
                return False
            page.wait_for_timeout(int(wait_s * 1000))
    return False


def discover_jswz_pages(page: Page, cfg: CrawlConfig, max_pages: int) -> list[str]:
    queue = [urljoin(BASE_URL, START_PATH)]
    seen = set()
    pages: list[str] = []

    while queue and len(pages) < max_pages:
        current = normalize_url(queue.pop(0))
        if current in seen:
            continue
        seen.add(current)
        print(f"[INFO] 访问列表页({len(pages) + 1}/{max_pages}): {current}")

        if not goto_with_retry(page, current, cfg):
            print(f"[WARN] 列表页访问失败: {current}")
            continue

        pages.append(current)
        links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
        for href in links:
            href = normalize_url(href)
            if not is_within_jswz(href):
                continue
            path = urlparse(href).path
            if href in seen or href in queue:
                continue
            if path.startswith(START_PATH + "/page/") or path in {START_PATH, START_PATH + "/"}:
                queue.append(href)

        print(f"[INFO] 已发现列表页 {len(pages)} 个，待访问 {len(queue)} 个")
        page.wait_for_timeout(int(cfg.min_interval * 1000))

    return pages


def extract_article_urls(page: Page, cfg: CrawlConfig, pages: Iterable[str]) -> list[str]:
    urls: set[str] = set()
    skipped_numeric = 0
    page_list = list(pages)
    for idx, list_url in enumerate(page_list, start=1):
        print(f"[INFO] 解析列表页文章链接({idx}/{len(page_list)}): {list_url}")
        if not goto_with_retry(page, list_url, cfg):
            print(f"[WARN] 跳过列表页: {list_url}")
            continue
        links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
        for href in links:
            href = normalize_url(href)
            ok, reason = article_url_reason(href)
            if ok:
                urls.add(href)
            elif reason == "numeric_slug":
                skipped_numeric += 1
        print(f"[INFO] 当前累计候选文章: {len(urls)} (过滤numeric_slug: {skipped_numeric})")
        page.wait_for_timeout(int(cfg.min_interval * 1000))
    return sorted(urls)


def pick_article_html(page: Page) -> str:
    for selector in ("article", ".entry-content", "main", "body"):
        loc = page.locator(selector)
        if loc.count() > 0:
            return loc.first.inner_html()
    return page.content()


def infer_ext_from_url(url: str) -> str:
    p = urlparse(url)
    suffix = Path(p.path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".avif"}:
        return suffix
    return ".bin"


def download_images(context: BrowserContext, article_url: str, article_html: str, images_dir: Path) -> str:
    soup = BeautifulSoup(article_html, "html.parser")
    images_dir.mkdir(parents=True, exist_ok=True)

    for idx, img in enumerate(soup.select("img[src]"), start=1):
        src = (img.get("src") or "").strip()
        if not src:
            continue
        if src.startswith("data:"):
            # 内联 base64 图片不下载，保留原始 data URI
            continue
        full_url = urljoin(article_url, src)
        ext = infer_ext_from_url(full_url)
        digest = hashlib.md5(full_url.encode("utf-8")).hexdigest()[:12]
        filename = f"img-{idx:03d}-{digest}{ext}"
        out_path = images_dir / filename

        try:
            resp = context.request.get(full_url, timeout=30000)
            if resp.ok:
                out_path.write_bytes(resp.body())
                img["src"] = f"images/{filename}"
            else:
                print(f"[WARN] 图片下载失败 status={resp.status} url={full_url}")
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] 图片下载异常 url={full_url}: {exc}")

    return str(soup)


def parse_article(page: Page, context: BrowserContext, cfg: CrawlConfig, url: str, output_dir: Path) -> dict[str, str] | None:
    if not goto_with_retry(page, url, cfg):
        print(f"[WARN] 文章抓取失败: {url}")
        return None

    title = safe_page_title(page, url)
    safe_title = sanitize_filename(title)

    article_html = pick_article_html(page)
    article_dir = output_dir / "assets" / safe_title
    rewritten_html = download_images(context, url, article_html, article_dir / "images")

    markdown = html2md(rewritten_html, heading_style="ATX", strip=["script", "style"])
    md_path = output_dir / "markdown" / f"{safe_title}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)

    escaped_title = title.replace("\"", "\\\"")
    front_matter = (
        "---\n"
        f'title: "{escaped_title}"\n'
        f"source: {url}\n"
        f"asset_dir: assets/{safe_title}\n"
        "---\n\n"
    )
    md_path.write_text(front_matter + markdown, encoding="utf-8")
    return {"title": title, "url": url, "filename": md_path.name, "asset_dir": f"assets/{safe_title}"}


def main() -> None:
    parser = argparse.ArgumentParser(description="抓取 mrxn/jswz 技术文章（Playwright）")
    parser.add_argument("--output", default="output/jswz", help="导出目录")
    parser.add_argument("--max-pages", type=int, default=100, help="最大列表页数")
    parser.add_argument("--delay", type=float, default=0.8, help="每篇文章抓取后的额外延时(秒)")
    parser.add_argument("--timeout", type=int, default=35, help="页面加载超时(秒)")
    parser.add_argument("--max-retries", type=int, default=5, help="页面请求最大重试")
    parser.add_argument("--base-backoff", type=float, default=2.0, help="指数退避基数(秒)")
    parser.add_argument("--min-interval", type=float, default=1.5, help="页面请求最小间隔(秒)")
    args = parser.parse_args()

    cfg = CrawlConfig(
        timeout=args.timeout,
        max_retries=args.max_retries,
        base_backoff=args.base_backoff,
        min_interval=args.min_interval,
        delay=args.delay,
    )

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] 配置: {cfg}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA)
        page = context.new_page()

        pages = discover_jswz_pages(page, cfg, args.max_pages)
        urls = extract_article_urls(page, cfg, pages)

        success: list[dict[str, str]] = []
        failed: list[dict[str, str]] = []
        for idx, url in enumerate(urls, start=1):
            print(f"[INFO] ({idx}/{len(urls)}) 抓取文章: {url}")
            item = parse_article(page, context, cfg, url, out)
            if item:
                success.append(item)
                print(f"[INFO] 保存成功: {item['filename']}")
            else:
                failed.append({"url": url, "reason": "page_blocked_or_parse_failed"})
            page.wait_for_timeout(int(cfg.delay * 1000))

        browser.close()

    (out / "manifest.json").write_text(json.dumps(success, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {
        "summary": {
            "discovered_pages": len(pages),
            "candidate_articles": len(urls),
            "success_articles": len(success),
            "failed_articles": len(failed),
        },
        "failed": failed,
    }
    (out / "crawl_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("[INFO] 抓取总结:")
    print(f"[INFO] - 列表页: {len(pages)}")
    print(f"[INFO] - 候选文章: {len(urls)}")
    print(f"[INFO] - 成功文章: {len(success)}")
    print(f"[INFO] - 失败文章: {len(failed)}")
    print(f"[INFO] - 输出目录: {out.resolve()}")


if __name__ == "__main__":
    main()
