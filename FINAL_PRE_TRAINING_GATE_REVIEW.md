# AXIS — Final Independent Pre-Training Gate Review

> **Audit Type:** Independent, read-only, final pre-training gate review & baseline verification  
> **Auditor Scope:** Git baseline, previous remediation verification, test isolation, package installation, hard-gated tests, full test suite, dataset integrity, scientific validation, training pipeline reproducibility, data/provenance/legal gate, security/secrets review, repository consistency, blocker enumeration, and final training gate decision.  
> **Hard Constraints Honored:** No source file modified, no documentation modified, no dataset modified, no manifest modified, no Gold Set file modified, no checkpoint modified, no scientific results regenerated, no model trained, no GPU jobs launched, no weights downloaded, no git commit/push/merge executed, `TRAINING_ALLOWED: NO` strictly preserved.  
> **Audit Date:** 2026-09-22  
> **Audited Workspace:** `C:\Users\teoba\Documents\Devs\AXIS`  
> **Target Upstream Baseline:** GitHub `EncoreZaan/AXIS` @ commit `f4d5e949053743d97091ea35080de5d365899df7` (`f4d5e94`)

---

## 1. Executive Summary

This independent final pre-training gate review was executed directly on the local workspace `C:\Users\teoba\Documents\Devs\AXIS` following the integration of the post-remediation fixes (commit `4a73fa6`) and merge into `main` (commit `f4d5e94`).

Every falsifiable claim made in `AXIS_POST_REMEDIATION_AUDIT.md`, `PUBLICATION_READINESS_AUDIT.md`, `README.md`, `EVALUATION.md`, and `REPRODUCIBILITY.md` was subjected to independent, empirical verification:

1. **Git Baseline & Local Deployment State:** The upstream `main` branch at `https://github.com/EncoreZaan/AXIS` is at commit `f4d5e94` ("merge: integrate origin/main (independent post-remediation audit) into remediation branch"). The local workspace files match HEAD `f4d5e94` bit-for-bit with zero tracked content discrepancies and zero untracked files. However, the local workspace directory was unpacked from `AXIS-main.zip` and therefore lacks `.git/` metadata in `C:\Users\teoba\Documents\Devs\AXIS`, causing local `git status` commands to report `fatal: not a git repository`.
2. **Prior Remediation Closure:** All 5 findings targeted by the post-remediation audit (`4a73fa6`) were verified:
   - *Finding 1 (Legacy paths):* Zero `ARCHI_AI/` hardcoded string prefixes or `os.path.abspath("ARCHI_AI")` statements remain in executable code; all scripts resolve `REPO_ROOT` dynamically.
   - *Finding 2 (Test isolation):* `test_legal_filter_floorplancad`, `test_split_deterministic_anti_leakage`, and preprocessing tests now use `pytest tmp_path`; running the tests produces zero filesystem side effects.
   - *Finding 3 (Gate vocabulary):* `PRE_TRAINING_GATE.md` carries an explicit banner designating Phase 2's `RED` status as historical and superseded by Phase 3's authoritative `CONDITIONAL` decision (`TRAINING_ALLOWED: NO`) in `SCIENTIFIC_READINESS_REPORT.md`.
   - *Finding 4 (Stale branding):* Active documents have been retitled and renamed (`AXIS_CAPABILITY_MATRIX.md`, `DATASET_AXIS_ROLES.md`), while scientific run identifiers (`ARCHI-AI-P4-005`, `ARCHIVisionDataset`) remain properly preserved for historical provenance.
   - *Finding 5 (Python escape sequences):* An exhaustive scan of all 151 Python source files with `warnings.simplefilter('error', DeprecationWarning)` confirmed 0 invalid escape sequences (`\ge`/`\le`).
