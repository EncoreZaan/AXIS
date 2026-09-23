# AXIS — Chronological Scientific & Experimental Timeline

> **Timeline Scope:** Phase 1 through Phase 6B (2026-09-21 to 2026-09-23)  
> **Last Synchronized:** 2026-09-23T17:45:00Z  
> **Integrity Guarantee:** All entries are backed by verifiable on-disk artifacts, cryptographic checksums, and execution logs.

---

## Chronological Overview

| Timestamp (UTC) | Milestone / Run ID | Phase | Primary Objective | Key Scientific Finding / Result | Status | Canonical Artifacts |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **2026-09-21 / 22** | **Pre-Training Audit & Remediation** | Phase 1 | Audit dataset corpus, resolve IP contradictions, isolate gold benchmarks | Master Dataset v2 consolidated (65,342 assets). FloorPlanCAD quarantined (`PDR-2026-001`). Gold Set V3 locked. | **PASS** | [`DATASET.md`](../DATASET.md), [`PDR-2026-001`](datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md) |
| **2026-09-22 21:38** | **Environment Readiness** | Infra | Validate remote GPU instance (`territorial_green_minnow`, RTX 3090) | PyTorch 2.6.0+cu124, CUDA 12.4, driver 580.159.04, 24GB VRAM verified. Baseline commit `f4d5e94`. | **PASS** | [`RUNPOD_ENVIRONMENT_READINESS.md`](../RUNPOD_ENVIRONMENT_READINESS.md) |
| **2026-09-22 21:50** | **RUN-001 to RUN-007** | Phase 2A | Single-session hardware stability, profiling, loss monotonicity, and reload | Thermal peak 58°C (<80°C), 4-bit NF4 memory confirmed (~10.5 GB), loss monotonic (1.958 $\to$ 1.727). | **PASS** | [`RUNPOD_EXPERIMENTAL_CAMPAIGN_REPORT.md`](../RUNPOD_EXPERIMENTAL_CAMPAIGN_REPORT.md) |
| **2026-09-22 22:20** | **RUN-008 to RUN-014** | Phase 2B | LoRA rank ablation, learning rate sensitivity, resolution scaling, inference profiling | Rank $r=16$ selected (faster descent, +1.7% VRAM). 768px causes +62.5% VRAM surge. Multi-adapter checksums verified. | **PASS** | [`RUNPOD_PHASE2_CAMPAIGN_REPORT.md`](../RUNPOD_PHASE2_CAMPAIGN_REPORT.md) |
| **2026-09-22 22:45** | **RUN-015 to RUN-018** | Phase 3 | Ingestion, auditing, locking, and dry-run of real multi-image dataset (`REAL_DATA_PILOT`) | 1,000 assets (990 RPLAN, 10 RESBIM paired). Train: 775, Val: 98, Test: 127. Zero leakage. Dry-run loss finite, zero weight drift. | **PASS** | [`RUN-015`](../RUN-015-REAL_DATA_READINESS/), [`RUN-016`](../RUN-016-REAL_DATA_AUDIT/), [`RUN-017`](../RUN-017-DATASET_LOCK/), [`RUN-018`](../RUN-018-REAL_DATA_DRY_RUN/) |
| **2026-09-23 01:40** | **RUN-019-FIRST-REAL-DATA-QLORA** | Phase 4 | First real-data QLoRA training on 1,000 architectural assets | 2 epochs (194 steps). Train loss: 0.0245, Eval loss: 0.0232 (-98.59% drop). Zero OOM, zero NaN. | **PASS** | [`RUN-019`](../RUN-019-FIRST-REAL-DATA-QLORA/TRAINING_REPORT.md), [`docs/RUN-019`](experiments/RUN-019/README.md) |
| **2026-09-23 03:02** | **RUN-020-SCIENTIFIC-GENERALIZATION** | Phase 5 | Scientific generalization & falsification evaluation of RUN-019 | Falsification revealed: 85.3% template reproduction, 100% ID hallucination, quasi-null visual dependency ($\text{VDI} \approx 1.0$). | **FALSIFIED** | [`RUN-020`](../RUN-020-SCIENTIFIC-GENERALIZATION/SCIENTIFIC_ANALYSIS.md), [`docs/RUN-020`](experiments/RUN-020/README.md) |
| **2026-09-23 03:50** | **Phase 6A / RUN-021-SPATIAL-SUPERVISION** | Phase 6A | Design, validation, and cryptographic lock of spatial supervision dataset | 1,000 assets, 7,950 examples (Train: 6,160, Val: 784, Test: 1,006). 100% VISUAL_REQUIRED tasks. Zero leakage. Automated geometric audit PASS. | **PASS** | [`RUN-021`](../RUN-021-SPATIAL-SUPERVISION/FINAL_GATE.md), [`docs/RUN-021`](experiments/RUN-021/README.md) |
| **2026-09-23 05:50** | **RUN-022 Pilot Launch & Interruption** | Phase 6B | Full-scale training pilot on Qwen2-VL-7B (2,310 steps, 3 epochs) | Process abruptly interrupted at step 1000 due to SSH disconnect. Forensics: GPU idle, zero OOM, no weight corruption. | **INTERRUPTED** | [`RUN-022`](../RUN-022-SPATIAL-GROUNDING-PILOT/TRAINING_REPORT.md) |
| **2026-09-23 08:45** | **RUN-022 Resumption** | Phase 6B | Resumption from last intact physical checkpoint (`checkpoint-750`) | Deterministic resumption confirmed: step 1000 loss pre: 0.1632, post: 0.1639; grad norm pre: 0.2412, post: 0.2405. | **RESUMED** | [`RUN-022`](../RUN-022-SPATIAL-GROUNDING-PILOT/training_resume.log) |
| **2026-09-23 12:46** | **RUN-022 Training Completion** | Phase 6B | Completion of 2,310 optimizer steps and final adapter export | Step 2310/2310 reached. Final train loss: 0.1218, eval loss: 0.1397. Adapter bit-identical to `checkpoint-2310`. | **PASS** | [`RUN-022`](../RUN-022-SPATIAL-GROUNDING-PILOT/TRAINING_REPORT.md), [`docs/RUN-022`](experiments/RUN-022/README.md) |
| **2026-09-23 13:00** | **RUN-022 Post-Training Gate** | Phase 6B | Verification of checkpoint integrity and protocol readiness | Sanctuaries verified intact. Caveat enforced: training loss does not prove visual grounding. RUN-023 protocol locked. | **PASS** | [`RUN-022 Gate`](../RUN-022-SPATIAL-GROUNDING-PILOT/POST_TRAINING_GATE.md) |
| **2026-09-23 13:08** | **RUN-023 Pre-Audit & Smoke Test** | Phase 6B | Cryptographic verification of test split and model/adapter loading | Test set locked (1,006 examples, zero leakage). Adapter loaded cleanly (392 LoRA tensors, zero parameter drift). | **PASS** | [`RUN-023 Pre-Audit`](../RUN-023-SPATIAL-GENERALIZATION-EVAL/PRE_AUDIT.md), [`Smoke Test`](../RUN-023-SPATIAL-GENERALIZATION-EVAL/SMOKE_TEST.md) |
| **2026-09-23 15:39** | **RUN-023 Spatial Grounding Evaluation** | Phase 6B | Benchmark on 1,006 test samples and 100-sample 5-condition visual ablation | Spatial grounding accuracy 63.12% (+48.61 pp vs base), format 100%, 0% hallucination. BUT VDI = 1.28 < 3.0 threshold. | **COMPLETE** | [`RUN-023 Report`](../RUN-023-SPATIAL-GENERALIZATION-EVAL/EVALUATION_REPORT.md), [`docs/RUN-023`](experiments/RUN-023/README.md) |
| **2026-09-23 17:45** | **Archival Synchronization Freeze** | Meta | Complete synchronization of all experimental documentation and code | Full audit trail committed to Git. Sanctuaries verified. Awaiting human review before Phase 7. | **FROZEN** | [`PROJECT_STATUS.md`](PROJECT_STATUS.md), [`GATES_AND_DECISIONS.md`](GATES_AND_DECISIONS.md) |

