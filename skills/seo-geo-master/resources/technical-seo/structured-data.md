# Technical SEO: Structured Data

Structured Data (Schema Markup) explicitly feeds entities and context to search engines, enabling Rich Snippets and boosting AI Search visibility.

## Implementation Standard
Always use **JSON-LD**. Do not use Microdata. Place the script tag in the `<head>` or clearly in the `<body>`.

## Core Schemas to Implement

### 1. Organization / LocalBusiness
- **Purpose**: Establishes the core entity identity for Knowledge Panels.
- **Required**: `name`, `url`, `logo`, `sameAs` (social profiles), and `contactPoint`.

### 2. Article / NewsArticle
- **Purpose**: Critical for blog posts to appear in Top Stories and AI digests.
- **Required**: `headline`, `image`, `datePublished`, `dateModified`, `author` (Must link to an author profile page URL for E-E-A-T).

### 3. FAQPage
- **Purpose**: Dominates "People Also Ask" blocks.
- **Rule**: Ensure every question and answer in the schema is 100% visible on the physical page.

### 4. Product & Review
- **Purpose**: Shows pricing, availability, and star ratings directly in SERPs.
- **Required**: `name`, `aggregateRating`, `offers.price`, `offers.availability`.

## Verification
- Agent must advise the user to run code through the **Google Rich Results Test** tool.
