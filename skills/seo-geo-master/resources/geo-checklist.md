# Generative Engine Optimization (GEO) Checklist

Unlike traditional SEO, GEO focuses on being retrieved by RAG (Retrieval-Augmented Generation) systems like ChatGPT, Gemini, and Perplexity.

## 1. Technical GEO Access
- [ ] `robots.txt` explicitly allows `GPTBot`, `Google-Extended`, `PerplexityBot`, and `ClaudeBot`.
- [ ] `llms.txt` is present at the root domain (`https://domain.com/llms.txt`).
- [ ] Site uses clean, semantic HTML (`<article>`, `<section>`, proper heading hierarchy). AI parsers strip out complex CSS/JS.
- [ ] Server-side rendering (SSR) or static generation is used (AI crawlers struggle with heavy SPA JavaScript).

## 2. Content Structure & Semantic Chunking
- [ ] **Direct Answer First**: The first 40-60 words of a section directly answer the H2 question.
- [ ] **Semantic Chunking**: Paragraphs are self-contained and make sense completely out of context.
- [ ] **Entity Clarity**: Key terms are defined explicitly (`[Term]: [Definition]`).

## 3. Fact Density & E-E-A-T
- [ ] **Statistics Addition**: Add a specific data point, percentage, or stat every 150-200 words.
- [ ] **Quotation Addition**: Include expert quotes and attributed statements.
- [ ] **Cite Sources**: Link out to highly authoritative external sources (`.edu`, `.gov`, major publications).
- [ ] **Recency**: Clearly date-stamp content. Perplexity heavily favors fresh, recently updated content.

## 4. Structured Data (JSON-LD)
- [ ] `Organization` schema includes brand description (used by AI for entity recognition).
- [ ] `FAQPage` schema is implemented for all Q&A and FAQ sections.
- [ ] `Article` schema includes proper Author URLs linking to credentialed author bio pages.
