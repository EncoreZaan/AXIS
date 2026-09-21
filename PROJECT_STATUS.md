# AXIS — Current Project & Scientific Status

> **Last Updated:** September 2026  
> **Official Policy:** Scientifically honest, falsifiable, and verifiable against real artefacts.

---

## 1. Status Legend

The AXIS project strictly enforces transparent status descriptors across all documentation:

- **`DONE`** : Completed, peer-audited, verified by automated tests, and backed by verifiable disk artifacts.
- **`IN PROGRESS`** : Active development or ongoing investigation under active execution.
- **`BLOCKED`** : Progress paused due to an explicit technical, legal, or data dependency.
- **`PLANNED`** : Structured for upcoming roadmap phases; no execution started yet.
- **`EXPERIMENTAL`** : Exploratory proof-of-concept; results are preliminary and cannot be generalized.
- **`NOT YET VALIDATED`** : Implementation exists in draft form but lacks formal benchmark or empirical verification.

---

## 2. Component & Milestone Matrix

| Component / Subsystem | Current Status | Empirical Evidence & Artifacts | Known Limitations / Notes |
| :--- | :---: | :--- | :--- |
| **Master Dataset v2** | `DONE` | 65,342 assets consolidated across 19 sources (`DATASET_SPLIT_REPORT.md`). Zero SHA256 / project leaks. | Requires 50-100 additional OpenBIM IFC models for multimodal scale. |
| **Data Partitioning (Splits)** | `DONE` | Train: 53,720 / Val: 5,724 / Test: 5,898 / Review: 1,563. Gated with seed 42. | Strictly partitioned by `project_group_id`. |
| **Test Suite** | `DONE` | **99/99 passing tests** covering raw audit, leakage, target contracts, and readiness. | Runs in ~4 minutes under `pytest`. |
| **ResPlan Scale Forensic** | `DONE` | Forensic analysis of 17,000 plans proving scale distortion (`net_area` anomaly). | **BLOCKED for metric tasks (m²).** Quarantined. 6 non-metric capabilities safe. |
| **FloorPlanCAD Status** | `BLOCKED` | 741 CAD vector drawings isolated under `LEGAL_REVIEW_REQUIRED`. | Blocked on intellectual property / license clarification. |
| **2D/3D Pair Discovery in RAW**| `DONE` | Exhaustive scan of 66,847 files confirmed 0 new hidden 2D/3D pairs exist in RAW. | 10 certified pairs exist (`CORE_RESBIM_PAIRED`). Arbitrary matching rejected. |
| **Phase 4 Task Gating** | `DONE` | 4/69 tasks approved (`FLOORPLAN_READING`, `ROOM_TOPOLOGY`, `OBJECT_RELATION`, `CLEARANCE_CHECK`). | 65 tasks excluded due to lack of ground truth or uncalibrated data. |
| **Dataset A Construction** | `DONE` | Built Small (800), Medium (2,400), Full (6,000) subsets (`dataset_a/`). | Zero collision with Gold Set V3. |
| **Gold Set V3 Sanctification**| `DONE` | 200 certified instances + 200 hard negatives. SHA256: `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`. | Read-only, immutable evaluation set. |
| **Checkpoint Evaluation (`005`)**| `DONE` | MAE: 0.0517 m on Gold Set (vs Baseline 0: 2.7739 m). Gain: +98.14%. 100% accuracy on clearance. | Validated exclusively for 3D spatial clearance regression. |
| **2D Vision Model (`ROOM_TOPOLOGY`)** | `NOT YET VALIDATED` | Baseline 0 calibrated (34% exact match). Model architecture not trained in Phase 4. | Labeled `NOT_EVALUATED` on Gold Set in Phase 4. |
| **VLM QLoRA Proof-of-Concept** | `EXPERIMENTAL` | Dry-run & 6-step run on Qwen2-VL-7B (loss 1.893 $\to$ 1.769). 0 OOM, 0 NaN. | **Micro-experiment only.** Not a trained production model. |
| **Multimodal 2D $\leftrightarrow$ 3D Reasoning** | `NOT YET VALIDATED` | Synthetic cross-modal reasoning without true pairs rejected. | Awaiting open-licensed paired BIM models. |
| **DSpark Acceleration** | `PLANNED` | Theoretical evaluation tracked in `docs/research/inference-optimization.md`. | No integration or benchmark exists yet. |
| **Pre-Training Gate** | `BLOCKED` | Status: `CONDITIONAL` (`TRAINING_ALLOWED: NO`). | Blocked until dataset expansion requirements are satisfied. |

---

## 3. What AXIS Is NOT (Scientifically Honest Boundary)

- **NOT Production-Ready:** AXIS is an active foundational research initiative.
- **NOT A Generalist Foundation Model:** The current validated checkpoint proves spatial clearance geometric regression, not general architectural autonomy.
- **NOT "AGI for Architecture":** All demonstrated capabilities are narrowly bounded by deterministic target contracts and falsifiable verification scripts.
