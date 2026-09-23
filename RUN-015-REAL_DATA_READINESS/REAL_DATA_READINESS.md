# AXIS — Real Data Environment Readiness Report (`RUN-015-REAL_DATA_READINESS`)

> **Audit Date:** 2026-09-22  
> **Environment:** RunPod Remote GPU Instance (`territorial_green_minnow`)  
> **Target Baseline Commit:** `f4d5e949053743d97091ea35080de5d365899df7`  
> **Status:** **REAL_DATA_READINESS: READY**  
> **Operational Invariants:** `TRAINING_ALLOWED: NO` | `TRAINING_MAY_BEGIN: NO`

---

## 1. Environment & Stack Verification

| Parameter | Specification | Measured State | Verdict |
| :--- | :--- | :--- | :---: |
| **Git Commit HEAD** | `f4d5e949053743d97091ea35080de5d365899df7` | `f4d5e949053743d97091ea35080de5d365899df7` | **PASS** |
| **Working Tree Status** | Clean (untracked outputs only) | Main branch, no code regressions | **PASS** |
| **GPU Model** | 24 GB VRAM Target Class | NVIDIA GeForce RTX 3090 | **PASS** |
| **GPU VRAM Detected** | >= 22.0 GiB | 24,124.2 MiB | **PASS** |
| **NVIDIA Driver** | >= 535 | `580.159.04` | **PASS** |
| **CUDA Runtime** | 12.4 compatible | CUDA `12.4` / PyTorch `2.6.0+cu124` | **PASS** |
| **Python Environment** | Python 3.12 isolated `.venv` | Python `3.12.3` | **PASS** |
| **Deep Learning Stack** | Pinned reproduction versions | `transformers 5.17.0`, `peft 0.21.0`, `bitsandbytes 0.50.2` | **PASS** |
| **Base Model Revision** | Qwen/Qwen2-VL-7B-Instruct | `eed13092ef92e448dd6875b2a00151bd3f7db0ac` | **PASS** |
| **Disk Storage (Workspace)**| >= 10 GB free | 50.0 GB total, 25.36 GB free | **PASS** |

---

## 2. Authorized Data Sources Census & Discovery

| Source ID | Official License | Domain | Raw Assets Available | Pilot Admitted | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **`CORE_RPLAN`** | Open Research License | 2D Raster Floorplans & Room Topology | 15,000 plans | **990** | **CLEARED** |
| **`CORE_RESBIM_PAIRED`** | MIT License | True Paired 2D CAD Plan ↔ 3D BIM IFC | 10 certified pairs | **10** | **CLEARED** |
| **`CORE_FLOORPLANCAD`** | Mixed / Conflicted | CAD Vector Floorplans | 0 (quarantined) | **0** | **EXCLUDED** |
| **`GOLD_SET_V3`** | Benchmark Sanctuary | 200 holdout examples | 0 on RunPod | **0** | **SANCTUARY** |
| **`RUNTIME_FIXTURE`** | Test Artifact (`sample_interior.jpg`) | Engineering Test Fixture | 25 files / 1 image | **0** | **EXCLUDED** |

---

## 3. Provenance & Legal Clearance Summary

1. **`CORE_RPLAN` Ingestion:**
   - Ingested via native repository script `dataset_tools/acquisition/acquire_core.py`.
   - Source: `metindeder/rplan-floorplan-edited` (HF archive `rplan_dataset.zip`, 23.5 MB).
   - Extracted 15,000 clean 256x256 architectural floor plans and full segmentation metadata.
   - Cleared for academic architectural research and non-commercial model pre-training.

2. **`CORE_RESBIM_PAIRED` Ingestion:**
   - Ingested via native repository script `dataset_tools/acquisition/acquire_p1_supplements.py`.
   - Source: `tsesterh/ResBIM-IFC`.
   - Exactly 10 certified residential units (`unit_000` to `unit_102`) comprising 10 high-resolution `.jpg` drawings and 10 native `.ifc` models.
   - Zero synthetic or ungrounded pairings fabricated.

3. **`CORE_FLOORPLANCAD` Exclusion:**
   - In accordance with Absolute Rule 4, FloorPlanCAD remains strictly excluded and quarantined. Zero assets were downloaded, converted, or admitted.

4. **`GOLD_SET_V3` Sanctuary Invariant:**
   - Gold Set V3 remains completely absent from the training pipeline and storage paths. Zero contamination.

---

## 4. Operational Invariant Signoff

```text
TRAINING_ALLOWED: NO
TRAINING_MAY_BEGIN: NO
```
The remote environment and raw data sources are certified READY for pilot construction and forensic auditing.
