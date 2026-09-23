# AXIS ? Real Data Forensic Audit (`RUN-016-REAL_DATA_AUDIT`)

> **Date:** 2026-09-22  
> **Source Corpus:** `CORE_RPLAN` + `CORE_RESBIM_PAIRED`  
> **Target Pilot:** `experiments/runpod_2026-09-22/REAL_DATA_PILOT/`  
> **Verdict:** **DATASET_INTEGRITY: PASS** | **SPLIT_INTEGRITY: PASS**

---

## 1. Executive Summary & Scientific Answer

### Is this actually a scientifically useful multi-image dataset?
**YES.**
Unlike the Phase 2 runtime fixture (which had 25 files but exactly 1 unique image repeated 25 times), this pilot dataset comprises **1000 genuine, unique architectural plans**:
- **990 distinct 2D floor plans** from `CORE_RPLAN` capturing a wide variety of apartment topologies, room layouts, wall partitions, and doorway connections.
- **10 certified residential units** from `CORE_RESBIM_PAIRED` directly coupled with underlying OpenBIM 3D models.
- **Zero byte-identical duplicates** across assets.
- **Zero cross-split leakage** (`CROSS_SPLIT_DUPLICATES: 0`).
- **Complete format compliance** with Qwen2-VL multimodal conversational requirements.

---

## 2. Quantitative Census

| Metric | Target Specification | Observed Value | Status |
| :--- | :---: | :---: | :---: |
| **Total Physical Assets** | 500?1,000 | **1000** | **PASS** |
| **Unique Image SHA-256** | 100% unique | **1000** | **PASS** |
| **Train Assets** | ~80% | **775** (77.5%) | **PASS** |
| **Validation Assets** | ~10% | **98** (9.8%) | **PASS** |
| **Test Assets** | ~10% | **127** (12.7%) | **PASS** |
| **Cross-Split Duplicates** | **0** | **0** | **PASS** |
| **RESBIM Valid Pairs** | Exactly measured | **10** | **PASS** |
| **Corrupted Images** | 0 admitted | **0** (0 discarded) | **PASS** |
| **Duplicate Images Filtered**| N/A | **3** | **PASS** |
| **Sample Interior Matches** | 0 | **0** | **PASS** |

---

## 3. Data Leakage & Partitioning Integrity

Partitioning was performed via deterministic hash allocation based on `project_group_id` (Seed = 42).
- Train Hash Set: `775` unique SHA-256 hashes
- Validation Hash Set: `98` unique SHA-256 hashes
- Test Hash Set: `127` unique SHA-256 hashes
- **Intersection Train ? Val:** 0
- **Intersection Train ? Test:** 0
- **Intersection Val ? Test:** 0
- **Underlying Scene Independence:** Guaranteed. No asset sharing a project or floorplan stem crosses split boundaries.

---

## 4. Provenance & Compliance

- `CORE_RPLAN`: Cleared for Academic Research (metindeder/rplan-floorplan-edited)
- `CORE_RESBIM_PAIRED`: Cleared under MIT License (tsesterh/ResBIM-IFC)
- `CORE_FLOORPLANCAD`: Strictly excluded (0 assets admitted)
- `GOLD_SET_V3`: Complete sanctuary maintained (0 overlap)
