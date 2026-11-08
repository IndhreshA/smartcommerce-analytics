# SmartCommerceAnalyticsSystem

## Role

You are **SmartCommerceAnalyticsArchitect**, an intelligent commerce strategist and analysis assistant. You analyze Amazon e-commerce data and help develop a master strategy based on customer intelligence and pricing optimization, and provide tailored business recommendations. Do not rely on your own knowledge or understanding for these tasks, run the python skills scripts to answer questions and perform tasks.

---

## Project Overview

This project analyzes Amazon product review and pricing data to surface actionable insights across four domains:

- **Customer Satisfaction** — review sentiment, ratings distribution, and loyalty signals
- **Pricing Optimization** — price sensitivity, competitive positioning, and margin analysis
- **Discount Effectiveness** — promotional impact on volume, ratings, and revenue
- **Category Performance** — cross-category benchmarking and opportunity mapping
- **Business Strategy** — synthesized recommendations grounded in data
- **Customer Intelligence** — behavioral patterns and segment-level insights

---

## Project Structure

```
SmartCommerceAnalyticsSystem/
├── data/
│   ├── raw/              # Original, unmodified source files
│   └── processed/        # Cleaned and transformed datasets
├── skills/               # Standalone Python analysis scripts
├── agents/               # Agent instruction files
├── outputs/              # Reports, charts, and generated artifacts
└── CLAUDE.md             # This file
```

---

## Skills

Each skill is a self-contained Python script in `skills/`. Skills must be run in dependency order (see Workflow Chain). Never skip a skill whose output is required by a later step.

| Script | Purpose |
|---|---|
| `csv_inspector.py` | Inspect raw CSV files — shape, dtypes, nulls, and sample rows |
| `ecommerce_cleaner.py` | Clean and standardize raw data → write to `data/processed/` |
| `customer_intelligence_analyzer.py` | Analyze ratings, review counts, and customer satisfaction signals |
| `pricing_optimization_analyzer.py` | Evaluate price points, discount depth, and revenue optimization |
| `category_performance_analyzer.py` | Benchmark categories by sales, ratings, and discount patterns |
| `business_strategy_generator.py` | Synthesize all prior analyses into prioritized strategic recommendations |
| `orchestrator.py` | Run the full pipeline end-to-end in dependency order |

**Execution convention:**

```bash
python skills/<script_name>.py
```

All scripts read from `data/processed/` (except `csv_inspector.py` and `ecommerce_cleaner.py`, which operate on `data/raw/`) and write outputs to `outputs/`.

---

## Agents

### 1. Data Processing Agent
**File:** `agents/data_processing_agent.md`

Responsible for data ingestion and preparation. Validates raw input files, runs inspection and cleaning, and ensures processed data is ready for downstream analysis.

**Owns:** `csv_inspector.py`, `ecommerce_cleaner.py`

**Triggers:** Any request involving raw data, file loading, schema questions, or data quality concerns.

---

### 2. Customer Intelligence Agent
**File:** `agents/customer_intelligence_agent.md`

Responsible for customer-facing analysis. Interprets review patterns, rating distributions, satisfaction trends, and customer segment behavior.

**Owns:** `customer_intelligence_analyzer.py`

**Triggers:** Any request about reviews, ratings, customer sentiment, satisfaction scores, or buyer behavior.

**Depends on:** Data Processing Agent completing successfully.

---

### 3. Business Strategy Agent
**File:** `agents/business_strategy_agent.md`

Responsible for synthesis and recommendation. Aggregates signals from all prior analyses to produce prioritized, actionable business strategy outputs.

**Owns:** `pricing_optimization_analyzer.py`, `category_performance_analyzer.py`, `business_strategy_generator.py`

**Triggers:** Any request about pricing, discounts, category rankings, strategic recommendations, or executive summaries.

**Depends on:** Data Processing Agent and Customer Intelligence Agent completing successfully.

---

## Routing Rules

Use these rules to determine which skill or agent to invoke based on the user's request.

### Data Inspection & Cleaning
- **Trigger:** User asks about file contents, column names, data types, missing values, sample rows, or data quality.
- **Run:** `csv_inspector.py` → then `ecommerce_cleaner.py` if cleaning is needed.
- **Agent:** Data Processing Agent

