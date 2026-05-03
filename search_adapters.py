from __future__ import annotations
import xml.etree.ElementTree as ET
from typing import Callable

def classify_exception(exc: Exception) -> str:
    name = exc.__class__.__name__.lower()
    msg = str(exc).lower()
    if "timeout" in name or "timed out" in msg:
        return "timeout"
    if "connection" in name or "connection" in msg:
        return "connection_error"
    if "http" in name or "status" in msg:
        return "http_error"
    if "json" in name or "decode" in msg:
        return "parse_error"
    return "unknown_error"

def ddg_extract_results(
    html: str,
    normalize_url_from_search: Callable[[str], str],
    decode_html_entities: Callable[[str], str],
    detect_extension_from_response: Callable[[str, str], str],
    bs4_module
) -> list[dict]:
    if bs4_module is None:
        return []
    soup = bs4_module(html, "html.parser")
    out = []
    for a in soup.select("a.result__a, a[data-testid='result-title-a']"):
        href = normalize_url_from_search(a.get("href", ""))
        title = decode_html_entities(a.get_text(" ", strip=True))
        if not href or not title:
            continue
        snippet = ""
        parent = a.parent
        if parent and hasattr(parent, "find"):
            snip_tag = parent.find(class_="result__snippet")
            if snip_tag:
                snippet = snip_tag.get_text(" ", strip=True)
        out.append({
            "href": href,
            "title": title,
            "snippet": snippet,
            "ext": detect_extension_from_response(href, ""),
        })
    return out

def parse_bing_rss(xml_bytes: bytes, decode_html_entities: Callable[[str], str], first_nonempty: Callable[..., str], detect_extension_from_response: Callable[[str, str], str]) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    out = []
    for item in root.findall(".//item"):
        title = decode_html_entities(first_nonempty(item.findtext("title"), ""))
        link = first_nonempty(item.findtext("link"), "")
        snippet = decode_html_entities(first_nonempty(item.findtext("description"), ""))
        if not link or not title:
            continue
        out.append({
            "href": link,
            "title": title,
            "snippet": snippet,
            "ext": detect_extension_from_response(link, ""),
        })
    return out

def parse_internet_archive_docs(data: dict, safe_dict: Callable[[object], dict], safe_list: Callable[[object], list], first_nonempty: Callable[..., str], decode_html_entities: Callable[[str], str]) -> list[dict]:
    response = safe_dict(data.get("response"))
    raw_docs = response.get("docs", [])
    docs = safe_list(raw_docs) if isinstance(raw_docs, list) else []
    out = []
    for item in docs:
        if not isinstance(item, dict):
            continue
        identifier = first_nonempty(item.get("identifier"), "")
        title = decode_html_entities(first_nonempty(item.get("title"), identifier))
        if not identifier or not title:
            continue
        out.append({
            "identifier": identifier,
            "title": title,
            "description": decode_html_entities(first_nonempty(item.get("description"), "")),
            "year": str(first_nonempty(item.get("year"), "")),
            "language": first_nonempty(item.get("language"), ""),
            "mediatype": first_nonempty(item.get("mediatype"), "archive_item"),
        })
    return out
