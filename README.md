# Execution-Aware Credit Structuring

**Synthetic research repository for graph-based credit risk and causal intervention in supply-chain execution networks.**

This repository supports two related research ideas:

1. **Robust Graph-Based Credit Risk Profiling Under Incomplete Transaction Networks**
2. **Execution-Aware Causal Credit Structuring**

## Core Thesis

> Credit risk is not only a property of a borrower.  
> It is an emergent property of execution networks, timing gaps, treasury dependencies, and localized bottlenecks.

## What is included

```text
data/
  raw/
    entities.csv
    transactions.csv
  processed/
    graph_features.csv

src/
  feature_engineering.py
  train_xgb.py
  stress_testing.py
  simulate_intervention.py

figures/
  01_execution_graph.png
  02_cash_tension_intervention.png
  03_expected_loss_reduction.png

api/
  app.py

notebooks/
  01_network_analysis.ipynb
```

## Dataset

The synthetic dataset includes:

- legal entities and treasury/core nodes
- operating flows
- treasury flows
- hidden/off-ledger channel flags
- delay and FX stress
- bottleneck indicators
- cash-tension before/after intervention
- expected loss before/after intervention
- graph-derived risk features

## Research Tasks

- XGBoost baseline on financial + graph features
- Graph neural network extension
- missing-edge stress testing
- causal intervention simulation
- IFRS 9-style expected loss reduction
- analyst-readable graph-risk evidence

## Quick Start

```bash
pip install -r requirements.txt
python src/simulate_intervention.py
python src/stress_testing.py
python src/train_xgb.py
```

## API Demo

```bash
uvicorn api.app:app --reload
```

Then open:

```text
http://localhost:8000/portfolio-summary
```

## Positioning

Most public credit-risk datasets are borrower-centric.  
This repository models the transaction/execution layer:

- where liquidity stress appears,
- where it propagates,
- which bottlenecks matter,
- and how structured credit products can reduce residual tension.

## Suggested Citation

Kazakov, D. (2026).  
Execution-Aware Causal Credit Structuring: A Practical Methodology for Dynamic Interventions in Supply-Chain Execution Graphs.

Kazakov, D. (2026).  
Robust Graph-Based Credit Risk Profiling Under Incomplete Transaction Networks.

## License

MIT