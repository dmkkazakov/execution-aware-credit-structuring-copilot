"""Fit a scikit-learn baseline on a static synthetic fixture.

The split is a random entity holdout, not a prospective credit validation.
"""

import json

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split

if __package__:
    from .feature_engineering import build_graph_features
    from .fixture_summary import REPOSITORY_ROOT, load_transactions
else:
    from feature_engineering import build_graph_features
    from fixture_summary import REPOSITORY_ROOT, load_transactions


FINANCIAL_FEATURES = (
    "is_core", "leverage_debt_ebitda", "ebitda_margin",
    "current_ratio", "interest_coverage",
)
GRAPH_FEATURES = (
    "total_inflow", "total_outflow", "top3_inflow_concentration",
    "treasury_dependency_ratio", "inflow_volatility",
)
FEATURE_COLUMNS = FINANCIAL_FEATURES + GRAPH_FEATURES


def prepare_training_data(entities, features, labels):
    """Select declared predictors; never ingest latent or outcome fields."""
    frame = entities.loc[:, ["entity_id", *FINANCIAL_FEATURES]].merge(
        features.loc[:, ["entity_id", *GRAPH_FEATURES]],
        on="entity_id", how="left", validate="one_to_one",
    ).merge(
        labels.loc[:, ["entity_id", "default_flag"]],
        on="entity_id", how="left", validate="one_to_one",
    )
    X = frame.loc[:, list(FEATURE_COLUMNS)].apply(pd.to_numeric, errors="raise")
    y = frame["default_flag"]
    if not np.isfinite(X.to_numpy(dtype=float)).all() or y.isna().any():
        raise ValueError("Every entity must have finite predictors and a supplied label")
    if set(y.unique()) != {0, 1}:
        raise ValueError("The baseline needs both binary default classes")
    return X, y.astype(int)


def run_baseline():
    entities = pd.read_csv(REPOSITORY_ROOT / "data" / "raw" / "entities.csv")
    # The historical processed table supplies labels only, never predictors.
    labels = pd.read_csv(REPOSITORY_ROOT / "data" / "processed" / "graph_features.csv")
    features = build_graph_features(load_transactions(), entity_ids=entities.entity_id)
    X, y = prepare_training_data(entities, features, labels)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=2026, stratify=y
    )
    model = GradientBoostingClassifier(random_state=2026)
    model.fit(X_train, y_train)
    p = model.predict_proba(X_test)[:, 1]
    return {
        "model": "sklearn.ensemble.GradientBoostingClassifier",
        "data_kind": "synthetic_static_fixture",
        "validation_design": "random_entity_holdout",
        "prospective_validation": False,
        "causal_effect_estimated": False,
        "notice": "Illustrative fitting exercise; target timing and independent network validation are not established.",
        "seed": 2026,
        "train_entities": len(y_train),
        "test_entities": len(y_test),
        "test_defaults": int(y_test.sum()),
        "feature_columns": list(FEATURE_COLUMNS),
        "roc_auc": round(roc_auc_score(y_test, p), 4),
        "average_precision": round(average_precision_score(y_test, p), 4),
        "brier": round(brier_score_loss(y_test, p), 4),
    }


def main():
    print(json.dumps(run_baseline(), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