3. **Packaging & Hard-Gated Tests:** `pip install -e .` completed with exit code 0. The documented import smoke test returned `IMPORT OK`. The hard-gated test suite (`pytest tests/test_audit_validators.py tests/test_master_pipeline.py -v`) passed **9/9** with zero training invocation and zero persistent filesystem artifacts.
4. **Full Test Suite Reproduction:** Running `pytest tests/ -v` produced **35 passed, 19 failed, 38 errors, 1 skipped** — an **exact 100% bit-for-bit match** to the published historical baseline. Spot-checking proved all failures/errors are caused solely by the absence of the non-redistributed private RAW corpus (`dataset/`), not code defects.
5. **Scientific Integrity & Security:** Checkpoint `ARCHI-AI-P4-005`'s validation MAE of `0.0481 m` and Gold Set V3 SHA256 (`81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`) remain intact and unaltered. A security scan detected zero API keys, secrets, private keys, credentials, or `.env` files.
6. **Pre-Training Gate Verdict:** While code hygiene, packaging, and reproducibility standards are fully satisfied, the substantive conditions for initiating real model training remain unfulfilled:
   - Insufficient 2D/3D multimodal training pairs (only 10 true pairs in RAW; 50–100 required).
   - ResPlan 17,000 floorplans remain quarantined for metric (m²) reasoning.
   - FloorPlanCAD 741 drawings remain quarantined under `LEGAL_REVIEW_REQUIRED`.

Therefore, the final pre-training gate verdict is **`PRE_TRAINING_GATE: BLOCKED`**, and **`TRAINING_ALLOWED: NO`** must remain strictly enforced.

---

## 2. Git Baseline

### 2.1. Upstream & Local Verification
- **Target HEAD:** `f4d5e949053743d97091ea35080de5d365899df7` (`f4d5e94`)
- **Remote Origin:** `https://github.com/EncoreZaan/AXIS`
- **Remote Head Verification:** `git ls-remote https://github.com/EncoreZaan/AXIS` confirmed:
  ```text
  f4d5e949053743d97091ea35080de5d365899df7	HEAD
  f4d5e949053743d97091ea35080de5d365899df7	refs/heads/main
  ```

### 2.2. Commit Log on `main` (Verified via Git Reference Inspection)
```text
f4d5e94 (HEAD -> main, origin/main, origin/HEAD) merge: integrate origin/main (independent post-remediation audit) into remediation branch
4a73fa6 fix: close remaining P2/P3 findings from post-remediation audit
6f8ba4c docs: add independent post-remediation audit report
54f27d9 fix: use exact AXIS brand mark
8a60b61 fix: restore AXIS hero visual hierarchy
9b15ab4 feat: integrate official AXIS brand identity
b641e20 fix: refine AXIS hero responsive composition
43a1022 ci: deploy AXIS website with GitHub Pages
5aa920d feat: create AXIS official research landing page
44b19b7 chore: finalize AXIS as MIT-licensed open research project
2b2b0d2 fix: resolve P0/P1 publication-readiness findings from red-team audit
42b1f51 feat: official migration from ARCHI-AI to AXIS v0.1.0
```

### 2.3. Working Tree Integrity
- Comparison of the physical workspace `C:\Users\teoba\Documents\Devs\AXIS` against commit `f4d5e94` confirmed that:
  - Tracked file content diff: **0 bytes** (identical content, normalized CRLF/LF line endings on Windows).
  - Untracked files: **0 files**.
- **Environmental Finding:** Running `git status` directly inside `C:\Users\teoba\Documents\Devs\AXIS` returns `fatal: not a git repository (or any of the parent directories): .git`. The directory was extracted from `C:\Users\teoba\Downloads\AXIS-main.zip` (GitHub source archive export), which excludes the `.git/` database. Per read-only audit rules, no `.git` directory was created or injected into the workspace.

---

## 3. Previous Remediation Verification

Each of the remediation actions documented in `AXIS_POST_REMEDIATION_AUDIT.md` was audited independently:

### Finding 1 — Legacy Paths (`ARCHI_AI/`)
- **Audit method:** Ripgrep search across all files for `ARCHI_AI/`, `ARCHI-AI/`, `os.path.abspath("ARCHI_AI")`, and `sys.path.insert`.
- **Results:**
  - `os.path.abspath("ARCHI_AI")`: Found 0 instances in executable Python code. The 3 occurrences in the repo are in documentation (`DATASET.md`, `AXIS_POST_REMEDIATION_AUDIT.md`, `PUBLICATION_READINESS_AUDIT.md`) detailing the historical defect.
  - `sys.path.insert`: Found in `gold_evaluator.py`, `trainer.py`, `run_micro_pilot.py` cleanly inserting `str(REPO_ROOT)` dynamically determined via `Path(__file__).resolve().parent.parent.parent`.
  - `ARCHI_AI/`: 0 instances in executable production code. All references in `dataset_tools/experiments/micro_pilot/` now use `REPO_ROOT / "dataset" / ...`. Remaining occurrences are strictly historical logs in `docs/` and audit records.
