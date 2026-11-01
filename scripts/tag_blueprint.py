#!/usr/bin/env python3
"""
SERP Rank-1 Tag & Blueprint Engine
Generates high-CTR title tags, search snippet meta descriptions, and
heading architectures for top rankings. Supports both English and Turkish.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def generate_blueprint(
    keyword: str,
    brand: str = "",
    lang: str = "en",
    page_type: str = "landing",  # landing, blog, product, tool
) -> dict[str, Any]:
    kw = keyword.strip()
    brand_suffix = f" | {brand.strip()}" if brand.strip() else ""

    if lang.lower().startswith("tr"):
        # Turkish Blueprint
        titles = [
            f"{kw.title()} Nedir ve Nasıl Kullanılır?{brand_suffix}",
            f"{kw.title()} — Doğrudan En İyisi ve İpuçları{brand_suffix}",
            f"En İyi {kw.title()} Çözümleri ve Karşılaştırma{brand_suffix}",
            f"{kw.title()} Fiyatları, Yorumları ve Özellikleri{brand_suffix}",
        ]
        # Trim to Google 60-char display limit
        titles = [t[:60] for t in titles]

        meta_descriptions = [
            f"{kw.title()} hakkında aradığınız tüm detaylar, uzman tavsiyeleri ve pratik ipuçları. Şimdi keşfedin ve veriminizi katlayın."[:155],
            f"En güncel {kw.lower()} rehberi: Doğru stratejiler, avantajlar ve dikkat edilmesi gerekenler tek bir yerde. Hemen inceleyin."[:155],
            f"{kw.title()} ile hedeflerinize daha hızlı ulaşın. Güvenilir, hızlı ve kanıtlanmış yöntemlerle fark yaratın."[:155],
        ]

        h1 = f"{kw.title()}: Kapsamlı Rehber ve En İyi Uygulamalar"
        h2_sections = [
            f"{kw.title()} Nedir ve Neden Önemlidir?",
            f"Adım Adım {kw.title()} Nasıl Uygulanır?",
            f"En Sık Yapılan Hatalar ve Kaçınma Yolları",
            f"Karşılaştırma: Hangi Yöntem Sizin İçin Uygun?",
            f"Sıkça Sorulan Sorular ({kw.title()} FAQ)",
        ]
        recommended_schemas = ["FAQPage", "Article", "BreadcrumbList"]
        if page_type == "tool":
            recommended_schemas.insert(0, "SoftwareApplication")
        elif page_type == "product":
            recommended_schemas.insert(0, "Product")
        else:
            recommended_schemas.insert(0, "WebSite")

    else:
        # English Blueprint
        titles = [
            f"{kw.title()} — The Complete Guide for 2026{brand_suffix}",
            f"Best {kw.title()} Software & Strategies{brand_suffix}",
            f"{kw.title()}: How to Choose & Scale Faster{brand_suffix}",
            f"{kw.title()} — #1 Platform for Modern Teams{brand_suffix}",
        ]
        titles = [t[:60] for t in titles]

        meta_descriptions = [
            f"Master {kw.lower()} with our actionable 2026 playbook. Discover proven steps, core features, and best practices to maximize results today."[:155],
            f"Looking for the best {kw.lower()}? Compare top approaches, calculate ROI, and automate your workflow with our in-depth analysis."[:155],
            f"The modern {kw.lower()} designed for high-growth teams. Streamline operations, boost performance, and scale effortlessly."[:155],
        ]

        h1 = f"{kw.title()}: Complete Strategic Guide & Best Practices"
        h2_sections = [
            f"What is {kw.title()} and How Does It Work?",
            f"Key Benefits and Critical Features to Look For",
            f"Step-by-Step Implementation Checklist",
            f"Common Mistakes and How to Avoid Them",
            f"Frequently Asked Questions About {kw.title()}",
        ]
        recommended_schemas = ["FAQPage", "Article", "BreadcrumbList"]
        if page_type == "tool":
            recommended_schemas.insert(0, "SoftwareApplication")
        elif page_type == "product":
            recommended_schemas.insert(0, "Product")
        else:
            recommended_schemas.insert(0, "WebSite")

    return {
        "target_keyword": kw,
        "language": lang,
        "page_type": page_type,
        "title_candidates": titles,
        "meta_description_candidates": meta_descriptions,
        "recommended_h1": h1,
        "heading_structure_h2": h2_sections,
        "recommended_schemas": recommended_schemas,
        "serp_guidelines": {
            "title_ideal_chars": "45-60 characters (keep primary keyword in first 35 chars)",
            "meta_description_ideal_chars": "130-155 characters (must end with clear active CTA)",
            "h1_count": "Exactly 1 per URL, perfectly matching search intent",
            "search_intent_match": "Informational + Transactional balance",
        },
    }


def format_blueprint_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# SERP Rank-1 Blueprint: `{data['target_keyword']}`",
        f"**Language:** `{data['language'].upper()}` | **Intent/Type:** `{data['page_type']}`",
        "",
        "## 1. High-CTR Title Tag Candidates",
        "> Recommended length: 50-60 characters. Place primary keyword near the beginning.",
    ]
    for i, t in enumerate(data["title_candidates"], 1):
        lines.append(f"{i}. `{t}` *({len(t)} chars)*")

    lines.extend([
        "",
        "## 2. Click-Worthy Meta Descriptions",
        "> Recommended length: 130-155 characters. Includes search keyword and clear action trigger.",
    ])
    for i, d in enumerate(data["meta_description_candidates"], 1):
        lines.append(f"{i}. \"{d}\" *({len(d)} chars)*")

    lines.extend([
        "",
        "## 3. Recommended Heading Hierarchy",
        f"- **Primary H1:** `{data['recommended_h1']}`",
        "- **H2 Topical Subsections:**",
    ])
    for h in data["heading_structure_h2"]:
        lines.append(f"  - `<h2>{h}</h2>`")

    lines.extend([
        "",
        "## 4. Required Schema Markup Types (JSON-LD)",
        f"- {', '.join(f'`{s}`' for s in data['recommended_schemas'])}",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Rank-1 SERP blueprint for tags and structure")
    parser.add_argument("keyword", help="Target search query or focus keyword")
    parser.add_argument("--brand", default="", help="Brand name to append (e.g. Acme)")
    parser.add_argument("--lang", default="en", choices=["en", "tr"], help="Language (en or tr, default: en)")
    parser.add_argument("--type", default="landing", choices=["landing", "blog", "product", "tool"], help="Page type")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Output format")

    args = parser.parse_args()
    data = generate_blueprint(keyword=args.keyword, brand=args.brand, lang=args.lang, page_type=args.type)

    if args.format == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(format_blueprint_markdown(data))


if __name__ == "__main__":
    main()
