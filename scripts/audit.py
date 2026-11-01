#!/usr/bin/env python3
"""
SEO Intelligence Auditor - Standalone Zero-Dependency Audit Tool
Analyzes live URLs or local HTML/JSX/TSX files for SEO compliance, meta tags,
schema markup, heading hierarchy, image alt text, and semantic structure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class HTMLSEOParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title: str = ""
        self.in_title: bool = False

        self.meta_tags: list[dict[str, str]] = []
        self.canonical: str | None = None
        self.robots: str | None = None

        self.headings: list[dict[str, Any]] = []
        self.current_tag: str | None = None
        self.current_heading_text: list[str] = []

        self.images: list[dict[str, Any]] = []
        self.links: list[dict[str, Any]] = []
        self.schemas: list[str] = []

        self.in_script: bool = False
        self.script_type: str | None = None
        self.current_script_text: list[str] = []

        self.body_tokens: list[str] = []
        self.in_body: bool = False
        self.skip_tags: set[str] = {"script", "style", "noscript", "svg"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {k.lower(): (v or "") for k, v in attrs}
        tag_lower = tag.lower()

        if tag_lower == "body":
            self.in_body = True

        if tag_lower == "title":
            self.in_title = True

        elif tag_lower == "meta":
            self.meta_tags.append(attr_dict)
            name = attr_dict.get("name", "").lower()
            if name == "robots":
                self.robots = attr_dict.get("content", "")

        elif tag_lower == "link":
            rel = attr_dict.get("rel", "").lower()
            if "canonical" in rel:
                self.canonical = attr_dict.get("href", "")

        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.current_tag = tag_lower
            self.current_heading_text = []

        elif tag_lower == "img":
            self.images.append({
                "src": attr_dict.get("src", ""),
                "alt": attr_dict.get("alt", None),
                "loading": attr_dict.get("loading", ""),
            })

        elif tag_lower == "a":
            href = attr_dict.get("href", "")
            if href:
                self.links.append({
                    "href": href,
                    "rel": attr_dict.get("rel", ""),
                    "target": attr_dict.get("target", ""),
                })

        elif tag_lower == "script":
            self.in_script = True
            self.script_type = attr_dict.get("type", "").lower()
            self.current_script_text = []

    def handle_endtag(self, tag: str) -> None:
        tag_lower = tag.lower()

        if tag_lower == "title":
            self.in_title = False

        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if self.current_tag == tag_lower:
                text = " ".join("".join(self.current_heading_text).split())
                if text:
                    self.headings.append({"level": tag_lower, "text": text})
            self.current_tag = None
            self.current_heading_text = []

        elif tag_lower == "script":
            if self.in_script and self.script_type == "application/ld+json":
                raw_json = "".join(self.current_script_text).strip()
                if raw_json:
                    self.schemas.append(raw_json)
            self.in_script = False
            self.script_type = None
            self.current_script_text = []

        elif tag_lower == "body":
            self.in_body = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        elif self.current_tag:
            self.current_heading_text.append(data)
        elif self.in_script:
            self.current_script_text.append(data)
        elif self.in_body:
            cleaned = re.sub(r"[^\w\s-]", " ", data.lower())
            words = [w for w in cleaned.split() if len(w) > 2]
            if words:
                self.body_tokens.extend(words)


def extract_meta_val(meta_tags: list[dict[str, str]], key_name: str, val: str) -> str | None:
    for m in meta_tags:
        if m.get(key_name, "").lower() == val.lower():
            return m.get("content", "")
    return None


def fetch_url(url: str, user_agent: str = "Mozilla/5.0 (compatible; SEOIntelligence/1.0)") -> str:
    parsed = urllib.parse.urlsplit(url)
    if not parsed.scheme:
        url = "https://" + url

    req = urllib.request.Request(
        url,
        headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        content = resp.read()
        return content.decode(charset, errors="replace")


def analyze_html(html_content: str, source_identifier: str = "") -> dict[str, Any]:
    parser = HTMLSEOParser()
    parser.feed(html_content)

    title = parser.title.strip()
    meta_desc = (
        extract_meta_val(parser.meta_tags, "name", "description")
        or extract_meta_val(parser.meta_tags, "property", "og:description")
        or ""
    )
    og_title = extract_meta_val(parser.meta_tags, "property", "og:title")
    og_image = extract_meta_val(parser.meta_tags, "property", "og:image")
    twitter_card = extract_meta_val(parser.meta_tags, "name", "twitter:card") or extract_meta_val(parser.meta_tags, "property", "twitter:card")
    viewport = extract_meta_val(parser.meta_tags, "name", "viewport")

    # Score calculation
    checks: list[dict[str, Any]] = []
    score = 100

    # 1. Title Audit
    if not title:
        score -= 20
        checks.append({"rule": "title_presence", "status": "FAIL", "message": "Missing <title> tag."})
    elif len(title) < 30:
        score -= 5
        checks.append({"rule": "title_length", "status": "WARN", "message": f"Title too short ({len(title)} chars). Recommended: 45-60 chars.", "value": title})
    elif len(title) > 65:
        score -= 5
        checks.append({"rule": "title_length", "status": "WARN", "message": f"Title likely truncated in SERP ({len(title)} chars > 65).", "value": title})
    else:
        checks.append({"rule": "title_length", "status": "PASS", "message": f"Optimal title length ({len(title)} chars).", "value": title})

    # 2. Meta Description
    if not meta_desc:
        score -= 15
        checks.append({"rule": "meta_description", "status": "FAIL", "message": "Missing meta description."})
    elif len(meta_desc) < 70:
        score -= 5
        checks.append({"rule": "meta_description", "status": "WARN", "message": f"Meta description is short ({len(meta_desc)} chars). Recommended: 120-155 chars.", "value": meta_desc})
    elif len(meta_desc) > 165:
        score -= 5
        checks.append({"rule": "meta_description", "status": "WARN", "message": f"Meta description exceeds SERP snippet limit ({len(meta_desc)} chars > 160).", "value": meta_desc})
    else:
        checks.append({"rule": "meta_description", "status": "PASS", "message": f"Meta description is within ideal range ({len(meta_desc)} chars).", "value": meta_desc})

    # 3. Canonical Tag
    if not parser.canonical:
        score -= 10
        checks.append({"rule": "canonical_tag", "status": "WARN", "message": "Missing rel='canonical' tag. Risk of duplicate content."})
    else:
        checks.append({"rule": "canonical_tag", "status": "PASS", "message": "Canonical tag present.", "value": parser.canonical})

    # 4. Viewport
    if not viewport:
        score -= 10
        checks.append({"rule": "mobile_viewport", "status": "FAIL", "message": "Missing mobile viewport meta tag."})
    else:
        checks.append({"rule": "mobile_viewport", "status": "PASS", "message": "Mobile viewport defined."})

    # 5. Headings Analysis
    h1s = [h["text"] for h in parser.headings if h["level"] == "h1"]
    h2s = [h["text"] for h in parser.headings if h["level"] == "h2"]

    if len(h1s) == 0:
        score -= 15
        checks.append({"rule": "h1_presence", "status": "FAIL", "message": "No <h1> heading detected on page."})
    elif len(h1s) > 1:
        score -= 5
        checks.append({"rule": "h1_count", "status": "WARN", "message": f"Multiple <h1> tags found ({len(h1s)}). Best practice is exactly one primary H1.", "items": h1s})
    else:
        checks.append({"rule": "h1_structure", "status": "PASS", "message": f"Single H1 detected: '{h1s[0]}'"})

    if len(h2s) == 0:
        checks.append({"rule": "h2_sections", "status": "WARN", "message": "No <h2> subheadings detected. Subsections improve topical authority."})
    else:
        checks.append({"rule": "h2_sections", "status": "PASS", "message": f"Detected {len(h2s)} <h2> sections."})

    # 6. Images & Alt Attributes
    images_missing_alt = [img["src"] for img in parser.images if img["alt"] is None or img["alt"].strip() == ""]
    if images_missing_alt:
        penalty = min(15, len(images_missing_alt) * 3)
        score -= penalty
        checks.append({"rule": "images_alt", "status": "FAIL" if len(images_missing_alt) > 3 else "WARN", "message": f"{len(images_missing_alt)} of {len(parser.images)} images lack alt text.", "count": len(images_missing_alt)})
    else:
        checks.append({"rule": "images_alt", "status": "PASS", "message": f"All {len(parser.images)} images have alt attributes."})

    # 7. OpenGraph / Social
    if not og_title or not og_image:
        score -= 5
        checks.append({"rule": "opengraph", "status": "WARN", "message": "Missing og:title or og:image tags for rich social sharing."})
    else:
        checks.append({"rule": "opengraph", "status": "PASS", "message": "OpenGraph social tags configured."})

    # 8. Schema Markup (JSON-LD)
    parsed_schemas = []
    for s_raw in parser.schemas:
        try:
            data = json.loads(s_raw)
            if isinstance(data, dict):
                parsed_schemas.append(data.get("@type", "Unknown"))
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        parsed_schemas.append(item.get("@type", "Unknown"))
        except Exception:
            pass

    if not parsed_schemas:
        score -= 10
        checks.append({"rule": "structured_data", "status": "WARN", "message": "No JSON-LD structured data detected. Consider adding WebSite, Article, or FAQPage schema."})
    else:
        checks.append({"rule": "structured_data", "status": "PASS", "message": f"Detected Schema types: {', '.join(set(parsed_schemas))}", "types": list(set(parsed_schemas))})

    score = max(0, min(100, score))

    # Keyword frequency & word count
    word_count = len(parser.body_tokens)
    top_keywords = Counter(parser.body_tokens).most_common(10)

    return {
        "source": source_identifier,
        "overall_score": score,
        "summary": {
            "title": title,
            "title_length": len(title),
            "meta_description": meta_desc,
            "meta_description_length": len(meta_desc),
            "canonical": parser.canonical,
            "robots": parser.robots,
            "h1_count": len(h1s),
            "h2_count": len(h2s),
            "total_images": len(parser.images),
            "images_missing_alt_count": len(images_missing_alt),
            "total_links": len(parser.links),
            "schemas_found": list(set(parsed_schemas)),
            "word_count": word_count,
        },
        "headings": parser.headings[:15],
        "top_keywords": top_keywords,
        "audit_checks": checks,
    }


def format_report_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    score = report["overall_score"]
    badge = "🟢 EXCELLENT" if score >= 90 else "🟡 NEEDS IMPROVEMENT" if score >= 70 else "🔴 CRITICAL ISSUES"

    lines = [
        f"# SEO Intelligence Audit Report",
        f"**Target:** `{report.get('source', 'Unknown')}`",
        f"**Overall Health Score:** **{score}/100** ({badge})",
        "",
        "## Key Meta Signals",
        f"- **Title ({summary['title_length']} chars):** `{summary['title'] or '[MISSING]'}`",
        f"- **Description ({summary['meta_description_length']} chars):** `{summary['meta_description'] or '[MISSING]'}`",
        f"- **Canonical URL:** `{summary['canonical'] or '[NOT SET]'}`",
        f"- **Robots Directive:** `{summary['robots'] or 'index, follow (default)'}`",
        f"- **Word Count:** `{summary['word_count']} words`",
        f"- **Schemas:** `{', '.join(summary['schemas_found']) if summary['schemas_found'] else 'None'}`",
        "",
        "## Audit Findings & Recommended Fixes",
        "| Rule | Status | Finding / Action Required |",
        "| :--- | :---: | :--- |",
    ]

    for c in report["audit_checks"]:
        icon = "✅" if c["status"] == "PASS" else "⚠️" if c["status"] == "WARN" else "❌"
        lines.append(f"| `{c['rule']}` | {icon} **{c['status']}** | {c['message']} |")

    lines.extend([
        "",
        "## Heading Hierarchy Sample",
    ])
    if report["headings"]:
        for h in report["headings"][:10]:
            indent = "  " * (int(h["level"][1]) - 1)
            lines.append(f"{indent}- **{h['level'].upper()}:** {h['text']}")
    else:
        lines.append("- *No headings found.*")

    lines.extend([
        "",
        "## Top Recurring Terms (Content Density)",
        f"- {', '.join(f'`{k}` ({v})' for k, v in report['top_keywords'])}",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="SEO Intelligence Standalone Page Auditor")
    parser.add_argument("target", help="URL or local file path (HTML/JSX/TSX) to audit")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--output", help="Save output to file instead of stdout")

    args = parser.parse_args()
    target_path = Path(args.target)

    if target_path.exists() and target_path.is_file():
        content = target_path.read_text(encoding="utf-8", errors="replace")
        source = str(target_path)
    else:
        source = args.target
        try:
            content = fetch_url(source)
        except Exception as e:
            sys.stderr.write(f"Error fetching URL '{source}': {e}\n")
            sys.exit(1)

    result = analyze_html(content, source_identifier=source)

    if args.format == "json":
        output_str = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        output_str = format_report_markdown(result)

    if args.output:
        Path(args.output).write_text(output_str, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
