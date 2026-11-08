# SmartCommerce Analytics System

A multi-agent AI workflow that turns raw Amazon product data into customer insights, charts, and a prioritized business strategy, automating analysis that would take hours to do by hand.

**Course:** Advanced Applied AI/ML, The University of Texas at Dallas (May 2026)
**Tools:** Python, Pandas, Matplotlib, Claude (agentic AI)

## How it works
An AI assistant (Claude) acts as the orchestrator, following the rules in [`CLAUDE.md`](CLAUDE.md). It routes each request to one of three specialized **agents**, and each agent runs deterministic Python **skills** instead of guessing, so every number in the output comes from code.

| Agent | Skills it runs | Output |
|---|---|---|
| **Data Processing** | `csv_inspector.py`, `ecommerce_cleaner.py` | Data-quality report, clean dataset |
| **Customer Intelligence** | `customer_intelligence_analyzer.py` | Rating distribution, satisfaction segments, top/bottom products |
| **Business Strategy** | `pricing_optimization_analyzer.py`, `category_performance_analyzer.py`, `business_strategy_generator.py` | Discount and price-band analysis, category benchmarks, strategy report |

```
csv_inspector → ecommerce_cleaner → ┬→ customer_intelligence ─┐
                                    ├→ pricing_optimization ──┼→ business_strategy_generator → outputs/
                                    └→ category_performance ──┘
```

## Project structure
```
SmartCommerceAnalyticsSystem/
├── CLAUDE.md        # Orchestrator rules: routing, dependencies, guardrails
├── agents/          # Instruction files for the 3 agents
├── skills/          # 7 Python skills, incl. orchestrator.py
├── data/raw/        # Place amazon.csv here (not committed)
├── data/processed/  # Cleaned data (generated)
└── outputs/         # Reports, JSON results, charts (generated)
```

## Run it
1. Download the [Amazon Sales Dataset](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset) from Kaggle and place `amazon.csv` in `data/raw/`.
2. Install dependencies and run the full pipeline:
```bash
pip install -r requirements.txt
python skills/orchestrator.py
```
The pipeline runs in seconds and writes everything to `outputs/`:
- `business_strategy_report.md`: prioritized recommendations
- `rating_distribution.png`, `discount_vs_rating.png`, `category_review_share.png`
- JSON results for each analysis

You can also run any single skill, e.g. `python skills/pricing_optimization_analyzer.py`, or ask Claude a question in a session opened in this folder and let it route to the right agent.
