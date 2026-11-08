"""Run the full SmartCommerce pipeline in dependency order."""
import subprocess
import sys
import time
from pathlib import Path

SKILLS = Path(__file__).resolve().parent
PIPELINE = [
    "csv_inspector.py",
    "ecommerce_cleaner.py",
    "customer_intelligence_analyzer.py",
    "pricing_optimization_analyzer.py",
    "category_performance_analyzer.py",
    "business_strategy_generator.py",
]

start = time.time()
for script in PIPELINE:
    print(f"\n=== Running {script} ===")
    result = subprocess.run([sys.executable, str(SKILLS / script)], cwd=SKILLS)
    if result.returncode != 0:
        sys.exit(f"Pipeline stopped: {script} failed (see error above).")
print(f"\nPipeline complete in {time.time() - start:.1f}s. See outputs/.")
