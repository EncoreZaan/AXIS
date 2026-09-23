# AXIS — Real Data Pre-Training Dry Run Report (`RUN-018-REAL_DATA_DRY_RUN`)

> **Date:** 2026-09-22  
> **Target Base Model:** `Qwen/Qwen2-VL-7B-Instruct` (Revision: `eed13092ef92e448dd6875b2a00151bd3f7db0ac`)  
> **Dataset:** Real Architectural Pilot (`REAL_DATA_PILOT`, 1,000 unique assets)  
> **Status:** **DRY_RUN: PASS** | **OPTIMIZER_STEP: DISABLED**

---

## 1. Dry Run Verification Summary

| Gate Requirement | Specification | Measured State | Verdict |
| :--- | :--- | :--- | :---: |
| **Dataset Ingestion** | Real multi-image architectural assets | 775 train samples loaded | **PASS** |
| **Image Decoding & Resolution** | 256x256 to high-res drawings | Validated via PIL & processor | **PASS** |
| **Processor Conversion** | Qwen2-VL processor with chat template | Successful tokenization & patching | **PASS** |
| **Quantization & LoRA** | 4-bit NF4, double quant, LoRA $r=16, lpha=32$ | Applied cleanly | **PASS** |
| **Batch Collation** | Multimodal dynamic padding | Shapes: `input_ids [1, L]`, `pixel_values [N, 1176]` | **PASS** |
| **Forward Pass** | Causal LM forward loss | Finite loss computed without NaN/Inf | **PASS** |
| **Backward Pass** | Graph construction & autograd | Gradients populated across LoRA adapters | **PASS** |
| **Peak VRAM** | < 24,000 MiB | **10052.2 MiB** | **PASS** |
| **Optimizer Execution** | **Strictly DISABLED** | `optimizer.step()` was **NOT** invoked | **PASS** |
| **Weight Constancy** | Zero model parameters updated | Verified bitwise unchanged | **PASS** |

---

## 2. Micro-Batch Step Execution Telemetry

| Step | Sample ID | Source | Loss | Grad Norm | Duration | VRAM Allocated |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `archi_pilot_0002` | `CORE_RESBIM_PAIRED` | 2.3580 | 0.1216 | 2033.7 ms | 8493.7 MiB |
| 2 | `archi_pilot_0003` | `CORE_RESBIM_PAIRED` | 2.3561 | 0.2401 | 1404.6 ms | 8494.0 MiB |
| 3 | `archi_pilot_0004` | `CORE_RESBIM_PAIRED` | 2.3505 | 0.3593 | 1352.3 ms | 8494.0 MiB |
| 4 | `archi_pilot_0006` | `CORE_RESBIM_PAIRED` | 2.3434 | 0.4768 | 1359.6 ms | 8494.0 MiB |
| 5 | `archi_pilot_0007` | `CORE_RESBIM_PAIRED` | 2.3527 | 0.5946 | 1355.8 ms | 8494.0 MiB |
| 6 | `archi_pilot_0008` | `CORE_RESBIM_PAIRED` | 2.3829 | 0.7116 | 1356.8 ms | 8494.0 MiB |
| 7 | `archi_pilot_0009` | `CORE_RESBIM_PAIRED` | 2.3684 | 0.8291 | 1359.8 ms | 8494.0 MiB |
| 8 | `archi_pilot_0010` | `CORE_RESBIM_PAIRED` | 2.3633 | 0.9478 | 1377.8 ms | 8494.0 MiB |

---

## 3. Telemetry & Invariants Check

- **Average Dry Run Loss:** `2.3594`
- **Peak VRAM Observed:** `10052.2 MiB`
- **CUDA Out of Memory:** `0`
- **CUDA Assertion Errors:** `0`
- **Model Weights Updated:** `False`
- **Operational Invariant Preserved:** `TRAINING_ALLOWED: NO` | `TRAINING_MAY_BEGIN: NO`
