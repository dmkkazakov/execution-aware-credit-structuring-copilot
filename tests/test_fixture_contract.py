import json
import math
import unittest

import numpy as np
import pandas as pd

from src.feature_engineering import build_graph_features
from src.fixture_summary import summarize_fixture
from src.stress_testing import apply_missing_edge_stress, summarize_el
from src.train_baseline import FEATURE_COLUMNS, FINANCIAL_FEATURES, GRAPH_FEATURES, prepare_training_data


def outcomes():
    return pd.DataFrame({
        "cash_tension_before": [10.0, 20.0],
        "cash_tension_after": [5.0, 15.0],
        "expected_loss_before": [1.0, 3.0],
        "expected_loss_after": [0.5, 1.5],
    })


class FixtureContractTests(unittest.TestCase):
    def test_summary_is_arithmetic_and_explicitly_non_causal(self):
        frame = outcomes()
        original = frame.copy(deep=True)
        result = summarize_fixture(frame)
        self.assertEqual(result["transactions"], 2)
        self.assertEqual(result["mean_cash_tension_before"], 15)
        self.assertEqual(result["mean_cash_tension_after"], 10)
        self.assertEqual(result["tension_reduction_pct"], 33.33)
        self.assertEqual(result["expected_loss_reduction_pct"], 50)
        self.assertFalse(result["causal_effect_estimated"])
        self.assertEqual(result["outcome_source"], "precomputed_before_after_columns")
        pd.testing.assert_frame_equal(frame, original)

    def test_empty_and_zero_baselines_have_undefined_ratios(self):
        for frame in (outcomes().iloc[:0], outcomes() * 0):
            result = summarize_fixture(frame)
            self.assertIsNone(result["tension_reduction_pct"])
            self.assertIsNone(result["expected_loss_reduction_pct"])
            self.assertIsNone(summarize_el(frame)["relative_reduction"])
            json.dumps(result, allow_nan=False)

    def test_invalid_outcomes_are_rejected(self):
        for value in (np.nan, np.inf, -1):
            frame = outcomes()
            frame.loc[0, "expected_loss_before"] = value
            with self.assertRaises(ValueError):
                summarize_fixture(frame)

    def test_row_removal_validates_rate_and_preserves_endpoints(self):
        frame = outcomes()
        pd.testing.assert_frame_equal(apply_missing_edge_stress(frame, 0), frame)
        self.assertTrue(apply_missing_edge_stress(frame, 1).empty)
        for rate in (-0.01, 1.01, np.nan, np.inf):
            with self.assertRaises(ValueError):
                apply_missing_edge_stress(frame, rate)

    def test_oracle_outcome_and_target_columns_cannot_become_predictors(self):
        entities = pd.DataFrame({"entity_id": ["a", "b"], **{name: [1.0, 2.0] for name in FINANCIAL_FEATURES}})
        features = pd.DataFrame({"entity_id": ["a", "b"], **{name: [3.0, 4.0] for name in GRAPH_FEATURES}})
        labels = pd.DataFrame({"entity_id": ["a", "b"], "default_flag": [0, 1]})
        for frame in (entities, features, labels):
            for name in ("latent_credit_quality", "mean_tension_reduction", "expected_loss_reduction", "ifrs9_stage", "hidden_channel_exposure", "bottleneck_exposure"):
                frame[name] = [999, -999]
        X, y = prepare_training_data(entities, features, labels)
        self.assertEqual(list(X), list(FEATURE_COLUMNS))
        self.assertEqual(y.tolist(), [0, 1])
        self.assertEqual(X.shape, (2, 10))

    def test_missing_labels_do_not_silently_drop_entities(self):
        entities = pd.DataFrame({"entity_id": ["a", "b"], **{name: [1.0, 2.0] for name in FINANCIAL_FEATURES}})
        features = pd.DataFrame({"entity_id": ["a", "b"], **{name: [3.0, 4.0] for name in GRAPH_FEATURES}})
        labels = pd.DataFrame({"entity_id": ["a"], "default_flag": [0]})
        with self.assertRaises(ValueError):
            prepare_training_data(entities, features, labels)

    def test_zero_inflow_months_and_isolated_entities_are_retained(self):
        transactions = pd.DataFrame({
            "month": ["2024-01-01", "2024-02-01"],
            "sender": ["a", "c"], "receiver": ["b", "a"],
            "operating_volume": [100.0, 10.0], "treasury_flow": [0.0, 0.0],
            "bottleneck_flag": [0, 0], "hidden_channel_flag": [0, 0],
        })
        result = build_graph_features(transactions, entity_ids=["a", "b", "c", "d"]).set_index("entity_id")
        self.assertAlmostEqual(result.loc["b", "inflow_volatility"], math.sqrt(2), places=6)
        self.assertEqual(result.loc["d", "total_inflow"], 0)
        self.assertEqual(result.loc["d", "total_outflow"], 0)
        self.assertTrue(np.isfinite(result.to_numpy()).all())


if __name__ == "__main__":
    unittest.main()
