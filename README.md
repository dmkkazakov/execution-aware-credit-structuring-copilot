# Execution-Aware Credit Structuring

**Illustrative synthetic data and a baseline modeling exercise for execution-network credit research.**

## Evidence status

The repository contains a fixed synthetic fixture, feature calculations and a scikit-learn baseline. It does **not** contain an identified causal model, a counterfactual intervention simulator or a reproduction of the related papers' experiments.

The `cash_tension_before/after` and `expected_loss_before/after` values are already present in `data/raw/transactions.csv`. The summary script adds and averages those values. A percentage difference between them is a **descriptive property of the fixture**, not an estimated treatment effect, measured credit-loss reduction or evidence of production validity. The fixture-generation code and calibration provenance are not included.

### Implemented and proposed components

| Component | Current implementation |
|---|---|
| Data | 650 synthetic entities, 23,526 transaction rows across 18 months |
| Feature engineering | Rebuilds inflow/outflow, concentration and other descriptive features from transaction rows |
| Baseline | `sklearn.ensemble.GradientBoostingClassifier`; random entity holdout on the supplied static fixture |
| Before/after summary | Aggregates supplied outcome columns; performs no intervention |
| Missing-data exercise | Independently removes transaction rows and recomputes the same aggregates; does not test prediction degradation or unique-edge robustness |
| API and notebook | Display the same illustrative aggregates |
| GraphSAGE, causal identification, credit-product optimization, IFRS 9 ECL engine | Research directions, not implemented or validated here |

The supplied target contains 33 positive labels among 650 entities. These are synthetic labels. The fixture does not establish when the target or each predictor became observable, so the random split is not a prospective credit-risk validation. Shared network relationships also prevent treating it as independent network validation.

## Quick start

Run these commands from the repository root with Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python -m src.summarize_fixtures
python -m src.stress_testing
python -m src.train_baseline
python -m unittest discover -s tests -v
```

`src/simulate_intervention.py` and `src/train_xgb.py` remain compatible entry points for older links. Their names are historical: the former summarizes a fixture and the latter runs scikit-learn gradient boosting, **not XGBoost**. Outputs identify their actual method and evidence status. No XGBoost dependency is required.

The baseline uses an explicit list of candidate financial and graph predictors. It excludes `latent_credit_quality`, synthetic hidden/bottleneck exposure flags, `ifrs9_stage`, post-intervention reductions and the target itself. Graph predictors are rebuilt from raw transactions; the historical `graph_features.csv` supplies labels only. This removes known oracle/outcome inputs, but does not establish temporal availability or causal validity.

Reported classification metrics are ROC-AUC, **average precision** and Brier score. Average precision is named explicitly; it is not presented as trapezoidal area under the precision-recall curve. The script does not claim that graph predictors improve on a financial-only model: that comparison has not been run here.

To save rebuilt descriptive features separately:

```bash
python -m src.feature_engineering
```

This writes `data/processed/graph_features_rebuilt.csv` and preserves the historical fixture. Missing inflows in a month observed elsewhere in the transaction table count as zero when calculating inflow volatility. A supplied entity with no transactions is retained with zero flow features. `treasury_dependency_ratio` divides treasury inflow by operating inflow; it is a ratio, not a share bounded by one.

## API demo

```bash
python -m uvicorn api.app:app --reload
```

Open [http://localhost:8000/portfolio-summary](http://localhost:8000/portfolio-summary). The response includes `analysis_type`, `data_kind` and `causal_effect_estimated: false`. The historical `reduction_pct` field is an alias for the descriptive expected-loss percentage difference. A percentage with a zero denominator is `null`, not an invented zero or a division error.

The notebook `notebooks/01_network_analysis.ipynb` can be opened with Jupyter from the repository root or its `notebooks` directory. It labels all summaries as precomputed synthetic outcomes.

## Repository contents

```text
data/raw/                     Fixed synthetic entity and transaction fixtures
data/processed/graph_features.csv
                              Historical feature/target fixture, preserved
src/feature_engineering.py    Descriptive features from raw transactions
src/train_baseline.py         scikit-learn fitting demonstration
src/summarize_fixtures.py      Descriptive before/after aggregation
src/stress_testing.py         Random row-removal aggregation exercise
api/app.py                    Read-only fixture summary API
notebooks/01_network_analysis.ipynb
figures/                      Historical illustrative figures
docs/architecture.md          Implemented components and proposed architecture
docs/VALIDATION_STATUS.md      Scope, corrections and remaining limitations
```

The PNG figures and the original CSVs are retained as historical illustrative assets. Their before/after labels do not establish an intervention effect. There is no script in this repository that regenerates the original fixture or all figures. `configs/experiment.yaml` is a design outline; the scripts do not consume it.

## Research direction

The motivating hypothesis is that execution networks, timing gaps and treasury dependencies can complement borrower-level credit analysis. Establishing predictive or causal value requires additional work: time-indexed labels, data-generation provenance, financial-only comparisons, held-out networks/time periods, and a specified treatment/counterfactual design with uncertainty estimates.

Related manuscript titles are retained for context:

- Kazakov, D. (2026). *Execution-Aware Causal Credit Structuring: A Practical Methodology for Dynamic Interventions in Supply-Chain Execution Graphs.*
- Kazakov, D. (2026). *Robust Graph-Based Credit Risk Profiling Under Incomplete Transaction Networks.*

The current scripts should not be cited as reproducing the manuscripts' causal or robustness results. In particular, aggregation of the fixture does not verify a claimed 25–40% causal improvement.

## License

MIT
