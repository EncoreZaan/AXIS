# RUN-022 Spatial Grounding Pilot — Final Training & Resumption Report

> **Run ID:** `RUN-022-SPATIAL-GROUNDING-PILOT`  
> **Scientific Campaign:** AXIS Phase 6B — Spatial Grounding Pilot  
> **Status:** **TRAINING_COMPLETED** | **GATE: PASS**  
> **Audited Baseline Git Commit:** `f4d5e949053743d97091ea35080de5d365899df7`  
> **Timestamp:** `2026-09-23T12:42:46Z`  

---

## 1. Run Identity & Scientific Objective

- **RUN_ID:** `RUN-022-SPATIAL-GROUNDING-PILOT`
- **RUN_NAME:** AXIS Spatial Grounding Scientific Training Pilot
- **SCIENTIFIC_OBJECTIVE:** Test whether spatial supervision grounding increases actual visual dependence and spatial reasoning accuracy without template shortcut
- **BASELINE_COMMIT:** `f4d5e949053743d97091ea35080de5d365899df7`
- **BASE_MODEL:** `Qwen/Qwen2-VL-7B-Instruct`
- **MODEL_REVISION:** `eed13092ef92e448dd6875b2a00151bd3f7db0ac`
- **DATASET:** `AXIS_SPATIAL_SUPERVISION_V1` (`RUN-021-SPATIAL-SUPERVISION`)
- **DATASET_CONFIG_HASH:** `9c0908c4c2bc25c647cfde7d885e4d8fe9ba507fb00fb79ce42852942ea60d6c`
- **TRAIN_SPLIT_HASH:** `227ba7db7769e3f25d365a33efd03126e18612cf5821f1f23dcd2342a701e849` (6,160 samples)
- **VAL_SPLIT_HASH:** `c543a319321534f016c94aeb8ee74503bc8f01511c232ec91394d69a307467d2` (784 samples)
- **TEST_SPLIT_HASH:** `aaba73433c9ccea7a5c6134154577ea80591e23755665794bec603ebdf53053f` (1,006 samples, held-out)
- **SEED:** `42` (Deterministic)
- **TRAINING_CONFIG:** `RUN-022-SPATIAL-GROUNDING-PILOT/training_config.yaml`
- **TOTAL_OPTIMIZER_STEPS:** `2310`
- **FINAL_EPOCH:** `3.0`
- **EFFECTIVE_BATCH_SIZE:** `8` (Micro-batch 1 × Gradient Accumulation 8)

---

## 2. Execution Environment

Recorded from verified runtime telemetry (`environment_snapshot.json`):

| Component | Value / Specification |
| :--- | :--- |
| **GPU Model** | NVIDIA GeForce RTX 3090 |
| **Total VRAM** | 24,124.19 MiB (24 GB) |
| **NVIDIA Driver** | 580.159.04 |
| **CUDA Version** | 12.4 |
| **PyTorch Version** | 2.6.0+cu124 |
| **Python Version** | 3.12.3 (GCC 13.3.0) |
| **Operating System** | Linux-6.8.0-124-generic-x86_64 (glibc 2.39) |
| **Transformers** | 5.17.0 |
| **PEFT** | 0.21.0 |
| **bitsandbytes** | 0.50.2 |
| **qwen-vl-utils** | 0.0.14 |
| **Pillow** | 12.3.0 |
| **NumPy** | 2.5.2 |
| **Base Model ID** | `Qwen/Qwen2-VL-7B-Instruct` |
| **Base Model Revision**| `eed13092ef92e448dd6875b2a00151bd3f7db0ac` |

---

## 3. Checkpoint Final & Adapter Verification

### 3.1 Final Checkpoint: `checkpoint-2310`
- **Path:** `RUN-022-SPATIAL-GROUNDING-PILOT/checkpoints/checkpoint-2310/`
- **Status:** **COMPLETE & INTACT** (8 files verified)
- **adapter_model.safetensors SHA-256:** `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479` (161,539,072 bytes)
- **adapter_config.json SHA-256:** `53701b89080d39a4466ed52e83b9d566e1a57d345a80714083ed01871d4ffd27` (1,181 bytes)
- **optimizer.pt SHA-256:** `dea0f759b150c5658ba04efaff86788e107994bde16528b222cb2fd01a4b9326` (83,484,738 bytes)
- **scheduler.pt SHA-256:** `3e8295ed3cedebf093876bb428a18c98f757f215ca33b40cae10a7aced578879` (1,064 bytes)
- **trainer_state.json SHA-256:** `aeaf5b8d421f8017ea0e3b2f2813d162d6446676b2c7ba66ac08b1be2910ef6f` (49,302 bytes)
- **rng_state.pth SHA-256:** `100947b8111f256c854bc82f1c91177994bcf8c2fd803162a70adc72d493b445` (14,244 bytes)
- **training_args.bin SHA-256:** `9ba182c47617bef4bbf3ada99016b494826c02d276ac7e9856dc0c9241326fe4` (4,792 bytes)
- **README.md SHA-256:** `5351fbef8003a16406d196bcff385af2c82c70eaee6e23e36c99f26ad644666e` (5,204 bytes)

