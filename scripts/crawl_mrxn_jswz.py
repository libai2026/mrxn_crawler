#!/usr/bin/env python3
"""抓取 https://mrxn.net/jswz 下的技术文章并导出为 HTML + Markdown。"""

from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html2md

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
class Article:
    url: str
    title: str
    slug: str
    html: str
    markdown: str


def normalize_url(url: str) -> str:
    normalized, _ = urldefrag(url)
    return normalized.rstrip("/") or normalized


def safe_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w\-\u4e00-\u9fff]", "", text)
    return text[:120] or "article"


def is_within_jswz(url: str) -> bool:
    p = urlparse(url)
    return p.netloc == urlparse(BASE_URL).netloc and p.path.startswith(START_PATH)


def likely_article_url(url: str) -> bool:
    p = urlparse(url)
    path = p.path
    if not path.startswith(START_PATH):
        return False
    if any(path.startswith(prefix) for prefix in SKIP_PATH_PREFIXES):
        return False
    if any(key in path for key in SKIP_PATH_CONTAINS):
        return False
    if path in {START_PATH, START_PATH + "/"}:
        return False
    if re.search(r"/page/\d+/?$", path):
        return False
    parts = [seg for seg in path.split("/") if seg]
    return len(parts) >= 2


def get_soup(session: requests.Session, url: str, timeout: int = 25) -> BeautifulSoup:
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def discover_jswz_pages(session: requests.Session, max_pages: int) -> list[str]:
    queue = [urljoin(BASE_URL, START_PATH)]
    seen = set()
    pages: list[str] = []

    while queue and len(pages) < max_pages:
        current = normalize_url(queue.pop(0))
        if current in seen:
            continue
        seen.add(current)
        try:
            soup = get_soup(session, current)
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] 无法访问列表页 {current}: {exc}")
            continue

        pages.append(current)
        for a in soup.select("a[href]"):
            href = normalize_url(urljoin(current, a.get("href", "")))
            if not is_within_jswz(href):
                continue
            path = urlparse(href).path
            if href in seen or href in queue:
                continue
            if path.startswith(START_PATH + "/page/") or path in {START_PATH, START_PATH + "/"}:
                queue.append(href)

    return pages


def extract_article_urls(session: requests.Session, pages: Iterable[str]) -> list[str]:
    urls: set[str] = set()
    for page in pages:
        try:
            soup = get_soup(session, page)
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] 跳过 {page}: {exc}")
            continue

        for a in soup.select("a[href]"):
            href = normalize_url(urljoin(page, a.get("href", "")))
            if likely_article_url(href):
                urls.add(href)
    return sorted(urls)


def parse_article(session: requests.Session, url: str) -> Article | None:
    try:
        soup = get_soup(session, url)
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] 文章抓取失败 {url}: {exc}")
        return None

    title = (
        soup.select_one("article h1")
        or soup.select_one("h1.entry-title")
        or soup.select_one("h1")
    )
    title_text = title.get_text(strip=True) if title else urlparse(url).path.split("/")[-1]

    article_node = (
        soup.select_one("article")
        or soup.select_one(".entry-content")
        or soup.select_one("main")
        or soup.body
    )
    if not article_node:
        print(f"[WARN] 未找到文章主体 {url}")
        return None

    html = article_node.prettify()
    markdown = html2md(html, heading_style="ATX", strip=["script", "style"])
    slug = safe_slug(urlparse(url).path.split("/")[-1] or title_text)

    return Article(url=url, title=title_text, slug=slug, html=html, markdown=markdown)


def save_article(article: Article, output_dir: Path) -> None:
    html_dir = output_dir / "html"
    md_dir = output_dir / "markdown"
    html_dir.mkdir(parents=True, exist_ok=True)
    md_dir.mkdir(parents=True, exist_ok=True)

    html_path = html_dir / f"{article.slug}.html"
    md_path = md_dir / f"{article.slug}.md"

    html_path.write_text(article.html, encoding="utf-8")
    escaped_title = article.title.replace("\"", "\\\"")
    front_matter = (
        "---\n"
        f'title: "{escaped_title}"\n'
        f"source: {article.url}\n"
        "---\n\n"
    )
    md_path.write_text(front_matter + article.markdown, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="抓取 mrxn/jswz 技术文章")
    parser.add_argument("--output", default="output/jswz", help="导出目录")
    parser.add_argument("--max-pages", type=int, default=100, help="最大列表页数")
    parser.add_argument("--delay", type=float, default=0.2, help="每篇文章抓取延时(秒)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": UA})

    print("[INFO] 发现列表页...")
    pages = discover_jswz_pages(session, max_pages=args.max_pages)
    print(f"[INFO] 列表页数量: {len(pages)}")

    urls = extract_article_urls(session, pages)
    print(f"[INFO] 候选文章数量: {len(urls)}")

    manifest = []
    for idx, url in enumerate(urls, start=1):
        print(f"[INFO] ({idx}/{len(urls)}) 抓取 {url}")
        article = parse_article(session, url)
        if not article:
            continue
        save_article(article, output_dir)
        manifest.append({"title": article.title, "url": article.url, "slug": article.slug})
        time.sleep(args.delay)

    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[INFO] 完成，成功保存 {len(manifest)} 篇文章到 {output_dir}")


if __name__ == "__main__":
    main()
