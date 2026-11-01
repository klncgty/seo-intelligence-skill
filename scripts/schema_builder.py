#!/usr/bin/env python3
"""
JSON-LD Schema Builder
Generates validated, rich-snippet structured data for modern web applications,
SaaS products, articles, FAQs, and organizations.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def build_faq_schema(questions_answers: list[tuple[str, str]]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a,
                },
            }
            for q, a in questions_answers
        ],
    }


def build_software_schema(
    name: str,
    url: str,
    description: str,
    price: str = "0.00",
    currency: str = "USD",
    category: str = "BusinessApplication",
) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "operatingSystem": "All",
        "applicationCategory": category,
        "url": url,
        "description": description,
        "offers": {
            "@type": "Offer",
            "price": price,
            "priceCurrency": currency,
        },
    }


def build_article_schema(
    headline: str,
    url: str,
    author_name: str,
    publisher_name: str,
    date_published: str,
    description: str = "",
    image_url: str = "",
) -> dict[str, Any]:
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "url": url,
        "author": {
            "@type": "Person",
            "name": author_name,
        },
        "publisher": {
            "@type": "Organization",
            "name": publisher_name,
        },
        "datePublished": date_published,
    }
    if description:
        schema["description"] = description
    if image_url:
        schema["image"] = image_url
    return schema


def build_organization_schema(
    name: str,
    url: str,
    logo_url: str = "",
    same_as_links: list[str] | None = None,
) -> dict[str, Any]:
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": name,
        "url": url,
    }
    if logo_url:
        schema["logo"] = logo_url
    if same_as_links:
        schema["sameAs"] = same_as_links
    return schema


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate JSON-LD Structured Data Schema")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # FAQ
    faq_p = subparsers.add_parser("faq", help="Generate FAQPage schema")
    faq_p.add_argument("--qa", nargs="+", help="Pairs in format 'Question:::Answer'", required=True)

    # Software / SaaS
    soft_p = subparsers.add_parser("software", help="Generate SoftwareApplication schema")
    soft_p.add_argument("--name", required=True)
    soft_p.add_argument("--url", required=True)
    soft_p.add_argument("--desc", required=True)
    soft_p.add_argument("--price", default="0.00")
    soft_p.add_argument("--currency", default="USD")

    # Article
    art_p = subparsers.add_parser("article", help="Generate Article schema")
    art_p.add_argument("--headline", required=True)
    art_p.add_argument("--url", required=True)
    art_p.add_argument("--author", default="Editorial Team")
    art_p.add_argument("--publisher", required=True)
    art_p.add_argument("--date", default="2026-01-01")
    art_p.add_argument("--desc", default="")

    # Org
    org_p = subparsers.add_parser("org", help="Generate Organization schema")
    org_p.add_argument("--name", required=True)
    org_p.add_argument("--url", required=True)
    org_p.add_argument("--logo", default="")

    args = parser.parse_args()

    if args.subcommand == "faq":
        pairs = []
        for item in args.qa:
            if ":::" in item:
                q, a = item.split(":::", 1)
                pairs.append((q.strip(), a.strip()))
        data = build_faq_schema(pairs)
    elif args.subcommand == "software":
        data = build_software_schema(args.name, args.url, args.desc, args.price, args.currency)
    elif args.subcommand == "article":
        data = build_article_schema(args.headline, args.url, args.author, args.publisher, args.date, args.desc)
    elif args.subcommand == "org":
        data = build_organization_schema(args.name, args.url, args.logo)
    else:
        sys.exit(1)

    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    print("<!-- Copy and paste into your <head> or component -->")
    print('<script type="application/ld+json">')
    print(json_str)
    print("</script>")


if __name__ == "__main__":
    main()
