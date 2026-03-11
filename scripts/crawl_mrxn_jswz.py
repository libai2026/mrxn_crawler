#!/usr/bin/env python3
"""抓取 https://mrxn.net/jswz 下的技术文章并导出为 HTML + Markdown。"""

from __future__ import annotations

import argparse
import json
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse

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
class CrawlConfig:
    timeout: int = 25
    max_retries: int = 6
    base_backoff: float = 1.5
    min_interval: float = 1.2
    jitter_max: float = 0.8


@dataclass
class Article:
    url: str
    title: str
    slug: str
    html: str
    markdown: str


class ThrottledClient:
    def __init__(self, session: requests.Session, cfg: CrawlConfig) -> None:
        self.session = session
        self.cfg = cfg
        self._last_request_ts = 0.0

    def _sleep_for_rate_limit(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_request_ts
        if elapsed < self.cfg.min_interval:
            wait_for = self.cfg.min_interval - elapsed
            print(f"[DEBUG] 速率控制等待 {wait_for:.2f}s")
            time.sleep(wait_for)

    def get_soup(self, url: str) -> BeautifulSoup:
        last_exc: Exception | None = None
        for attempt in range(1, self.cfg.max_retries + 1):
            self._sleep_for_rate_limit()
            try:
                print(f"[DEBUG] GET attempt={attempt} url={url}")
                resp = self.session.get(url, timeout=self.cfg.timeout)
                self._last_request_ts = time.monotonic()
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        wait_seconds = int(retry_after)
                    else:
                        wait_seconds = self.cfg.base_backoff * (2 ** (attempt - 1))
                    wait_seconds += random.uniform(0, self.cfg.jitter_max)
                    print(f"[WARN] 429 Too Many Requests: {url}, 等待 {wait_seconds:.2f}s 后重试")
                    time.sleep(wait_seconds)
                    continue

                resp.raise_for_status()
                return BeautifulSoup(resp.text, "lxml")
            except requests.RequestException as exc:
                last_exc = exc
                wait_seconds = self.cfg.base_backoff * (2 ** (attempt - 1))
                wait_seconds += random.uniform(0, self.cfg.jitter_max)
                print(f"[WARN] 请求失败 attempt={attempt}/{self.cfg.max_retries} url={url}: {exc}")
                if attempt == self.cfg.max_retries:
                    break
                print(f"[WARN] 等待 {wait_seconds:.2f}s 后重试")
                time.sleep(wait_seconds)

        raise RuntimeError(f"请求失败(重试耗尽): {url}; last_error={last_exc}")


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


def discover_jswz_pages(client: ThrottledClient, max_pages: int) -> list[str]:
    queue = [urljoin(BASE_URL, START_PATH)]
    seen = set()
    pages: list[str] = []

    while queue and len(pages) < max_pages:
        current = normalize_url(queue.pop(0))
        if current in seen:
            continue
        seen.add(current)
        try:
            soup = client.get_soup(current)
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


def extract_article_urls(client: ThrottledClient, pages: Iterable[str]) -> list[str]:
    urls: set[str] = set()
    for page in pages:
        try:
            soup = client.get_soup(page)
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] 跳过 {page}: {exc}")
            continue

        for a in soup.select("a[href]"):
            href = normalize_url(urljoin(page, a.get("href", "")))
            if likely_article_url(href):
                urls.add(href)
    return sorted(urls)


def parse_article(client: ThrottledClient, url: str) -> Article | None:
    try:
        soup = client.get_soup(url)
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
    escaped_title = article.title.replace('"', '\\"')
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
    parser.add_argument("--delay", type=float, default=0.5, help="每篇文章额外延时(秒)")
    parser.add_argument("--timeout", type=int, default=25, help="单次请求超时(秒)")
    parser.add_argument("--max-retries", type=int, default=6, help="请求最大重试次数")
    parser.add_argument("--base-backoff", type=float, default=1.5, help="指数退避基数(秒)")
    parser.add_argument("--min-interval", type=float, default=1.2, help="请求最小间隔(秒)")
    parser.add_argument("--jitter-max", type=float, default=0.8, help="重试随机抖动上限(秒)")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    cfg = CrawlConfig(
        timeout=args.timeout,
        max_retries=args.max_retries,
        base_backoff=args.base_backoff,
        min_interval=args.min_interval,
        jitter_max=args.jitter_max,
    )

    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    client = ThrottledClient(session, cfg)

    print(f"[INFO] 配置: {cfg}")
    print("[INFO] 发现列表页...")
    pages = discover_jswz_pages(client, max_pages=args.max_pages)
    print(f"[INFO] 列表页数量: {len(pages)}")

    urls = extract_article_urls(client, pages)
    print(f"[INFO] 候选文章数量: {len(urls)}")

    manifest = []
    for idx, url in enumerate(urls, start=1):
        print(f"[INFO] ({idx}/{len(urls)}) 抓取 {url}")
        article = parse_article(client, url)
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
