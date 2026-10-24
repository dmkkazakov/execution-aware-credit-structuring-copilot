# Architecture and implementation status

## Implemented demonstration

The raw synthetic transaction fixture feeds two independent exercises:

1. **Descriptive aggregation:** `fixture_summary.py` reads precomputed before/after columns. `summarize_fixtures.py`, the legacy `simulate_intervention.py` entry point and the API expose those aggregates with explicit synthetic/non-causal metadata.
2. **Baseline fitting:** raw transactions produce declared graph predictors; entity financial columns and supplied synthetic labels feed `GradientBoostingClassifier`. A random entity holdout produces classification metrics. Latent, hidden, staging and post-intervention fields are excluded. This is a static fitting exercise, not a prospective validation or a causal estimator.

`stress_testing.py` drops transaction rows and re-aggregates their supplied outcomes. Multiple rows may describe the same sender-receiver relationship, so a row-removal rate is not a unique-edge removal rate. The script does not rebuild and evaluate a risk model under missingness.

## Proposed research architecture

The broader design remains a research proposal:

Payments / ERP / trade documents → entity resolution → dynamic execution graph → feature store → risk models → causal intervention engine → governance and analyst rationale.

Entity resolution, a causal intervention engine, dynamic product optimization and a governed production decision workflow are **not implemented** in this repository. The current fixture has no documented treatment assignment, counterfactual generation or identification assumptions. Its before/after values cannot establish a causal effect.

See [VALIDATION_STATUS.md](VALIDATION_STATUS.md) for the evidence boundary and corrections.
