# Analytics: Google Search Console (GSC)

Google Search Console is the ultimate source of truth for literal search performance. Third-party tools (Ahrefs, Semrush) estimate; GSC provides actual data.

## 1. Index Coverage Triage
- Navigating to the **Pages** report is the first step of any Technical Audit.
- Identify the reasons pages are not indexed:
  - *Discovered - currently not indexed*: Often implies crawl budget issues or low-quality content.
  - *Crawled - currently not indexed*: Google read the page but decided it wasn't worth indexing (Thin Content penalty).
  - *Soft 404s*: Pages that say they are missing but return a 200 OK status. Must be fixed by serving a true 404 or redirecting.

## 2. Performance Analysis (Striking Distance)
- Filter the Performance report for the last 3 months.
- Look for queries ranking in Positions 11–20 (Page 2) that already have high impressions.
- **Agent Action**: These are "Striking Distance" keywords. A slight optimization in On-Page SEO (Title tag, H1, internal linking) can push them to Page 1 and drastically increase clicks.

## 3. CTR Optimization
- Sort queries by Impressions (High) and CTR (Low).
- A high impression/low CTR metric means the page *is* ranking, but the Title Tag or Meta Description is failing to attract the user's click.
- **Agent Action**: Rewrite the meta data to be more compelling or intent-aligned.
