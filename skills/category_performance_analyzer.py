"""Skill 5 — Category performance: benchmark categories on ratings, engagement, and discounting."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import load_clean, save_json, OUTPUTS

df = load_clean()

cat = (df.groupby("main_category")
         .agg(products=("product_id", "count"), avg_rating=("rating", "mean"),
              total_reviews=("rating_count", "sum"), avg_discount=("discount_percentage", "mean"),
              avg_price=("discounted_price", "mean"))
         .round(2))
cat = cat[cat["products"] >= 5]
cat["review_share_pct"] = (cat["total_reviews"] / cat["total_reviews"].sum() * 100).round(1)
cat = cat.sort_values("total_reviews", ascending=False)

result = {
    "categories_compared": int(len(cat)),
    "top_by_engagement": cat.index[0],
    "top_by_rating": cat["avg_rating"].idxmax(),
    "lowest_by_rating": cat["avg_rating"].idxmin(),
    "most_discounted": cat["avg_discount"].idxmax(),
    "categories": cat.reset_index().to_dict("records"),
}
save_json("category_performance.json", result)

fig, ax = plt.subplots(figsize=(8, 4))
cat["review_share_pct"].head(8).plot.barh(ax=ax, color="#C44E52")
ax.invert_yaxis()
ax.set(title="Share of Customer Reviews by Category", xlabel="% of all reviews", ylabel="")
fig.tight_layout()
fig.savefig(OUTPUTS / "category_review_share.png", dpi=150)

print(f"{result['categories_compared']} categories | top engagement: {result['top_by_engagement']} "
      f"| top rating: {result['top_by_rating']}")
print("Saved: outputs/category_performance.json, outputs/category_review_share.png")