---

## Detailed Milestone Narratives

### 1. Phase 1 — Pre-Training Remediation & Sanctuarization (2026-09-21 to 2026-09-22)
- **Problem:** Historical AXIS codebase contained contradictory dataset claims, unverified pairwise 2D/3D assertions, and an upstream licensing conflict in `CORE_FLOORPLANCAD` (HuggingFace declared CC-BY-SA 4.0 while README text and ICCV 2021 publication declared CC-BY-NC 4.0).
- **Remediation:**
  - Formally established Provenance Decision Record `PDR-2026-001` isolating FloorPlanCAD into strict quarantine (`LEGAL_REVIEW_REQUIRED`).
  - Master Dataset v2 formally frozen at 65,342 physical assets with verified zero cross-split leakage.
  - Gold Set V3 locked and cryptographically sealed (SHA-256: `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`).
  - Baseline Git commit fixed at `f4d5e949053743d97091ea35080de5d365899df7`.

### 2. Phase 2 — RunPod Pilot Campaigns (2026-09-22)
- **Campaign 1 (RUN-001 to RUN-007):** Evaluated hardware stability, thermal margin, and base 4-bit NF4 footprint on an NVIDIA RTX 3090. Established that microbatch 1 with gradient accumulation 8 operates comfortably within 10.5 GB VRAM (57% headroom). Validated loss monotonicity across 8 epochs (1.958 $\to$ 1.727).
- **Campaign 2 (RUN-008 to RUN-014):** Conducted parameter sensitivity benchmarks. LoRA rank ablation demonstrated that doubling rank ($r=8 \to r=16$) yielded substantially faster convergence with only +1.7% VRAM overhead. Resolution scaling to 768px incurred a prohibitive +62.5% VRAM penalty and was rejected in favor of 512px (`max_pixels: 262144`).

