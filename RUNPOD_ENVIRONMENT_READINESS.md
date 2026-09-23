# AXIS — RunPod Environment Readiness Report (`RUNPOD_ENVIRONMENT_READINESS.md`)

> **Audit & Gate Date:** 2026-09-22  
> **Environment:** RunPod Remote GPU Instance  
> **Pod Name:** `territorial_green_minnow`  
> **Pod ID:** `kqgdq6zb1022eu`  
> **Target Baseline Commit:** `f4d5e949053743d97091ea35080de5d365899df7` (`f4d5e94`)  
> **Operational Invariant:** `TRAINING_ALLOWED: NO` | `TRAINING_MAY_BEGIN: NO`  

---

## 1. Machine & Hardware Forensics

| Parameter | Observed Value | Specification Status |
| :--- | :--- | :---: |
| **Pod ID** | `kqgdq6zb1022eu` | Verified |
| **Pod Name** | `territorial_green_minnow` | Verified |
| **Direct SSH Endpoint** | `213.181.122.2:57661` -> `:22` | Verified |
| **GPU Model** | NVIDIA GeForce RTX 3090 | Target 24 GB class met |
| **GPU Total VRAM** | 24,576 MiB (23.56 GiB detected by PyTorch) | **PASS** (>= 22.0 GiB) |
| **NVIDIA Driver Version** | `580.159.04` | Verified |
| **System CUDA Runtime** | CUDA 13.0 (Driver) / CUDA 12.4 (PyTorch) | Verified |
| **Host CPU** | AMD EPYC-Rome Processor (26 vCPUs) | Verified |
| **System RAM** | 445 GiB total (429 GiB available) | Verified |
| **Filesystem & Disk** | Root overlay 50 GB (5.8 GB used, 45 GB available) | Verified |
| **Operating System** | Ubuntu 24.04.3 LTS (Noble Numbat), Kernel `6.8.0-124-generic` | Verified |
| **Base Python** | Python 3.12.3 (`/usr/bin/python3`) | Verified |

---

## 2. Repository Integrity

| Parameter | Observed Value | Status |
| :--- | :--- | :---: |
| **Repository URL** | `https://github.com/EncoreZaan/AXIS.git` | Authoritative |
| **Cloned Destination** | `/workspace/AXIS` | Verified |
| **Commit HEAD** | `f4d5e949053743d97091ea35080de5d365899df7` | Exact Match |
| **Short Hash** | `f4d5e94` | Exact Match |
| **Git Branch** | `main` | Verified |
| **Working Tree Status** | Clean (untracked: `configs/training_corpus_cleared.json` uncommitted) | **PASS** |
| **Git Policy** | Zero commits, zero pushes, history strictly preserved | **PASS** |

---

## 3. Python Virtual Environment & Dependencies

* **Isolated Environment Path:** `/workspace/AXIS/.venv/` (Python 3.12.3)
* **PyTorch Version:** `2.6.0+cu124`
* **Torchvision Version:** `0.21.0+cu124`
* **CUDA Availability:** `True` (Device: `NVIDIA GeForce RTX 3090`)

### Authoritative Installed Packages (`pip freeze`)
```text
accelerate==1.15.0
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.15.1
av==18.1.0
-e git+https://github.com/EncoreZaan/AXIS.git@f4d5e949053743d97091ea35080de5d365899df7#egg=axis_ai
bitsandbytes==0.50.2
certifi==2026.7.22
charset-normalizer==3.5.1
click==8.5.0
filelock==3.32.3
fsspec==2026.7.0
h11==0.16.0
hf-xet==1.6.0
httpcore==1.0.9
httpx==0.28.1
huggingface_hub==1.32.0
idna==3.20
ifcopenshell==0.8.5
iniconfig==2.3.0
isodate==0.7.2
Jinja2==3.1.6
lark==1.3.1
markdown-it-py==4.2.0
MarkupSafe==3.0.3
mdurl==0.1.2
mpmath==1.3.0
networkx==3.6.1
numpy==2.5.2
nvidia-cublas-cu12==12.4.5.8
nvidia-cuda-cupti-cu12==12.4.127
nvidia-cuda-nvrtc-cu12==12.4.127
nvidia-cuda-runtime-cu12==12.4.127
nvidia-cudnn-cu12==9.1.0.70
nvidia-cufft-cu12==11.2.1.3
nvidia-curand-cu12==10.3.5.147
nvidia-cusolver-cu12==11.6.1.9
nvidia-cusparse-cu12==12.3.1.170
nvidia-cusparselt-cu12==0.6.2
nvidia-nccl-cu12==2.21.5
nvidia-nvjitlink-cu12==12.4.127
nvidia-nvtx-cu12==12.4.127
packaging==26.3
peft==0.21.0
pillow==12.3.0
pluggy==1.6.0
psutil==7.2.2
pyarrow==25.0.1
pydantic==2.13.5
pydantic_core==2.46.5
Pygments==2.21.0
pytest==9.1.1
python-dateutil==2.9.0.post0
PyYAML==6.0.3
qwen-vl-utils==0.0.14
regex==2026.9.10
requests==2.34.2
rich==15.0.0
safetensors==0.8.0
setuptools==78.1.0
shapely==2.1.2
shellingham==1.5.4
six==1.17.0
sympy==1.13.1
tokenizers==0.23.2
torch==2.6.0+cu124
torchvision==0.21.0+cu124
tqdm==4.70.1
transformers==5.17.0
triton==3.2.0
typer==0.27.2
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.8.0
```

