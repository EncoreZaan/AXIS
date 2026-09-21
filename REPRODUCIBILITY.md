# AXIS — Experimental Reproducibility Guide

> **Standard:** Bit-exact reproducibility, deterministic seeds, verified cryptographic hashes.

---

## 1. Physical Hardware & Software Profile

The published benchmarks were produced and verified across two verified configurations:

### Configuration 1: Local Engineering Workstation
- **GPU:** NVIDIA GeForce RTX 4060 Ti (8,188 MiB VRAM, Ada Lovelace, Compute Capability 8.9)
- **CPU:** Intel(R) Core(TM) i5-14400F (10 cores, 16 threads)
- **RAM:** 16 GB DDR5 (15.72 GB total)
- **OS:** Windows 11 Pro (Build 26200)
- **Driver:** NVIDIA 616.92, CUDA 13.4 compatible
- **Python:** 3.11.9

### Configuration 2: Remote / Cluster Node
- **GPU:** NVIDIA GeForce RTX 3090 (24 GB GDDR6X)
- **Software Stack:** PyTorch 2.6.0+cu124, Transformers 5.17.0, PEFT 0.21.0, BitsAndBytes 0.50.2

---

## 2. Reproducing Phase 4 Step 6 (Gold Set V3 Evaluation)

### Step 1: Verify Gold Set V3 Integrity
Before evaluation, verify that your local manifest matches the certified cryptographic hash:

```python
import hashlib

def verify_file_sha256(path, expected_hash):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    computed = hasher.hexdigest()
    assert computed == expected_hash, f"Hash mismatch: {computed} != {expected_hash}"
    print(f"PASSED: {path} SHA256 verified.")

# Target manifest
verify_file_sha256(
    "dataset/supervision/v1/manifests/GOLD_V3_MANIFEST.jsonl",
    "81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca"
)
```

### Step 2: Run Baseline 0 Calibration
```bash
python scripts/evaluate_baseline.py \
    --manifest dataset/supervision/v1/manifests/GOLD_V3_MANIFEST.jsonl \
    --task CLEARANCE_CHECK
```
**Expected Output:**
- MAE: `2.7739 m` ($\pm 0.0001$ m)
- Accuracy: `99.00%` (Majority class predictor)

### Step 3: Run Model Evaluation on Checkpoint `ARCHI-AI-P4-005`
```bash
python scripts/evaluate_baseline.py \
    --checkpoint experiments/phase4_micro_pilot/runs/ARCHI-AI-P4-005/checkpoint/checkpoint_best_validation.pt \
    --manifest dataset/supervision/v1/manifests/GOLD_V3_MANIFEST.jsonl \
    --seed 42
```
**Expected Output:**
- MAE on `CLEARANCE_CHECK`: `0.0517 m` (95% CI: `[0.0428, 0.0616]`)
- Classification Accuracy: `100.00%`
- F1-Score: `100.00%`

### Reproducibility limitations for Phase 4 Step 6

The three artifacts referenced by the commands above are **NOT PUBLIC**:

| Artifact | Status | Why |
| :--- | :--- | :--- |
| `dataset/supervision/v1/manifests/GOLD_V3_MANIFEST.jsonl` (Gold Set V3) | **NOT AVAILABLE** in this repository | Excluded under `.gitignore` (`dataset/`). Only its SHA256 hash is published, so a researcher who independently reconstructs an equivalent manifest can verify bit-exact identity against it, but cannot download the file itself here. |
| `experiments/phase4_micro_pilot/runs/ARCHI-AI-P4-005/checkpoint/checkpoint_best_validation.pt` (model checkpoint) | **NOT AVAILABLE** in this repository | Excluded under `.gitignore` (`*.pt`, `outputs/`). Only its SHA256 hash and the metrics it produced are published. No public download link or release currently exists for this checkpoint. |
| `dataset_tools`-built Dataset A (Small/Medium/Full) | **NOT AVAILABLE** in this repository | Derived from raw sources under `dataset_tools/acquisition/`, which are themselves not redistributed (see `DATASET.md`). |

**Practical consequence:** the commands in Steps 1–3 document the exact
procedure and expected numeric output the maintainer obtained; they are not
independently runnable against this public repository until the maintainer
publishes the checkpoint and manifest under an explicit release (tracked in
`ROADMAP.md`, "Public Model Checkpoints & Comprehensive Benchmark Suite" —
currently `PLANNED`, no date committed). A researcher can still: (1) verify
the SHA256 hashes above are internally consistent across `README.md`,
`EVALUATION.md`, `PROJECT_STATUS.md`, and `docs/history/project-history.md`;
(2) rebuild an equivalent Dataset A locally from permissively-licensed
upstream sources via `dataset_tools/acquisition/` and re-run the same
scripts against their own build, though this will not reproduce bit-exact
numbers without the exact seed-42 corpus snapshot the maintainer used.

---

## 3. Reproducing VLM Proof-of-Concept Dry-Run