### 3.2 Final Adapter: `final_adapter`
- **Path:** `RUN-022-SPATIAL-GROUNDING-PILOT/checkpoints/final_adapter/`
- **Status:** **COMPLETE & INTACT** (7 files verified)
- **adapter_model.safetensors SHA-256:** `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479` (161,539,072 bytes)
- **Bit-exact equivalence:** Identical SHA-256 between `checkpoint-2310/adapter_model.safetensors` and `final_adapter/adapter_model.safetensors` (**PASS**).
- **Associated tokenizer & configs:**
  - `adapter_config.json`: `53701b89080d39a4466ed52e83b9d566e1a57d345a80714083ed01871d4ffd27` (1,181 bytes)
  - `tokenizer_config.json`: `3b1b5c1bf22e8ff5ec310659004861840da7e00241dcd5328a71e317b59e6c84` (808 bytes)
  - `tokenizer.json`: `ff8cce547abc110590d19c6b5b6e0c6a7b4c8d1012d78b9c42131bae7f494a02` (11,420,367 bytes)
  - `processor_config.json`: `e3eb6920d4bb0b82d3de3949e4220e47edab7fa53fe59560239c7a5da74ade99` (1,291 bytes)
  - `chat_template.jinja`: `a0bc6f6fc7a29a80017a433e8f03a1cc1236e838a944a2d034295a60c4f2fddb` (1,017 bytes)
  - `README.md`: `5351fbef8003a16406d196bcff385af2c82c70eaee6e23e36c99f26ad644666e` (5,204 bytes)

---

## 4. Historic Checkpoint Inventory

All intermediate and periodic checkpoints are fully indexed, cryptographically sealed, and catalogued in `checkpoint_hashes.json`:

| Checkpoint | Epoch | Timestamp (UTC) | Files | `adapter_model.safetensors` SHA-256 | Adapter Size |
| :--- | :---: | :---: | :---: | :--- | :---: |
| `checkpoint-250` | 0.3247 | 2026-09-23T04:26:41 | 8 | `8a7986e37660035cba59558463df86d376d3d67ec47ed281e71b0bbfd8c21c1b` | 161,539,072 B |
| `checkpoint-500` | 0.6494 | 2026-09-23T04:54:15 | 8 | `82b4f9f35e816ef6f0729aab5ad5ce8128e2a075bb71b410940605c1085e735b` | 161,539,072 B |
| `checkpoint-750` | 0.9740 | 2026-09-23T05:22:20 | 8 | `f7e3bd392fc2d5da7a0796134c2b0211c5f1a0dea237d8c1a333f7e07898e271` | 161,539,072 B |
| `checkpoint-1000`| 1.2987 | 2026-09-23T10:01:21 | 8 | `42ac83c4a8af1f0833dc8cae4ffb635e4d7608c24875dc46159f24b936e0b50e` | 161,539,072 B |
| `checkpoint-1250`| 1.6234 | 2026-09-23T10:33:05 | 8 | `d5f1af2bb83aee8af3282842c72894580fbd174de23c6c186a6e208801bd52b8` | 161,539,072 B |
| `checkpoint-1500`| 1.9481 | 2026-09-23T11:04:47 | 8 | `fa8fdaac9926ef6128f9f188e1a2b26a84b3709ce8386f65e699906ab6b3e93b` | 161,539,072 B |
| `checkpoint-1750`| 2.2727 | 2026-09-23T11:36:28 | 8 | `8e24ff322b2005720f1005124dace16aa453e4d48da9d081cad0a7f1161a456b` | 161,539,072 B |
| `checkpoint-2000`| 2.5974 | 2026-09-23T12:08:12 | 8 | `6a72cea7b3be619775e9ed35497c770c2cf991aeb1f3b22955ff1596277b30aa` | 161,539,072 B |
| `checkpoint-2250`| 2.9221 | 2026-09-23T12:35:45 | 8 | `2f0a1d2bafccd6128f2f36661518f1d6ded11ec536aa65fb6e0663b7f175e367` | 161,539,072 B |
| `checkpoint-2310`| 3.0000 | 2026-09-23T12:42:46 | 8 | `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479` | 161,539,072 B |
| `final_adapter`  | 3.0000 | 2026-09-23T12:42:46 | 7 | `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479` | 161,539,072 B |

---

## 5. Complete Metrics Trajectory

Extract from `training_metrics.jsonl` (259 records):

