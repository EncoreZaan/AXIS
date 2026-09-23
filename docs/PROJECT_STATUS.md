# AXIS — Authoritative Current Project & Scientific Status

> **Document Version:** 2.0.0  
> **Last Updated:** 2026-09-23  
> **Governing Commit:** `f4d5e949053743d97091ea35080de5d365899df7` (`f4d5e94`)  
> **Scientific Integrity Policy:** Strictly verifiable, falsifiable, and traceable against physical artifacts.

---

## 1. What is AXIS?

**AXIS** (*Architectural eXtensible Intelligence System*) is an open-source, reproducible artificial intelligence research initiative aimed at developing vision-language models capable of genuine architectural reasoning, metric spatial grounding, and multimodal 2D/3D building plan understanding.

AXIS rejects ungrounded generation, narrative hallucinations, and superficial template memorization. Instead, it enforces strict empirical gates, automated counterfactual visual ablations, and cryptographic data provenance across all architectural domains.

---

## 2. What Has Been Completed?

As of 2026-09-23, AXIS has executed and archived six major technical and scientific phases:

1. **Phase 1 — Dataset Architecture & Remediation:**
   - Consolidated the 65,342-asset **Master Dataset v2** across 19 physical sources with zero cross-split leakage.
   - Quarantined `CORE_FLOORPLANCAD` (741 CAD vectors) under **Provenance Decision Record PDR-2026-001** due to upstream Hugging Face licensing contradictions (`CC-BY-SA 4.0` metadata vs `CC-BY-NC 4.0` README text).
   - Sealed **Gold Set V3** (200 certified instances, SHA-256: `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`).
2. **Phase 2 — Remote GPU Characterization (RUN-001 to RUN-014):**
   - Profiled hardware, thermals, and VRAM on an NVIDIA RTX 3090 (24 GB).
   - Validated 4-bit NormalFloat (NF4) mixed-precision QLoRA training dynamics.
   - Conducted LoRA rank ablations ($r=16, \alpha=32$ selected) and image resolution bounds (512px selected; 768px rejected due to +62.5% VRAM surge).
3. **Phase 3 — Real Data Ingestion & Dry Run (RUN-015 to RUN-018):**
   - Ingested 1,000 real architectural assets (`CORE_RPLAN` rasters and `CORE_RESBIM_PAIRED` units) into `REAL_DATA_PILOT`.
   - Executed a zero-step pre-flight dry run verifying lossless collation and gradient flow with zero parameter mutation.
4. **Phase 4 — First Real-Data QLoRA Pilot (RUN-019):**
   - Completed 194 optimizer steps (2 full epochs) on `Qwen/Qwen2-VL-7B-Instruct`.
   - Achieved monotonic loss reduction: training loss dropped from 1.769 to 0.0245, validation loss from 1.644 to 0.0232 (-98.59%).
5. **Phase 5 — Scientific Falsification & Generalization (RUN-020):**
   - Evaluated RUN-019 on unseen holdout test assets and 5-condition counterfactual visual ablations.
   - **Crucial Falsification Finding:** Revealed that the -98.59% loss reduction was a language shortcut. The model memorized a rigid 5-heading text template (85.3% similarity), hallucinated training IDs (100%), and exhibited quasi-null visual dependency ($\text{VDI} \approx 1.0$, producing 92.0% identical critique text when fed an entirely black image).
6. **Phase 6A — Spatial Supervision Dataset Engineering (RUN-021):**
   - Engineered `AXIS_SPATIAL_SUPERVISION_V1` with 1,006 physical assets and 7,950 discrete examples across 5 spatial task families (Directional, Connectivity, Adjacency, Cardinality, Shortest Paths).
   - 100% of tasks enforce strict visual requirement (`VISUAL_REQUIRED`).
   - Verified zero cross-split leakage and completed an automated geometric audit on 50 samples (100% concordance; `MANUAL_AUDIT_HUMAN = NOT_PERFORMED`, `AUTOMATED_GEOMETRIC_AUDIT = PASS`).
