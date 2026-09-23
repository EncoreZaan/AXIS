# RUN-021 — Spatial Supervision Dataset Engineering & Lock

> **Canonical Run ID:** `RUN-021-SPATIAL-SUPERVISION`  
> **Scientific Phase:** Phase 6A — Spatial Supervision Dataset Construction  
> **Date:** 2026-09-23  
> **Dataset Name:** `AXIS_SPATIAL_SUPERVISION_V1`  
> **Status:** **COMPLETE** | **DATASET_LOCK: PASS**  
> **Evidence Directory:** [`RUN-021-SPATIAL-SUPERVISION/`](../../../RUN-021-SPATIAL-SUPERVISION/)  

---

## 1. Objective & Design Rationale

In response to the falsification findings of RUN-020 (template memorization, ID hallucinations, and quasi-null visual dependency), Phase 6A designed and engineered an entirely new supervision corpus: **`AXIS_SPATIAL_SUPERVISION_V1`**.

The objective was to replace unstructured narrative critiques with discrete, mathematically grounded, falsifiable spatial queries where:
1. Every answer requires visual parsing of the underlying floorplan image (`100% VISUAL_REQUIRED`).
2. Answers are concise (average length 12.3 words) to prevent causal LM template exploitation.
3. Tasks cover rigorous architectural topology and geometric reasoning.

---

## 2. Dataset Composition & Partitions

Built from 1,006 certified physical assets (1,000 RPLAN 2D rasters and certified 2D/3D BIM pairs):

| Split | Number of Examples | Percentage | Assets Covered | Cross-Split Leakage | SHA-256 Checksum |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`train.jsonl`** | **6,160** | 77.48% | 775 unique | 0 leaks (**PASS**) | `227ba7db7769e3f25d365a33efd03126e18612cf5821f1f23dcd2342a701e849` |
| **`validation.jsonl`** | **784** | 9.86% | 98 unique | 0 leaks (**PASS**) | `c543a319321534f016c94aeb8ee74503bc8f01511c232ec91394d69a307467d2` |
| **`test.jsonl`** | **1,006** | 12.65% | 127 unique | 0 leaks (**PASS**) | `aaba73433c9ccea7a5c6134154577ea80591e23755665794bec603ebdf53053f` |
| **Total** | **7,950** | 100.0% | 1,000 unique | **Hermetic Isolation** | Config: `9c0908c4c2bc25c647cfde7d885e4d8fe9ba507fb00fb79ce42852942ea60d6c` |

---

## 3. Spatial Task Families & Ground Truth Definitions

1. **Directional Relations:** Determine relative Cartesian orientation (`ABOVE`, `BELOW`, `LEFT_OF`, `RIGHT_OF`) between distinct architectural rooms using centroids.
2. **Door Connectivity (Positive & Negative):** Determine whether two rooms share an immediate, traversable physical door opening (evaluating true positives and hard negatives).
3. **Room Adjacency:** Determine topological wall-sharing adjacency without direct door connectivity.
4. **Room & Door Cardinality:** Exact integer counting of closed room polygons and physical door symbols.
5. **Multi-Hop Reachability / Shortest Path:** Calculate the minimum integer number of doors to cross to navigate between distant rooms in a graph topology.
6. **Circulation Hub Identification:** Identify the central architectural room connecting the maximum number of access doors, returning room ID, count, and bounding box `[ymin, xmin, ymax, xmax]`.
7. **Largest Room Identification:** Identify the room with the maximum interior pixel surface area.

---

## 4. Quality Audits & Clarifications

### 4.1. Leakage & Sanitization Verification
- **Example ID Isolation:** $\text{Train} \cap \text{Val} \cap \text{Test} = \emptyset$ (0 collisions).
- **Asset ID Isolation:** 0 overlapping floorplan assets across partitions.
- **Image Hash Isolation:** 0 SHA-256 collisions across images.
- **Sanctuary Isolation:** Zero exposure of `Gold Set V3` or quarantined `CORE_FLOORPLANCAD`.

### 4.2. Sampled Audit Status Clarification

> [!IMPORTANT]
> **Audit Status Clarification:**  
> Historical documentation in `RUN-021-SPATIAL-SUPERVISION/MANUAL_AUDIT.md` recorded `MANUAL_AUDIT: PASS`.  
> Forensic review confirms that this audit was an **automated geometric script check** of 50 sampled instances verifying bounding boxes, coordinates, and derived ground truth against physical image files.  
>  
> To maintain absolute scientific honesty:
> - **`MANUAL_AUDIT_HUMAN:`** `NOT_PERFORMED`
> - **`AUTOMATED_GEOMETRIC_AUDIT:`** `PASS` (50/50 samples verified with 100% geometric concordance).

---

## 5. Pre-Training Dry Run

A zero-step forward pass dry-run was executed (`RUN-021-SPATIAL-SUPERVISION/DRY_RUN_REPORT.md`):
- Collation and forward pass executed cleanly on `Qwen/Qwen2-VL-7B-Instruct`.
- Peak VRAM observed: 10,317.73 MiB.
- Forward loss computed: `0.9412` (finite, zero NaN/Inf).
- Zero optimizer steps executed; model parameter hash remained 100% bit-identical.

---

## 6. Conclusion & Authorized Next Step

- **Conclusion:** Phase 6A successfully produced and cryptographically sealed a high-integrity spatial supervision dataset (`AXIS_SPATIAL_SUPERVISION_V1`) designed to eliminate template shortcuts.
- **Next Step:** Authorize **RUN-022**, a full-scale 3-epoch QLoRA training pilot on `Qwen/Qwen2-VL-7B-Instruct`.
