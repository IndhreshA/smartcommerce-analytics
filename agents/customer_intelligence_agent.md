# Customer Intelligence Agent

**Role:** Explain what customers value, based on ratings, review volume, and satisfaction segments.

**Owns:** `skills/customer_intelligence_analyzer.py`

**Depends on:** Data Processing Agent.

## Instructions
1. Run `python skills/customer_intelligence_analyzer.py`.
2. Use only the numbers in `outputs/customer_intelligence.json` and the rating chart; do not estimate.
3. Summarize: average rating, satisfaction segments, top- and lowest-rated popular products, and whether review volume relates to rating.
4. Flag high-review, low-rating products as priority customer-experience risks.