7. **Phase 6B — Spatial Grounding Pilot Training (RUN-022):**
   - Completed 2,310 optimizer steps (3 full epochs, batch size 8) on `Qwen2-VL-7B-Instruct`.
   - Handled a mid-training remote SSH disconnection at step 1000 with a clean, verified deterministic resumption from `checkpoint-750`.
   - Reached final train loss 0.1218 and final eval loss 0.1397.
   - Final adapter verified bit-identical to `checkpoint-2310` (SHA-256: `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`).
8. **Phase 6B — Spatial Generalization & Visual Grounding Evaluation (RUN-023):**
   - Benchmarked 1,006 held-out test samples and 100 visual ablation samples.
   - Scientific grounding accuracy jumped to **63.12%** (+48.61 percentage points over Base Model 14.51% and RUN-019 15.81%).
   - Syntax and format adherence reached **100.0%**.
   - Directional reasoning reached **98.40%**; door connectivity reached **94.00%**; shortest path reachability reached **80.00%**.
   - ID hallucinations were **completely eradicated (0.00%)**.
   - Deterministic reproducibility was confirmed bit-exact on 20/20 samples (Seed 42).

---

## 3. What is the Current Scientific State?

AXIS has definitively proven that targeted spatial supervision can overcome catastrophic template memorization and ID hallucination in vision-language models, elevating discrete architectural topological reasoning from 14.51% to 63.12%.

However, under the pre-registered Visual Dependency Index metric, **visual dependency has NOT been established** ($\text{VDI} = 1.28$, below the required $\text{VDI} \ge 3.0$ threshold; `VDI_PASS: NO`). While the model demonstrates strong syntactic mastery and spatial relational competence, the empirical evidence does not yet prove that the model's reasoning is causally dependent on visual image pixels rather than textual coordinate cues.

---

## 4. Full Experiment Inventory

| Run ID | Scope | Dataset | Epochs / Steps | Key Metric | Verdict |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **RUN-001** | Hardware & memory profiling | Synthetic matmuls | N/A | 10,566.8 MiB peak | **PASS** |
| **RUN-002** | 2-epoch training pipeline smoke | Runtime fixture | 2 ep / 6 steps | Eval: 1.9337 | **PASS** |
| **RUN-003** | Operating envelope characterization | Runtime fixture | 5 configs | 18,810.4 MiB max | **PASS** |
| **RUN-004** | 3-epoch trajectory validation | Runtime fixture | 3 ep / 9 steps | Eval: 1.8941 | **PASS** |
| **RUN-005** | Cross-seed numerical stability | Runtime fixture | 2 ep / 6 steps | Seed 123: 1.9333 | **PASS** |
| **RUN-006** | Checkpoint save / reload / resume | Runtime fixture | 3+3 steps | Resumed: 1.9582 | **PASS** |
| **RUN-007** | 8-epoch controlled QLoRA | Runtime fixture | 8 ep / 24 steps | Eval: 1.7271 | **PASS** |
| **RUN-008** | Meta-analysis of runs 001–007 | Telemetry logs | N/A | Synthesis complete | **PASS** |
| **RUN-009** | Census & provenance audit | Runtime fixture | N/A | 1 unique image hash | **PASS** |
| **RUN-010** | LoRA rank ablation ($r=16$ vs $r=8$) | Runtime fixture | 2 ep / 6 steps | $r=16$: Eval 1.8879 | **PASS** |
| **RUN-011** | Learning rate sensitivity ($\eta$) | Runtime fixture | 6+6 steps | $2\times 10^{-4}$: 1.8701 | **PASS** |
| **RUN-012** | Resolution scaling ($768\times 768$) | Runtime fixture | 2 ep / 6 steps | 19,101.3 MiB VRAM | **PASS** (768px rejected) |
| **RUN-013** | Multimodal inference benchmark | Runtime fixture | 3 prompt types | Greedy deterministic | **PASS** |
| **RUN-014** | Cross-adapter checksum registry | 6 adapters | N/A | All SHA256 verified | **PASS** |
| **RUN-015** | Real data readiness audit | Real data assets | N/A | 1,000 assets verified | **PASS** |
| **RUN-016** | Real data dataset audit | RPLAN + ResBIM | N/A | Zero split leakage | **PASS** |
| **RUN-017** | Real data dataset lock | RPLAN + ResBIM | N/A | `hashes.json` sealed | **PASS** |
| **RUN-018** | Pre-training dry run | REAL_DATA_PILOT | 0 opt steps | Zero weight drift | **PASS** |
| **RUN-019** | First real-data QLoRA pilot | REAL_DATA_PILOT | 2 ep / 194 steps | Eval loss: 0.0232 | **PASS** |
| **RUN-020** | Scientific falsification benchmark | Held-out test set | 127 samples | $\text{VDI} \approx 1.0$, 85.3% template | **FALSIFIED** |
| **RUN-021** | Spatial supervision dataset lock | Spatial Supervision | 7,950 examples | Config SHA: `9c0908c4...` | **PASS** |
| **RUN-022** | Spatial grounding training pilot | Spatial Supervision | 3 ep / 2,310 steps | Train: 0.1218, Eval: 0.1397 | **PASS** |
| **RUN-023** | Spatial grounding scientific eval | Held-out test set | 1,006 samples | Acc: 63.12%, VDI: 1.28 | **COMPLETE / VDI FAIL** |

