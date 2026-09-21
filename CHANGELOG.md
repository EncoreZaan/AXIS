# Changelog

All notable changes to the **AXIS** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-09-21

### Official Renaming & Public Transition
- **Project Renamed:** Transitioned official naming from historical research codename `ARCHI-AI` to **`AXIS` (Architectural eXpert Intelligence System)**.
- **Historical Provenance Preserved:** Historical identifiers, run IDs (`ARCHI-AI-P4-001` through `ARCHI-AI-P4-005`), and cryptographic manifest hashes (`81561fae...`) remain intact and documented for unbroken scientific traceability.
- **Official Repository:** Published repository on [`https://github.com/EncoreZaan/AXIS.git`](https://github.com/EncoreZaan/AXIS.git).

### Phase 4 — Controlled Unimodal Micro-Pilot Completed
- **Task Selection:** Restated 69-task architectural catalog down to 4 strictly deterministic unimodal tasks: `FLOORPLAN_READING`, `ROOM_TOPOLOGY`, `OBJECT_RELATION`, `CLEARANCE_CHECK`. Excluded 65 tasks lacking ground truth or uncalibrated.
- **Dataset A Construction:** Structured deterministic subsets (Small: 800, Medium: 2,400, Full: 6,000) with strict `project_group_id` split isolation (0% project leakage, seed 42).
- **Gold Set V3 Sanctified:** Implemented read-only, immutable Gold Set V3 (200 examples: 100 clearance + 100 room topology) with 200 adversarial hard negatives (`counterexamples.jsonl`).
- **Benchmark Results (`CLEARANCE_CHECK`):**
  - Baseline 0 MAE: **2.7739 m**
  - Checkpoint `ARCHI-AI-P4-005` (A-Full, seed 42) Validation MAE: **0.0481 m**
  - Checkpoint `ARCHI-AI-P4-005` Gold Set MAE: **0.0517 m** (+98.14% relative error reduction vs Baseline 0).
  - Normative decision accuracy (`Pass/Fail`): **100.00%** (F1-score 100.00%).
- **Ablation Studies:** Audited conditions A (clean), B (sanitized metadata), and C (shuffled inputs), proving performance collapse without spatial signal and confirming zero shortcut leakage.

### Phase 3 — Scientific Readiness & Corpus Expansion
- **Corpus Investigation:** Forensic audit across 66,847 RAW files confirmed exactly 10 genuine 2D floorplan $\leftrightarrow$ 3D BIM pairs in existence (`CORE_RESBIM_PAIRED`). Refused arbitrary cross-dataset pairings.
- **ResPlan Calibration Forensic:** Demonstrated scale normalization anomaly on 17,000 vector plans; quarantined ResPlan for all physical metric tasks (m²), while validating 6 topological safe capabilities.
- **FloorPlanCAD Status:** Isolated 741 CAD files under legal quarantine (`LEGAL_REVIEW_REQUIRED`).
- **Pre-Training Gate:** Evaluated gate status as `CONDITIONAL` / `TRAINING_ALLOWED: NO` pending acquisition of 50-100 open-licensed OpenBIM IFC models.

### Phase 2 — Supervision Engine & Quality Audits
- **Supervision v1:** Compiled and repaired 608 examples; identified and removed 41 harmful records (pixel-as-m² confusion, fake multimodal dependencies).
- **Multi-dimensional Audit:** Evaluated visual, structural, metadata, semantic, and provenance quality across all assets.

### Phase 1 — Master Dataset v2 Infrastructure
- **Dataset Consolidation:** Built Master Dataset v2 comprising **65,342 unique assets** across 19 physical sources.
- **Splits:** 53,720 train / 5,724 validation / 5,898 test, with 1,563 items held in review. Zero SHA256 leakage, zero project-group leakage.
- **Test Suite:** Expanded automated test suite to 99 unit and integration tests (100% passing).

### Phase 0 — Environment & Feasibility
- Hardware audit and benchmark on local RTX 4060 Ti (8 GB VRAM) and remote 24 GB GPU configurations. Evaluated RWKV-7 state-tuning vs QLoRA VLM backbones.
