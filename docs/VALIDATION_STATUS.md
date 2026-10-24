# Validation status and corrections

## What can be reproduced

- Descriptive aggregates of the checked-in synthetic CSVs.
- Descriptive graph features rebuilt from those transaction rows.
- A seeded scikit-learn gradient-boosting fit with a random entity holdout.
- The effect of independently dropping rows on the descriptive aggregates.

The original CSVs and PNGs are preserved. The dataset generator, original calibration process, intervention assignment and counterfactual generation are not included. Recomputing a difference between stored outcomes does not reproduce an experiment that generated those outcomes.

## Corrected claims and behavior

1. `simulate_intervention.py` is identified as a historical name for fixture aggregation. The canonical entry point is `summarize_fixtures.py`; the CLI and API explicitly report `causal_effect_estimated: false`.
2. `train_xgb.py` has always used scikit-learn gradient boosting. The canonical entry point is now `train_baseline.py`, and outputs name the actual estimator. XGBoost is not required.
3. The former all-numeric-columns feature selection included latent credit quality and post-intervention reductions. The baseline now selects declared financial/graph candidates and uses the historical processed table only for labels. It excludes the latent variable, intervention outcomes, IFRS 9 stage and synthetic hidden/bottleneck exposure flags. No prospective validity follows from this correction alone.
4. The metric formerly called `pr_auc` is now named `average_precision`, matching the function being evaluated.
5. Random row removal is labeled as aggregation sensitivity, not graph-model robustness. Its rate is validated. Empty samples and zero denominators produce defined `null` ratios instead of nonfinite output.
6. Data paths are resolved relative to the repository's source files, so direct script invocations also work outside the repository directory.
7. Notebook cells use real newlines and executable source. The notebook explains the status of the precomputed outcomes.
8. Inflow volatility includes zero inflows for months observed in the transaction table, and supplied entities with no transactions remain in rebuilt features.

## What remains unproven

- Any causal treatment effect, including a 25–40% improvement claim.
- Added predictive value from graph features versus a financial-only baseline.
- Robustness of predictions to absent unique edges, different missingness mechanisms or unseen networks.
- Production credit performance, calibration, IFRS 9 compliance or portfolio ECL reduction.

The fixture has 650 entities and only 33 synthetic positive labels. Its target event times and predictor availability dates are not documented. A random holdout is therefore an illustrative code exercise; it is not a substitute for a temporal/network validation design. The related manuscript results require their own data, generator, protocol and evidence.

## Checks

Run `python -m unittest discover -s tests -v`. The focused checks cover arithmetic interpretation, zero/empty cases, rejection of invalid outcomes and row-removal rates, exclusion of oracle/outcome predictors, zero-flow months and isolated entities. CLI commands and notebook cells can then be executed as shown in the README.