---

## 4. Dataset Validation & Provenance Boundaries

* **Master Dataset v2 Certified Total:** 65,342 unique assets across 19 physical sources.
  - **Train Partition:** 53,720 assets
  - **Validation Partition:** 5,724 assets
  - **Test Partition:** 5,898 assets
  - **Review Queue:** 1,563 items (strictly quarantined, isolated, non-additive).
* **Cleared Training Configuration:** `configs/training_corpus_cleared.json` (SHA256: `5fd39698864be5facb1f07c7f44829da65d8e065da1324f1787f9da358d05d49`).
* **FloorPlanCAD Exclusion:** `CORE_FLOORPLANCAD` (741 RAW assets) is hermetically isolated under `LEGAL_REVIEW_REQUIRED`. Confirmed 0 FloorPlanCAD assets in Master Dataset v2, 0 in splits, 0 in `configs/training_corpus_cleared.json` cleared list.
* **ResPlan Quarantine:** `CORE_RESPLAN` metric scaling quarantine verified. Physical metric area and dimensional regression are prohibited; only topological classification is permitted.
* **OpenBIM Status:** `OPENBIM_BLOCKER: NON_BLOCKING` (10 valid residential paired units in `CORE_RESBIM_PAIRED`, no ungrounded pairs).
* **Gold Set V3 Sanctuary:** 200 instances isolated from training; manifest SHA256 `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`. Historical benchmark MAE `0.0517 m`.

---

## 5. Model Access & Configuration

