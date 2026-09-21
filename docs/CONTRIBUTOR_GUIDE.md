# Contributor Guide

**"I just discovered AXIS. Where do I start?"** This document is the answer.

It assumes you've already skimmed [`START_HERE.md`](../START_HERE.md) or the [`README`](../README.md) and want to actually get your hands on the code. If you haven't read [`CONTRIBUTING.md`](../CONTRIBUTING.md) yet, read that first for the setup steps (fork, clone, install, branch, PR workflow) — this guide is about *what* to work on and *how the repository is organized*, not the git mechanics.

---

## 1. Repository Architecture, In Plain Terms

AXIS has four layers. Understanding which layer a file belongs to tells you what it's for and what depends on it.

```
Raw data (private, not in this repo)
        │
        ▼
dataset_tools/        ← ingests, audits, and structures raw data into Master Dataset v2
        │
        ▼
evaluation/            ← benchmark harnesses, baselines, scoring
        │
        ▼
experiment_package/    ← a self-contained, portable reproduction of the QLoRA micro-pilot
        │
        ▼
scripts/                ← thin CLI entry points that call into the above
```

- **`dataset_tools/`** — the largest package. Subpackages worth knowing:
  - `master_pipeline/` — the module that actually built Master Dataset v2 (65,342 assets). Fully portable (resolves paths relative to the repo root). Covered by `tests/test_master_pipeline.py`.
  - `preprocessing/`, `resplan/` — per-source ingestion and normalization logic (needs the `dataset` extras: `shapely`, `pyarrow`, `ifcopenshell`).
  - `experiments/micro_pilot/` — the scripts that trained/evaluated checkpoint `ARCHI-AI-P4-005`. **Not** fully portable yet — see §4 below and [`DATASET.md` §6](../DATASET.md#6-local-directory-convention-for-the-full-pipeline).
- **`evaluation/`** — benchmark runners and baseline calculators (`evaluate_baseline.py` calls into here).
- **`experiment_package/`** — a standalone, pinned-dependency package for reproducing the VLM QLoRA proof-of-concept in isolation. Has its own `requirements.txt` and `README.md`.
- **`configs/`** — YAML experiment configurations.
- **`tests/`** — the automated test suite (see §3).
- **`docs/`** — everything that isn't top-level project documentation:
  - `docs/research/` — scientific readiness reports, gate decisions, pipeline reports.
  - `docs/datasets/` — dataset audits, license audits, acquisition matrices (one file per investigation — these are historical research artifacts, read them as a lab notebook, not a spec).
  - `docs/evaluation/` — independent Gold Set audits (difficulty, diversity, grounding).
  - `docs/experiments/` — ablation plans and phase selection reports.
  - `docs/history/` — the `ARCHI-AI` → `AXIS` transition record and a legacy prototype kept for traceability.

## 2. Important Scripts

| Script | What it does |
| :--- | :--- |
| `scripts/build_dataset.py` | Runs the master pipeline to (re)build the dataset from local raw sources. |
| `scripts/rebuild_dataset.py` | Rebuilds derived artifacts without re-running the full ingestion. |
| `scripts/validate_dataset.py` | Runs the anti-leakage / provenance validators over a built dataset. |
| `scripts/evaluate_baseline.py` | Runs Baseline 0 (and, with local data/checkpoint, the trained model) against a benchmark. Runnable with `--help` with no data present. |
| `scripts/inference_baseline.py` | Single-example inference against a baseline. |

## 3. Tests: What You Can Actually Run

```bash
pytest tests
```

On a fresh clone, without the private dataset corpus, this collects 93 tests: **35 pass, 19 fail, 38 error, 1 is skipped** (verified on a clean environment for this release — see [`REPRODUCIBILITY.md` §4](../REPRODUCIBILITY.md#4-automated-test-suite-what-actually-runs-on-a-fresh-clone)). The failures and errors are not bugs in your setup — they assert against `dataset/...` paths that are intentionally not redistributed (see [`DATASET.md` §5](../DATASET.md#5-data-access-policy)).

**The subset that always works** (no private data needed) is the CI gate:
```bash
pytest tests/test_audit_validators.py tests/test_master_pipeline.py -v
```
This is the fastest way to confirm your environment is set up correctly, and the tests a documentation-only or logic-only PR should keep passing.

If you have the private corpus locally (maintainer environment), the full 99-test suite is expected to pass. If your change breaks a data-dependent test and you can't verify it locally, say so explicitly in your PR rather than claiming it passes.

## 4. Datasets & Experiments

- The Master Dataset v2 (65,342 assets) is **not** in this repository. Its source registry, splits, and quarantines are documented in [`DATASET.md`](../DATASET.md).
- The Gold Set V3 (the immutable evaluation set) and the trained checkpoint `ARCHI-AI-P4-005` are also **not public** — see [`EVALUATION.md` §4](../EVALUATION.md#4-artifact-availability).
- If you want to run `dataset_tools/experiments/micro_pilot/` scripts specifically (not `dataset_tools.master_pipeline`, which works without it), you currently need to recreate a local `ARCHI_AI/`-prefixed directory layout — this is a known, documented limitation, not a bug you need to silently work around. See [`DATASET.md` §6`](../DATASET.md#6-local-directory-convention-for-the-full-pipeline) for the exact workaround, and consider picking up the "Path Portability" item in [`ROADMAP.md`](../ROADMAP.md) if you want to fix it properly.

## 5. Scientific Documentation

If you're going to touch anything that affects a reported number (a metric, a split, a dataset count), read [`RESEARCH.md`](../RESEARCH.md) first. AXIS enforces a small number of non-negotiable rules (no fabricated metrics, the Gold Set is read-only, zero split leakage, no metric shortcuts) — see [`CONTRIBUTING.md`](../CONTRIBUTING.md#scientific-ground-rules-non-negotiable). These aren't style preferences; PRs that violate them will be rejected regardless of code quality.

## 6. Roadmap & Picking a First Contribution

[`ROADMAP.md`](../ROADMAP.md) lists what's done, current, next, and future. If nothing there grabs you, these are reliable starting points:

### 🟢 Easy
- Fix an unclear explanation or broken link in any `.md` file.
- Add a missing docstring or type hint in `dataset_tools/` or `evaluation/`.
- Add a unit test for an untested pure function (no private data needed).
- Improve `docs/CONTRIBUTOR_GUIDE.md` (this file) based on friction you actually hit.

### 🟡 Intermediate
- Extend `dataset_tools/acquisition/` to help contributors fetch a public source more easily.
- Add a new metric or visualization to `evaluation/`.
- Improve CI (`.github/workflows/tests.yml`) — e.g. caching, faster installs.
- Work on the "Path Portability" roadmap item (§4 above).

### 🔴 Advanced
- Geometric deep learning experiments on `dataset_tools/master_pipeline`-derived data.
- IFC schema / `ifcopenshell` extraction improvements.
- Multimodal (2D↔3D) representation work, once paired data availability improves.
- Inference optimization (quantization, custom kernels) — see [`docs/research/inference-optimization.md`](research/inference-optimization.md).

This difficulty label is a rough complexity signal, not a ranking of importance — a good documentation fix is exactly as valuable a contribution as a model experiment.

## 7. Proposing a New Experiment

Don't just start training something. Follow [`docs/RESEARCH_CONTRIBUTION_PROTOCOL.md`](RESEARCH_CONTRIBUTION_PROTOCOL.md), which defines the hypothesis/baseline/metrics/reproducibility structure every AXIS experiment is expected to follow, and open an issue with the `experiment_proposal.md` template first.
