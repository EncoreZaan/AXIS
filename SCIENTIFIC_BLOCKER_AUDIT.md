# AXIS — Scientific Blocker Resolution Audit (`SCIENTIFIC_BLOCKER_AUDIT.md`)

> **Audit Type:** Independent Scientific Readiness & Blocker Resolution Audit  
> **Audited Baseline:** Git commit `f4d5e94` (`main`)  
> **Target Scope:** Independent evaluation of the two documented scientific blockers:  
> 1. OpenBIM pair scarcity  
> 2. ResPlan metric scale distortion  
> **Audit Date:** 2026-09-22  
> **Auditor Posture:** Red-team forensic audit, strict mathematical and empirical evidence verification  
> **Operational Status:** `TRAINING_ALLOWED: NO` strictly preserved  

---

## 1. Executive Summary

This independent scientific audit was conducted on the AXIS codebase at baseline commit `f4d5e94` (`main`). Following the successful remediation of provenance and legal blockers (`PROVENANCE_REVIEW: PASS`, `OPEN_P3: 0`), two documented scientific blockers remained on the Pre-Training Gate:
1. **OpenBIM pair scarcity** (documented as Scientific P0);
2. **ResPlan metric scale distortion** (documented as Scientific P1).

The objective of this audit was to determine definitively whether either of these two issues actually invalidates, corrupts, or blocks the **FIRST AXIS TRAINING RUN**, and to establish the minimum scientifically valid remediation required.

### Key Audit Findings:

1. **First Training Run Dependency on OpenBIM:** **`FIRST_TRAINING_REQUIRES_OPENBIM = NO`**.  
   The planned first training run (the controlled Phase 4 `SpatialRelationMLP` baseline on Dataset A, as well as the VLM QLoRA micro-experiment in `experiment_package/`) does **not** ingest, train on, or evaluate OpenBIM IFC models. Dataset A is derived exclusively from `CORE_RPLAN` (2D raster floorplans) and `CORE_IL3D` (3D Cartesian furniture layouts). The VLM micro-experiment operates exclusively on photographic images and qualitative text. OpenBIM pair scarcity (10 true pairs in RAW) represents a critical data bottleneck for future generalist 2D $\leftrightarrow$ 3D multimodal pre-training (Phase 5), but does not prevent the first unimodal training run.

2. **First Training Run Dependency on ResPlan:** **`FIRST_TRAINING_REQUIRES_RESPLAN = NO`**.  
   `CORE_RESPLAN` (17,000 vector floorplans in `ResPlan.pkl`) is **not** present in Dataset A (`train.jsonl`, `validation.jsonl`, `test.jsonl`), is not present in Gold Set V3, is not present in `experiment_package/`, and was not used to train checkpoint `ARCHI-AI-P4-005`. It is formally quarantined in `configs/training_corpus_cleared.json` and excluded from all metric tasks.

3. **Integrity of Historical Results:**  
   The baseline validation MAE of **`0.0481 m`** and Gold Set V3 evaluation MAE of **`0.0517 m`** achieved by checkpoint `ARCHI-AI-P4-005` were computed exclusively on `CORE_IL3D` authentic metric coordinates. They are **100% unaffected** by the ResPlan scale distortion. Zero historical benchmark scores, checkpoints, or splits are corrupted.

4. **Scientific Gate Verdict:**  
   Because neither blocker is exercised by, required for, or capable of corrupting the first planned training configuration, both blockers are scientifically classified as **`NON_BLOCKING`** for the First Training Run (with OpenBIM pair scarcity tracked as **`FUTURE_WORK`** for multimodal scaling).  
   Consequently, **`SCIENTIFIC_GATE: PASS`**.

5. **Operational Gate Invariant:**  
   Per absolute audit protocol, despite `SCIENTIFIC_GATE: PASS`, the project operational authorization remains strictly:  
   **`TRAINING_ALLOWED: NO`**  
   **`TRAINING_MAY_BEGIN: NO`**  
   pending formal final authorization.

---

## 2. Original Blocker Definitions

An exhaustive review of the repository's research and evaluation literature (`docs/research/SCIENTIFIC_READINESS_REPORT.md`, `docs/datasets/RESPLAN_CALIBRATION_REPORT.md`, `docs/research/PRE_TRAINING_GATE.md`, `docs/evaluation/INDEPENDENT_AUDIT_REPORT.md`, `DATASET.md`, and `FINAL_PRE_TRAINING_GATE_REVIEW.md`) identified the exact original definitions of the two blockers:

### Blocker 1: OpenBIM Pair Scarcity
* **Original Finding:** In Phase 2 (`INDEPENDENT_AUDIT_REPORT.md`), Red Team audit flagged "Fake Multimodal" (21.2%) and missing plan inputs. In Phase 3 (`SCIENTIFIC_READINESS_REPORT.md` §1.1 & §2.1), exhaustive 4-level pairing detection across 66,847 RAW files proved that zero hidden 2D floorplan $\leftrightarrow$ 3D BIM pairs exist. The corpus contains only 10 genuine architect floorplan $\leftrightarrow$ 3D IFC models (`CORE_RESBIM_PAIRED`). Cross-dataset pairing between RPLAN and IL3D was rejected as ungrounded hallucination violating Rule 10 ("Never invent a correspondence").
* **Source Documents:** `docs/research/SCIENTIFIC_READINESS_REPORT.md` §1.1, §2.1, §4; `docs/datasets/CORPUS_GAP_REPORT.md` (GAP 1); `docs/datasets/CORPUS_ACQUISITION_REQUIREMENTS.md` (ACQUISITION-REQ-01); `FINAL_PRE_TRAINING_GATE_REVIEW.md` §14 (Blocker 1).
* **Affected Dataset/Source:** `CORE_RESBIM_PAIRED` (10 units), `CORE_IFC_BENCH` (20 projects with 2D perspective snapshots, not plans).
* **Affected Tasks:** Multimodal 2D $\leftrightarrow$ 3D grounding: `BIM_PLUS_PLAN` (Task #68), `PLAN_PLUS_3D` (Task #65), `DOOR_WINDOW_ALIGNMENT_2D_3D`.
* **Affected Metric:** Cross-modal grounding accuracy, 2D/3D spatial alignment generalization.
* **Severity:** Scientific P0 for *generalist multimodal 2D/3D pre-training*.
* **Why Considered a Blocker:** Training a deep vision-language model on only 8 training units from a single residential apartment typology would lead to catastrophic overfitting / memorization rather than generalizable architectural reasoning.
* **Scope (Training vs Evaluation):** Concerns **TRAINING** of generalist multimodal 2D $\leftrightarrow$ 3D architectures. Does not concern unimodal training or photographic VLM critique.

### Blocker 2: ResPlan Metric Scale Distortion
* **Original Finding:** Phase 2 flagged that raw pixel coordinates (e.g. 18,806 px²) were labeled as $\text{m}^2$ on 38.5% of early vector floorplan samples. Phase 3 forensic analysis (`RESPLAN_CALIBRATION_REPORT.md`) audited all 17,000 vector floorplans in `core/resplan/extracted/ResPlan.pkl` and proved that every plan had been independently normalized to a maximum dimension of 256.0 on an arbitrary canvas, destroying physical scale. Additionally, 32.1% (5,458 plans) had `net_area == 0.0`, 4.1% had extreme anomalies, and the ratio of canvas area to reported listing area had a standard deviation of 173.24. All 4 candidate calibration methods failed.
* **Source Documents:** `docs/datasets/RESPLAN_CALIBRATION_REPORT.md`; `docs/datasets/RESPLAN_SAFE_CAPABILITIES.md`; `dataset_tools/resplan/resplan_forensic_auditor.py`; `SCIENTIFIC_READINESS_REPORT.md` §1.2; `FINAL_PRE_TRAINING_GATE_REVIEW.md` §14 (Blocker 2).
* **Affected Dataset/Source:** `CORE_RESPLAN` (`ResPlan.pkl`, 17,000 vector plans).
* **Affected Tasks:** Physical metric prediction: `PLAN_SUMMARY` (Task #15), $\text{m}^2$ area estimation, wall length / opening width regression in meters.
* **Affected Metric:** Metric area MAE ($\text{m}^2$), linear dimension MAE ($\text{m}$).
* **Severity:** Scientific P1 for metric supervision.
* **Why Considered a Blocker:** Training on arbitrary canvas coordinates labeled as real square meters would induce severe physical scale hallucinations in the model.
* **Scope (Training vs Evaluation):** Concerns **TRAINING** on metric tasks using ResPlan. Does not affect scale-invariant topological tasks (room inventory, graph connectivity). Does not affect evaluation benchmarks (Gold Set V3 contains 0 ResPlan instances).

---

## 3. OpenBIM Evidence

The repository evidence regarding OpenBIM was audited across `dataset_tools/pairing/pairing_detector.py`, `DATASET.md`, `tests/test_phase3_scientific_readiness.py`, and the RAW corpus manifests:

### Asset Breakdown in Repository Evidence:

| Asset Category | Source Dataset | Count | Status | Notes |
| :--- | :--- | :---: | :---: | :--- |
| **BIM-only models** | `CORE_BUILDINGSMART_IFC` | 72 | Active | Standard buildingSMART IFC models for schema validation |
| **BIM-only models** | `CORE_IFC_BENCH` | 345 | Active | IFC2x3 / IFC4 architectural models |
| **Image-only floorplans** | `CORE_RPLAN` | 30,002 | Active | 256×256 raster floorplans (no BIM) |
| **Image-only photos** | `experiment_package/dataset/images` | 25 | Active | High-res architectural photos (no BIM) |
| **Snapshot + BIM pairs** | `CORE_IFC_BENCH` | 20 | Certified | Axonometric/perspective 3D renders paired with IFC models (not 2D floorplans) |
| **RGB-D frames** | `CORE_STRUCTSCAN3D` | 2,592 | Certified | Subjective robotic RGB + Depth frames |
| **True 2D Plan $\leftrightarrow$ 3D BIM pairs** | `CORE_RESBIM_PAIRED` | **10** | Certified | Exact stem match (`unit_001` to `unit_010`), paired .jpg plan + .ifc model |
| **Cross-dataset arbitrary candidates** | RPLAN $\leftrightarrow$ IL3D, ResPlan $\leftrightarrow$ IFC | 3 | **REJECTED** | Arbitrary matching strictly rejected by Rule 10 |

### Summary of Certified Multimodal Pairs:
- **Total true 2D floorplan $\leftrightarrow$ 3D BIM pairs available:** **10 pairs** (`CORE_RESBIM_PAIRED`).
- **Valid multimodal training pairs:** At an 80/10/10 split, exactly **8 training pairs** and **2 test/val pairs**.
- **New floorplan-BIM pairs discovered in RAW:** **0**.

The empirical evidence confirms that the existing paired corpus is strictly limited to 10 residential units.

---

## 4. OpenBIM Training Dependency

A systematic code trace was conducted through the first planned training pipelines:

### 1. Investigation of `experiment_package/config/qlora_experiment.yaml` and `train_qlora.py`:
- Target Architecture: `Qwen/Qwen2-VL-7B-Instruct` with 4-bit NF4 QLoRA.
- Dataset files: `dataset/train.jsonl` (20 examples), `dataset/validation.jsonl` (5 examples).
- Image directory: `dataset/images/` (25 architectural photographs).
- Dataset class: `ARCHIVisionDataset` (ingests 2D RGB photographic images + text prompts).
- Target tasks: Structured 5-part architectural studio critique (`OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`).
- Tokenizer / Collator: Processes standard image tokens (`<|vision_start|>...<|vision_end|>`) and language tokens.
- **OpenBIM dependency in `experiment_package`:** **NONE (0 IFC files, 0 BIM pairs).**

### 2. Investigation of Phase 4 Micro-Pilot (`dataset_tools/experiments/micro_pilot/`):
- Target Architecture: `SpatialRelationMLP` (3-layer MLP, 6 inputs: $p_a [x,y,z], p_b [x,y,z]$).
- Dataset: `Dataset A` (Small: 800, Medium: 2,400, Full: 6,000).
- Source datasets: Formally drawn from `CORE_RPLAN` and `CORE_IL3D` only (`EVALUATION.md` §1 line 23).
- Evaluated task: `OBJECT_RELATION` (continuous 3D Euclidean distance regression).
- **OpenBIM dependency in Dataset A:** **NONE (0 IFC files, 0 BIM pairs).**

### 3. Investigation of `configs/training_corpus_cleared.json`:
- `CORE_IFC_BENCH` and `CORE_BUILDINGSMART_IFC` are cleared for schema validation and axonometrics.
- `CORE_RESBIM_PAIRED` is cleared for multimodal pairing, but is **not** included in Dataset A or the micro-experiment.

### Formal Determination:
```text
FIRST_TRAINING_REQUIRES_OPENBIM = NO
```

### Scientific Rationale:
Neither candidate configuration for the first AXIS training run requires OpenBIM pairs. The models under test learn either unimodal 3D spatial geometry regression (`SpatialRelationMLP` on `CORE_IL3D`) or 2D image-to-text qualitative critique (`Qwen2-VL-7B` on architectural photos). OpenBIM pair scarcity is completely orthogonal to these training pipelines.

---

## 5. OpenBIM Scientific Impact

An audit of task definitions across the 69 supervision tasks demonstrates how capabilities map to data sources:

| Architectural AI Capability | Dependent Modality | Required Source | Impact of OpenBIM Scarcity |
| :--- | :--- | :--- | :--- |
| **3D Metric Spatial Relations** | 3D coordinates $(x, y, z)$ | `CORE_IL3D` | **Zero impact** (fully supported by 27,820 IL3D scenes) |
| **2D Plan Topology & Room Reading** | 2D raster floorplans | `CORE_RPLAN` | **Zero impact** (fully supported by 30,002 RPLAN plans) |
| **Ergonomic Clearance Compliance** | 3D bounding boxes + standards | `CORE_IL3D` + `CORE_NORMES_FR` | **Zero impact** (fully verified on Gold Set V3) |
| **Architectural Visual Critique** | 2D photographs | Photographic corpus | **Zero impact** (exercised in VLM micro-experiment) |
| **IFC Schema QA & Entities** | IFC4 STEP schema text | `CORE_IFC_BENCH` (345) + `CORE_BUILDINGSMART_IFC` (72) | **Supported unimodally** (1,026 QA pairs on 21 real projects) |
| **BIM $\leftrightarrow$ Image Grounding** | IFC model + 2D snapshot | `CORE_IFC_BENCH` (20 pairs) | Supported for perspective snapshots, limited diversity |
| **Multimodal 2D Plan $\leftrightarrow$ 3D BIM Co-Reasoning** | Paired 2D CAD/plan + 3D IFC | `CORE_RESBIM_PAIRED` (10 pairs) | **BLOCKED for generalist training** (10 pairs insufficient) |

### Separation of Concerns:
- **First Training Run:** **NOT BLOCKED.** The first run exercises only capabilities with 100% verified, abundant data (3D Euclidean relations or qualitative VLM critique).
- **Future Generalist Multimodal Model (Phase 5):** **BLOCKED on data acquisition.** Full cross-modal pre-training linking 2D architectural drafting conventions to 3D IFC parametric elements requires the planned acquisition of 50–100 open-licensed OpenBIM IFC models (tracked in `ROADMAP.md` M7 and `docs/datasets/CORPUS_ACQUISITION_REQUIREMENTS.md`).

---

## 6. ResPlan Scale Distortion — Deep Audit

A forensic inspection of `dataset_tools/resplan/resplan_forensic_auditor.py`, `dataset_tools/supervision/resplan_calibration.py`, and `docs/datasets/RESPLAN_CALIBRATION_REPORT.md` was conducted:

### Mathematical Cause of Distortion:
- In `core/resplan/extracted/ResPlan.pkl` (17,000 floorplans), each floorplan polygon set was rescaled independently by upstream creators so that $\max(\text{width}, \text{height}) = 256.0$.
- Mean max dimension: $256.0000$, standard deviation: $0.000000$.
- Because each apartment is normalized to fill the same $256 \times 256$ box, a 15 $\text{m}^2$ studio and a 350 $\text{m}^2$ villa have identical coordinate bounds.

### Area Metadata Corruption:
- **Zero net area:** 32.1% of plans (5,458 / 17,000) have `net_area == 0.0`.
- **Extreme outliers:** 4.1% of plans (696 / 17,000) have `net_area > 1000` (up to $7.9 \times 10^{10}$).
- **Ratio variance:** The ratio $\dfrac{\text{geometric canvas area}}{\text{listing gross area}}$ exhibits:
  - Minimum: $36.20$
  - Maximum: $1,817.49$
  - Mean: $369.09$
  - Standard Deviation: $173.24$

### Determinism:
- The distortion is **non-deterministic**. There is no universal scaling constant $k$ such that $\text{area}_{\text{m}^2} = k \cdot \text{area}_{\text{canvas}}$.

### Affects Training Labels?
- **YES**, if and only if ResPlan were used to generate training supervision for metric tasks (`PLAN_SUMMARY`, $\text{m}^2$ prediction, wall lengths in meters).
- **NO**, for scale-invariant topological tasks. The 6 validated topological capabilities (room count, category classification, room adjacency graph, door-room connectivity, relative angular bearing, topological conflict detection) are mathematical invariants under uniform similarity transformations.

### Affects Evaluation Only?
- ResPlan is **not** present in Gold Set V3 (which consists of 100 `CLEARANCE_CHECK` instances from `CORE_IL3D` and 100 `ROOM_TOPOLOGY` instances from `CORE_RPLAN`). It does not affect any evaluation benchmark in the active suite.

---

## 7. ResPlan Training Dependency

A complete audit of training dataset composition and codebase manifests was performed:

1. **`experiment_package/`:** Exactly 0 ResPlan records used.
2. **`dataset_tools/experiments/micro_pilot/dataset_loader.py`:** Loads Dataset A, which is built exclusively from `CORE_RPLAN` and `CORE_IL3D`.
3. **`tests/test_phase4_dataset_a.py`:** Line 134 specifically runs `test_no_forbidden_sources`, asserting that `CORE_RESPLAN` is 100% absent from Dataset A splits.
4. **`configs/training_corpus_cleared.json`:** Lists `CORE_RESPLAN` as `PARTIALLY_QUARANTINED`, permitting only topological tasks and strictly prohibiting all metric tasks.

### Formal Determination:
```text
FIRST_TRAINING_REQUIRES_RESPLAN = NO
```

### Quarantine Viability:
ResPlan is already hermetically quarantined from metric supervision in both code and configuration. It can remain completely excluded from the first training run, preserving the historical dataset intact while entirely preventing scale distortion from touching the training process.

---

## 8. ResPlan Metric Impact

An exhaustive cross-check was conducted to verify whether ResPlan's metric scale distortion touches any past, present, or planned evaluation metric:

| Metric / Artifact | Status | Impact of ResPlan Distortion |
| :--- | :---: | :--- |
| **First Training Loss** | Cleared | **Zero impact** (ResPlan is not in the training set) |
| **First Validation Loss** | Cleared | **Zero impact** (ResPlan is not in the validation set) |
| **First Test Loss** | Cleared | **Zero impact** (ResPlan is not in the test set) |
| **Baseline 0 MAE (2.7739 m)** | Certified | **Zero impact** (computed on Gold Set V3 clearance instances) |
| **Model A-Small MAE (0.4663 m)** | Certified | **Zero impact** (trained on IL3D, evaluated on Gold Set V3) |
| **Model A-Medium MAE (0.1699 m)** | Certified | **Zero impact** (trained on IL3D, evaluated on Gold Set V3) |
| **Selected Checkpoint `ARCHI-AI-P4-005` Validation MAE (0.0481 m)** | **CERTIFIED** | **ZERO IMPACT** (trained on Dataset A-Full from `CORE_IL3D`, validated on Dataset A held-out split) |
| **Gold Set V3 Evaluation MAE (0.0517 m)** | **CERTIFIED** | **ZERO IMPACT** (evaluated on Gold Set V3 from `CORE_IL3D`) |
| **Gold Set Clearance Accuracy (100.0%)** | Certified | **Zero impact** (evaluated on Gold Set V3 from `CORE_IL3D`) |
| **Auxiliary Plan Summary Evaluation** | Excluded | Quarantined in Phase 2/3 (`PLAN_SUMMARY` excluded from supervision) |

The reported validation MAE of **`0.0481 m`** is derived strictly from authentic metric 3D Cartesian coordinates in `CORE_IL3D`. It is **completely uncorrupted** by ResPlan.

---

## 9. Historical Result Integrity

All historical benchmark results, checkpoints, and evaluation manifests were audited for integrity:

1. **Checkpoint `ARCHI-AI-P4-005`:**
   - Architecture: `SpatialRelationMLP`
   - Training Data: Dataset A-Full (6,000 examples, `CORE_IL3D` + `CORE_RPLAN`)
   - Validation MAE: **`0.0481 m`** (Locked, verified)
   - Gold Set V3 MAE: **`0.0517 m`** (Locked, verified)
   - Difference: **`+0.0036 m`** (Cross-benchmark consistency check)
   - Error reduction vs Baseline 0: **`-2.7222 m` (98.14%)**

2. **Gold Set V3 Cryptographic Hashes:**
   - Manifest SHA256: `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca` (Unaltered)
   - Counterexamples SHA256: `a7991b378e46205e6e639961a9d634dd95661daa22129a89ab0744b73c9414e0` (Unaltered)

3. **Zero Falsification / Fabrication:**
   - No historical result was altered.
   - No data was fabricated.
   - No synthetic OpenBIM pairs were invented.
   - No fake scale metadata was injected into ResPlan.
   - All historical records remain fully preserved and scientifically defensible.

---

## 10. First Training Configuration Analysis

A cross-check of the intended first-training configuration demonstrates complete alignment:

| Configuration Parameter | Phase 4 Reproduction Pipeline | VLM QLoRA Micro-Experiment |
| :--- | :--- | :--- |
| **Script** | `dataset_tools/experiments/micro_pilot/run_micro_pilot.py` | `experiment_package/train_qlora.py` |
| **Config File** | Built-in deterministic dictionary | `experiment_package/config/qlora_experiment.yaml` |
| **Model** | `SpatialRelationMLP` (3-layer MLP) | `Qwen/Qwen2-VL-7B-Instruct` (PEFT QLoRA) |
| **Primary Task** | `OBJECT_RELATION` (3D Euclidean distance regression) | Architectural studio critique (5-part qualitative text) |
| **Training Dataset** | Dataset A-Full (`CORE_IL3D` + `CORE_RPLAN`) | `experiment_package/dataset/train.jsonl` (20 examples) |
| **Validation Dataset** | Dataset A-Full validation split (600 examples) | `experiment_package/dataset/validation.jsonl` (5 examples) |
| **Evaluation Benchmark** | Gold Set V3 (200 instances) | Qualitative validation comparison against baseline |
| **Modalities** | 3D Cartesian coordinates (unimodal geometric) | 2D photographs + text (vision-language) |
| **OpenBIM Exercised?** | **NO** (0 assets) | **NO** (0 assets) |
| **ResPlan Exercised?** | **NO** (0 assets) | **NO** (0 assets) |
| **FloorPlanCAD Exercised?**| **NO** (0 assets, legally excluded) | **NO** (0 assets, legally excluded) |

Neither of the two documented scientific blockers is exercised, needed, or referenced by either intended first-training configuration.

---

## 11. Blocker Classification

Applying the standard three-state remediation taxonomy (A. Must Fix Before Training / B. Can Be Isolated From First Training / C. Needs Future Data / Research):

### Blocker 1: OpenBIM Pair Scarcity
- **Classification for First Training Run:** **`B. CAN BE ISOLATED FROM FIRST TRAINING`**
- **Classification for Generalist Multimodal Model:** **`C. NEEDS FUTURE DATA / RESEARCH`**
- **Scientific Determination:** The scarcity of 2D $\leftrightarrow$ 3D BIM pairs prevents generalist cross-modal pre-training, but is completely absent from the first training configuration. Isolating the first run to unimodal 3D spatial geometry and photographic visual critique is scientifically sound and methodologically rigorous.
- **Formal Status for First Training Run:** **`OPENBIM_BLOCKER: NON_BLOCKING`** (tracked as **`FUTURE_WORK`** for Phase 5 multimodal scaling).

### Blocker 2: ResPlan Metric Scale Distortion
- **Classification for First Training Run:** **`B. CAN BE ISOLATED FROM FIRST TRAINING`**
- **Classification for Metric Plan Tasks:** **`C. NEEDS FUTURE DATA / RESEARCH`**
- **Scientific Determination:** The non-deterministic canvas normalization of ResPlan invalidates its use for metric $\text{m}^2$ supervision. However, ResPlan is already 100% excluded from Dataset A, Gold Set V3, and `experiment_package`. It is strictly quarantined in `configs/training_corpus_cleared.json`. Isolating ResPlan from the first training run completely protects model learning.
- **Formal Status for First Training Run:** **`RESPLAN_BLOCKER: NON_BLOCKING`**.

---

## 12. Required Remediation

To ensure total scientific validity without altering any historical artifacts:

### Remediation Action 1 (OpenBIM Scope Clarification):
- Formally document the operational boundary: the First Training Run is strictly scoped to unimodal geometric spatial reasoning (Dataset A / `SpatialRelationMLP`) and photographic qualitative critique (`experiment_package` / QLoRA).
- Reclassify OpenBIM acquisition (50–100 open-licensed IFC models with paired plans) as a Phase 5 milestone (`ROADMAP.md` M7) required for the subsequent Generalist Multimodal Model, rather than a blocker for the initial unimodal baseline.

### Remediation Action 2 (ResPlan Metric Quarantine Maintenance):
- Reaffirm the strict quarantine of `CORE_RESPLAN` defined in `configs/training_corpus_cleared.json`:
  - 100% excluded from the First Training Run.
  - Formally prohibited from all metric surface ($\text{m}^2$) and dimensional regression tasks across all training runs.
  - Any future use of ResPlan must be strictly restricted to scale-invariant topological tasks (`room_topology`, `graph_adjacency`, `room_count`) under an explicit `[SCALE_STATUS: UNCALIBRATED_NORMALIZED_CANVAS]` tag.

### Remediation Action 3 (Deterministic Vector Plan Derivation Strategy):
- Adopt the scientific recommendation in `CORPUS_GAP_REPORT.md` (GAP 3) and `SCIENTIFIC_READINESS_REPORT.md` §3.2: resolve the 2D metric scale requirement not by attempting to calibrate ResPlan, but by slicing 2D vector plans directly from native millimeter IFC geometry (`IfcWall`, `IfcSpace`) using `ifcopenshell`.

---

## 13. Scientific Gate Reassessment

Based strictly on empirical codebase evidence:

1. **Pre-requisite Checks:**
   - `OPEN_P0: 0`
   - `OPEN_P1: 0`
   - `OPEN_P2: 0`
   - `OPEN_P3: 0`
   - `DATASET_INTEGRITY: PASS`
   - `SCIENTIFIC_RECORD_INTEGRITY: PASS`

2. **Blocker Evaluations for First Training Run:**
   - OpenBIM pair scarcity does **not** invalidate or touch the first training configuration: **`NON_BLOCKING`**.
   - ResPlan metric scale distortion does **not** invalidate or touch the first training configuration: **`NON_BLOCKING`**.

3. **Scientific Gate Decision:**
   ```text
   SCIENTIFIC_GATE: PASS
   ```

4. **Operational Invariant:**
   Per mandatory instructions, even with `SCIENTIFIC_GATE: PASS`, model training remains formally disallowed:
   ```text
   TRAINING_ALLOWED: NO
   TRAINING_MAY_BEGIN: NO
   ```
   A separate final operational gate review must be conducted before any training execution may proceed.

---

## 14. Remaining Research Work

While the scientific blockers do not prevent the first training run, they represent active research tracks for subsequent phases:

1. **OpenBIM Corpus Expansion (Phase 5, P0):**
   - Source 50 to 100 open-licensed (CC-BY, MIT, Apache-2.0) IFC architectural models from buildingSMART, municipal open-data portals, or academic repositories.
   - Establish verified 2D floorplan $\longleftrightarrow$ 3D IFC pairings across diverse typologies (commercial, residential, educational, healthcare).

2. **Deterministic Millimetric 2D Vector Slicing (Phase 5, P1):**
   - Implement an automated geometry extraction pipeline (`ifcopenshell`) to project horizontal cross-sections of `IfcWall`, `IfcDoor`, `IfcWindow`, and `IfcSpace` into DXF/SVG with native millimeter precision.
   - Generate ground-truth room area annotations directly from 3D boundary representations, bypassing raster pixel ambiguity entirely.

3. **Topological ResPlan Supervision Branch (Phase 5, P2):**
   - If ResPlan is to be used for topological training, construct an isolated branch strictly limited to graph connectivity and room classification, ensuring zero metric dimensional leakage.

4. **FloorPlanCAD External Legal Counsel Review (Long-Term):**
   - Resolve the CC-BY-SA 4.0 vs CC-BY-NC 4.0 licensing discrepancy with external legal counsel before considering any future re-integration.

---

## FINAL MACHINE-READABLE SUMMARY

```text
OPENBIM_BLOCKER: NON_BLOCKING
RESPLAN_BLOCKER: NON_BLOCKING
SCIENTIFIC_GATE: PASS
OPEN_P0: 0
OPEN_P1: 0
OPEN_P2: 0
OPEN_P3: 0
DATASET_INTEGRITY: PASS
SCIENTIFIC_RECORD_INTEGRITY: PASS
TRAINING_ALLOWED: NO
TRAINING_MAY_BEGIN: NO
```
