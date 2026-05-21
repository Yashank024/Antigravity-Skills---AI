# Analytics: Google Analytics 4 (GA4)

Analytics are required to prove the ROI of SEO and GEO efforts. GA4 is the industry standard for tracking user behavior post-click.

## 1. Core Implementation Checks
- Verify the GA4 Measurement ID (`G-XXXXXXXXXX`) is firing correctly in the `<head>` of all pages, or deployed flawlessly via Google Tag Manager (GTM).
- Do not double-fire tags (which heavily skews Bounce Rate and Engagement metrics).

## 2. SEO Conversion Tracking
- Traffic without conversion tracking is a vanity metric.
- Verify that **Key Events** (formerly Conversions) are actively tracking.
  - Examples: Form submissions, purchases, newsletter signups.
- Filter GA4 reports by `Session default channel group` = `Organic Search` to isolate the impact of the SEO strategy.

## 3. Analyzing Engagement (The New Bounce Rate)
- GA4 measures "Engaged Sessions" (sessions that last > 10s, have a conversion, or 2+ pageviews).
- If a high-traffic SEO page has a terrible Engagement Rate (< 20%), the Search Intent is mismatched. The page is ranking, but users are immediately leaving because it does not answer their question.
