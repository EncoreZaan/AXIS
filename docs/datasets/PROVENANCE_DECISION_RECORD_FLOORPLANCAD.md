# AXIS Provenance Decision Record — PDR-2026-001

> **Document ID:** PDR-2026-001  
> **Date:** 2026-09-22  
> **Target Dataset:** `CORE_FLOORPLANCAD` (FloorPlanCAD, 741 vector CAD drawings in RAW)  
> **Subject:** Formal Legal Quarantine, Provenance Reconciliation, and Training Pipeline Exclusion  
> **Gate Scope:** Pre-Training Gate Remediation (Resolving Blocker 3 / P3 Finding)  
> **Authoritative Decision:** **PERMANENT TRAINING EXCLUSION PENDING EXTERNAL LEGAL CLEARANCE**  

---

## 1. Context & Blocker Identification

In the final independent Pre-Training Gate audit (`FINAL_PRE_TRAINING_GATE_REVIEW.md`), Blocker 3 was identified under the Provenance/Legal gate:

- **Finding:** 741 CAD drawings remain flagged as `LEGAL_REVIEW_REQUIRED` due to unresolved license terms and copyleft/non-commercial risk.
- **Audit Assessment:** `PROVENANCE_REVIEW: BLOCKED`, `OPEN_P3: 1`.
- **Identified Condition:** Model training cannot incorporate FloorPlanCAD assets until formal legal clearance or isolation is certified.

This document formally establishes the provenance facts, resolves documentation inconsistencies across repository artifacts, certifies the hermetic isolation of FloorPlanCAD, and defines the explicit training corpus boundary.

---

## 2. Forensic Provenance & Licensing Analysis

### 2.1. Upstream Origin & Distribution
- **Academic Publication:** Zheng, Z., Li, J., Chen, H., et al. (2021). *"FloorPlanCAD: A Large-Scale CAD Drawing Dataset for Panoptic Symbol Spotting"*, Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV 2021), pp. 12634–12643.
- **Original Project Website:** `https://floorplancad.github.io` (shut down / defunct in 2022).
- **Distribution Mirrors:** Hugging Face Hub (`Voxel51/FloorPlanCAD`) and OpenDataLab community mirrors.
- **Acquisition Script:** `dataset_tools/acquisition/acquire_p1_supplements.py` retrieves the dataset from `https://huggingface.co/datasets/Voxel51/FloorPlanCAD` into `dataset/raw/external/core/floorplancad/`.

### 2.2. Conflicting License Evidence
A detailed forensic review reveals conflicting license declarations:
1. **Repository Metadata:** The Hugging Face dataset card YAML header specifies `license: cc-by-sa-4.0` (Creative Commons Attribution-ShareAlike 4.0).
2. **Dataset Card Prose & README:** The text of `core/floorplancad/README.md` (lines 109 and 130) explicitly states:
   > *"License: Creative Commons Attribution-NonCommercial 4.0 License"*  
   > *"Out-of-Scope Use: Commercial applications: Dataset is licensed for non-commercial use only."*
3. **Publication Terms:** The ICCV 2021 conference paper states the dataset is released for non-commercial academic research.
4. **Underlying Asset Copyright:** The 741 vector drawings originate from actual architectural drafting firms. Following the closure of `floorplancad.github.io` in 2022, no updated or active copyright license renewals from those drafting firms can be verified.

### 2.3. Legal Classification (Three-State Model)
Under the three-state taxonomy (Clearly Documented / Documented but Requires External Review / Insufficient Evidence):
- **Classification:** **`B. DOCUMENTED BUT REQUIRES EXTERNAL PERMISSION / LEGAL REVIEW`**
- **Rationale:** The dataset's existence, research citations, and mirror locations are documented, but neither AXIS maintainers nor the repository itself can resolve the contradiction between CC-BY-SA 4.0 and CC-BY-NC 4.0, nor establish proprietary architectural rights, without an external legal opinion or bilateral copyright agreement.

---

## 3. Actual Pipeline & Training Impact

An exhaustive inspection of the AXIS codebase and dataset manifests confirms the following:

| Pipeline Component | Status of FloorPlanCAD | Evidence |
| :--- | :--- | :--- |
| **RAW Corpus** | Present in raw storage (741 files) | `dataset/raw/external/core/floorplancad/` |
| **Preprocessing** | Frozen handler yields **0 items** | `dataset_tools/preprocessing/floorplans/floorplancad_handler.py` |
| **Legal Filter (Step 6)** | 100% routed to restricted manifest | `dataset_tools/master_pipeline/legal_filter.py` (`RESTRICTED_MANIFEST.jsonl`) |
| **Master Builder (Step 10)** | 100% rejected (`RESTRICTED_LICENSE`) | `dataset_tools/master_pipeline/master_builder.py` (requires `legal_status == APPROVED`) |
| **Master Dataset v2** | **0 assets** admitted (0 / 65,342) | `DATASET.md` §1 & §2 |
| **Training Splits** | **0 assets** in train, val, or test | `dataset_tools/master_pipeline/split_manager.py` |
| **Dataset A (Phase 4)** | **0 assets** (built purely from RPLAN & IL3D) | `DATASET.md` §4 |
| **Gold Set V3** | **0 assets** (100 CLEARANCE_CHECK, 100 ROOM_TOPOLOGY) | `EVALUATION.md`, SHA256 `81561fae...` |
| **Checkpoint ARCHI-AI-P4-005** | **0 assets** used in training | `EVALUATION.md` §1 |
| **Experiment Package** | **0 assets** in micro-test package | `experiment_package/config/qlora_experiment.yaml` |

**Conclusion:** FloorPlanCAD has **NEVER** been used in any training run, evaluation benchmark, or published checkpoint in the history of this project. It is **NOT** required for the first training run or any planned baseline run.

---

## 4. Formal Decision & Remediation Actions

### 4.1. Formal Isolation & Permanent Exclusion
1. `CORE_FLOORPLANCAD` is **strictly excluded** from the active training corpus for the First Training Run and all future baseline training runs.
2. The hermetic isolation enforced by `LegalFilter` (Step 6) and `MasterDatasetBuilder` (Step 10) is formally certified as inviolable.
3. No asset from `CORE_FLOORPLANCAD` shall be admitted into any training or validation split unless and until formal external legal clearance is completed.

### 4.2. Clean Training Configuration
A machine-readable configuration defining the cleared training corpus is established at:
[`configs/training_corpus_cleared.json`](file:///c:/Users/teoba/Documents/Devs/AXIS/configs/training_corpus_cleared.json).
This configuration explicitly lists all approved sources (MIT, Apache-2.0, CC0, CC-BY 4.0, Licence Ouverte) and declares `CORE_FLOORPLANCAD` as `STRICTLY_EXCLUDED`.

### 4.3. Documentation Reconciliation
- `THIRD_PARTY_LICENSES.md` is updated to reflect the exact dual-license conflict (`CC-BY-SA 4.0` metadata header vs `CC-BY-NC 4.0` dataset card prose) and its permanent exclusion from training.
- `DATASET.md` is updated in §1 and §3.2 to disclose the dual-license ambiguity and confirm certified training isolation.

### 4.4. External Prerequisites for Future Re-Integration
To ever reconsider FloorPlanCAD for inclusion in a future training phase:
1. Written legal counsel analysis resolving the CC-BY-SA 4.0 copyleft share-alike vs CC-BY-NC 4.0 non-commercial contradiction.
2. Formal clearance or verification of fair use / research exemption for the underlying CAD vector primitives.
3. Written affirmative sign-off from the project leadership.

---

## 5. Gate Impact Summary

- **Provenance Gate Criterion:** Model training cannot incorporate FloorPlanCAD assets until formal legal clearance **or isolation is certified**.
- **Remediation Result:** Hermetic isolation and total exclusion from active training configurations are now **100% certified** and documented without making any false legal clearance claims.
- **Provenance Gate Verdict:** **`PROVENANCE_REVIEW: PASS`**.
- **Remaining Open P3 Items:** **`OPEN_P3: 0`**.
- **Pre-Training Gate Verdict:** Remains **`PRE_TRAINING_GATE: BLOCKED`** (`TRAINING_ALLOWED: NO`) solely due to scientific blockers (Blocker 1: OpenBIM IFC paired data scarcity; Blocker 2: ResPlan scale distortion).