---

## 5. What Has Been Proven?

1. **Eradication of Structural Hallucinations:** Training ID reuse and fabricated entity names were reduced from 100.0% in RUN-019 to **0.00%** in RUN-022/RUN-023.
2. **Absolute Format Discipline:** Format adherence on structured spatial queries reached **100.00%** (up from 65.61% Base and 56.06% RUN-019).
3. **Discrete Spatial Reasoning Competence:**
   - Directional relative reasoning (`ABOVE`, `BELOW`, `LEFT_OF`, `RIGHT_OF`): **98.40%** (vs 3.20% Base).
   - Door connectivity identification: **94.00%** (Positive: 92.80%, Negative: 95.20%).
   - Room and door cardinality: **69.20%** (Rooms: 67.20%, Doors: 71.20%).
   - Multi-hop path reachability through doors: **80.00%** (vs 0.00% Base).
4. **Substantial Overall Grounding Gain:** Scientific grounding accuracy improved by **+48.61 percentage points** (14.51% $\to$ 63.12%).
5. **Exact Numeric Determinism:** 20/20 bit-exact output reproduction under Seed 42 with bfloat16 NF4 quantization.

---

## 6. What Has NOT Been Proven?

1. **Visual Dependency Has NOT Been Proven:** Under the official VDI formulation ($\text{Acc}_{\text{original}} / \max(\text{Acc}_{\text{black}}, \text{Acc}_{\text{text\_only}})$), RUN-022 achieved **1.28**, failing the pre-registered threshold ($\text{VDI} \ge 3.0$).
2. **Causal Visual Grounding Has NOT Been Proven:** The current evidence does not demonstrate that the model looks at floorplan pixels rather than deducing answers from coordinate information embedded in text prompts.
3. **General Architectural Autonomy Has NOT Been Proven:** AXIS cannot produce complete building layouts, validate structural code compliance, or replace professional architectural design.
4. **Circulation Hub Identification Is Unproven:** The evaluation scored 0.00% on circulation hubs due to strict integer bounding-box equality metric sensitivity.
5. **Human Annotation Has NOT Been Performed:** `HUMAN_BLIND_EVALUATION = NOT_PERFORMED`. No human expert evaluation has taken place.

---

## 7. What Datasets Are Locked?

