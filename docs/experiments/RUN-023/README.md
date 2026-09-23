# RUN-023 — Spatial Generalization & Visual Grounding Evaluation

> **Canonical Run ID:** `RUN-023-SPATIAL-GENERALIZATION-EVAL`  
> **Scientific Phase:** Phase 6B — Spatial Grounding & Visual Dependency Benchmark  
> **Date:** 2026-09-23  
> **Evaluated Model:** `RUN-022-SPATIAL-GROUNDING-PILOT/final_adapter` on `Qwen/Qwen2-VL-7B-Instruct`  
> **Adapter SHA-256:** `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`  
> **Status:** **EVALUATION_COMPLETED** | **VDI_PASS: NO**  
> **Evidence Directory:** [`RUN-023-SPATIAL-GENERALIZATION-EVAL/`](../../../RUN-023-SPATIAL-GENERALIZATION-EVAL/)  

---

## 1. Objective & Pre-Registered Protocol

RUN-023 executed the definitive empirical evaluation of the spatial reasoning capabilities and visual dependency acquired during RUN-022.

Governed by [`RUN_023_PROTOCOL.md`](../../../RUN-022-SPATIAL-GROUNDING-PILOT/RUN_023_PROTOCOL.md) and [`docs/experiments/RUN-023_EVALUATION_PROTOCOL.md`](../RUN-023_EVALUATION_PROTOCOL.md), the benchmark evaluated:
1. Exact accuracy across 6 core architectural spatial tasks.
2. Visual Dependency Index ($\text{VDI}$) across 5 counterfactual image ablation conditions.
3. ID hallucination and training set memorization rates.
4. Syntactic formatting and JSON schema adherence.
5. Bit-exact reproducibility under Seed 42.

---

## 2. Pre-Audit & Smoke Test

Before evaluating the test split, two mandatory verification gates were passed:
1. **Pre-Audit ([`PRE_AUDIT.md`](../../../RUN-023-SPATIAL-GENERALIZATION-EVAL/PRE_AUDIT.md)):**
   - Held-out test set verified: 1,006 samples (SHA-256: `aaba73433c9ccea7a5c6134154577ea80591e23755665794bec603ebdf53053f`).
   - Cross-split contamination verified: $\text{Train} \cap \text{Test} = \emptyset$ (0 example, 0 asset, 0 image hash leaks).
   - Adapter hash verified: `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`.
2. **Smoke Test ([`SMOKE_TEST.md`](../../../RUN-023-SPATIAL-GENERALIZATION-EVAL/SMOKE_TEST.md)):**
   - 392 LoRA tensors attached to 4-bit NF4 base model.
   - Processor configured: `min_pixels: 200704`, `max_pixels: 262144`.
   - Sample inference verified; pre/post inference parameter hashes confirmed **100% bit-identical (zero weight mutation)**.

---

## 3. Comprehensive Evaluation Results (1,006 Samples)

Comparative performance across zero-shot Base Model, RUN-019, and RUN-022:

| Task Dimension | Base Model (Zero-Shot) | RUN-019 (Real Data Pilot) | RUN-022 (Spatial Pilot) | Delta vs Base | Delta vs RUN-019 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Directional Relations** | 3.20% | 10.40% | **98.40%** | **+95.20 pp** | **+88.00 pp** |
| **Door Connectivity (Positive)** | 100.00% | 98.40% | **92.80%** | -7.20 pp | -5.60 pp |
| **Door Connectivity (Negative)** | 0.00% | 2.40% | **95.20%** | **+95.20 pp** | **+92.80 pp** |
| **Room Adjacency** | 0.00% | 0.00% | **94.00%** | **+94.00 pp** | **+94.00 pp** |
| **Room Cardinality** | 7.20% | 6.40% | **67.20%** | **+60.00 pp** | **+60.80 pp** |
| **Door Cardinality** | 5.60% | 9.60% | **71.20%** | **+65.60 pp** | **+61.60 pp** |
| **BIM Cardinality** | 16.67% | 0.00% | **66.67%** | **+50.00 pp** | **+66.67 pp** |
| **Multi-Hop Reachability** | 0.00% | 0.00% | **80.00%** | **+80.00 pp** | **+80.00 pp** |
| **Circulation Hub Identification**| 0.00% | 0.00% | **0.00%** | +0.00 pp | +0.00 pp |
| **Overall Scientific Grounding** | **14.51%** | **15.81%** | **63.12%** | **+48.61 pp** | **+47.31 pp** |
| **Format Adherence** | **65.61%** | **56.06%** | **100.00%** | **+34.39 pp** | **+43.94 pp** |
| **ID Hallucination Rate** | 0.00% | 100.00% | **0.00%** | 0.00 pp | **-100.00 pp** |

---

## 4. Visual Ablation Benchmark & VDI Analysis

Evaluated on 100 deterministic test samples across 5 counterfactual conditions:

| Condition | Description | Grounding Accuracy | Format Adherence | Hallucination Rate |
| :--- | :--- | :---: | :---: | :---: |
| **`ORIGINAL`** | Pristine floorplan image | **64.00%** | 100.00% | 0.00% |
| **`BLACK`** | 100% black pixels (`RGB = 0, 0, 0`) | **50.00%** | 100.00% | 0.00% |
| **`ARCHITECTURAL_MASK`** | Structural walls/perimeters masked | **46.00%** | 96.00% | 0.00% |
| **`UNIFORM_NOISE`** | Random pixel noise | **51.00%** | 88.00% | 0.00% |
| **`TEXT_ONLY`** | Text prompt without image tensor | **47.00%** | 63.00% | 0.00% |

