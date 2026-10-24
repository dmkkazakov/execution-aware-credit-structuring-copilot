"""Sensitivity of fixture aggregates to random transaction-row removal.

This does not re-estimate losses, retrain a model, or remove unique graph edges.
"""

import json
import numpy as np

if __package__:
    from .fixture_summary import load_transactions, summarize_fixture
else:
    from fixture_summary import load_transactions, summarize_fixture


def apply_missing_edge_stress(transactions, missing_rate=0.2, seed=2026):
    """Legacy function name: independently remove rows, not unique edges."""
    if not np.isfinite(missing_rate) or not 0 <= missing_rate <= 1:
        raise ValueError("missing_rate must be finite and between 0 and 1")
    rng = np.random.default_rng(seed)
    keep = rng.random(len(transactions)) >= missing_rate
    return transactions.loc[keep].copy()


def summarize_el(transactions):
    summary = summarize_fixture(transactions)
    reduction = summary["expected_loss_reduction_pct"]
    return {
        **summary,
        "analysis_type": "transaction_row_removal_aggregation",
        "relative_reduction": None if reduction is None else round(reduction / 100, 4),
        "notice": "Only supplied rows are removed and re-aggregated; this is not model robustness or causal stress testing.",
    }


if __name__ == "__main__":
    tx = load_transactions()
    for rate in [0.0, 0.1, 0.2, 0.3, 0.4]:
        stressed = apply_missing_edge_stress(tx, rate)
        print(json.dumps({"requested_missing_row_rate": rate, **summarize_el(stressed)}, allow_nan=False))
