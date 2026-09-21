# Research Contribution Protocol

This document defines the structure every new AXIS experiment — proposed by the maintainer or by a contributor — is expected to follow, so that future contributions remain scientifically traceable and comparable to what is already documented (see [`RESEARCH.md`](../RESEARCH.md) for the underlying philosophy and [`CONTRIBUTING.md`](../CONTRIBUTING.md#scientific-ground-rules-non-negotiable) for the non-negotiable rules this protocol operationalizes).

It is a template, not a bureaucratic gate: a short experiment can fill this out in a page. The point is that every claim in the result is traceable to something reproducible.

---

## 1. Before You Start

Open an issue using the `experiment_proposal.md` template *before* investing significant training/compute time. This lets maintainers and domain experts flag an obviously flawed design (e.g. a metric shortcut, a split that will leak) before it costs you a training run.

## 2. Required Sections

### 2.1 Hypothesis
What specific, falsifiable claim are you testing? Bad: "the model will understand floorplans better." Good: "a model trained with vector-graph inputs will have lower MAE than one trained on raster-only inputs on the `ROOM_TOPOLOGY` task."

### 2.2 Objective
What decision does this experiment inform? (e.g. "decide whether to lift a roadmap blocker," "compare two architectures," "validate a new task contract.")

### 2.3 Dataset
- Which source(s) from [`DATASET.md`](../DATASET.md) §1, by identifier (e.g. `CORE_RPLAN`).
- Exact subset size and construction method (e.g. Dataset A-Small/Medium/Full, or a new subset — document how it was built).
- Any quarantine that applies (ResPlan metric quarantine, FloorPlanCAD legal quarantine) and confirmation the experiment respects it.

### 2.4 Split
- How the split was constructed (must be by `project_group_id`, never by individual asset — see the anti-leakage rule in `CONTRIBUTING.md`).
- Train / validation / test sizes.
- Confirmation of zero leakage (SHA256 and project-group), ideally via an automated check similar to `tests/test_master_pipeline.py::test_split_deterministic_anti_leakage`.
- Explicit confirmation the Gold Set V3 was **not** touched during training or tuning, if applicable.

### 2.5 Seed
The exact random seed(s) used, for every source of randomness that matters (data split, model init, training). AXIS's existing experiments use `seed = 42`; you may use a different one, but it must be stated and fixed.

### 2.6 Baseline
Every experiment needs a baseline for comparison — typically Baseline 0 (a trivial constant, majority-class, or random predictor) run with the exact same evaluation protocol. Results without a baseline are not interpretable and will not be accepted as evidence of a capability.

### 2.7 Metrics
- Which metric(s), and why they're appropriate for the task (e.g. MAE for continuous regression, exact-match for discrete classification).
- If reporting an accuracy/precision-style metric, state the class balance explicitly (see [`EVALUATION.md` §3.2](../EVALUATION.md#32-why-100-accuracy-is-not-a-robustness-proof) for why this matters — a 99/1 imbalance makes 99% accuracy trivial).

### 2.8 Protocol
- Ablation conditions run, if applicable (Condition A: clean, Condition B: metadata-sanitized, Condition C: scrambled — see [`RESEARCH.md`](../RESEARCH.md)).
- Hardware and approximate compute budget.
- Software versions (pin exact versions if the result depends on them, per `experiment_package/requirements.txt`'s approach).

### 2.9 Result
Raw numbers, not adjectives. A table comparing your model to the baseline, with the same structure as the existing tables in [`EVALUATION.md`](../EVALUATION.md).

### 2.10 Interpretation
What does the result actually support? Distinguish clearly between:
- What the numbers show (e.g. "MAE dropped from X to Y on this specific task and split").
- What they do *not* show (e.g. "this does not demonstrate general architectural reasoning" — see the caveats already modeled in `README.md`/`EVALUATION.md`).

### 2.11 Limitations
State plainly what would need to change for this result to generalize further: more data, a different split strategy, an independent replication, a larger Gold Set, etc.

### 2.12 Reproducibility
- Exact commands to reproduce the run.
- Which parts require private data (and are therefore not runnable by an external reviewer) versus which parts are runnable on public data alone.
- Where results/logs/configs are stored (`experiments/<experiment_name>/`, per `CONTRIBUTING.md`).

---

## 3. Where This Goes

- Experiment configs: `configs/`.
- Run logs, curves, and final metrics in standardized JSON: `experiments/<experiment_name>/`.
- A write-up following this protocol: `docs/experiments/` or `docs/research/`, whichever matches the existing convention for similar work.
- Update [`EXPERIMENTS.md`](../EXPERIMENTS.md) with a registry entry.

## 4. What Happens If a Result Is Negative

Document it anyway. A rejected hypothesis (e.g. "synthetic multimodal pairing was tried and rejected due to raw pair rarity," already recorded in `PROJECT_STATUS.md`) is exactly as valuable to the project's scientific record as a positive result, and prevents future contributors from re-running a failed approach. Never omit a negative result to make the roadmap look further along than it is.