> **Canonical script:** `experiment_package/train_qlora.py` is the single canonical,
> portable entry point for this experiment (paths resolve relative to the
> package root, not to a hardcoded local directory). An earlier prototype
> (`scripts/train_qlora.py` + `configs/qlora_experiment.yaml`) used
> machine-specific hardcoded paths and has been archived, unmodified, under
> [`docs/history/legacy_qlora_prototype/`](docs/history/legacy_qlora_prototype/)
> for traceability — do not use it for reproduction.

```bash
cd experiment_package
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

# Optional: verify the environment before touching the model
python check_environment.py

# Execute safe dry-run (1 forward pass, no backward, no model updates)
python train_qlora.py --validate-only
```
**Expected Output:**
- Model loaded in 4-bit NF4: 730/730 tensors
- Trainable parameters: `20,185,088` (0.2429%)
- Dry-run forward loss: `1.9771`
- Backward pass: Skipped (safe mode)

See [`experiment_package/README.md`](experiment_package/README.md) for the full
installation and validation procedure, and the `--train` flag for launching an
actual (non-dry-run) training run on a 24 GB GPU.

### Reproducibility limitations for this experiment

- **The `experiment_package/dataset/` directory is NOT present in this
  repository.** `experiment_package/README.md` documents its expected
  contents (20 train / 5 validation examples, 25 architecture photographs),
  but the actual files are not published here (photographs and hand-written
  critiques are excluded under the same policy as other raw assets — see
  `DATASET.md`, "Data Access Policy"). This means `python train_qlora.py
  --validate-only` and `--dry-run` **cannot currently be executed by an
  external researcher** against this public repository as-is; the commands
  above document the procedure the maintainer ran, not a runnable path
  without first supplying an equivalent dataset in the documented JSONL
  format (see `docs/research/QLORA_PIPELINE.md`, section 2, for the schema).
- The resulting LoRA adapter weights and `outputs/archi_ai_micro_experiment/`
  artifacts are **NOT** published in this repository (see `.gitignore`:
  `outputs/`, `*.safetensors`, `*.bin`) — only the metrics recorded in
  `EXPERIMENTS.md` are available. Re-running the script reproduces the
  training procedure, not necessarily bit-identical loss values unless run on
  matching hardware/driver/library versions.
- This proof-of-concept has not been evaluated against the Gold Set V3 or any
  other held-out benchmark; treat its loss curve as evidence of technical
  feasibility (no OOM, no NaN, loss decreasing), not as a capability claim.

---

## 4. Automated Test Suite: What Actually Runs on a Fresh Clone

`tests/` contains 99 test functions in total (92 collectible + 7 in
`tests/test_dataset_infra.py`, which is skipped — see below). The
**"99/99 passing"** figure quoted in `README.md` / `PROJECT_STATUS.md`
reflects the maintainer's original local environment, where the full private
RAW dataset corpus (`dataset/`, ~66,847 files, 3.48 GB, not redistributed —
see `DATASET.md`, "Data Access Policy") was materialized on disk. It is
**not** what a fresh `git clone` + `pip install -r requirements.txt` +
`pytest tests` currently produces.

After fixing the two dependency/packaging issues below, running the suite
against a fresh clone (no private dataset present) currently yields
approximately **35 passed, 19 failed, 38 errored, 1 module skipped**:

- **35 passing tests** exercise pure logic that needs no external data:
  deduplication hashing, schema validation, leak-detection algorithms,
  taxonomy enums, and similar unit-level behavior.
- **19 failed + 38 errored tests** all fail for the same reason: they assert
  against files under `dataset/raw/...`, `dataset/master/...`, or
  `dataset/supervision/...`, none of which exist outside the maintainer's
  private workspace. These are not code bugs — they are data-validation
  tests correctly gated behind data that is intentionally not published.
- **`tests/test_dataset_infra.py` (7 tests) is skipped** at module level: it
  imports `dataset.master.schema.models.MasterAnnotation`, a module that was
  never migrated into the public `dataset_tools` package and does not exist
  in this repository. This is a genuine orphaned reference from before the
  `ARCHI-AI` → `dataset_tools` restructuring, not something this remediation
  can reconstruct (its schema definition is not available anywhere in the
  repository, so it cannot be recreated without fabricating it).

Two previously-undeclared dependencies (`shapely`, `pyarrow`, `ifcopenshell`)
were missing from `requirements.txt` / `pyproject.toml`, and `pyproject.toml`
had no explicit package list, so `pip install -e .` failed outright with a
"Multiple top-level packages discovered" error on every fresh checkout,
before even reaching the private-data-dependent failures above. Both are
fixed as of this revision.

**Bottom line for an external researcher:** you can install the package and
run roughly a third of the test suite out of the box today; the remaining
two-thirds require either the private dataset corpus (which is not published)
or, for `test_dataset_infra.py`, a module that no longer exists anywhere in
the project's history as committed to this repository.
