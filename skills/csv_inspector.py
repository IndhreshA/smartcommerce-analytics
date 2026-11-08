"""Skill 1 — Inspect the raw CSV: shape, dtypes, nulls, sample rows."""
import pandas as pd
from common import find_raw_csv, OUTPUTS

path = find_raw_csv()
df = pd.read_csv(path)

lines = [
    f"File: {path.name}",
    f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns",
    "",
    "Columns and dtypes:",
    df.dtypes.to_string(),
    "",
    "Missing values:",
    df.isna().sum().to_string(),
    "",
    f"Duplicate rows: {df.duplicated().sum():,}",
    "",
    "Sample rows:",
    df.head(5).to_string(max_colwidth=40),
]
report = "\n".join(lines)
(OUTPUTS / "inspection_report.txt").write_text(report)
print(report)
print("\nSaved: outputs/inspection_report.txt")
