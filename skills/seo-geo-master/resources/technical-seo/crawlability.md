# Technical SEO: Crawlability

Crawlability dictates how easily search engine bots (Googlebot, Bingbot, GPTBot) can discover and read pages on a site.

## 1. Robots.txt
- **Check**: Ensure `robots.txt` is present at the root (`/robots.txt`).
- **Rule**: Verify that vital paths are not accidentally blocked.
- **AI Rule**: explicitly `Allow: /` for AI bots (`GPTBot`, `ChatGPT-User`, `Google-Extended`, `PerplexityBot`).

## 2. XML Sitemaps
- **Check**: `sitemap.xml` must exist and be submitted to Search Console.
- **Rule**: It must only contain status `200 OK` indexable pages. No 404s, 301s, or `noindex` pages.
- **Rule**: Ensure `<lastmod>` is accurately reflecting true updates.

## 3. Core Web Vitals (CWV) & Page Speed
- **LCP (Largest Contentful Paint)**: Must be under 2.5s. Optimize hero images.
- **INP (Interaction to Next Paint)**: Must be under 200ms. Reduce main-thread JS blocking.
- **CLS (Cumulative Layout Shift)**: Must be under 0.1. Add strict width/height dimensions to images and ads.

## 4. Crawl Budget Optimization
- Identify infinite URL spaces (e.g., parameter driven faceted navigation like `?color=red&size=large`). Rel=canonical or robots block these to save crawl budget on large e-commerce sites.
