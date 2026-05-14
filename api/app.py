from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Execution-Aware Credit Structuring API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/portfolio-summary")
def portfolio_summary():
    tx = pd.read_csv("data/raw/transactions.csv")
    return {
        "transactions": int(len(tx)),
        "expected_loss_before": float(tx.expected_loss_before.sum()),
        "expected_loss_after": float(tx.expected_loss_after.sum()),
        "reduction_pct": float((tx.expected_loss_before.sum() - tx.expected_loss_after.sum()) / tx.expected_loss_before.sum() * 100)
    }