# Content SEO: Programmatic SEO (pSEO)

Programmatic SEO involves creating large-scale, template-driven landing pages based on datasets to capture vast amounts of long-tail search volume.

## 1. When to Use pSEO
- When search intent is identical across hundreds of variations.
- Examples: 
  - *Flights from [City A] to [City B]* (Travel)
  - *Best [Profession] in [City]* (Local Directories)
  - *[Software A] vs [Software B]* (SaaS Tool Comparisons)

## 2. The Mechanics
1. **The Dataset**: A structured database (Airtable, SQL, JSON) containing unique modifiers (cities, software names, statistics).
2. **The Blueprint**: A highly optimized page template with dynamic variables.
   - Example: `<title>Hire the Best {profession} in {city} | Verified Reviews</title>`

## 3. Prevention of "Thin Content" Penalties
- Google heavily penalizes programmatic pages that offer no unique value (Doorway Pages).
- **Rule**: Every dynamically generated page must inject unique data variables (e.g., dynamic charts, specific local statistics, unique user reviews) so no two pages look like spun duplicates.
- **Crawl Optimization**: Do not deploy 10,000 pSEO pages at once. Stagger rollout to protect the Crawl Budget and submit via XML sitemaps.
