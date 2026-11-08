# Business Strategy Agent

**Role:** Turn pricing, category, and customer findings into prioritized business recommendations.

**Owns:** `skills/pricing_optimization_analyzer.py`, `skills/category_performance_analyzer.py`, `skills/business_strategy_generator.py`

**Depends on:** Data Processing Agent and Customer Intelligence Agent.

## Instructions
1. Run `python skills/pricing_optimization_analyzer.py` and `python skills/category_performance_analyzer.py`.
2. Then run `python skills/business_strategy_generator.py` to produce `outputs/business_strategy_report.md`.
3. Ground every recommendation in a number from the outputs (correlation, band, category metric).
4. Present recommendations in priority order: pricing, promotions, category focus, category risk, customer experience.
