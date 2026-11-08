"""Skill 2 — Clean and standardize raw Amazon data -> data/processed/amazon_clean.csv.

Expected columns (Kaggle "Amazon Sales Dataset"): product_id, product_name, category,
discounted_price, actual_price, discount_percentage, rating, rating_count.
"""
import pandas as pd
from common import find_raw_csv, CLEAN_FILE


def to_number(s):
    return pd.to_numeric(
        s.astype(str).str.replace(r"[^\d.]", "", regex=True).replace("", None), errors="coerce"
    )


raw = pd.read_csv(find_raw_csv())
df = raw.copy()
start = len(df)

for col in ("discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"):
    if col in df.columns:
        df[col] = to_number(df[col])

df["main_category"] = df["category"].astype(str).str.split("|").str[0]
df["sub_category"] = df["category"].astype(str).str.split("|").str[-1]

if "discount_percentage" not in df.columns or df["discount_percentage"].isna().all():
    df["discount_percentage"] = (1 - df["discounted_price"] / df["actual_price"]) * 100

df = df.drop_duplicates(subset="product_id")
df = df.dropna(subset=["discounted_price", "actual_price", "rating"])
df["rating_count"] = df["rating_count"].fillna(0)
df = df[(df["rating"].between(1, 5)) & (df["actual_price"] > 0)]

keep = ["product_id", "product_name", "main_category", "sub_category", "discounted_price",
        "actual_price", "discount_percentage", "rating", "rating_count"]
df[keep].to_csv(CLEAN_FILE, index=False)

print(f"Raw rows: {start:,} -> clean rows: {len(df):,} (removed {start - len(df):,})")
print(f"Categories: {df['main_category'].nunique()}  |  Saved: data/processed/{CLEAN_FILE.name}")