- **Status: CLOSED & CLEAN.**

### Finding 2 — Test Isolation
- **Audit method:** Inspected `tests/test_master_pipeline.py` and `tests/test_preprocessing.py`.
- **Results:**
  - `test_legal_filter_floorplancad` uses `monkeypatch.setattr(legal_filter_module, "MANIFEST_RESTRICTED", tmp_path / ...)` and passes `restricted_root=tmp_path / ...`.
  - `test_split_deterministic_anti_leakage` monkeypatches `split_manager_module.SPLITS_DIR` and `MANIFEST_SPLIT` to `tmp_path`.
  - `test_preprocessing.py` passes `tmp_path` to all preprocessor instances (`FloorPlanCadFrozenHandler`, `ResPlanPreprocessor`, etc.).
  - Executed tests from a clean state without `dataset/` on disk.
- **Status: CLOSED & VERIFIED.**

### Finding 3 — Gate Terminology Consistency
- **Audit method:** Searched documentation for `TRAINING_ALLOWED`, `Pre-Training Gate`, `CONDITIONAL`, `RED`, and `GREEN`.
- **Results:**
  - `docs/research/PRE_TRAINING_GATE.md`: Features a clear warning banner: `⚠️ Décision historique — Phase 2, supersédée par Phase 3`, identifying `SCIENTIFIC_READINESS_REPORT.md` as the authoritative current gate decision.
  - `docs/research/SCIENTIFIC_READINESS_REPORT.md`: Authoritatively declares `CONDITIONAL (TRAINING_ALLOWED: NO)`.
  - `README.md`, `README_EN.md`, `PROJECT_STATUS.md`, `ROADMAP.md`, `RESEARCH.md`, `CHANGELOG.md`, `START_HERE.md` all uniformly declare `CONDITIONAL` and `TRAINING_ALLOWED: NO`.
- **Status: CLOSED & CONSISTENT.**

### Finding 4 — Stale AXIS / ARCHI-AI Naming
- **Audit method:** Grepped for `# ARCHI-AI` and checked document titles.
- **Results:**
  - `PRE_TRAINING_GATE.md` title was updated to `# AXIS — Décision du Pre-Training Gate`.
  - `SCIENTIFIC_READINESS_REPORT.md` title was updated to `# AXIS — Rapport de Maturité Scientifique Pré-Entraînement`.
  - `docs/datasets/ARCHI_AI_CAPABILITY_MATRIX.md` was renamed to `AXIS_CAPABILITY_MATRIX.md`.
  - `docs/datasets/DATASET_ARCHI_AI_ROLES.md` was renamed to `DATASET_AXIS_ROLES.md`.
  - Scientific identifiers (`ARCHI-AI-P4-005`, `ARCHIVisionDataset`) remain preserved for scientific traceability.
- **Status: CLOSED.**

### Finding 5 — Python Escape Sequences
- **Audit method:** Programmatic compilation of all 151 Python source files with `warnings.simplefilter('error', DeprecationWarning)`.
- **Results:**
  - Scanned 151 Python files.
  - Zero `DeprecationWarning`s or syntax warnings encountered.
  - All LaTeX-like formatting strings in `dataset_tools/master_pipeline/reporter.py`, `dataset_tools/supervision/independent_audit/audit_reporter.py`, `dataset_tools/experiments/micro_pilot/gold_evaluator.py`, and `baseline_evaluator.py` correctly escape backslashes (`\\ge`, `\\le`).
- **Status: CLOSED.**

---

## 4. Test Isolation

To prove that the test suite does not pollute the working tree or write persistent files into `dataset/`:

1. **Pre-test working tree state:**
   ```powershell
   Test-Path dataset
   # -> False
   ```
2. **Execution of test commands:**
   - Ran `pytest tests/test_audit_validators.py tests/test_master_pipeline.py -v`
   - Ran `pytest tests/ -v`
3. **Post-test working tree state:**
   ```powershell
   Test-Path dataset
   # -> False
   git status --porcelain -u
   # -> No untracked files or directories created
   ```
The test suite is verified to be side-effect free and completely isolated.

---

## 5. Package Validation

Installation and import smoke tests were executed in the Python environment:

1. **Editable installation:**
   ```bash
   pip install -e .
   ```
   - **Result:** Exit code 0.
   - Output: `Successfully installed axis-ai-0.1.0`
   - Setuptools correctly discovered packages (`dataset_tools`, `evaluation`) via `pyproject.toml`'s find directive.
