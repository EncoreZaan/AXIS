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
| `CORE_RPLAN` | 2D Floorplan Rasters (256x256) | 30,002 | **ACTIVE** | Academic Research Only | Plan topology & room reading |
| `CORE_IL3D` | 3D Interior Scenes & Objects | 27,820 | **ACTIVE** | Academic Research Only | 3D Cartesian coordinates & clearance |
| `CORE_STRUCTSCAN3D` | RGB-D Scans & Bounding Boxes | 7,814 | **ACTIVE** | Open Research | Subjective perspective & depth |
| `CORE_FLOORPLANCAD` | CAD Vector Drawings | 741 | **QUARANTINED** | CC-BY-SA 4.0 | Quarantined (`LEGAL_REVIEW_REQUIRED`) |
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

### 3.2. FloorPlanCAD Legal Quarantine
- **Status:** `LEGAL_REVIEW_REQUIRED`.
- **Enforcement:** All 741 CAD vector drawings remain strictly isolated from training splits until legal clearance is completed.

---

## 4. Controlled Subsets: Dataset A (Phase 4)

Built from `CORE_RPLAN` and `CORE_IL3D` to test 4 approved tasks without dataset contamination:
- **Dataset A-Small:** 800 examples (640 train / 80 val / 80 test)
- **Dataset A-Medium:** 2,400 examples (1,920 train / 240 val / 240 test)
- **Dataset A-Full:** 6,000 examples (4,800 train / 600 val / 600 test)

$$\text{Gold Set V3} \cap \text{Dataset A} = \emptyset$$

---

## 5. Data Access Policy

In compliance with open-source licensing standards and intellectual property restrictions of academic datasets:
- **No Third-Party Raw Assets are Redistributed:** This repository contains ingestion scripts, validation manifests, metadata schemas, and benchmark definitions.
- **Reproduction:** Contributors can download public source datasets directly from their official upstream repositories and run `dataset_tools/acquisition/` to reconstruct the Master Dataset v2 locally.
