# RUN-020 — Scientific Generalization & Falsification Benchmark

> **Canonical Run ID:** `RUN-020-SCIENTIFIC-GENERALIZATION`  
> **Scientific Phase:** Phase 5 — Scientific Falsification & Visual Ablation  
> **Date:** 2026-09-23  
> **Evaluated Model:** `RUN-019-FIRST-REAL-DATA-QLORA` adapter on `Qwen/Qwen2-VL-7B-Instruct`  
> **Status:** **COMPLETE** | **SCIENTIFIC HYPOTHESIS: FALSIFIED**  
> **Evidence Directory:** [`RUN-020-SCIENTIFIC-GENERALIZATION/`](../../../RUN-020-SCIENTIFIC-GENERALIZATION/)  

---

## 1. Objective

To subject the trained RUN-019 checkpoint to rigorous scientific falsification testing across three core questions:
1. Does the model generalize its architectural critique capability to unseen floorplans?
2. Does the model demonstrate measurable spatial or geometric understanding?
3. Does the model causally depend on visual image pixels, or does it exploit linguistic shortcuts?

---

## 2. Evaluation Datasets & Counterfactual Benchmark

- **Held-Out Test Set:** 127 unseen architectural plans from `REAL_DATA_PILOT/test.jsonl` (125 RPLAN rasters, 2 ResBIM paired units; zero training overlap).
- **Ablation Benchmark (EVAL-D):** 10 representative test plans evaluated across 5 controlled visual conditions:
  1. `ORIGINAL`: Pristine floorplan image.
  2. `BLACK`: Image replaced with 100% black pixels (`RGB = 0, 0, 0`).
  3. `ARCHITECTURAL_MASK`: Building perimeter and walls selectively masked out.
  4. `UNIFORM_NOISE`: Pixels replaced with random Gaussian/uniform noise.
  5. `TEXT_ONLY`: Prompt executed without any image input tensor.

---

## 3. Empirical Results & Falsification Findings

### 3.1. Generalization vs Template Memorization
- **Format Adherence:** RUN-019 achieved **80.2%** adherence to the 5-heading critique format (vs 0.0% for the zero-shot Base Model).
- **Template Reproduction:** On the 125 unseen RPLAN test plans, RUN-019 produced responses with **85.3% lexical and structural similarity** to the canonical training template.
- **ID Hallucination Rate:** **100.0%** of generated critiques fabricated a numerical plan identifier (e.g., `20220`, `1012`, `50001`) copied directly from the training split rather than reflecting the real asset.

### 3.2. Counterfactual Visual Ablation (Visual Dependency)

The lexical and semantic similarity between responses generated on the `ORIGINAL` image versus perturbed conditions was measured:

| Visual Condition | Base Model Similarity to Original | RUN-019 Similarity to Original | Scientific Interpretation |
| :--- | :---: | :---: | :--- |
| **`BLACK` (100% Black)** | **4.3%** | **92.0%** | RUN-019 produces the same critique with no image |
| **`ARCHITECTURAL_MASK`** | **6.2%** | **95.3%** | Masking walls does not alter the generated critique |
| **`UNIFORM_NOISE`** | **0.9%** | **90.6%** | Replacing image with pure noise has almost no effect |
| **`TEXT_ONLY` (No Image)** | N/A | **95.7%** | Response is fully generated from the text prompt alone |

$$\text{VDI} \approx \frac{1.0}{0.957} \approx 1.04 \quad (\text{Threshold: } \ge 3.0)$$

---

## 4. Scientific Conclusion

> [!CAUTION]
> **Falsification Verdict:**  
> The hypothesis that RUN-019 acquired architectural visual understanding was **decisively falsified**.
> - The -98.59% loss reduction observed during Phase 4 training was an artifact of language prior shift and deterministic template memorization.
> - The model's visual dependency was **quasi-null** ($\text{VDI} \approx 1.0$).
> - The model exhibited systematic hallucinations, injecting arbitrary training identifiers into unfamiliar plans.

---

## 5. Architectural Decision & Next Step

- **Decision (Gate 8):** Terminate unstructured paragraph-level architectural critique training.
- **Strategic Pivot:** Transition to **Phase 6A (Spatial Supervision)**:
  1. Eliminate narrative text templates entirely.
  2. Formulate discrete, falsifiable spatial queries (Directional relations, Door connectivity, Room/Door cardinality, Multi-hop path reachability).
  3. Enforce 100% `VISUAL_REQUIRED` tasks to mandate causal image parsing.