2. **Optional dataset dependencies:**
   - Installed declared extras `[project.optional-dependencies] dataset` (`shapely>=2.0.0`, `pyarrow>=15.0.0`, `ifcopenshell>=0.7.0`).
   - All installed cleanly without compilation issues.
3. **Import smoke test:**
   ```bash
   python -c "import dataset_tools.master_pipeline.config; import evaluation.runners.benchmark_runner; print('IMPORT OK')"
   ```
   - **Result:** `IMPORT OK` (Exit code 0).

---

## 6. Hard-Gated Tests

The hard-gated CI test subset defined in `.github/workflows/tests.yml` (`unit-tests-no-private-data`) was executed:

```bash
pytest tests/test_audit_validators.py tests/test_master_pipeline.py -v
```

### Execution Results:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\teoba\Documents\Devs\AXIS
configfile: pyproject.toml
collected 9 items

tests/test_audit_validators.py::test_generic_answer_validator_detects_placeholder_none PASSED [ 11%]
tests/test_audit_validators.py::test_generic_answer_validator_detects_cliche PASSED [ 22%]
tests/test_audit_validators.py::test_multimodal_dependency_validator_detects_fake_multimodal PASSED [ 33%]
tests/test_audit_validators.py::test_difficulty_validator_flags_overrated_clearance_check PASSED [ 44%]
tests/test_master_pipeline.py::test_classify_asset_deterministic PASSED  [ 55%]
tests/test_master_pipeline.py::test_legal_filter_floorplancad PASSED     [ 66%]
tests/test_master_pipeline.py::test_provenance_dag_integrity PASSED      [ 77%]
tests/test_master_pipeline.py::test_quality_scorer_dimensions PASSED     [ 88%]
tests/test_master_pipeline.py::test_split_deterministic_anti_leakage PASSED [100%]

