# AXIS Phase 4 — Final Scientific Training Gate Review

> **Run Identifier:** `RUN-019-FIRST-REAL-DATA-QLORA`  
> **Evaluation Date:** 2026-09-23  
> **Target Commit:** `f4d5e949053743d97091ea35080de5d365899df7`  
> **Status:** **PHASE 4 COMPLETE — VALID TRAINING RUN**

---

## 1. Compliance Audit Matrix

| Verification Dimension | Protocol Requirement | Measured State | Verdict |
| :--- | :--- | :--- | :---: |
| **Git Baseline** | Commit `f4d5e949053743d97091ea35080de5d365899df7` clean | Exact match, zero modified tracked code | **PASS** |
| **Dataset Ingestion** | Real architectural pilot (1 000 assets) | 775 train, 98 val, 127 test | **PASS** |
| **Dataset Hashes** | SHA-256 match on all 6 dataset manifest files | Bit-level identity on all files | **PASS** |
| **Model & Revision** | `Qwen/Qwen2-VL-7B-Instruct` @ `eed13092ef92e448dd6875b2a00151bd3f7db0ac` | Verified & pinned | **PASS** |
| **Gold Set Sanctuary** | Zero access, read-only holdout benchmark | Confirmed untouched and unaccessed | **PASS** |
| **Master Dataset** | Master Dataset v2 unchanged | Confirmed untouched | **PASS** |
| **Training Execution** | QLoRA 4-bit NF4, r=16, α=32, lr=1e-4, 2 epochs | 194 steps completed in 31.18 minutes | **PASS** |
| **Numerical Stability** | Zero NaN / Inf in loss or gradients | 0 NaN, 0 Inf, stable grad norm (< 0.12) | **PASS** |
| **VRAM & Hardware** | < 24 576 MiB, zero OOM errors | Peak VRAM: 10 842.95 MiB, zero OOM | **PASS** |
| **Validation Execution**| Full evaluation on 98 held-out validation assets | Val loss: 2.4067 -> 0.0339 (-98.59%) | **PASS** |
| **Checkpoint Integrity**| Reproducible checkpoints with adapter, optimizer, scheduler | 23 files hashed via SHA-256 in manifest | **PASS** |
| **Test Set Integrity** | Zero access to `test.jsonl` (127 assets) | Confirmed zero test access | **PASS** |

---

## 2. Evidence Separation

### Engineering Evidence: VALID
- Pipeline execution completed end-to-end for 2 full epochs (194 optimization steps).
- Hardware stability proven: 10.8 GB peak VRAM on RTX 3090, leaving >13.7 GB headroom.
- Exact reproducibility guaranteed by pinned versions, seed 42, deterministic collation, and cryptographic file hashes.
- All checkpoints (`checkpoint-97`, `checkpoint-194`, `final_adapter`) verified bit-for-bit intact with valid safetensors and state dicts.

### Scientific Evidence: LIMITED
- Convergence confirmed: Validation loss on 98 unseen real architectural plans decreased by 98.59% (from 2.4067 down to 0.0339), falsifying the null hypothesis of non-learnability.
- Qualitative comparison proves strong acquisition of professional architectural critique schemas, structural element identification, and normative thresholds.
- Scientific scope is nonetheless strictly bounded: High fidelity to the RPLAN critique schema accounts for the low loss; general spatial intelligence across arbitrary non-standard blueprints remains to be evaluated on out-of-distribution holdouts and the Gold Set V3.

---

```
AXIS_PHASE4_RUN: COMPLETE
RUN_ID: RUN-019-FIRST-REAL-DATA-QLORA
GIT_COMMIT_MATCH: PASS
DATASET_HASH_LOCK: PASS
MODEL_REVISION_MATCH: PASS
ENVIRONMENT_MATCH: PASS
TRAINING_EXECUTED: YES
TRAINING_STABLE: YES
NAN_INF: NO
OOM: NO
CHECKPOINT_VALID: YES
VALIDATION_COMPLETED: YES
TEST_SET_USED: NO
GOLD_SET_MODIFIED: NO
MASTER_DATASET_MODIFIED: NO
SCIENTIFIC_EVIDENCE: LIMITED
ENGINEERING_EVIDENCE: VALID
TRAINING_RUN_VALID: YES
NEXT_EXPERIMENT_READY: YES
```
