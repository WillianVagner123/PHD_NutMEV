from __future__ import annotations

from urllib.parse import urljoin
from typing import Callable


def extract_candidate_links_from_html(
    base_url: str,
    html_soup,
    page_title: str,
    page_text_excerpt: str,
    workstream: str,
    source_name: str,
    seed_url: str,
    looks_like_relevant_link: Callable[[str, str], bool],
    detect_extension_from_response: Callable[[str, str], str],
    downloadable_ext: set[str],
    paywall_hints: list[str] | None = None,
    max_links_per_page: int = 20,
):
    rows = []
    local_count = 0
    paywall_hints = paywall_hints or []

    for a in html_soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        href_low = href.lower()
        if any(h in href_low for h in paywall_hints):
            continue
        anchor_text = a.get_text(" ", strip=True)
        if not looks_like_relevant_link(href, anchor_text):
            continue
        ext = detect_extension_from_response(href, "")
        if ext not in downloadable_ext and ext != ".html":
            continue
        rows.append({
            "workstream": workstream,
            "source_name": source_name,
            "seed_url": seed_url,
            "page_url": base_url,
            "page_title": page_title,
            "page_text_excerpt": page_text_excerpt[:400],
            "link_text": anchor_text,
            "link_url": href,
            "link_ext": ext,
            "link_bucket": "document_link" if ext in downloadable_ext else "landing_page",
        })
        local_count += 1
        if local_count >= max_links_per_page:
            break
    return rows