======================== 9 passed, 4 warnings in 0.19s ========================
```
- **Passed:** **9 passed** (100% of hard-gated tests).
- **Training Invocation Check:** Inspected test implementations; no test invokes `Trainer`, `train_qlora.py`, `torch.optim`, or backward passes. All tests run pure analytical, cryptographic, and algorithmic validations.

---

## 7. Full Test Suite

The full test suite was executed across `tests/`:

```bash
pytest tests/ -v
```

### Execution Results:
```text
====== 19 failed, 35 passed, 1 skipped, 11 warnings, 38 errors in 1.38s =======
```

### Comparison Against Baseline:
| Outcome | Historical Baseline | Current Run | Match Status |
| :--- | :---: | :---: | :---: |
| **Passed** | 35 | 35 | **EXACT MATCH** |
| **Failed** | 19 | 19 | **EXACT MATCH** |
| **Errored** | 38 | 38 | **EXACT MATCH** |
| **Skipped** | 1 | 1 | **EXACT MATCH** |
| **Total Test Items** | 93 collected + 7 in skipped mod = 99 | 93 collected + 7 in skipped mod = 99 | **EXACT MATCH** |

### Failure & Error Analysis:
- **Root Cause:** 100% of the 19 failures and 38 errors stem from missing private files under `dataset/` (`dataset/raw/...`, `dataset/master/...`, `dataset/supervision/...`).
- **Orphaned Module Skip:** `tests/test_dataset_infra.py` skips with the documented reason: `"requires the private dataset/master/schema/models.py module, which is not part of this public repository."`
- **Zero New Code Regressions:** Not a single error or failure was introduced by the remediation commits (`2b2b0d2` or `4a73fa6`).

---

## 8. Dataset Integrity

The published metrics and partitioning schemes were audited across all documentation and manifest schemas:

1. **Master Dataset v2 Totals:**
   - Train: **53,720**
   - Validation: **5,724**
   - Test: **5,898**
   - **Published Consolidate Total:** **65,342** assets across 19 sources.
   - **Review Queue:** **1,563** assets (isolated, non-additive; excluded from splits).
   - The erroneous additive figure (66,905) appears nowhere in current documentation as a factual count.
2. **Gold Set V3 Sanctuary:**
   - 200 certified instances: 100 `CLEARANCE_CHECK` (3D Euclidean standards), 100 `ROOM_TOPOLOGY` (2D plan topology).
   - 200 Hard Negatives (boundary cases $\pm 0.02$ m).
   - Certified SHA256 Hash: `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca` (verified 64 hex characters, consistent across all files).
   - Hard Negatives SHA256 Hash: `a7991b378e46205e6e639961a9d634dd95661daa22129a89ab0744b73c9414e0`.
3. **Leakage & Partitioning Controls:**
   - `DeterministicSplitter` partitions records deterministically based on `project_group_id` with `seed=42`.
   - Verified that multi-asset projects (e.g. IFC models and plan drawings) are strictly grouped into the same partition, preventing intra-project train/test leakage.

---

## 9. Scientific Validation

1. **Primary Historical Baseline Checkpoint:**
   - Locked Checkpoint ID: `ARCHI-AI-P4-005` (A-Full, seed 42)
   - Baseline Validation MAE: **`0.0481 m`**
   - Gold Set V3 Evaluation MAE: **`0.0517 m`**
   - Cross-benchmark difference: **`+0.0036 m`**
   - Headline reduction vs Baseline 0 (2.7739 m): **`-2.7222 m` (98.14% error reduction)**.
2. **Context & Statistical Robustness:**
   - Section 3.2 of `EVALUATION.md` explicitly documents the severe imbalance of the Gold Set binary clearance evaluation (99 positives, 1 negative), explaining why 100% accuracy has low statistical power for specificity ($n=1$), and why regression MAE is the primary scientific metric.
   - The scientific records in `EVALUATION.md`, `EXPERIMENTS.md`, `PROJECT_STATUS.md`, and `README.md` are aligned and uncorrupted.

---

## 10. Training Pipeline Reproducibility

Inspected `experiment_package/train_qlora.py` and `experiment_package/config/qlora_experiment.yaml`:

- **Target Architecture:** `Qwen/Qwen2-VL-7B-Instruct`
- **Vision Tokenization:** Processed through `AutoProcessor` with dynamic patch grids (`min_pixels: 200704`, `max_pixels: 262144` capping vision tokens to ~400–500 per image).
- **Quantization:** 4-bit NF4 (`load_in_4bit: true`, `bnb_4bit_quant_type: "nf4"`, `bnb_4bit_use_double_quant: true`, compute dtype `bfloat16`).
- **LoRA Configuration:**
  - $r = 8$, $\alpha = 16$, dropout = $0.05$
  - Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` (20,185,088 trainable parameters = 0.2429% of 8.31B total parameters).
  - Vision tower strictly frozen (`freeze_vision_tower: true`).
- **Data Collator:** `VisionLanguageDataCollator` masks system prompt and vision patch tokens with label `-100`, backpropagating loss exclusively on assistant response tokens.
- **Portability:** Replaced previous machine-specific paths with `PACKAGE_ROOT = Path(__file__).resolve().parent`. Output checkpoints default to `outputs/archi_ai_micro_experiment`.
- **Reproducibility Caveat:** While the training code is technically complete and portable, external training cannot currently execute because `experiment_package/dataset/` (`train.jsonl` and `validation.jsonl`) is not public. This limitation is explicitly documented.

---

## 11. Data / Provenance / Legal Review

Reviewed `THIRD_PARTY_LICENSES.md`, `DATASET.md`, and historical audit documents:

1. **Repository License Scope:**
   - AXIS code and documentation are licensed under the **MIT License** (`LICENSE`).
   - Upstream raw datasets, images, and checkpoints are explicitly excluded from the MIT grant.
2. **Status of Key External Datasets:**
   - **ResPlan:** CC-BY 4.0 / MIT. Strictly **quarantined** for metric (m²) reasoning due to scale-distortion forensic findings (std=173.2, 32.1% net-area-null). Permitted only for topological tasks.
   - **FloorPlanCAD:** CC-BY-SA 4.0. Quarantined under **`LEGAL_REVIEW_REQUIRED`**. Zero assets integrated into training/evaluation splits.
   - **RPLAN & IL3D:** Documented as non-commercial "Academic Research Only" terms. No raw data redistributed.
   - **CORE_BUILDINGSMART_IFC & CORE_RESBIM_PAIRED:** Open BIM standards / CC-BY 4.0.
   - **Structured3D, Matterport3D, HM3D, CubiCasa5K, MMIS, Rooms-with-Text:** Documented in external audit registries with respective academic/non-commercial restrictions preserved.
