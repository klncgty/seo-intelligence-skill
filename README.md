# SEO Intelligence — AI Agent Skill Documentation

> **Autonomous Technical SEO Auditor, SERP Rank-1 Blueprint Engine & JSON-LD Schema Generator for AI Coding Agents.**

[![Agent Skill Compatible](https://img.shields.io/badge/Agent%20Skill-Compatible-blue.svg)](https://agensi.io)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20Pip-orange.svg)](https://github.com/klncgty/seo-intelligence-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Overview

**SEO Intelligence** is an autonomous skill engineered for AI coding agents (**Claude Code**, **Cursor**, **Windsurf**, **OpenAI Codex**, and **Gemini CLI**). 

Instead of requiring external bloated databases, API subscriptions, or complex setups, it provides a self-contained, zero-pip-dependency toolchain that allows your AI agent to:
1. **Audit any live website or local code** (Next.js, Astro, HTML) for critical ranking deficiencies.
2. **Generate Rank-1 SERP blueprints** (Title tags, CTR-optimized descriptions, heading outlines).
3. **Build Google-compliant JSON-LD structured data** (SoftwareApplication, FAQPage, Article, Organization).
4. **Auto-fix code issues in-place** through agentic refactoring.

---

## ⚡ Quick Start

### 1. Installation

#### In Claude Code
Place the skill into your project or global skills directory:
```bash
# In your project root:
mkdir -p .claude/skills
cp -r /path/to/seo-intelligence-skill .claude/skills/seo-intelligence
```

#### In Cursor / Windsurf
Add to your project root or rules:
```bash
# Add as a project reference
cp -r /path/to/seo-intelligence-skill ./skills/seo-intelligence
```

---

## 🛠️ CLI & Agent Tools Reference

All tools are located in `scripts/` and run using standard Python 3:

### 1. Technical SEO Auditor (`scripts/audit.py`)
Evaluates 12 critical on-page ranking signals and outputs an actionable score (0–100):

```bash
# Audit a live URL:
python3 scripts/audit.py https://example.com

# Audit a local file (HTML, TSX, JSX):
python3 scripts/audit.py ./app/page.tsx

# Output raw JSON for programmatic agent consumption:
python3 scripts/audit.py https://example.com --format json
```

#### Audited Signals:
- **Title Tag:** Length (45–60 chars), primary keyword placement, truncation checks.
- **Meta Description:** Length (130–155 chars), CTA presence, snippet limits.
- **Heading Structure:** Exact single `<h1>` enforcement, `<h2>` hierarchy.
- **Image Optimization:** Missing or empty `alt` attributes.
- **Canonicalization:** `rel="canonical"` tag presence and syntax.
- **Social Tags:** OpenGraph (`og:title`, `og:image`, `og:type`) & Twitter Cards.
- **Structured Data:** JSON-LD schema detection and validation.
- **Mobile Friendliness:** Mobile viewport tag compliance.

---

### 2. SERP Rank-1 Blueprint Engine (`scripts/tag_blueprint.py`)
Generates high-CTR title variations, search snippet descriptions, and topical outlines.

```bash
# Generate English Blueprint:
python3 scripts/tag_blueprint.py "ai agent marketplace" --brand "Agensi" --lang en --type landing

# Generate Turkish Blueprint:
python3 scripts/tag_blueprint.py "doğal zeytinyağı" --brand "EgeHasat" --lang tr --type product
```

#### Outputs:
- 4 High-CTR Title Candidates (under 60 characters).
- 3 Click-Worthy Meta Descriptions (under 155 characters).
- Single primary `<h1>` and structured `<h2>` topical sections.
- Recommended Schema types.

---

### 3. JSON-LD Schema Builder (`scripts/schema_builder.py`)
Produces validated structured data to win Google Rich Snippets:

```bash
# Software / SaaS Application Schema:
python3 scripts/schema_builder.py software \
  --name "MetricFlow" \
  --url "https://metricflow.app" \
  --desc "Real-time product analytics platform" \
  --price "0.00"

# FAQPage Schema:
python3 scripts/schema_builder.py faq \
  --qa "What is MetricFlow?:::It is an analytics tool" "Is there a free trial?:::Yes, 14 days"

# Article / Blog Post Schema:
python3 scripts/schema_builder.py article \
  --headline "How to Optimize Next.js SEO" \
  --url "https://site.com/blog/nextjs-seo" \
  --publisher "DevPress"
```

---

## 🤖 Example Agent Prompts

Give these instructions to your AI coding agent (Claude Code, Cursor, etc.):

```text
> "Inspect https://my-site.com using the seo-intelligence skill, list all critical SEO deficiencies, and propose code fixes."
```

```text
> "Using seo-intelligence, generate a Rank-1 title and meta description blueprint for the keyword 'b2b cold email tool', then update our app/layout.tsx metadata."
```

```text
> "Check all <img> tags in our components for missing alt attributes and fix them with descriptive keywords."
```

```text
> "Generate a validated SoftwareApplication and FAQPage JSON-LD schema for our SaaS landing page and inject it into app/components/JsonLd.tsx."
```

---

## 📋 Technical SEO Checklist

For the full 50-point modern web app checklist, review [`references/technical-seo-checklist.md`](references/technical-seo-checklist.md).

For high-CTR formulas and swipe files, review [`references/rank1-tag-benchmarks.md`](references/rank1-tag-benchmarks.md).

---

## 📄 License & Author

- **Author:** Çağatay Kılınç ([@klncgty](https://github.com/klncgty))
- **License:** MIT License. Free for commercial and personal use.
