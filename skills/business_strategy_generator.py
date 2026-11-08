"""Skill 6 — Synthesize all analyses into a prioritized strategy report (outputs/business_strategy_report.md)."""
from common import load_json, OUTPUTS

ci = load_json("customer_intelligence.json")
po = load_json("pricing_optimization.json")
cp = load_json("category_performance.json")

recs = []

# Pricing: does discounting buy satisfaction or engagement?
if abs(po["discount_vs_rating_corr"]) < 0.1:
    recs.append(("Pricing", "Deep discounts do not lift ratings "
                 f"(corr {po['discount_vs_rating_corr']}). Cap routine discounts and reallocate margin "
                 "to product quality and listing content."))
else:
    direction = "higher" if po["discount_vs_rating_corr"] > 0 else "lower"
    recs.append(("Pricing", f"Discount depth is linked to {direction} ratings "
                 f"(corr {po['discount_vs_rating_corr']}); test discount levels by category before scaling."))
recs.append(("Promotions", f"The {po['highest_engagement_discount_band']} discount band drives the most "
             "reviews per product; anchor promotional campaigns around this range."))

# Categories
recs.append(("Category focus", f"Double down on {cp['top_by_engagement']}, which leads customer engagement, "
             f"and use {cp['top_by_rating']} (highest rated) as the quality benchmark."))
recs.append(("Category risk", f"Audit {cp['lowest_by_rating']}: lowest average rating; review top complaints "
             "and supplier quality."))

# Customers
low_pct = ci["satisfaction_segments_pct"].get("Low (<3.5)", 0)
recs.append(("Customer experience", f"{low_pct}% of products rate below 3.5. Prioritize fixes for "
             "high-review, low-rating items, since they shape the most buyer impressions."))

lines = ["# SmartCommerce Business Strategy Report", "",
         f"Products analyzed: {ci['products_analyzed']:,} | Avg rating: {ci['avg_rating']} | "
         f"Avg discount: {po['avg_discount_pct']}% | Categories: {cp['categories_compared']}", "",
         "## Prioritized recommendations", ""]
lines += [f"{i}. **{area}:** {text}" for i, (area, text) in enumerate(recs, 1)]
lines += ["", "## Supporting charts",
          "- rating_distribution.png", "- discount_vs_rating.png", "- category_review_share.png"]

report = "\n".join(lines)
(OUTPUTS / "business_strategy_report.md").write_text(report)
print(report)
print("\nSaved: outputs/business_strategy_report.md")