### 3. Phase 3 — Real Data Ingestion & Audit (2026-09-22)
- **RUN-015 to RUN-018:** Formed the `REAL_DATA_PILOT` corpus containing 1,000 real architectural plans (990 RPLAN rasters, 10 paired ResBIM units).
- Partitioned into Train (775), Validation (98), and Test (127) with zero cross-split project or image overlap.
- Zero-step dry-run verified forward collation and gradient backpropagation with zero parameter drift.

### 4. Phase 4 — First Real-Data QLoRA Training (2026-09-23 01:40 UTC)
- **RUN-019:** Trained `Qwen/Qwen2-VL-7B-Instruct` for 194 optimizer steps (2 epochs) on `REAL_DATA_PILOT`.
- Observed training loss drop from 1.769 to 0.0245, and validation loss drop from 1.644 to 0.0232 (-98.59%).
- All optimizer operations completed cleanly without OOM or NaN.

### 5. Phase 5 — Scientific Falsification of RUN-019 (2026-09-23 03:02 UTC)
- **RUN-020:** Conducted rigorous holdout evaluation and counterfactual visual ablation on the trained RUN-019 checkpoint.
- **Falsification Findings:**
  1. The -98.59% loss reduction was a linguistic artifact: the model had memorized a deterministic 5-section critique template (85.3% text template similarity).
  2. 100% of generated responses hallucinated numerical asset IDs copied from the training split.
  3. Visual ablation demonstrated that feeding a 100% black image yielded 92.0% response similarity, and text-only prompting yielded 95.7% response similarity.
  4. Visual Dependency Index was $\text{VDI} \approx 1.0$, proving that RUN-019 suffered from complete visual blindness and zero visual grounding.

### 6. Phase 6A — Spatial Supervision Dataset Engineering (2026-09-23 03:50 UTC)
- **RUN-021:** Created `AXIS_SPATIAL_SUPERVISION_V1` specifically engineered to eliminate template shortcuts and demand genuine visual conditioning.
- 1,006 physical assets transformed into 7,950 discrete spatial reasoning instances across 5 core families:
  1. Directional relations (`ABOVE`, `BELOW`, `LEFT_OF`, `RIGHT_OF`)
  2. Door connectivity (positive and negative)
  3. Room and door cardinality
  4. Multi-hop reachability / shortest paths
  5. Circulation hub and largest room identification