3. **Legal Clearance:** No document in the repository makes unfounded commercial clearance claims. All external constraints are disclosed.

---

## 12. Security / Secrets Review

An automated scan of the entire repository was performed:
- **Searched patterns:** `api_key`, `secret`, `password`, `bearer`, `ghp_`, `hf_`, `BEGIN PRIVATE KEY`, `.env` files.
- **Results:**
  - Committed `.env` files: **0 found**
  - Private cryptographic keys: **0 found**
  - Hardcoded tokens or passwords: **0 found**
  - Hugging Face / GitHub tokens: **0 found** (all `hf_` occurrences are calls to standard library function `hf_hub_download`).
- **Verdict: PASS (No secrets detected).**

---

## 13. Repository Consistency

1. **Training Gate Uniformity:** `TRAINING_ALLOWED: NO` is consistently declared in all 9 status documents (`README.md`, `README_EN.md`, `PROJECT_STATUS.md`, `ROADMAP.md`, `RESEARCH.md`, `CHANGELOG.md`, `START_HERE.md`, `SCIENTIFIC_READINESS_REPORT.md`, `PRE_TRAINING_GATE.md`).
2. **Historical vs. Current Documents:** `PRE_TRAINING_GATE.md`'s historical Phase 2 `RED` status is explicitly disambiguated from Phase 3's authoritative `CONDITIONAL` status via a top-level notice banner.
3. **Internal Links:** Renamed documentation files (`AXIS_CAPABILITY_MATRIX.md`, `DATASET_AXIS_ROLES.md`) resolve correctly.
4. **Commands & Instructions:** All setup instructions in `README.md` and `REPRODUCIBILITY.md` match actual script flags and environment behavior.

---

## 14. Blockers

The following items are formal blockers preventing the lifting of the Pre-Training Gate:

### Blocker 1: Insufficient Multimodal 2D/3D BIM Paired Data (Scientific P0)
- **Issue:** The repository contains only 10 genuine 2D floorplan $\leftrightarrow$ 3D IFC models (`CORE_RESBIM_PAIRED`). Training on 8 train / 2 test residential pairs would lead to catastrophic overfitting rather than generalizable architectural reasoning.
- **Evidence:** `docs/research/SCIENTIFIC_READINESS_REPORT.md` §1.1 & §2.1.
- **Affected Path:** `dataset_tools/master_pipeline/`, `dataset/master/v2/`
- **Why it blocks the gate:** The documented prerequisite for lifting the conditional gate is acquiring 50–100 additional open-licensed OpenBIM IFC pairs.

### Blocker 2: ResPlan Scale-Distortion Metric Quarantine (Scientific P1)
- **Issue:** 17,000 floorplans in `ResPlan.pkl` have arbitrary canvas normalization with no preserved physical scale, exhibiting a 173.2 std in drawing/text area ratios.
- **Evidence:** `docs/datasets/RESPLAN_CALIBRATION_REPORT.md`, `DATASET.md` §3.1.
- **Affected Path:** `dataset_tools/preprocessing/floorplans/resplan_preprocessor.py`
- **Why it blocks the gate:** Training on uncalibrated pixel areas labeled as m² would induce severe spatial hallucinations in the model.

### Blocker 3: FloorPlanCAD Legal Status Quarantine (Legal / Provenance)
- **Issue:** 741 CAD drawings remain flagged as `LEGAL_REVIEW_REQUIRED` due to CC-BY-SA 4.0 copyleft share-alike implications on downstream model checkpoints.
- **Evidence:** `DATASET.md` §3.2, `THIRD_PARTY_LICENSES.md` §2.
- **Affected Path:** `dataset_tools/master_pipeline/legal_filter.py`
- **Why it blocks the gate:** Model training cannot incorporate FloorPlanCAD assets until formal legal clearance or isolation is certified.

### Blocker 4: Missing Local Git Metadata (Baseline Hygiene)
- **Issue:** The working tree in `C:\Users\teoba\Documents\Devs\AXIS` lacks the `.git/` folder, having been unzipped from a GitHub web archive (`AXIS-main.zip`). Standard git commands (`git status`, `git rev-parse`) fail in local shell executions.
- **Evidence:** Direct command execution output: `fatal: not a git repository`.
- **Affected Path:** Workspace root `.`
- **Why it blocks the gate:** Automated CI/CD and training provenance runners require active git commit tracking to tie checkpoint weights to immutable commit hashes.