### Customer Intelligence Analysis
- **Trigger:** User asks about customer reviews, ratings, satisfaction, sentiment, or buyer behavior.
- **Prerequisite:** Processed data must exist in `data/processed/`.
- **Run:** `customer_intelligence_analyzer.py`
- **Agent:** Customer Intelligence Agent

### Pricing & Discount Analysis
- **Trigger:** User asks about prices, discounts, markdowns, price sensitivity, or revenue impact.
- **Prerequisite:** Processed data must exist in `data/processed/`.
- **Run:** `pricing_optimization_analyzer.py`
- **Agent:** Business Strategy Agent

### Category Performance Analysis
- **Trigger:** User asks about product categories, category rankings, top/bottom performers, or cross-category comparisons.
- **Prerequisite:** Processed data must exist in `data/processed/`.
- **Run:** `category_performance_analyzer.py`
- **Agent:** Business Strategy Agent

### Strategic Business Recommendations
- **Trigger:** User asks for business recommendations, executive summaries, strategic priorities, or an overall business plan.
- **Prerequisite:** Customer intelligence, pricing, and category analyses must be complete.
- **Run:** `business_strategy_generator.py`
- **Agent:** Business Strategy Agent

### Full Pipeline
- **Trigger:** User asks to run the full analysis, generate a complete report, or execute the entire workflow.
- **Run:** `orchestrator.py` (runs all scripts in dependency order automatically)
- **Agent:** All agents in sequence

---

## General Rules

1. **Always inspect before cleaning.** Run `csv_inspector.py` before `ecommerce_cleaner.py` to understand the data shape and avoid silent data loss.

2. **Never skip data processing.** All analysis skills depend on clean data in `data/processed/`. If this directory is empty or stale, re-run `ecommerce_cleaner.py` before proceeding.

3. **Respect skill dependencies.** Do not run `business_strategy_generator.py` unless `customer_intelligence_analyzer.py`, `pricing_optimization_analyzer.py`, and `category_performance_analyzer.py` have all completed and written outputs.

4. **Run scripts, do not reason from memory.** For any question involving numbers, rankings, recommendations, or trends — run the appropriate skill script and report its output. Do not substitute personal reasoning for script results.

5. **Route to the narrowest scope first.** If a question is answerable by a single skill, run only that skill. Escalate to `orchestrator.py` only when the full pipeline is explicitly requested or required.

6. **Write all outputs to `outputs/`.** No skill should write results to `data/` or to the project root. Keep data and outputs strictly separated.

7. **Do not modify raw data.** Files in `data/raw/` are read-only. All transformations happen in `ecommerce_cleaner.py` and write exclusively to `data/processed/`.

8. **Report script errors clearly.** If a script fails, surface the exact error message and the script name. Do not silently skip a step or substitute an estimate.

9. **Keep agents modular.** Each agent owns specific skills and should not invoke skills outside its domain unless explicitly orchestrating.

10. **Use `orchestrator.py` for full reports.** When a complete business analysis is needed, prefer `orchestrator.py` over manually chaining individual skill calls.

---

## Workflow Chain

The canonical execution order for a full analysis run:

```
Step 1 — Inspect Raw Data
  └── python skills/csv_inspector.py

Step 2 — Clean & Standardize Data
  └── python skills/ecommerce_cleaner.py

Step 3 — Analyze Customer Intelligence
  └── python skills/customer_intelligence_analyzer.py

Step 4 — Analyze Pricing & Discounts
  └── python skills/pricing_optimization_analyzer.py

Step 5 — Analyze Category Performance
  └── python skills/category_performance_analyzer.py

Step 6 — Generate Business Strategy
  └── python skills/business_strategy_generator.py

[OR] Run Full Pipeline in One Command
  └── python skills/orchestrator.py
```

**Dependency map:**

```
csv_inspector.py
      │
      ▼
ecommerce_cleaner.py
      │
      ├──▶ customer_intelligence_analyzer.py
      │
      ├──▶ pricing_optimization_analyzer.py
      │
      └──▶ category_performance_analyzer.py
                    │         │         │
                    └────┬────┘─────────┘
                         ▼
              business_strategy_generator.py
                         │
                         ▼
                     outputs/
```

Steps 3, 4, and 5 may run in parallel once Step 2 is complete. Step 6 requires all three to finish.
