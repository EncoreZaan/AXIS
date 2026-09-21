# AXIS — Scientific Evaluation Protocol & Benchmarks

> **Benchmark:** Gold Set V3 & Hard Negatives  
> **Integrity Status:** IMMUTABLE, READ-ONLY, BIT-EXACT VERIFIED  
> **Primary Checkpoint:** `ARCHI-AI-P4-005` (A-Full, seed 42)

---

## 1. The Gold Set V3 Sanctuary

To establish indisputable, falsifiable claims, the evaluation of AXIS relies on a sanctified benchmark:

$$\textbf{Gold Set V3} \quad (n = 200 \text{ certified instances})$$

- **Tâche 1 (`CLEARANCE_CHECK`):** 100 3D spatial instances testing exact Euclidean distances against official ergonomic standards (Neufert, French PMR accessibility).
- **Tâche 2 (`ROOM_TOPOLOGY`):** 100 2D plan instances testing connected components, interior partitioning, and topological adjacency.
- **Counterexamples (Hard Negatives):** 200 adversarial instances with near-boundary distances ($\pm 0.02$ m from regulation threshold) designed to defeat superficial threshold heuristics.

### Certified Manifest Cryptographic Hashes:
- **Gold Set V3 Manifest SHA256:**  
  `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`
- **Counterexamples Manifest SHA256:**  
  `a7991b378e46205e6e639961a9d634dd95661daa22129a89ab0744b73c9414e0`

---

## 2. Why the Gold Set Must Never Be Modified

1. **Pre-Selection Integrity:** The evaluation checkpoint (`ARCHI-AI-P4-005`) was selected **strictly and exclusively** on Dataset A validation loss before any exposure to Gold Set V3.
2. **Prevention of Goodhart's Law:** Modifying the Gold Set or training on its examples immediately destroys its benchmark validity.
3. **Reproducibility Guarantee:** Any researcher running the evaluation script against `GOLD_V3_MANIFEST.jsonl` must obtain bit-exact metrics matching this report.

---

## 3. Verified Benchmark Results

### 3.1. Task 1: `CLEARANCE_CHECK` ($n = 100$)

#### Distance Error Regression (Meters)
| Model / Configuration | MAE (m) | Median (m) | Std Dev (m) | RMSE (m) | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline 0 (Trivial Constant)** | **2.7739 m** | 1.2200 m | 2.6915 m | 3.8649 m | [2.2850, 3.3210] |
| **Model A-Small (`001`)** | 0.4663 m | 0.2609 m | 0.6361 m | 0.7887 m | [0.3540, 0.6010] |
| **Model A-Medium (`004`)** | 0.1699 m | 0.1082 m | 0.2114 m | 0.2712 m | [0.1320, 0.2160] |
| **Selected Checkpoint A-Full (`005`)** | **0.0517 m** | **0.0412 m** | **0.0476 m** | **0.0703 m** | **[0.0428, 0.0616]** |

- **Absolute Error Reduction vs Baseline 0:** **$-2.7222$ m**
- **Relative Precision Gain:** **$+98.14\%$**
- **Generalization Gap:** **$+0.0036$ m** (Validation MAE $0.0481$ m $\to$ Gold MAE $0.0517$ m, certified as LOW GAP).

#### Regulatory Clearance Verdict (Binary Classification)
| Model | Accuracy | Precision | Recall | F1-Score | Confusion Matrix (TP/FP/TN/FN) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline 0** | 99.00% | 99.00% | 100.00% | 99.50% | 99 / 1 / 0 / 0 |
| **Selected Checkpoint (`005`)** | **100.00%** | **100.00%** | **100.00%** | **100.00%** | **99 / 0 / 1 / 0** |

---

### 3.2. Task 2: `ROOM_TOPOLOGY` ($n = 100$)
- In Phase 4, the micro-pilot trained exclusively the 3D spatial geometry model.
- Because post-hoc fine-tuning on the Gold Set is strictly forbidden, `ROOM_TOPOLOGY` is documented as **`NOT_EVALUATED`** on checkpoint `005`.
- **Baseline 0 Calibration:**
  - Exact Match on room count: **34.00%** (34/100)
  - MAE on room count: **0.7600**
  - MAE on largest room pixels: **1,040.04 px**

---

## 4. Scientific Limitations
- The 0.0517 m MAE proves signal survival on geometric 3D clearance regression, **not** general architectural reasoning.
- Multimodal 2D $\leftrightarrow$ 3D evaluation remains limited by the rarity of genuine paired BIM models (10 pairs in RAW).