| Dataset Identifier | Physical Path | Total Assets / Records | SHA-256 Checksum / Manifest | Status |
| :--- | :--- | :---: | :--- | :---: |
| **Master Dataset v2** | `dataset/` (maintainer store) | 65,342 assets | Partitioned by `project_group_id` | **IMMUTABLE** |
| **Gold Set V3** | `evaluation/gold_set_v3.jsonl` | 200 items | `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca` | **SANCTUARY** |
| **REAL_DATA_PILOT (RUN-017)** | `experiments/runpod_2026-09-22/REAL_DATA_PILOT/` | 1,000 assets | `1d07982755f61200614039912b498c2df5e29f8701599e3ef8da605a55f18996` | **LOCKED** |
| **SPATIAL_SUPERVISION_V1 (RUN-021)** | `RUN-021-SPATIAL-SUPERVISION/` | 7,950 examples | `9c0908c4c2bc25c647cfde7d885e4d8fe9ba507fb00fb79ce42852942ea60d6c` | **LOCKED** |

---

## 8. What Checkpoints Are Locked?

| Checkpoint Name | Run Identifier | Parameter Size | File Size | `adapter_model.safetensors` SHA-256 |
| :--- | :--- | :---: | :---: | :--- |
| **RUN-019 Final Adapter** | `RUN-019-FIRST-REAL-DATA-QLORA` | LoRA $r=16, \alpha=32$ | 161.5 MB | `246e22b372180a6b4be6c61eeea77e10a2c2d35b7128503463d32d6185ec3c47` |
| **RUN-022 Checkpoint-2310** | `RUN-022-SPATIAL-GROUNDING-PILOT` | LoRA $r=16, \alpha=32$ | 161.5 MB | `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479` |
| **RUN-022 Final Adapter** | `RUN-022-SPATIAL-GROUNDING-PILOT` | LoRA $r=16, \alpha=32$ | 161.5 MB | `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479` |

`RUN-022/checkpoint-2310` and `RUN-022/final_adapter` are cryptographically certified bit-identical.

---

## 9. Current Methodological & Empirical Limitations

1. **Confounding Textual Cues in VDI:** Directional task prompts provide Cartesian coordinates in the text string (e.g., `subject_center: [x, y]`, `object_center: [x, y]`), allowing language-only reasoning to deduce `ABOVE`/`BELOW`/`LEFT_OF`/`RIGHT_OF` without parsing the image.
2. **Binary Choice Accuracy Floor:** Connectivity and directional queries with binary choices provide a 50% chance baseline under random guessing or blind majority voting, compressing the achievable VDI ratio.
3. **Strict Integer Bounding-Box Sensitivity:** Circulation hub evaluation demanded exact 4-tuple integer pixel match (`[ymin, xmin, ymax, xmax]`), scoring 0.00% even when the predicted room was structurally correct but varied by sub-pixel rounding.
4. **Quarantine of CAD Vectors:** `CORE_FLOORPLANCAD` remains quarantined and excluded from training due to licensing ambiguity (`PDR-2026-001`).
5. **Absence of Blind Human Review:** The qualitative side-by-side benchmark was compiled automatically (`HUMAN_BLIND_EVALUATION = NOT_PERFORMED`).

---

## 10. Which Experiments Must NOT Be Rerun?

Under the non-regression and immutability invariants:
- **DO NOT rerun RUN-019:** Historical proof of language prior memorization.
- **DO NOT rerun RUN-020:** Historical falsification benchmark.
- **DO NOT rerun RUN-021:** Frozen spatial supervision dataset.
- **DO NOT rerun RUN-022:** Completed and locked training pilot.
- **DO NOT rerun RUN-023:** Completed and locked evaluation benchmark.

---

## 11. What is the Next Authorized Step?

> [!CAUTION]
> **Operational Invariant:** `TRAINING_ALLOWED: NO` | `NEW_EXPERIMENT_ALLOWED: NO`

**The next authorized step is:**
1. Await explicit human validation and steering review of the RUN-023 findings.
2. Formulate Phase 7 experimental protocol:
   - Redesign visual ablation queries to strip spatial coordinate prompts from text (decoupling language from image).
   - Implement Intersection-over-Union (IoU $\ge 0.50$) tolerance for bounding-box room predictions.
   - Design a genuine blind human evaluation protocol with qualified architects.
