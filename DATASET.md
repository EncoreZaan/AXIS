# AXIS — Master Dataset v2 Documentation

> **Status:** AUDITED, ISOLATED & CERTIFIED  
> **Total Consolidated Records:** **65,342 assets**  
> **Physical Source Files Scanned:** **66,847 files** (3.48 GB on disk)  
> **Cryptographic Integrity:** 100% SHA256 streaming verification, zero leakage.

---

## 1. Physical Sources & Distribution

The Master Dataset v2 is compiled from 19 independent physical repositories, categorized by operational status:

| Source Identifier | Domain / Format | Files in RAW | Status in Master v2 | Primary License | Role in AXIS |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `CORE_RPLAN` | 2D Floorplan Rasters (256x256) | 30,002 | **ACTIVE** | Academic Research Only [^1] | Plan topology & room reading |
| `CORE_IL3D` | 3D Interior Scenes & Objects | 27,820 | **ACTIVE** | Academic Research Only [^1] | 3D Cartesian coordinates & clearance |
| `CORE_STRUCTSCAN3D` | RGB-D Scans & Bounding Boxes | 7,814 | **ACTIVE** | Open Research | Subjective perspective & depth |
| `CORE_FLOORPLANCAD` | CAD Vector Drawings | 741 | **QUARANTINED** | CC-BY-SA 4.0 / CC-BY-NC 4.0 [^2] | Quarantined & excluded (`LEGAL_REVIEW_REQUIRED`) |
| `CORE_IFC_BENCH` | OpenBIM IFC Models | 345 | **ACTIVE** | CC-BY 4.0 / Open | BIM schema entities & axonometric views |
| `CORE_BUILDINGSMART_IFC` | Standard buildingSMART IFCs | 72 | **ACTIVE** | Open Standard | IFC schema validation & testbeds |
| `CORE_RESBIM_PAIRED` | True Paired BIM + Floorplan | 20 | **ACTIVE** | CC-BY 4.0 / MIT | Ground truth multimodal 2D/3D (10 pairs) |
| `CORE_RESPLAN` | Vector floorplans (extracted PKL) | 6 (17,000 pkl) | **QUARANTINED** | CC-BY 4.0 / MIT | Quarantined for metric m²; safe for topology |
| `CORE_POLYHAVEN_MATERIALS` | PBR Architectural Textures | 5 | **ACTIVE** | CC0 | Material identification |
| `CORE_MOMA_COLLECTION` | Architectural Design History | 4 | **ACTIVE** | Public Domain | Design history & typography |
| `CORE_POLYHAVEN_LIGHTING` | HDR Environment Maps | 4 | **ACTIVE** | CC0 | Lighting reasoning |
| `CORE_MET_OPENACCESS` | Historical Architecture Texts | 3 | **ACTIVE** | CC0 | Architectural history & styles |
| `CORE_MMMU_ARCHITECTURE` | Visual QA Benchmark Subset | 3 | **ACTIVE** | CC-BY 4.0 | Multimodal architecture evaluation |
| `CORE_NORMES_FR` | French Building Regulations | 3 | **ACTIVE** | Public Domain (Legifrance) | Ergonomic clearance thresholds (PMR) |
| `CORE_ERGONOMIE` | Neufert Spatial Standards | 1 | **ACTIVE** | Open Reference | Standard passage & furniture tolerances |
| `CORE_AMBIENTCG` | PBR Textures | 1 | **ACTIVE** | CC0 | Material textures |
| `CORE_TRENDS_2026` | Contemporary Design Catalog | 1 | **ACTIVE** | Public Reference | Stylistic reference |
| `UNKNOWN_SOURCE` / `RESEARCH`| Internal Test Manifests | 2 | **ACTIVE** | Internal | Test scaffolding |

---

