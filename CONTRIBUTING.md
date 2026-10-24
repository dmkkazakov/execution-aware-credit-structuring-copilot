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
python -m src.summarize_fixtures
python -m src.stress_testing
python -m src.train_baseline
python -m unittest discover -s tests -v
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

## Evidence boundary

The current code aggregates precomputed synthetic outcomes and fits a static scikit-learn baseline. It does not reproduce a causal intervention experiment. Keep this distinction in CLI/API outputs and documentation. Do not train on latent simulation variables, post-intervention outcomes or labels. Read [validation status](docs/VALIDATION_STATUS.md) before extending the experiment.
