from fastapi import FastAPI
from src.summarize_fixtures import run_demo

app = FastAPI(
    title="Execution-Network Synthetic Fixture API",
    description="Descriptive aggregation of precomputed synthetic outcomes; no causal intervention is estimated.",
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/portfolio-summary")
def portfolio_summary():
    summary = run_demo()
    # Retain the original API key as an alias for the descriptive fixture metric.
    return {**summary, "reduction_pct": summary["expected_loss_reduction_pct"]}