| Step | Epoch | Train Loss | Eval Loss | Learning Rate | Gradient Norm |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | 0.0000 | — | 1.3967 | 0.0000 | — |
| **800** | 1.0390 | 0.2092 | 0.1407 | 7.7894e-05 | 0.1138 |
| **900** | 1.1688 | 0.1496 | 0.1384 | 7.1690e-05 | 0.2550 |
| **1000** | 1.2987 | 0.1639 | 0.1383 | 6.5042e-05 | 0.2405 |
| **1100** | 1.4286 | 0.1748 | 0.1341 | 5.8087e-05 | 0.2297 |
| **1200** | 1.5584 | 0.1492 | 0.1371 | 5.0966e-05 | 0.2708 |
| **1300** | 1.6883 | 0.2193 | 0.1332 | 4.3826e-05 | 0.4282 |
| **1400** | 1.8182 | 0.1782 | 0.1302 | 3.6812e-05 | 0.5588 |
| **1500** | 1.9481 | 0.1640 | 0.1295 | 3.0067e-05 | 0.4857 |
| **1600** | 2.0779 | 0.1754 | 0.1330 | 2.3730e-05 | 0.6144 |
| **1700** | 2.2078 | 0.1470 | 0.1333 | 1.7931e-05 | 0.1105 |
| **1800** | 2.3377 | 0.1555 | 0.1374 | 1.2787e-05 | 0.5116 |
| **1900** | 2.4675 | 0.1217 | 0.1348 | 8.4042e-06 | 0.1244 |
| **2000** | 2.5974 | 0.1507 | 0.1362 | 4.8720e-06 | 1.0390 |
| **2100** | 2.7273 | 0.1071 | 0.1392 | 2.2627e-06 | 0.9443 |
| **2200** | 2.8571 | 0.1249 | 0.1396 | 6.2966e-07 | 0.1987 |
| **2300** | 2.9870 | 0.1412 | 0.1398 | 6.1965e-09 | 0.4836 |
| **2310** | **3.0000** | **0.1218** | **0.1397** | **5.1212e-11**| **0.8919** |

- **FINAL_TRAIN_LOSS:** `0.1218`
- **FINAL_EVAL_LOSS:** `0.1397`
- **AVERAGE_TRAIN_LOSS:** `0.1055`
- **INITIAL_EVAL_LOSS:** `1.3967`
- **EVAL_LOSS_DELTA:** `-1.2570`
- **TOTAL_DURATION:** `13,941.3` s (~3h 52m 21s)

---

## 6. Interruption & Resumption Chronology

**Historical Event:**  
Training was NOT executed in an uninterrupted single run. It experienced an abrupt process termination and was deterministically resumed.

1. **Initial Execution Phase:**
   - 1,000 optimizer steps were completed.
   - Upon forensic diagnostics: process was found halted, GPU was idle (0% utilization, 4 MiB memory), with no system deadlock or hardware freeze.
   - `checkpoint-1000` was NOT available on disk at the time of resumption because the interruption occurred before checkpoint serialization (configured for `save_steps: 250`).
2. **Last Valid Physical Checkpoint Identified:**
   - `checkpoint-750` (`/workspace/AXIS/RUN-022-SPATIAL-GROUNDING-PILOT/checkpoints/checkpoint-750`).
3. **Historic Checkpoint Preservation:**
   - `checkpoint-250`, `checkpoint-500`, and `checkpoint-750` were duplicated into `historical_checkpoints/` prior to resuming the HuggingFace Trainer to prevent garbage collection by `save_total_limit: 3`.
4. **Resumption:**
   - Optimizer step `751` $\to$ `2310` executed cleanly to completion.
   - Telemetry from steps 0–1000 prior to interruption is preserved in `training_metrics_interrupted_step1000.jsonl`.

---

## 7. Resumption Reproducibility & Stability

The comparison between pre-interruption recordings and post-resumption recomputed values confirms numeric determinism:

| Metric | Pre-Interruption (Original Run) | Post-Resumption (Recomputed) | Variance / Delta |
| :--- | :---: | :---: | :---: |
| **Step 1000 Train Loss** | `0.1632` (0.16319) | `0.1639` (0.16391) | $+0.0007$ |
| **Step 1000 Gradient Norm** | `0.2412` (0.24116) | `0.2405` (0.24052) | $-0.0007$ |
| **Eval Loss (Step 800)** | `0.1403` (0.14028) | `0.1407` (0.14072) | $+0.0004$ |
| **Eval Loss (Step 1000)**| `0.1389` (pre-step-900: 0.13895) | `0.1383` (0.13831) | $-0.0006$ |

The tiny delta confirms numerical consistency under deterministic seed 42 with bfloat16 mixed precision.

---

## 8. Warnings & Errors Audit

