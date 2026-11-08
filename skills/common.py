"""Shared paths and helpers for all SmartCommerce skills."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
CLEAN_FILE = PROCESSED / "amazon_clean.csv"

for d in (PROCESSED, OUTPUTS):
    d.mkdir(parents=True, exist_ok=True)


def find_raw_csv():
    files = sorted(RAW.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV found in {RAW}. Put the Amazon dataset (e.g. amazon.csv) there.")
    return files[0]


def load_clean():
    import pandas as pd
    if not CLEAN_FILE.exists():
        raise FileNotFoundError("Processed data missing. Run: python skills/ecommerce_cleaner.py")
    return pd.read_csv(CLEAN_FILE)


def save_json(name, obj):
    path = OUTPUTS / name
    path.write_text(json.dumps(obj, indent=2, default=float))
    return path


def load_json(name):
    path = OUTPUTS / name
    if not path.exists():
        raise FileNotFoundError(f"{name} missing in outputs/. Run the skill that produces it first.")
    return json.loads(path.read_text())
