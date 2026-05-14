# Contributing

This repository is a research engineering asset for graph-based credit risk and execution-aware credit structuring.

## Principles

1. Reproducibility first.
2. Synthetic data must be clearly labeled as synthetic.
3. Do not overclaim production validity.
4. Prefer strong baselines before complex models.
5. Keep credit explanations evidence-grounded.

## Development

```bash
pip install -r requirements.txt
python src/simulate_intervention.py
python src/stress_testing.py
python src/train_xgb.py
```

## Branch naming

```text
feature/<short-name>
fix/<short-name>
docs/<short-name>
experiment/<short-name>
```

## Pull Request Checklist

- Code runs from repository root.
- No absolute paths.
- Results are reproducible.
- README/docs updated if needed.
- Synthetic-data limitations remain explicit.