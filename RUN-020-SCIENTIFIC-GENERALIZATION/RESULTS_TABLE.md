# AXIS Phase 5 — Scientific Evaluation Results Table (`RUN-020`)

> **Evaluated Checkpoint:** `RUN-019-FIRST-REAL-DATA-QLORA` (final_adapter)  
> **Base Model:** `Qwen/Qwen2-VL-7B-Instruct` @ `eed13092ef92e448dd6875b2a00151bd3f7db0ac`  
> **Git Commit Baseline:** `f4d5e949053743d97091ea35080de5d365899df7`  
> **Seed:** 42 | **Decoding:** Greedy (`do_sample=False`, `max_new_tokens=256`)  

---

## 1. Disaggregated Metric Performance

| Evaluation Axis | Metric Dimension | BASE MODEL | RUN-019 MODEL | Delta / Verdict |
| :--- | :--- | :---: | :---: | :---: |
| **EVAL-A (In-Domain)** | Format Adherence (5 Sections) | 0.0 % | **80.2 %** | +80.2 % |
| **EVAL-A (In-Domain)** | Mean Word Count | 161.0 words | 139.9 words | Target Length Reached |
| **EVAL-A (In-Domain)** | Canonical Template Similarity | 1.5 % | **85.3 %** | Strong Template Memorization |
| **EVAL-A (In-Domain)** | Unique Responses (125 RPLAN) | 125 / 125 | **41 / 125** | High Redundancy (Normalized: 2 template) |
| **EVAL-A (In-Domain)** | ID Hallucination Rate | 0.0 % | **100.0 %** | Model invents IDs from training |
| **EVAL-B (Cross-Source)** | Unseen ResBIM Generalization | N/A | N/A | **NOT_AVAILABLE** (All 10 absorbed) |
| **EVAL-C (Spatial)** | Numerical Distance (MAE/RMSE)| N/A | N/A | **METRIC_UNAVAILABLE** (No GT coords) |
| **EVAL-C (Spatial)** | Layout-Specific Grounding | High | Invariant | No spatial differentiation |
| **EVAL-D (Vision)** | Similarity: Original vs Solid Black | 4.3 % | **92.0 %** | Invariant to visual ablation |
| **EVAL-D (Vision)** | Similarity: Original vs Masked Floorplan | 6.2 % | **95.3 %** | Invariant to floorplan removal |
| **EVAL-D (Vision)** | Similarity: Original vs Noise | 0.9 % | **90.6 %** | Invariant to visual noise |
| **Control (Text-Only)**| Similarity: Original vs No-Image | 8.9 % | **95.7 %** | Invariant to complete image omission |
| **EVAL-E (Gold Set)** | Blind Benchmark Evaluation | N/A | N/A | **BLOCKED / NOT_AVAILABLE** |

---

## 2. Anti-Leakage & Reproducibility Matrix

| Audit Dimension | Measured Status | Standard | Verdict |
| :--- | :---: | :---: | :---: |
| Test $\cap$ Train ID Overlap | 0 | 0 | **PASS** |
| Test $\cap$ Val ID Overlap | 0 | 0 | **PASS** |
| Image Bit-Exact Hash Overlap | 0 | 0 | **PASS** |
| LoRA Adapter SHA-256 Match | `409d...5f22` | Exact Match | **PASS** |
| Bit-Exact Reproducibility Check | 3 / 3 (100 %) | 100 % | **PASS** |