- Partitioned into 6,160 train, 784 validation, and 1,006 test samples with zero project, asset, or image hash leakage.
- Automated geometric audit of 50 samples verified 100% ground-truth concordance (clarified: `MANUAL_AUDIT_HUMAN = NOT_PERFORMED`, `AUTOMATED_GEOMETRIC_AUDIT = PASS`).
- Dataset cryptographically locked (`dataset_config.json` SHA-256: `9c0908c4c2bc25c647cfde7d885e4d8fe9ba507fb00fb79ce42852942ea60d6c`).

### 7. Phase 6B — Spatial Grounding Pilot Training (2026-09-23 04:00 to 12:46 UTC)
- **RUN-022:** Fine-tuned `Qwen/Qwen2-VL-7B-Instruct` on `AXIS_SPATIAL_SUPERVISION_V1` (LoRA $r=16, \alpha=32$, 512px, lr $1.0\times 10^{-4}$, 3 epochs, 2,310 optimizer steps).
- **Interruption Event:** At step 1000, remote SSH dropped during monitoring. Process inspection revealed zero running processes, GPU idle (4 MiB memory), zero OOM, and no OS freeze. `checkpoint-1000` had not been serialized.
- **Resumption:** Cleanly resumed from `checkpoint-750`. Step 1000 telemetry pre- and post-resumption matched within numerical tolerances (Train loss: 0.1632 vs 0.1639; Grad norm: 0.2412 vs 0.2405).
- **Completion:** All 2,310 steps completed. Final train loss: 0.1218, final eval loss: 0.1397.
- **Adapter Integrity:** `checkpoint-2310/adapter_model.safetensors` and `final_adapter/adapter_model.safetensors` confirmed bit-identical (SHA-256: `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`).
- **Post-Training Gate:** Formally certified training completion while enforcing the strict boundary: *Loss convergence does NOT demonstrate spatial grounding or visual dependency.*

### 8. Phase 6B — Comprehensive Spatial Evaluation (2026-09-23 13:00 to 15:40 UTC)
- **RUN-023:** Conducted the definitive empirical evaluation across 1,006 held-out test samples and 100 visual ablation samples.
- **Results:**
  - Overall scientific grounding accuracy rose from 14.51% (Base Model) and 15.81% (RUN-019) to **63.12%** (+48.61 percentage points).
  - Format adherence reached **100.0%**.
  - Directional reasoning: **98.40%**.
  - Door connectivity: **94.00%** (Positive: 92.80%, Negative: 95.20%).
  - Room/Door cardinality: **69.20%**.
  - Multi-hop shortest paths: **80.00%**.
  - ID hallucination rate: **0.00%** (eradicated).
  - Reproducibility: **20/20 bit-exact** concordance under Seed 42.
- **Methodological Limitations Revealed:**
  1. **Circulation Hub (0.00%):** Caused by strict integer bounding box equality evaluation metric sensitivity. Sub-pixel and rounding differences caused false fails despite valid door count distributions.
  2. **Visual Dependency Index ($\text{VDI} = 1.28 < 3.0$ threshold, VDI_PASS = NO):** Binary yes/no questions set a 50% accuracy floor. Text prompts containing bounding box coordinates allowed linguistic/numerical inference without visual parsing.
  3. **Qualitative Blind Evaluation:** Compiled programmatically (`HUMAN_BLIND_EVALUATION = NOT_PERFORMED`).

---

## Current Scientific State & Authorized Next Step

- **Current State:** AXIS has successfully established strong format discipline (100%), eliminated ID hallucination (0.0%), and demonstrated high accuracy on discrete architectural topological questions (63.12%). However, under the strict official VDI standard ($\text{VDI} \ge 3.0$), **visual dependency has NOT been proven**, and the model cannot yet be claimed to possess genuine visual grounding.
- **Authorized Next Step:** Await explicit human validation before commencing Phase 7. Refactor the visual ablation protocol to remove coordinate leakage from textual prompts and implement bounding-box IoU tolerance for spatial hubs.
