# Contributing to AXIS

First off, welcome to **AXIS (Architectural eXpert Intelligence System)**! We are excited to collaborate with researchers, engineers, architects, and developers to build specialized intelligence for spatial and architectural reasoning.

---

## Who Can Contribute?

AXIS is an interdisciplinary initiative at the intersection of computer vision, geometric deep learning, building information modeling (BIM), and architectural practice. We actively seek contributors across diverse domains:

- **ML Researchers:** Geometric deep learning, spatial reasoning representations, vision-language alignment, multimodal rotary embeddings (M-RoPE).
- **ML Engineers:** Distributed training, reproducible pipelines, dataset loaders, Hugging Face Trainer & PEFT integrations.
- **Python Developers:** Pipeline orchestration, clean data schemas, unit testing (`pytest`), CLI tooling.
- **GPU & Inference Engineers:** Kernel optimization (Triton/CUDA), quantization (NF4, AWQ, FP8), memory management, prospective acceleration investigations (DSpark).
- **Computer Vision Researchers:** Floorplan raster segmentation, vector edge extraction, topological graph reconstruction.
- **BIM & CAD Specialists:** IFC schema parsing (`ifcopenshell`), geometric conversion, coordinate referencing, STEP decoding.
- **Architects & Designers:** Architectural taxonomy, spatial ergonomics, building code rules (Neufert, PMR, accessibility, fire safety), ground truth validation.
- **Dataset Engineers:** Deduplication, license auditing, data provenance, streaming hash verification.
- **Evaluation & Red-Team Researchers:** Benchmark falsification, shortcut detection, data contamination prevention, adversarial negative design.
- **Documentation & Technical Writers:** Architectural tutorials, API docs, scientific reports.

---

## Scientific Ground Rules (Non-Negotiable)

To maintain absolute scientific integrity, all contributors must adhere to four strict principles:

1. **NEVER FABRICATE DATA OR METRICS:** Every claim, number, and result must be backed by a deterministic script, logged artifact, or reproducible seed. If an evaluation is missing, state `Not yet documented / not yet verified`.
2. **THE GOLD SET IS IMMUTABLE:** The Gold Set V3 is strictly read-only and reserved exclusively for post-training evaluation. Training or hyperparameter tuning on the Gold Set is strictly forbidden.
3. **ZERO LEAKAGE ACROSS SPLITS:** Datasets must be split strictly by project/building identifier (`project_group_id`). Never split floors of the same building across train and test.
4. **NO METRIC SHORTCUTS:** Never invent synthetic scale conversions (e.g., arbitrarily mapping pixels to square meters without a physical reference scale).

---

## Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/EncoreZaan/AXIS.git
cd AXIS
```

### 2. Set Up a Python Virtual Environment
Python **3.10** or **3.11** is recommended.

```bash
# On Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# On Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 4. Run the Test Suite
Ensure that all 99 tests pass before making any changes:
```bash
pytest tests
```

---

## How to Run & Add Experiments

### Running Existing Micro-Pilot Baselines
```bash
# Run baseline evaluation on spatial clearance
python scripts/evaluate_baseline.py --help
```

### Adding a New Experiment
1. Create a dedicated experiment configuration in `configs/` (e.g. `configs/experiment_my_task.yaml`).
2. Log all runs, curves, and final metrics into `experiments/<experiment_name>/` in standardized JSON format.
3. Include Baseline 0 (empirical constant, random, or majority class) to benchmark genuine learning.
4. Conduct an ablation study (Condition A: clean, Condition B: metadata sanitized, Condition C: input scrambled) to rule out shortcut learning.
5. Document findings in `docs/experiments/` with full reproducibility specifications.

---

## Workflow: Issues & Pull Requests

### 1. Opening an Issue
Before writing substantial code, please open an issue using the relevant template:
- `bug_report.md` for bugs in pipelines or runners
- `research_question.md` for scientific inquiries
- `experiment_proposal.md` for proposing training runs
- `dataset_issue.md` for reporting data anomalies or licensing issues
- `feature_request.md` for new functionality

### 2. Git Branching & Commit Conventions
- Branch naming: `feat/<feature-name>`, `fix/<bug-name>`, `research/<topic>`, `docs/<topic>`
- Commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
  - `feat: add IFC wall bounding box extractor`
  - `fix: correct coordinate axis orientation in 3D relation verifier`
  - `docs: update Gold Set V3 evaluation metrics table`
  - `test: add unit test for project-group leakage detector`

### 3. Submitting a Pull Request
1. Ensure `pytest tests` passes with 0 failures.
2. Verify that no secrets, credentials, or large binary datasets are included (`git status`).
3. Open a Pull Request against `main` using `.github/PULL_REQUEST_TEMPLATE.md`.
4. Engage constructively in code review.