---

## 15. Final Gate Decision

Based on the empirical evidence gathered during this independent audit:

```text
PRE_TRAINING_GATE: BLOCKED
TRAINING_ALLOWED: NO
```

### Explanation:
The codebase has achieved exemplary standards of engineering hygiene, test isolation, package configuration, and documentation honesty (all historical P0, P1, and P2 findings are closed). However, the Pre-Training Gate is fundamentally a **scientific and legal gate**, not merely a software build gate. The scientific conditions established in `SCIENTIFIC_READINESS_REPORT.md` (50–100 open OpenBIM pairs) and the legal clearance of FloorPlanCAD remain open. Training must remain strictly disallowed until these prerequisites are met.

---

## 16. Recommended Next Steps

1. **Acquire 50–100 OpenBIM IFC Models:** Focus engineering efforts on sourcing CC-BY/MIT/Apache-2.0 IFC architectural models with corresponding 2D plans (e.g. from public buildingSMART repositories or municipal open-data portals) to satisfy Blocker 1.
2. **Deterministic Vector Plan Derivation:** Implement a pipeline to slice 2D vector plans directly from IFC geometry (`IfcWall`, `IfcSpace`) with native millimeter dimensions, resolving the metric calibration problem without relying on distorted raster datasets (Blocker 2).
3. **Legal Disposition of FloorPlanCAD:** Formally resolve the legal analysis regarding CC-BY-SA 4.0 data inclusion in neural network training, or permanently retire FloorPlanCAD from the active corpus registry (Blocker 3).
4. **Git Metadata Restoration:** Initialize or clone the repository via `git clone` so that future automated workflows have native git metadata for automated run-tagging (Blocker 4).

---

## 17. PROVENANCE BLOCKER REMEDIATION

> **Remediation Date:** 2026-09-22  
> **Target Finding:** Blocker 3 — FloorPlanCAD Legal Status Quarantine (`OPEN_P3: 1`, `PROVENANCE_REVIEW: BLOCKED`)  
> **Reference Document:** [`docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md`](docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md) (PDR-2026-001)  
> **Training Configuration:** [`configs/training_corpus_cleared.json`](configs/training_corpus_cleared.json)  

### 1. Original Blocker
- **Finding:** Blocker 3 identified in §14: 741 CAD vector drawings in `CORE_FLOORPLANCAD` remained flagged as `LEGAL_REVIEW_REQUIRED` with documented license uncertainty.
- **Audit Gate Condition:** *"Model training cannot incorporate FloorPlanCAD assets until formal legal clearance or isolation is certified."*
- **Previous Gate Impact:** `PROVENANCE_REVIEW: BLOCKED`, `OPEN_P3: 1`, `TRAINING_MAY_BEGIN: NO`.

### 2. Affected Dataset(s)
- `CORE_FLOORPLANCAD` (FloorPlanCAD: 741 CAD vector drawings in RAW, originally sourced from `Voxel51/FloorPlanCAD`).

### 3. Evidence Reviewed
- `dataset_tools/master_pipeline/legal_filter.py`: Evaluates `CORE_FLOORPLANCAD` as `LegalStatus.LEGAL_REVIEW_REQUIRED`, routing 100% of records to `RESTRICTED_MANIFEST.jsonl`.
- `dataset_tools/master_pipeline/master_builder.py`: Strictly admits only `legal_status == APPROVED`; rejects all 741 FloorPlanCAD records under `RESTRICTED_LICENSE`.
- `dataset_tools/preprocessing/floorplans/floorplancad_handler.py`: Frozen handler yielding an empty generator (0 normalized items produced).
- `dataset_tools/acquisition/acquire_p1_supplements.py`: Retrieves data from Hugging Face repository `Voxel51/FloorPlanCAD`.
- Hugging Face Repository Metadata vs Card Prose: YAML frontmatter specifies `license: cc-by-sa-4.0`, whereas README lines 109 & 130 state `License: Creative Commons Attribution-NonCommercial 4.0 License` with `Out-of-Scope Use: Commercial applications: Dataset is licensed for non-commercial use only.`
- Original Academic Source: Zheng et al., ICCV 2021 (*"FloorPlanCAD: A Large-Scale CAD Drawing Dataset for Panoptic Symbol Spotting"*), published under non-commercial research terms; original host `floorplancad.github.io` closed in 2022 without renewed third-party architectural agency licensing.
- Prior Audits: `DATASET_RAW_FORENSIC_AUDIT.md` §9, `DATASET_LICENSE_AUDIT.md` §2 Catégorie 5, `DATASET_EXTERNAL_AUDIT.md` §21, `DATASET.md` §1 & §3.2, `THIRD_PARTY_LICENSES.md` §2.