[^1]: "Academic Research Only" is the maintainer's short paraphrase of the upstream license terms for RPLAN and IL3D, not a formal SPDX license identifier — these sources do not use a standard OSI license. It means: non-commercial use for research/academic purposes, no redistribution of the raw assets, as stated by each source's original release terms. AXIS does not sublicense or alter these terms; a contributor building the Master Dataset v2 locally is bound by the original upstream terms directly, and should consult the upstream license text (linked from each source's original release page, not reproduced here) rather than rely on this paraphrase alone.

[^2]: Upstream Voxel51 Hugging Face metadata specifies `cc-by-sa-4.0`, whereas the repository README text (lines 109, 130) and ICCV 2021 publication specify `CC-BY-NC 4.0` / non-commercial research use only. The original site `floorplancad.github.io` shut down in 2022. Quarantined and permanently excluded from active training corpus configurations. See [`docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md`](docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md).

## 2. Dataset Partitions & Anti-Leakage Guarantees

The 65,342 consolidated assets are partitioned strictly by `project_group_id` (individual building or distinct residential plan) using a locked seed (`seed = 42`):

```text
=============================================================================
SPLIT           RECORDS (ASSETS)    DISTINCT PROJECTS   PROJECT LEAKAGE SHA256 LEAKAGE
=============================================================================
Train           53,720              ~35,000             0                   0
Validation       5,724               ~3,700             0                   0
Test             5,898               ~3,900             0                   0
Review Queue     1,563                  -               Isolated            0
=============================================================================
TOTAL           65,342 assets       42,667 projects     PASS (0 leaks)      PASS (0 leaks)
=============================================================================
```

---

## 3. Quarantines & Scientific Safeguards

### 3.1. ResPlan Metric Quarantine
- **Forensic Finding:** All 17,000 floorplans in `ResPlan.pkl` were rescaled onto an arbitrary maximum dimension of 256.0 without preserving absolute metric ratios ($\text{std} = 173.2$, 32.1% net area null).
- **Enforcement:** Strictly prohibited from all metric surface ($\text{m}^2$) and physical dimension tasks.
- **Permitted Use:** Scale-invariant topological graphs (room adjacency, room count).

### 3.2. FloorPlanCAD Legal Quarantine & Training Pipeline Exclusion
- **Status:** `LEGAL_REVIEW_REQUIRED` (Formally Quarantined & Strictly Excluded).
- **Licensing Discrepancy:** The Hugging Face mirror (`Voxel51/FloorPlanCAD`) contains conflicting license declarations: repository metadata header specifies `license: cc-by-sa-4.0`, while README text lines 109 & 130 declare `CC-BY-NC 4.0` ("Out-of-Scope Use: Commercial applications"). The ICCV 2021 publication (Zheng et al.) declared non-commercial research use, and the original project host (`floorplancad.github.io`) closed in 2022.
- **Pipeline Enforcement:**
  - `FloorPlanCadFrozenHandler` yields an empty iterator (0 items generated).
  - `LegalFilter` routes 100% of FloorPlanCAD raw records to `restricted/legal_review/floorplancad/` and `RESTRICTED_MANIFEST.jsonl`.
  - `MasterDatasetBuilder` enforces `legal_status == APPROVED`, rejecting all 741 records (`RESTRICTED_LICENSE`).
  - **Zero FloorPlanCAD records exist in Master Dataset v2 (0 / 65,342) and zero exist in any partition (`train`, `validation`, `test`).**
  - **Zero FloorPlanCAD records exist in Dataset A, Gold Set V3, or `experiment_package`.**
- **Training Boundary:** Formally certified as excluded from active training configurations in [`configs/training_corpus_cleared.json`](configs/training_corpus_cleared.json).
- **Provenance Decision Record:** Formally governed by [`docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md`](docs/datasets/PROVENANCE_DECISION_RECORD_FLOORPLANCAD.md) (PDR-2026-001). Re-integration is prohibited absent formal written legal counsel review and copyright clearance.

---

## 4. Controlled Subsets: Dataset A (Phase 4)

Built from `CORE_RPLAN` and `CORE_IL3D` to test 4 approved tasks without dataset contamination:
- **Dataset A-Small:** 800 examples (640 train / 80 val / 80 test)
- **Dataset A-Medium:** 2,400 examples (1,920 train / 240 val / 240 test)
- **Dataset A-Full:** 6,000 examples (4,800 train / 600 val / 600 test)

$$\text{Gold Set V3} \cap \text{Dataset A} = \emptyset$$

---

## 5. Data Access Policy

In compliance with the individual licensing terms of each upstream academic/research dataset listed in §1 (AXIS's own code is MIT-licensed, but that grant does not modify or supersede these third-party terms — see [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) and `GOVERNANCE.md`):
- **No Third-Party Raw Assets are Redistributed:** This repository contains ingestion scripts, validation manifests, metadata schemas, and benchmark definitions.
- **Reproduction:** Contributors can download public source datasets directly from their official upstream repositories and run `dataset_tools/acquisition/` to reconstruct the Master Dataset v2 locally.

---

## 6. Local Directory Convention for the Full Pipeline (Historical — Resolved)

> **Status: RESOLVED as of the pre-training-gate remediation pass.** The `ARCHI_AI/`-prefixed
> path convention described below no longer exists in this codebase. This section is kept as
> a historical record of the limitation and how it was fixed — it is not a setup step current
> contributors need to perform.

The `dataset_tools` package was not previously internally uniform in how it located data on disk:

- **`dataset_tools/master_pipeline/`** (the module that actually built Master Dataset v2, covered by `tests/test_master_pipeline.py`) already resolved every path relative to the repository root at runtime (`BASE_DIR = Path(__file__).resolve().parent.parent.parent`, e.g. `dataset_tools/master_pipeline/config.py`). It required no special setup beyond a `dataset/` directory existing under the repo root.
- **`dataset_tools/experiments/micro_pilot/`** (the scripts that produced checkpoint `ARCHI-AI-P4-005` and the Gold Set V3 evaluation — `trainer.py`, `run_micro_pilot.py`, `gold_evaluator.py`, `dataset_loader.py`, `baseline_evaluator.py`) and several standalone Wave-1-era audit scripts at the top of `dataset_tools/` (`gold_set_builder.py`, `audit_calculator.py`, `decision_classifier.py`, `deep_audit.py`, `audit_diagnostics.py`) instead used hardcoded string paths prefixed with `ARCHI_AI/` (e.g. `ARCHI_AI/dataset/master/v1/...`) and, in a few files, `sys.path.insert(0, os.path.abspath("ARCHI_AI"))` followed by `from ARCHI_AI.dataset_tools... import ...`.

That `ARCHI_AI/` prefix was not a typo: it was a deliberate local convention from the project's original (pre-AXIS-rename) development setup, where a directory of symlinks named `ARCHI_AI` sat at the repository root, each pointing back at the corresponding real subdirectory (`dataset_tools`, `dataset`, `experiments`) — confirmed by the `# Legacy junctions` / `ARCHI_AI` entry in `.gitignore`. Because each `ARCHI_AI/<subdir>` symlink resolved back to the identical physical directory at the repo root, the fix below is a pure path-resolution change: it does not alter which files on disk these scripts read from or write to, and does not touch the checkpoint, Gold Set, or benchmark results those scripts previously produced.

**Fix applied:** every affected file now resolves the repository root at runtime the same way `dataset_tools/master_pipeline/config.py` and `dataset_tools/supervision/independent_audit/run_audit.py` already did — `REPO_ROOT = Path(__file__).resolve().parent(.parent...)` walked up to the repo root — and builds all data/report paths from that, and imports switched from `from ARCHI_AI.dataset_tools... import ...` to the direct `from dataset_tools... import ...` form (with `REPO_ROOT` added to `sys.path` instead of a synthetic `ARCHI_AI` path segment). No external researcher needs to recreate the `ARCHI_AI/` symlink layout anymore; these scripts now run correctly from a plain `git clone` given the same repo-root-relative `dataset/` and `experiments/` layout `master_pipeline` already assumed.
