"""Aggregate supplied outcomes; this module does not simulate interventions."""

import math
from pathlib import Path

import numpy as np
import pandas as pd


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TRANSACTIONS_PATH = REPOSITORY_ROOT / "data" / "raw" / "transactions.csv"
OUTCOME_COLUMNS = (
    "cash_tension_before",
    "cash_tension_after",
    "expected_loss_before",
    "expected_loss_after",
)


def load_transactions():
    return pd.read_csv(TRANSACTIONS_PATH)


def percentage_reduction(before, after):
    """Return an arithmetic difference, or None when its denominator is zero."""
    return None if before == 0 else (before - after) / before * 100


def summarize_fixture(transactions):
    """Summarize precomputed columns without inferring a treatment effect."""
    missing = set(OUTCOME_COLUMNS).difference(transactions.columns)
    if missing:
        raise ValueError(f"Missing outcome columns: {sorted(missing)}")
    values = transactions.loc[:, list(OUTCOME_COLUMNS)].apply(pd.to_numeric, errors="raise")
    if not np.isfinite(values.to_numpy(dtype=float)).all() or (values < 0).any().any():
        raise ValueError("Fixture outcomes must be finite, nonnegative numbers")
    totals = {column: math.fsum(values[column]) for column in OUTCOME_COLUMNS}
    count = len(values)
    before = totals["cash_tension_before"] / count if count else None
    after = totals["cash_tension_after"] / count if count else None
    el_before, el_after = totals["expected_loss_before"], totals["expected_loss_after"]
    return {
        "analysis_type": "illustrative_fixture_aggregation",
        "data_kind": "synthetic",
        "outcome_source": "precomputed_before_after_columns",
        "causal_effect_estimated": False,
        "notice": "Differences summarize supplied fixture values; no intervention or counterfactual is estimated.",
        "transactions": count,
        "mean_cash_tension_before": None if before is None else round(before, 4),
        "mean_cash_tension_after": None if after is None else round(after, 4),
        "tension_reduction_pct": None if before is None or before == 0 else round(percentage_reduction(before, after), 2),
        "expected_loss_before": round(el_before, 4),
        "expected_loss_after": round(el_after, 4),
        "expected_loss_reduction_pct": None if el_before == 0 else round(percentage_reduction(el_before, el_after), 2),
    }