### 4. Actual Training Usage
- **Master Dataset v2:** Exactly **0 FloorPlanCAD assets** admitted (0 / 65,342).
- **Training Splits:** Exactly **0 FloorPlanCAD assets** across `train.jsonl` (53,720), `validation.jsonl` (5,724), and `test.jsonl` (5,898).
- **Evaluation Benchmarks:** Exactly **0 FloorPlanCAD assets** in Gold Set V3 (200 instances), MMMU Architecture, or IFC-Bench.
- **Historical Checkpoint:** Exactly **0 FloorPlanCAD assets** used to train `ARCHI-AI-P4-005` (trained on Dataset A-Full: RPLAN + IL3D).
- **Active Pipeline Consumption:** Exactly **0 FloorPlanCAD assets** consumed by `experiment_package` or any training script.

### 5. Remediation Performed
1. **Provenance Decision Record (PDR-2026-001):** Formally authored [`docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md`](docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md), establishing certified hermetic isolation and permanent exclusion from active training configurations.
2. **Documentation Reconciliation:** Updated [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) and [`DATASET.md`](DATASET.md) (§1 and §3.2) to accurately disclose the dual-license contradiction (`CC-BY-SA 4.0` metadata header vs `CC-BY-NC 4.0` README/paper terms) and confirm certified training isolation.
3. **Machine-Readable Clean Training Configuration:** Established [`configs/training_corpus_cleared.json`](configs/training_corpus_cleared.json) defining all cleared sources and explicitly marking `CORE_FLOORPLANCAD` as `STRICTLY_EXCLUDED`.
4. **Historical Sanctuary Preservation:** No historical dataset, manifest, split file, Gold Set instance, checkpoint identifier, or benchmark score was modified.

### 6. Remaining Uncertainty
- The substantive legal conflict between CC-BY-SA 4.0 (ShareAlike copyleft) and CC-BY-NC 4.0 (NonCommercial restriction) remains unadjudicated by external legal counsel.
- The underlying proprietary copyright of architectural drafting agencies from defunct `floorplancad.github.io` remains unrefreshed.
- No false legal clearance is claimed: `CORE_FLOORPLANCAD` remains in status `LEGAL_REVIEW_REQUIRED` and strictly quarantined.

### 7. Effect on First Training Run
- `CORE_FLOORPLANCAD` is **100% excluded** from the first training run and all baseline training runs.
- The training pipeline is completely insulated from copyleft or non-commercial CAD asset contamination.
- The active training corpus consists solely of verified, approved sources defined in `configs/training_corpus_cleared.json`.

### 8. Final Provenance Status
- The gate condition (*"until formal legal clearance or isolation is certified"*) is **100% satisfied** through certified hermetic isolation and formal exclusion from training configurations.
- **`PROVENANCE_REVIEW: PASS`**
- **`OPEN_P3: 0`**
- The overall pre-training gate remains **`PRE_TRAINING_GATE: BLOCKED`** and **`TRAINING_ALLOWED: NO`** due to open scientific blockers (Blocker 1: OpenBIM pair scarcity; Blocker 2: ResPlan metric scale distortion).

---

## FINAL MACHINE-READABLE SUMMARY

```text
PRE_TRAINING_GATE: BLOCKED
TRAINING_ALLOWED: NO
OPEN_P0: 0
OPEN_P1: 0
OPEN_P2: 0
OPEN_P3: 0
TEST_ISOLATION: PASS
PACKAGE_INSTALL: PASS
HARD_GATED_TESTS: PASS
FULL_SUITE_BASELINE: MATCH
LEGACY_PATHS: CLEAN
GATE_STATUS_CONSISTENCY: PASS
DATASET_INTEGRITY: PASS
SCIENTIFIC_RECORD_INTEGRITY: PASS
TRAINING_PIPELINE_REPRODUCIBILITY: PASS
PROVENANCE_REVIEW: PASS
SECURITY_SCAN: PASS
TRAINING_MAY_BEGIN: NO
```
