"""Legacy entry point for fixture aggregation, not a causal simulation.

Prefer ``python -m src.summarize_fixtures``. The old filename is retained so
existing links and commands continue to work with explicit result metadata.
"""

if __package__:
    from .summarize_fixtures import main, run_demo
else:
    from summarize_fixtures import main, run_demo

if __name__ == "__main__":
    main()
