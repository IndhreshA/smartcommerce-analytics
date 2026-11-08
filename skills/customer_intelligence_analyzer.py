"""Skill 3 — Customer intelligence: ratings, review volume, satisfaction segments."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from common import load_clean, save_json, OUTPUTS

df = load_clean()
min_reviews = int(df["rating_count"].quantile(0.5))

df["satisfaction"] = pd.cut(df["rating"], [0, 3.5, 4.0, 4.3, 5.0],
                            labels=["Low (<3.5)", "Average (3.5-4.0)", "Good (4.0-4.3)", "Excellent (4.3+)"])
seg = df["satisfaction"].value_counts(normalize=True).sort_index().mul(100).round(1)

popular = df[df["rating_count"] >= min_reviews]
top = popular.nlargest(5, ["rating", "rating_count"])[["product_name", "main_category", "rating", "rating_count"]]
low = popular.nsmallest(5, "rating")[["product_name", "main_category", "rating", "rating_count"]]

result = {
    "products_analyzed": int(len(df)),
    "avg_rating": round(df["rating"].mean(), 2),
    "median_reviews_per_product": int(df["rating_count"].median()),
    "rating_vs_reviews_corr": round(df["rating"].corr(df["rating_count"]), 3),
    "satisfaction_segments_pct": seg.to_dict(),
    "top_rated_popular": top.assign(product_name=top["product_name"].str[:60]).to_dict("records"),
    "lowest_rated_popular": low.assign(product_name=low["product_name"].str[:60]).to_dict("records"),
}
save_json("customer_intelligence.json", result)

fig, ax = plt.subplots(figsize=(7, 4))
df["rating"].plot.hist(bins=20, ax=ax, color="#4C72B0", edgecolor="white")
ax.set(title="Product Rating Distribution", xlabel="Rating", ylabel="Products")
fig.tight_layout()
fig.savefig(OUTPUTS / "rating_distribution.png", dpi=150)

print(f"Avg rating {result['avg_rating']} across {result['products_analyzed']:,} products")
print("Satisfaction segments (%):", result["satisfaction_segments_pct"])
print("Saved: outputs/customer_intelligence.json, outputs/rating_distribution.png")
