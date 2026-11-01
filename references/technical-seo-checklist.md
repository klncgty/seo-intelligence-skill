# Technical SEO Checklist for Modern Web Apps (2026 Edition)

When optimizing Next.js, Nuxt, Astro, SvelteKit, Remix, or static HTML applications, evaluate these critical areas:

---

## 1. Crawlability & Indexation
- [ ] **Robots.txt:** Verified that `/robots.txt` does not block critical CSS, JS, or image assets.
- [ ] **XML Sitemap:** Dynamic sitemap generated at `/sitemap.xml` and referenced in `robots.txt`.
- [ ] **Canonical URL:** Every indexable page declares `<link rel="canonical" href="..." />` matching its definitive trailing-slash protocol.
- [ ] **Status Codes:** Clean 200 OK responses, no redirect chains (avoid 301 -> 301 -> 200).
- [ ] **Noindex Guard:** Staging/development environments strictly blocked with `<meta name="robots" content="noindex, nofollow" />`.

---

## 2. On-Page & SERP Optimization
- [ ] **Title Tag:** 45–60 characters. Primary keyword in first 35 characters. Brand name appended with separator (`|` or `—`).
- [ ] **Meta Description:** 125–155 characters. Summarizes value proposition and contains a direct call to action.
- [ ] **Heading Architecture:**
  - Exactly one `<h1>` per page reflecting primary keyword/intent.
  - Logical hierarchy (`<h2>` for major sections, `<h3>` for nested subtopics). No skipped levels (e.g. avoid `<h1>` straight to `<h3>`).
- [ ] **Image Optimization:**
  - Descriptive, keyword-rich `alt` text on all informational images.
  - Empty `alt=""` on purely decorative assets.
  - Native lazy loading (`loading="lazy"`) on below-the-fold images.
  - Modern formats (`.webp` or `.avif`) with explicit `width` and `height` to eliminate Cumulative Layout Shift (CLS).

---

## 3. Structured Data (Schema.org)
- [ ] **JSON-LD Implementation:** Placed within `<script type="application/ld+json">`.
- [ ] **Entity Validation:** Validated through Schema.org validator / Google Rich Results test.
- [ ] **Required Rich Types:**
  - SaaS / Tools: `SoftwareApplication` or `WebApplication`
  - Landing / Homepage: `Organization` or `WebSite`
  - Knowledge / Guides: `Article` or `BlogPosting` + `BreadcrumbList`
  - Q&A Sections: `FAQPage`

---

## 4. Performance & Core Web Vitals (CWV)
- [ ] **Largest Contentful Paint (LCP):** Under 2.5s. Hero image preloaded with `<link rel="preload" as="image" ...>`.
- [ ] **Cumulative Layout Shift (CLS):** Under 0.1. Explicit aspect-ratio or dimensions on embeds, iframes, and banners.
- [ ] **Interaction to Next Paint (INP):** Under 200ms. Heavy JavaScript deferral and minimal main-thread blocking.

---

## 5. Social & Sharing Signals
- [ ] `og:title`, `og:description`, `og:image` (1200x630px recommended).
- [ ] `twitter:card` set to `summary_large_image`.
