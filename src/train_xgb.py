"""Legacy filename; this baseline uses scikit-learn, not XGBoost.

Prefer ``python -m src.train_baseline``.
"""

if __package__:
    from .train_baseline import main
else:
    from train_baseline import main

if __name__ == "__main__":
    main()
