"""Print descriptive aggregates of the bundled synthetic outcome fixture."""

import json

if __package__:
    from .fixture_summary import load_transactions, summarize_fixture
else:
    from fixture_summary import load_transactions, summarize_fixture


def run_demo():
    return summarize_fixture(load_transactions())


def main():
    print(json.dumps(run_demo(), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
