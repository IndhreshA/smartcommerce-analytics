"""Skill 4 — Pricing & discount effectiveness: do deeper discounts drive ratings or engagement?"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from common import load_clean, save_json, OUTPUTS

df = load_clean()

df["discount_band"] = pd.cut(df["discount_percentage"], [-1, 20, 40, 60, 80, 100],
                             labels=["0-20%", "20-40%", "40-60%", "60-80%", "80%+"])
bands = (df.groupby("discount_band", observed=True)
           .agg(products=("product_id", "count"), avg_rating=("rating", "mean"),
                median_reviews=("rating_count", "median"), avg_price=("discounted_price", "mean"))
           .round(2))

df["price_band"] = pd.qcut(df["discounted_price"], 4, labels=["Budget", "Mid", "Upper-mid", "Premium"])
price = (df.groupby("price_band", observed=True)
           .agg(avg_rating=("rating", "mean"), median_reviews=("rating_count", "median"),
                avg_discount=("discount_percentage", "mean"))
           .round(2))

best_band = bands["median_reviews"].idxmax()
result = {
    "avg_discount_pct": round(df["discount_percentage"].mean(), 1),
    "discount_vs_rating_corr": round(df["discount_percentage"].corr(df["rating"]), 3),
    "discount_vs_reviews_corr": round(df["discount_percentage"].corr(df["rating_count"]), 3),
    "highest_engagement_discount_band": str(best_band),
    "discount_bands": bands.reset_index().astype({"discount_band": str}).to_dict("records"),
    "price_bands": price.reset_index().astype({"price_band": str}).to_dict("records"),
}
save_json("pricing_optimization.json", result)

fig, ax = plt.subplots(figsize=(7, 4))
bands["avg_rating"].plot.bar(ax=ax, color="#55A868")
ax.set(title="Average Rating by Discount Band", xlabel="Discount", ylabel="Avg rating",
       ylim=(bands["avg_rating"].min() - 0.2, bands["avg_rating"].max() + 0.1))
fig.tight_layout()
fig.savefig(OUTPUTS / "discount_vs_rating.png", dpi=150)

print(f"Avg discount {result['avg_discount_pct']}%  |  discount-rating corr {result['discount_vs_rating_corr']}")
print(f"Highest-engagement discount band: {best_band}")
print("Saved: outputs/pricing_optimization.json, outputs/discount_vs_rating.png")
