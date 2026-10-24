# Copilot Research Backlog — Not Implemented

Use this file as a backlog for GitHub Copilot Workspace / coding agent. These are proposed tasks, not a description of the current implementation. See [VALIDATION_STATUS.md](VALIDATION_STATUS.md) before reporting research results. Any causal experiment requires an explicit data generator, treatment assignment, counterfactual design and identification assumptions; stored before/after columns do not provide them.

## Priority 1 — Make the repository executable

### Task 1.1: Add unified pipeline runner

Create `src/run_pipeline.py` that:

1. loads raw entities and transactions;
2. rebuilds graph features;
3. trains the baseline model;
4. runs the currently implemented transaction-row removal aggregation exercise;
5. summarizes the precomputed fixture with explicit non-causal metadata;
6. writes results to `outputs/metrics.json`.

Acceptance criteria:

```bash
python src/run_pipeline.py
```

must complete without manual steps.

---

### Task 1.2: Add evaluation module

Create `src/evaluate.py` with functions:

- `classification_metrics(y_true, y_score)`
- `expected_loss_summary(df)`
- `stress_curve_summary(results)`

Metrics:

- ROC-AUC
- Average precision (or explicitly specified precision-recall integration)
- Brier score
- EL before
- EL after
- Descriptive fixture difference %, clearly distinguished from an estimated effect
- Future predictive degradation under missing unique edges, only after implementing actual model evaluation

---

### Task 1.3: Add outputs folder

Create generated outputs:

```text
outputs/
  metrics.json
  stress_results.csv
  model_report.md
```

---

## Priority 2 — Strong research demonstration

### Task 2.1: Add financial-only vs graph-enhanced benchmark

Compare:

1. financial-only model;
2. financial + graph features model.

Output benchmark table:

```text
Model | ROC-AUC | Average precision | Brier
```

---

### Task 2.2: Add stress-testing chart

Generate chart:

```text
figures/04_missing_edge_stress.png
```

x-axis: explicitly defined missing unique-edge rate
y-axis: held-out predictive metric after feature reconstruction and evaluation

Do not substitute the sum of surviving precomputed outcome rows for model robustness or causal improvement.

---

### Task 2.3: Add intervention demo

Create an explicitly illustrative deterministic scenario with a published generator; this alone is not an identified causal effect:

- one EFU path;
- one bottleneck;
- baseline product;
- optimized bundle;
- before/after cash-tension.

Output:

```text
figures/05_intervention_demo.png
outputs/intervention_demo.json
```

---

## Priority 3 — GitHub polish

### Task 3.1: Improve README

Add:

- benchmark table;
- architecture diagram reference;
- figures;
- limitations;
- "How to cite";
- "How to reproduce".

---

### Task 3.2: Add CONTRIBUTING.md

Explain:

- branch naming;
- code quality;
- reproducibility;
- synthetic data limits.

---

### Task 3.3: Add GitHub issue templates

Add templates for:

- modeling task;
- dataset issue;
- documentation issue.