* **Target Base Model:** `Qwen/Qwen2-VL-7B-Instruct`
* **Model Revision / SHA:** `eed13092ef92e448dd6875b2a00151bd3f7db0ac`
* **Authentication Requirement:** None (publicly accessible open model on Hugging Face Hub).
* **Tokenizer & Processor:** `Qwen2VLProcessor` initialized and validated successfully.
* **Quantization:** 4-bit NF4 (`bnb_4bit_quant_type: "nf4"`, `bnb_4bit_use_double_quant: true`, `compute_dtype: bfloat16`).
* **LoRA Target Modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` (`r: 8`, `alpha: 16`, `dropout: 0.05`, `freeze_vision_tower: true`).
* **Training Hyperparameters:** `lr: 1.0e-4`, `batch_size: 1`, `grad_accum: 8` (effective batch 8), `optim: paged_adamw_8bit`, `bf16: true`.

---

## 6. Storage Validation

* **Total Filesystem Capacity:** 50 GB (overlay root)
* **Used Storage:** 5.8 GB
* **Free / Available Storage:** 45 GB (44.2 GB free)
* **Expected Model Cache (`Qwen2-VL-7B-Instruct`):** ~14.5 GB
* **Expected Checkpoint Storage (LoRA adapter only):** ~150 MB
* **Expected Dataset Footprint:** ~3.5 GB
* **Storage Verdict:** **PASS** (45 GB available comfortably accommodates total peak requirement of ~18-20 GB).

---

## 7. Hard-Gated Tests & Verification Suite

### Hard-Gated CI Tests (`tests/test_audit_validators.py`, `tests/test_master_pipeline.py`)
```text
tests/test_audit_validators.py::test_generic_answer_validator_detects_placeholder_none PASSED
tests/test_audit_validators.py::test_generic_answer_validator_detects_cliche PASSED
tests/test_audit_validators.py::test_multimodal_dependency_validator_detects_fake_multimodal PASSED
tests/test_audit_validators.py::test_difficulty_validator_flags_overrated_clearance_check PASSED
tests/test_master_pipeline.py::test_classify_asset_deterministic PASSED
tests/test_master_pipeline.py::test_legal_filter_floorplancad PASSED
tests/test_master_pipeline.py::test_provenance_dag_integrity PASSED
tests/test_master_pipeline.py::test_quality_scorer_dimensions PASSED
tests/test_master_pipeline.py::test_split_deterministic_anti_leakage PASSED
======================== 9 passed, 4 warnings in 0.32s =========================
```
Result: **9/9 PASSED (100%)**

### Full Repository Test Suite Baseline
* **Observed Result:** `19 failed, 35 passed, 1 skipped, 38 errors in 1.43s`
* **Historical Baseline:** `35 passed, 19 failed, 38 errors, 1 skipped`
* **Correlation:** **100% exact match to historical baseline**. Failures/errors are the known and documented consequence of the private raw dataset assets being excluded from git.

---

## 8. Non-Training Dry Run

A rigorous 10-point dry run was executed on the remote GPU environment:
1. **Module Imports:** PyTorch, Transformers, PEFT, BitsAndBytes, Accelerate, Qwen-VL-Utils, PyYAML, PIL verified.
2. **AutoProcessor:** `AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")` loaded.
3. **Multimodal Preprocessing:** Formatted chat template with `test_images/sample_interior.jpg` (1024x768). Verified tensor generation (`input_ids`, `pixel_values`, `image_grid_thw`).
4. **BitsAndBytes 4-bit CUDA Allocation:** Allocated `Linear4bit(64, 64, compute_dtype=bfloat16)` on `cuda`. Forward pass executed with zero error.
5. **LoRA Injection:** Tested PEFT `LoraConfig` injection into projection layers with `r=8`, `alpha=16`. Trainable parameters reported accurately.
6. **Data Collator:** `VisionLanguageDataCollator` batched multimodal tensors with dynamic padding.
7. **Baseline Model Smoke Test:** AXIS `SpatialRelationMLP` forward pass on CUDA (shape: `torch.Size([4])`, output values computed without backward).
8. **Filesystem Write Permissions:** Verified write/delete permissions for `outputs/` without creating training checkpoints.
9. **Cleared Boundary Verification:** Loaded `configs/training_corpus_cleared.json`, confirmed `CORE_FLOORPLANCAD` quarantined and excluded from training.
10. **Invariants Preserved:** Zero backward passes, zero optimizer steps, zero weights updated.
* **Dry Run Result:** **PASS**

---

## 9. Reproducibility Configuration Hashes

| Configuration Artifact | Path | SHA256 Hash |
| :--- | :--- | :--- |
| **QLoRA Experiment Config** | `experiment_package/config/qlora_experiment.yaml` | `49b11ac9b1f82b604c9478006f2021d3b602be33b7172eb02d8315f9197f9ed8` |
| **Task Catalogue** | `configs/task_catalogue.json` | `b9fe4d90dbd596bae03c6dc2aaf6aa21cd53f1be048dc36ab098bbdb17ebd985` |
| **Cleared Training Corpus** | `configs/training_corpus_cleared.json` | `5fd39698864be5facb1f07c7f44829da65d8e065da1324f1787f9da358d05d49` |
| **pyproject.toml** | `pyproject.toml` | `dd803edcb7955115151fc0cd8033ab76eaad4a11647f3955709bfb5be92f43e9` |
| **Core Requirements** | `requirements.txt` | `9e029ec08b1a947bed2d4d1148cc3c136fe355e8d983b5e09f13a0a65055ffbb` |
| **Experiment Requirements** | `experiment_package/requirements.txt` | `881046ff808c308505e44c28e0ae987e0c3779d3a85fbb28091ad45d61fd7e71` |

---

## 10. Security Audit

* **SSH Private Keys in Repo:** None.
* **API / HF Tokens in Repo:** None.
* **Credentials in Git Remote:** None (`origin: https://github.com/EncoreZaan/AXIS.git`).
* **Environment Files (`.env`):** None tracked.
* **Secret Leakage:** 0 secrets detected.

---

## 11. Final Machine-Readable Gate

```text
RUNPOD_ENVIRONMENT: READY
GPU_COMPATIBILITY: PASS
PYTORCH_CUDA: PASS
REPOSITORY_INTEGRITY: PASS
DEPENDENCIES: PASS
TRAINING_CONFIGURATION: PASS
TRAINING_DATASET: PASS
MODEL_ACCESS: PASS
STORAGE: PASS
DRY_RUN: PASS
REPRODUCIBILITY: PASS
SECURITY: PASS
TRAINING_ALLOWED: NO
TRAINING_MAY_BEGIN: NO
```
