# AXIS ? RunPod Phase 2: Dataset Availability Audit (`DATASET_AUDIT.md`)

> **Run ID:** `RUN-009-DATASET_AUDIT`  
> **Timestamp:** 2026-09-22 22:35:00 UTC  
> **Host Environment:** RunPod Instance `territorial_green_minnow` (`kqgdq6zb1022eu`)  
> **Audit Classification:** **`RUNTIME_TEST_CORPUS`**  
> **Audit Status:** **PASS (STRICT FORENSIC AUDIT)**

---

## 1. Executive Summary & Explicit Classification

Following a comprehensive, read-only audit of all filesystems, mounted volumes, directory trees, and cached directories on this Pod instance, the available dataset is formally and explicitly classified as:

$$\mathbf{RUNTIME\_TEST\_CORPUS}$$

**No real scientific training corpus is present on the machine.** Claims that this runtime environment contains Master Dataset v2 or that training on this environment represents foundation architectural adaptation are factually false and strictly prohibited under Absolute Rule #3.

---

## 2. Quantitative Census of Datasets

| Dimension | Count | Note |
| :--- | :---: | :--- |
| **Training Records** | **20** | `/workspace/AXIS/experiment_package/dataset/train.jsonl` |
| **Validation Records** | **5** | `/workspace/AXIS/experiment_package/dataset/validation.jsonl` |
| **Test Records** | **0** | No `test.jsonl` exists in package |
| **Total JSONL Records** | **25** | Combined training + validation |
| **Physical Image Files** | **25** | `images/archi_001.jpg` through `archi_025.jpg` |
| **Unique Image Checksums (SHA256)** | **1** | Only **1 unique image** exists |
| **Duplicate Image Files** | **24** | 24 out of 25 files are redundant bitwise duplicates |
| **Image Resolution / Color** | 1024x768, RGB, JPEG | Size: 159,688 bytes |
| **Origin Fixture** | `test_images/sample_interior.jpg` | SHA256: `e6b036c6081a5c4f4219173c238d02beec00e00216e3dbbc5782230b95f3e350` |

---

## 3. Provenance Boundaries & Legal Quarantine

* **Master Dataset v2 Isolation:** The full 65,342-sample Master Dataset v2 (comprising 53,720 training assets across 14 cleared sources) is **not present** on the pod.
* **FloorPlanCAD Exclusion:** Confirmed **0 FloorPlanCAD records** or images present. The legal quarantine under `LEGAL_REVIEW_REQUIRED` remains 100% intact.
* **Gold Set V3 Sanctuary:** Manifest SHA256 `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`. Confirmed **0 Gold Set samples** consumed or present in the training splits.
* **Cleared Configuration Integrity:** `configs/training_corpus_cleared.json` verified with SHA256 `5fd39698864be5facb1f07c7f44829da65d8e065da1324f1787f9da358d05d49`.

---

## 4. Modality and Distribution Breakdown

* **Modalities:** 100% of records are multimodal image-text conversational pairs (formatted with `system`, `user`, and `assistant` turns).
* **Category Breakdown:**
  - `ANALYSE D'ESPACE`: 5 records (20%)
  - `STYLE / MATERIAUX / AMBIANCE`: 5 records (20%)
  - `ERGONOMIE / CIRCULATION`: 5 records (20%)
  - `CRITIQUE DE PROJET`: 5 records (20%)
  - `PROPOSITION D'AM?LIORATION`: 5 records (20%)
* **Space Types in Prompts:** `salon` (11), `espace ext?rieur` (2), `salle de bain` (3), `cuisine` (3), `petit espace` (3), `bureau` (1), `chambre` (1), `espace ouvert` (1).
* **Grounding Anomaly:** While the text prompts refer to various space types (e.g. bathroom, exterior terrace, kitchen), the visual input provided to the vision encoder is invariably the living room photograph `sample_interior.jpg`. Thus, visual grounding is nonexistent.

---

## 5. Decision Gate Implication (Phase 3)

Because the available dataset is classified as **`RUNTIME_TEST_CORPUS`**, the protocol dictates selecting:

$$\mathbf{PATH\ B\ ?\ ONLY\ RUNTIME\ TEST\ CORPUS\ AVAILABLE}$$

Under Path B, no large-scale training runs will be launched. Instead, the remaining GPU session will be utilized strictly for high-value engineering ablations and inference benchmarks that resolve concrete technical questions without misrepresenting data scale.
