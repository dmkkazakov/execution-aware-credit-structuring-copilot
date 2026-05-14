import pandas as pd

def run_demo():
    tx = pd.read_csv("data/raw/transactions.csv")
    before = tx["cash_tension_before"].mean()
    after = tx["cash_tension_after"].mean()
    el_before = tx["expected_loss_before"].sum()
    el_after = tx["expected_loss_after"].sum()

    return {
        "mean_cash_tension_before": round(before, 4),
        "mean_cash_tension_after": round(after, 4),
        "tension_reduction_pct": round((before-after)/before*100, 2),
        "expected_loss_reduction_pct": round((el_before-el_after)/el_before*100, 2)
    }

if __name__ == "__main__":
    print(run_demo())