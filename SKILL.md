---
name: seo-intelligence
description: Complete SEO auditing, Rank-1 meta tag blueprint generation, JSON-LD structured data creation, and technical on-page optimization. Use when inspecting web applications, auditing pages for search engines, fixing meta titles, descriptions, canonical tags, open-graph cards, heading hierarchy, or adding schema markup to Next.js, React, Astro, or HTML projects.
license: MIT
compatibility: Requires python3 (standard library only, zero pip dependencies)
metadata:
  author: Çağatay Kılınç
  version: "1.0.0"
  category: "seo"
  keywords: "seo, audit, serp, json-ld, meta-tags, technical-seo, nextjs-seo, agent-skills"
---

# SEO Intelligence Skill

A comprehensive suite for AI coding agents to diagnose, audit, and optimize web applications for search engine dominance.

---

## Capabilities & Available Tools

This skill bundles three zero-dependency Python tools inside `scripts/`:

1. **`python scripts/audit.py <URL_or_FilePath>`**
   - Full technical audit of any live website or local file (`.html`, `.tsx`, `.jsx`).
   - Evaluates title length, meta description, canonical tags, mobile viewport, H1–H6 hierarchy, missing image alt attributes, OpenGraph, Twitter cards, and Schema presence.
   - Outputs a markdown report or JSON with an overall score (0–100).

2. **`python scripts/tag_blueprint.py "<keyword>" [--brand "<name>"] [--lang en|tr] [--type landing|blog|product|tool]`**
   - Generates high-CTR title candidates (50–60 chars), snippet meta descriptions (130–155 chars), primary H1, and H2 topical outline for search intent dominance.

3. **`python scripts/schema_builder.py <faq|software|article|org> [options]`**
   - Builds validated, Google-compliant JSON-LD structured data scripts ready to inject directly into templates or `<head>`.

---

## Agent Workflow Instructions

When tasked with auditing or optimizing SEO for a project:

### Step 1: Run the SEO Audit
If auditing an existing page or component:
```bash
python scripts/audit.py <target_url_or_path>
```
Review the health score and flagged warnings/failures (missing alt tags, unoptimized meta descriptions, multiple H1s, missing canonicals).

### Step 2: Formulate the Target Keyword & Blueprint
If creating or revising metadata for a specific topic:
```bash
python scripts/tag_blueprint.py "your target search query" --brand "YourBrand" --lang en
```
Extract the highest-converting title and meta description candidate.

### Step 3: Implement Code Fixes
Modify the project files directly:
- **Next.js (App Router):** Inject into `export const metadata: Metadata = { title, description, openGraph, alternates: { canonical } }`.
- **Next.js (Pages Router):** Place inside `<Head>` component.
- **Astro / HTML / Static:** Update `<title>`, `<meta>`, and heading tags (`<h1>`, `<h2>`).
- **Images:** Add descriptive `alt` text to `<img>` or `<Image />` elements.

### Step 4: Add Structured Data (JSON-LD)
Generate the relevant schema:
```bash
python scripts/schema_builder.py software --name "App Name" --url "https://app.com" --desc "Description"
```
Place the resulting `<script type="application/ld+json">` into the root layout or page component.

### Step 5: Verification
Rerun `scripts/audit.py` to confirm all issues are resolved and the score reaches 90+.

---

## Reference Guides

- [Technical SEO Checklist](references/technical-seo-checklist.md)
- [Rank-1 Meta Tag Benchmarks & Formulas](references/rank1-tag-benchmarks.md)
