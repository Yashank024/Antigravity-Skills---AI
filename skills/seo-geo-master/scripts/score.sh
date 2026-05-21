#!/bin/bash
# score.sh
# AntiGravity Agent Framework: SEO/GEO Score Generator Utility
# Generates the 10/10 SEO Pillar framework outline for agent use.

echo "=========================================================="
echo "    AntiGravity SEO & GEO Score Generator (10 Pillars)"
echo "=========================================================="

if [ -z "$1" ]; then
  echo "Usage: ./score.sh [domain.com]"
  exit 1
fi

DOMAIN=$1

echo "Target Domain: $DOMAIN"
echo "Initializing SEO Audit Pillars..."
echo ""

declare -a pillars=(
    "P1: Technical Foundation (HTTPS, robots, sitemap, 4xx/5xx)"
    "P2: Core Web Vitals (LCP <2.5s, INP <200ms, CLS <0.1)"
    "P3: On-Page SEO (Titles, H1s, Keyword placement)"
    "P4: Content Quality/E-E-A-T (Author bios, citations, data)"
    "P5: Schema Markup (Organization, Article, FAQ)"
    "P6: Backlink Authority (DR, quality of domains)"
    "P7: Topic Authority (Content clusters, internal linking)"
    "P8: GEO Readiness (llms.txt, fact density, AI crawler access)"
    "P9: Local SEO (GBP completeness, NAP consistency)"
    "P10: Keyword Performance (Target keywords, CTR, trends)"
)

# Print interactive prompt for the agent to fill out
for i in "${!pillars[@]}"; do
  echo "=> [ ] ${pillars[$i]}"
  echo "       Score (0.0 - 1.0): "
  echo "       Findings: "
  echo "------------------------------------------------------"
done

echo ""
echo "INSTRUCTIONS FOR AGENT:"
echo "1. Run manual checks or API tools for each pillar."
echo "2. Assign a score from 0.0 to 1.0."
echo "3. Sum the 10 scores to get the final /10.0 grade."
echo "4. Use examples/audit-report-sample.md to format the final output."
echo "=========================================================="
