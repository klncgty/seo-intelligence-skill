# SEO Intelligence — AI Agent Skill Documentation

> **Autonomous Technical SEO Auditor, SERP Rank-1 Blueprint Engine & JSON-LD Schema Generator for AI Coding Agents.**

[![Agent Skill Compatible](https://img.shields.io/badge/Agent%20Skill-Compatible-blue.svg)](https://agensi.io)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20Pip-orange.svg)](https://agensi.io)
[![License: Commercial / Skill](https://img.shields.io/badge/License-Commercial%20Skill-purple.svg)](https://agensi.io)

---

### 🛒 How to Get the Full Skill Bundle

The complete `seo-intelligence` executable skill package (including standalone Python audit tools, SERP blueprint generator, JSON-LD schema builder, and complete checklist swipe files) is available exclusively on the **Agensi.io Marketplace**:

👉 **[Get SEO Intelligence on Agensi.io ($19.00)](https://www.agensi.io)**

*(Instant download • Works out-of-the-box with Claude Code, Cursor, Windsurf, Codex, and Gemini CLI • Zero pip dependencies)*

---

## 📖 Overview

**SEO Intelligence** is an autonomous skill engineered specifically for AI coding agents. 

Instead of forcing developers to configure heavy databases, Docker stacks, or expensive monthly SaaS subscriptions (like Semrush or Ahrefs), it equips your agent with a self-contained, zero-dependency toolchain that operates directly on your code and live deployments.

### Key Capabilities:
1. **Instant On-Page Technical Audit:** Evaluates live URLs or local Next.js / Astro / HTML files across 12 ranking factors (title bounds, snippet truncation, H1–H6 hierarchy, missing image alt tags, canonicals, viewport, open graph). Outputs a 0–100 health score with actionable code fixes.
2. **SERP Rank-1 Blueprint Engine:** Generates high-CTR title variations (50–60 chars), snippet-optimized meta descriptions (130–155 chars), and topical H2 outlines in both English and Turkish.
3. **Automated JSON-LD Schema Generator:** Builds validated structured data for Software Applications (SaaS), FAQPages, Articles, and Organizations to capture rich Google snippets.
4. **Agentic Code Refactoring:** Allows Claude Code or Cursor to directly modify your `app/layout.tsx`, inject schemas, and fix missing image alt tags in a single prompt.

---

## ⚡ Installation (After Purchase)

Once downloaded from Agensi.io, simply extract the bundle into your agent's skills directory:

### For Claude Code
```bash
# In your project root:
mkdir -p .claude/skills
cp -r /path/to/seo-intelligence-skill .claude/skills/seo-intelligence
```

### For Cursor / Windsurf
Add to your project root or rules:
```bash
# Place inside your project skills:
cp -r /path/to/seo-intelligence-skill ./skills/seo-intelligence
```

---

## 🤖 Example Agent Interactions

Once loaded, you can command your agent with natural language:

### 1. Full Technical Audit & Health Check
```text
> "Inspect https://my-saas-platform.com using the seo-intelligence skill, list all critical SEO deficiencies, and propose code fixes."
```

### 2. High-CTR Meta Tags & Blueprint Generation
```text
> "Using seo-intelligence, generate a Rank-1 title and meta description blueprint for the keyword 'b2b cold email software', then update our app/layout.tsx metadata."
```

### 3. Automated Image Alt-Tag Audit
```text
> "Check all <img> and <Image> tags in our components for missing alt attributes and fix them with descriptive keywords."
```

### 4. Rich Snippet Schema Injection
```text
> "Generate a validated SoftwareApplication and FAQPage JSON-LD schema for our landing page and inject it into app/components/JsonLd.tsx."
```

---

## 🛠️ Bundled Tools Reference (Included in Package)

| Tool | Description | Usage |
| :--- | :--- | :--- |
| `scripts/audit.py` | Standalone zero-pip auditor for URLs or local HTML/TSX files. | `python3 scripts/audit.py <URL_or_Path>` |
| `scripts/tag_blueprint.py` | High-CTR title, meta snippet, and heading hierarchy generator (EN & TR). | `python3 scripts/tag_blueprint.py "<kw>" --brand "<brand>" --lang en` |
| `scripts/schema_builder.py` | Google-compliant JSON-LD structured data generator. | `python3 scripts/schema_builder.py <faq\|software\|article\|org> [args]` |
| `references/` | 50-point technical SEO checklist and Rank-1 CTR formula swipe file. | Markdown guides loaded on-demand by agent. |

---

## 💻 Compatibility & Environment

- **Runtimes:** Python 3.8+ (standard library only, zero pip install required)
- **Platforms:** macOS, Linux, Windows
- **Supported Agents:** Claude Code, Cursor, Windsurf, GitHub Copilot CLI, OpenAI Codex, Gemini CLI

---

## 📄 License & Creator

- **Created by:** Çağatay Kılınç ([@klncgty](https://github.com/klncgty))
- **Distribution:** Exclusively distributed via [Agensi.io](https://www.agensi.io)
