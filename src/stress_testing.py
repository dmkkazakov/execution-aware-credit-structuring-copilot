import pandas as pd
import numpy as np

def apply_missing_edge_stress(transactions, missing_rate=0.2, seed=2026):
    rng = np.random.default_rng(seed)
    keep = rng.random(len(transactions)) > missing_rate
    return transactions.loc[keep].copy()

def summarize_el(transactions):
    before = transactions.expected_loss_before.sum()
    after = transactions.expected_loss_after.sum()
    return {
        "expected_loss_before": round(before, 4),
        "expected_loss_after": round(after, 4),
        "relative_reduction": round((before-after)/(before+1e-9), 4)
    }

if __name__ == "__main__":
    tx = pd.read_csv("data/raw/transactions.csv")
    for rate in [0.0, 0.1, 0.2, 0.3, 0.4]:
        stressed = apply_missing_edge_stress(tx, rate)
        print(rate, summarize_el(stressed))