- **Unauthenticated HF Hub Request Warning:**
  `Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.`
  *Impact:* None. Base weights and processor configuration loaded successfully from cache/public repository.
- **Cache Compatibility Warning:**
  `[transformers] use_cache=True is incompatible with gradient checkpointing. Setting use_cache=False.`
  *Impact:* None. Transformers automatically and correctly disabled KV-caching during gradient checkpointing training passes.
- **No Fatal CUDA or NaN Errors:** Zero gradient overflows, zero NaN losses, zero unrecoverable CUDA exceptions recorded across all 2,310 steps.

---

## 9. Sanctuary Invariants Verification

All sanctuarized assets were verified strictly in read-only mode:

- **RUN-021 Spatial Supervision:** **UNMODIFIED** (all 12 files verified against `RUN-021-SPATIAL-SUPERVISION/hashes.json`).
- **Master Dataset:** **UNMODIFIED** (all 6 files in `experiments/runpod_2026-09-22/REAL_DATA_PILOT/` match `RUN-017-DATASET_LOCK/hashes.json` exactly).
- **Gold Set V3:** **UNMODIFIED & ISOLATED** (SHA-256 `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`).
- **Baseline Git Commit:** **UNMODIFIED** (`f4d5e949053743d97091ea35080de5d365899df7`).

---

## 10. Manual Audit Caveat

> [!IMPORTANT]
> **Clarification of RUN-021 Audit Status:**  
> Historical documentation in RUN-021 contained the shorthand label `MANUAL_AUDIT: PASS`.  
> Forensic code inspection reveals that this audit was an **automated programmatic geometric verification** of 50 sampled instances against bounding boxes and coordinates, **not** an inspection performed by a human annotator.  
>  
> To prevent misleading claims:
> - **`MANUAL_AUDIT_HUMAN:`** `NOT_PERFORMED`
> - **`AUTOMATED_GEOMETRIC_AUDIT:`** `PASS` (100% concordance verified by script)

---

## 11. Scientific Limitations

> [!WARNING]
> **Strict Scientific Scope:**  
> RUN-022 demonstrates that the vision-language model (`Qwen2-VL-7B-Instruct`) was successfully trained with converging training and evaluation loss on the spatial supervision dataset produced by RUN-021.  
>  
> The decrease in training and validation loss does **NOT** by itself demonstrate:
> 1. An improvement in spatial reasoning accuracy;
> 2. A causal dependency on visual pixels (visual grounding);
> 3. Generalization to unseen architectural layouts;
> 4. A reduction in spatial hallucinations;
> 5. An improvement in the Visual Dependency Index (VDI).  
>  
> **These scientific properties cannot be inferred from loss convergence and MUST be rigorously and independently measured by RUN-023.**

---

## 12. RUN-023 Evaluation Protocol Preparedness

- **RUN-023 Launched:** **NO** (`RUN-023_STARTED: NO`)
- **Protocol Document:** `docs/experiments/RUN-023_EVALUATION_PROTOCOL.md` and `RUN-022-SPATIAL-GROUNDING-PILOT/RUN_023_PROTOCOL.md`
- **Evaluation Engine:** `scripts/evaluate_phase6b.py`
- **Tasks Specified:**
  1. Directional relations (`ABOVE`, `BELOW`, `LEFT_OF`, `RIGHT_OF`)
  2. Door connectivity (Positive / Negative)
  3. Room adjacency
  4. Room and door cardinality
  5. Shortest path reachability
  6. Circulation hub identification
  7. Visual Dependency Index (VDI) across 5 conditions: Original, Black, Masked, Noise, Text-Only
  8. Hallucination rate analysis
  9. Format adherence validation
  10. Blind qualitative evaluation
  11. Deterministic reproducibility (Seed 42)
- **Held-Out Test Set:** `RUN-021-SPATIAL-SUPERVISION/test.jsonl` (1,006 locked instances, zero training exposure).

---

## 13. Visual Dependency Index (VDI) Formal Definition

The Visual Dependency Index (VDI) definition is strictly preserved from `RUN-021-SPATIAL-SUPERVISION/SCIENTIFIC_DESIGN_REPORT.md` (§ "Indicateur de Dépendance Visuelle (VDI)", lines 103–106 & 125):

$$\text{VDI} = \frac{\text{Acc}_{\text{original}}}{\max(\text{Acc}_{\text{black}}, \text{Acc}_{\text{text\_only}})}$$

- **Historical Calibration:** In RUN-019, $\text{VDI} \approx 1.0$ (indicating complete visual blindness / textual shortcut).
- **Official Grounding Threshold:** $\text{VDI} \ge 3.0$ required to demonstrate visual dependency.
- **Provenance:** `RUN-021-SPATIAL-SUPERVISION/SCIENTIFIC_DESIGN_REPORT.md` (unmodified).