### Official VDI Calculation

$$\text{VDI} = \frac{\text{Acc}_{\text{original}}}{\max(\text{Acc}_{\text{black}}, \text{Acc}_{\text{text\_only}})} = \frac{64.00}{\max(50.00, 47.00)} = \frac{64.00}{50.00} = 1.28$$

- **Official Threshold:** $\text{VDI} \ge 3.0$
- **Official Verdict:** **`VDI_PASS: NO`**
- **Scientific Meaning:** Visual dependency was not proven. The performance gain cannot be causally attributed to visual processing under the pre-registered metric.

---

## 5. In-Depth Scientific Limitations

### 5.1. Circulation Hub Evaluation Metric Sensitivity
- **Observed Score:** 0.00%.
- **Diagnostic:** The evaluation script required exact integer equality on 4-tuple bounding boxes (`[ymin, xmin, ymax, xmax]`).
- **Observed Behavior:** The model correctly identified the central circulation room and access door count, but predicted coordinates deviated by 2–10 pixels due to integer rounding and rasterization.
- **Enforcement:** The metric was **not** altered retroactively. AXIS records this as an evaluation metric sensitivity limitation.

### 5.2. Text Prompt Coordinate Confounding
- Prompts for directional tasks included room centroid coordinates (e.g., `subject_center: [x1, y1]`, `object_center: [x2, y2]`).
- The model's language backbone was able to perform arithmetic numerical comparisons (e.g., $y_1 < y_2 \implies \text{ABOVE}$) without parsing image patches.
- This creates a 50% baseline accuracy floor under image removal, confounding the VDI measurement.

### 5.3. Human Evaluation Status
- **`HUMAN_BLIND_EVALUATION:`** `NOT_PERFORMED`
- The qualitative comparison in [`qualitative_blind_eval.json`](../../../RUN-023-SPATIAL-GENERALIZATION-EVAL/qualitative_blind_eval.json) is an automated side-by-side benchmark, not a human panel evaluation.

---

## 6. Reproducibility & Cryptographic Hashes

- **Reproducibility Test:** 20/20 bit-exact concordance under Seed 42 (**PASS**).
- **Artifact Hashes (from [`hashes.json`](../../../RUN-023-SPATIAL-GENERALIZATION-EVAL/hashes.json)):**
  - `evaluation_config.json`: `01c0f85607ed953f6c9b955f91f47e3e578361f061c6e3e638a9243c03396342`
  - `results.json`: `c06544bd92353e5a5a4febd7970b560f4f1e3f389fe90063d210e35c79df6ffe`
  - `metrics.json`: `0a8dcaf4b4bcdc84d3792a980284aad24da316f5a366d8a874af6e84a4e51ad3`
  - `predictions.jsonl`: `2db396416ee232ec6977a1321dd62d3af1fb9fa0e3ff42335d9dfe2063c378f8`
  - `summary.json`: `663a1738fa26aa253a9bce7e9b03ea8cba5ca329f6b8f4b62d574ff4ec14ad98`
  - `visual_dependency.json`: `5d987f42b5b2b6426ee96bc6da6a966c28062bfe9d672a1f96086f8ef91d8db3`
  - `hallucination_analysis.json`: `9952eb2d5cec26fa71cc6e31be32e1ded4a47e847c8b711cf7ab78f8a248ad85`
  - `reproducibility.json`: `c96eb4efc87f6bb8dcdfad1e6599854b341289fbbe7f0a2e8ac22bc70624bbab`
  - `qualitative_evaluation.json`: `73cb43ec0294d1e380dec8f391bbaba684440c2d19cd24fed7c2dd78e444e670`
  - `EVALUATION_REPORT.md`: `589b36a2bab6cb04230e7a2675508dbba09ebefbc4acb40c22fcae8eff539154`
  - `WALKTHROUGH.md`: `694d45f162e029cbd8af501e831959654da737476f99c911f544beec3c6043cd`
  - `RUN-023_eval.log`: Captured live execution log (~7.1 KB).

---

## 7. Sanctuary Verification

All sanctuarized assets were verified before and after evaluation:
- `RUN-021-SPATIAL-SUPERVISION/train.jsonl`: **UNMODIFIED** (`227ba7db...`)
- `RUN-021-SPATIAL-SUPERVISION/validation.jsonl`: **UNMODIFIED** (`c543a319...`)
- `RUN-021-SPATIAL-SUPERVISION/test.jsonl`: **UNMODIFIED** (`aaba7343...`)
- `RUN-021-SPATIAL-SUPERVISION/dataset_config.json`: **UNMODIFIED** (`9c0908c4...`)
- `RUN-022-SPATIAL-GROUNDING-PILOT/final_adapter`: **UNMODIFIED** (`71c3f3ea...`)
- Baseline Commit: **UNMODIFIED** (`f4d5e949053743d97091ea35080de5d365899df7`)
- `Master Dataset v2`: **UNTOUCHED**
- `Gold Set V3`: **UNTOUCHED**

---

## 8. Conclusion & Next Authorized Step

- **Conclusion:** RUN-023 proves that spatial supervision resolves the failure modes of RUN-019, delivering substantial gains on discrete spatial queries (+48.61 pp) with 100% format adherence and 0% ID hallucination. However, because $\text{VDI} = 1.28 < 3.0$, visual dependency has not been demonstrated.
- **Next Authorized Step:** Maintain `TRAINING_ALLOWED: NO`. Await explicit human validation before designing Phase 7 protocols.
