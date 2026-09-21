# AXIS — Scientific Evaluation Protocol & Benchmarks

> **Benchmark:** Gold Set V3 & Hard Negatives
> **Integrity Status:** IMMUTABLE, READ-ONLY (as a design constraint on the maintainer's local copy); see [Artifact Availability](#4-artifact-availability) for what is actually publishable.
> **Primary Checkpoint:** `ARCHI-AI-P4-005` (A-Full, seed 42)

---

## 1. Dataset & Split Context

The checkpoint evaluated here (`ARCHI-AI-P4-005`) was trained on **Dataset A-Full**, a controlled 6,000-example subset built from the Master Dataset v2 (see [`DATASET.md`](DATASET.md)). The Master Dataset v2 itself is partitioned as follows:

| Split | Assets | Notes |
| :--- | ---: | :--- |
| Train | 53,720 | |
| Validation | 5,724 | |
| Test | 5,898 | |
| **Subtotal (Train + Val + Test)** | **65,342** | **= the published "65,342 assets" total.** |
| Review queue | 1,563 | **Isolated, held separately — not summed into the 65,342 total above.** Assets awaiting manual QA disposition; excluded from all splits until resolved. |

**Why this needs to be spelled out:** an earlier version of this documentation listed all four numbers side by side without stating that "review" is a separate, non-additive bucket, which reads as if the total were 66,905 (53,720+5,724+5,898+1,563). It is not — the certified total is 65,342, and the review queue is explicitly excluded from it. See [`DATASET.md`, §2](DATASET.md#2-dataset-partitions--anti-leakage-guarantees) for the full anti-leakage split report.

Dataset A-Full (6,000 examples: 4,800 train / 600 val / 600 test) is drawn from `CORE_RPLAN` and `CORE_IL3D` only, with zero overlap with the Gold Set V3 (see §2 below).

---

## 2. The Gold Set V3 Sanctuary

To establish indisputable, falsifiable claims, the evaluation of AXIS relies on a sanctified benchmark:

$$\textbf{Gold Set V3} \quad (n = 200 \text{ certified instances})$$

- **Task 1 (`CLEARANCE_CHECK`):** 100 3D spatial instances testing exact Euclidean distances against official ergonomic standards (Neufert, French PMR accessibility).
- **Task 2 (`ROOM_TOPOLOGY`):** 100 2D plan instances testing connected components, interior partitioning, and topological adjacency.
- **Counterexamples (Hard Negatives):** 200 adversarial instances with near-boundary distances ($\pm 0.02$ m from regulation threshold) designed to defeat superficial threshold heuristics.

### Certified Manifest Cryptographic Hashes:
- **Gold Set V3 Manifest SHA256:**
  `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`
- **Counterexamples Manifest SHA256:**
  `a7991b378e46205e6e639961a9d634dd95661daa22129a89ab0744b73c9414e0`

### Why the Gold Set Must Never Be Modified

1. **Pre-Selection Integrity:** The evaluation checkpoint (`ARCHI-AI-P4-005`) was selected **strictly and exclusively** on Dataset A validation loss before any exposure to Gold Set V3.
2. **Prevention of Goodhart's Law:** Modifying the Gold Set or training on its examples immediately destroys its benchmark validity.
3. **Reproducibility Guarantee:** Any researcher running the evaluation script against `GOLD_V3_MANIFEST.jsonl` must obtain bit-exact metrics matching this report — *provided they have the manifest, which is currently not published; see below.*

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

- **Absolute Error Reduction vs Baseline 0:** **$-2.7222$ m** — i.e. $2.7739 - 0.0517 = 2.7222$ m.
- **Relative MAE Reduction:** **$98.14\%$** — i.e. $\dfrac{2.7739 - 0.0517}{2.7739} = 0.9814$. This is an arithmetic fact about the two MAE values above, not an independent claim; it does not by itself establish generalization beyond this benchmark.
- **Validation → Gold Set MAE Difference:** **$+0.0036$ m** (Validation MAE $0.0481$ m $\to$ Gold MAE $0.0517$ m).
  This figure was previously labeled "Generalization Gap." That label is imprecise: a classical generalization gap compares *training* performance against *held-out* performance within one protocol. Here, both numbers come from held-out sets — Dataset A's internal validation split and the separately-constructed Gold Set V3 — so this is better described as a **cross-benchmark consistency check**: the checkpoint's error on a second, independently sanctified evaluation set is close to its error on the set used for model selection. A small difference here is evidence against overfitting to Dataset A's specific validation split, but it does not demonstrate generalization to out-of-distribution inputs (different sources, sensors, or geographies), which has not been tested.

#### Regulatory Clearance Verdict (Binary Classification)
| Model | Accuracy | Precision | Recall | F1-Score | Confusion Matrix (TP/FP/TN/FN) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline 0 (Trivial "always PASS")** | 99.00% | 99.00% | 100.00% | 99.50% | 99 / 1 / 0 / 0 |
| **Selected Checkpoint (`005`)** | **100.00%** | **100.00%** | **100.00%** | **100.00%** | **99 / 0 / 1 / 0** |

### 3.2. Why "100% Accuracy" Is Not a Robustness Proof

This is the single most important caveat in this document, and it is stated explicitly rather than left implicit in a headline number:

- **The evaluation set is small and heavily imbalanced:** $n = 100$, with **99 positive (PASS) instances and only 1 negative (FAIL) instance.**
- **A trivial baseline already scores 99%.** The table above shows Baseline 0 — a model that always predicts "PASS" regardless of input — achieves 99.00% accuracy on this same set, by construction, because it gets the 99 positives right and only misses the single negative.
- **Consequently, accuracy alone cannot distinguish a genuinely capable model from a model that has simply learned to always say PASS.** The checkpoint's 100.00% accuracy is one percentage point above this trivial floor.
- **What the checkpoint actually demonstrates beyond the trivial baseline** is that it correctly classified the *one* negative instance (moving TN from 0 to 1) *in addition to* the 99 positives, and — more informatively — that its underlying MAE regression (§3.1) is 53× tighter than Baseline 0's. The regression MAE, not the binary accuracy, is the more discriminating metric on this benchmark.
- **The single negative instance means specificity (true-negative rate) is estimated from exactly one example.** A specificity estimate of "100%" from $n=1$ has essentially no statistical power — a single different hard negative could flip it to 0%. No claim about the model's general ability to correctly reject non-compliant designs can be supported by this number alone.
- **This is neither dismissed nor inflated:** the checkpoint did correctly classify every instance in this set, including the one hard case. It is a real, verified result. It is simply not, on its own, evidence of general robustness — that would require a substantially larger and better-balanced held-out set, which does not currently exist for this task.

---

### 3.3. Task 2: `ROOM_TOPOLOGY` ($n = 100$)
- In Phase 4, the micro-pilot trained exclusively the 3D spatial geometry model.
- Because post-hoc fine-tuning on the Gold Set is strictly forbidden, `ROOM_TOPOLOGY` is documented as **`NOT_EVALUATED`** on checkpoint `005`.
- **Baseline 0 Calibration:**
  - Exact Match on room count: **34.00%** (34/100)
  - MAE on room count: **0.7600**
  - MAE on largest room pixels: **1,040.04 px**

---

## 4. Artifact Availability

An external researcher needs to know precisely what they can and cannot obtain from this repository:

| Artifact | Status | Detail |
| :--- | :--- | :--- |
| Gold Set V3 manifest (`GOLD_V3_MANIFEST.jsonl`) | **NOT PUBLIC** | Excluded via `.gitignore` (`dataset/`). Only its SHA256 hash is published here, for verification against an independently-obtained or independently-reconstructed copy — it cannot be downloaded from this repository. |
| Counterexamples manifest (`counterexamples.jsonl`) | **NOT PUBLIC** | Same as above. |
| Checkpoint `ARCHI-AI-P4-005` weights | **NOT PUBLIC** | Excluded via `.gitignore` (`*.pt`, `outputs/`). Only its SHA256 hash and the metrics it produced are published. No release or download link currently exists. Tracked as `PLANNED` in `ROADMAP.md` ("Public Model Checkpoints & Comprehensive Benchmark Suite") with no committed date. |
| Dataset A (Small/Medium/Full) | **NOT PUBLIC** | Derived locally from raw sources; the build script (`dataset_tools/`) is public, its output is not. |
| Baseline 0 evaluation code (`scripts/evaluate_baseline.py`, `evaluation/runners/`) | **PUBLIC** | Present in this repository. |
| Raw upstream source datasets (`RPLAN`, `IL3D`, etc.) | **NOT REDISTRIBUTED** | Available from their own upstream sources under their own licenses; see `DATASET.md`. |

**Practical implication:** the numbers in §3 are independently checkable only insofar as the reader trusts the maintainer's reported measurement, or reconstructs an equivalent Gold Set / checkpoint themselves and compares SHA256 hashes for exact matches. This is a real limitation on third-party falsifiability, stated here explicitly rather than glossed over. See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md#reproducibility-limitations-for-phase-4-step-6) for the practical steps a researcher can still take, and [`DATASET.md`, §6](DATASET.md#6-local-directory-convention-for-the-full-pipeline) for why the scripts that produced these numbers (`dataset_tools/experiments/micro_pilot/`) also require a specific local directory layout not needed by the rest of `dataset_tools`.

---

## 5. Scientific Limitations
- The 0.0517 m MAE proves signal survival on geometric 3D clearance regression, **not** general architectural reasoning.
- The 100% Pass/Fail accuracy on `CLEARANCE_CHECK` is measured on a 99/1 class-imbalanced set of 100 instances and should not be read as a general robustness or specificity claim (§3.2).
- `ROOM_TOPOLOGY` has no trained-model evaluation on the Gold Set — only a Baseline 0 calibration exists.
- Multimodal 2D $\leftrightarrow$ 3D evaluation remains limited by the rarity of genuine paired BIM models (10 pairs in RAW).
- Neither the Gold Set manifest nor the checkpoint weights are currently public (§4), which limits independent third-party verification to hash-matching against an equivalently reconstructed artifact.
