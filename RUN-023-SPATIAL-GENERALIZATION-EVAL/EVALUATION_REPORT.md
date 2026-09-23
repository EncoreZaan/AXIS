# AXIS RUN-023 — Scientific Spatial Grounding Evaluation Report

> **Experiment ID:** `RUN-023-SPATIAL-GENERALIZATION-EVAL`  
> **Evaluated Checkpoint:** `RUN-022-SPATIAL-GROUNDING-PILOT/final_adapter` (`71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`)  
> **Evaluation Dataset:** `RUN-021-SPATIAL-SUPERVISION/test.jsonl` (1,006 held-out samples)  
> **Date:** 2026-09-23T15:39:35.154449+00:00  
> **Status:** **EVALUATION_COMPLETED**  

---

## 1. Executive Scientific Summary

RUN-023 conducted a rigorous empirical evaluation of the architectural spatial reasoning and visual dependency acquired during RUN-022 fine-tuning on `Qwen/Qwen2-VL-7B-Instruct`.

```
========================================
AXIS — RUN-023 SCIENTIFIC EVALUATION
========================================
STATUS: EVALUATION_COMPLETED
TEST_EXAMPLES: 1006
MODEL: Qwen/Qwen2-VL-7B-Instruct
ADAPTER: RUN-022-SPATIAL-GROUNDING-PILOT/final_adapter
ADAPTER_HASH: 71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479
DIRECTIONAL_ACCURACY: 98.40%
CONNECTIVITY_ACCURACY: 94.00% (Pos: 92.80%, Neg: 95.20%)
ADJACENCY_ACCURACY: 94.00%
CARDINALITY_ACCURACY: 69.20% (Rooms: 67.20%, Doors: 71.20%)
SHORTEST_PATH_ACCURACY: 80.00%
CIRCULATION_HUB_ACCURACY: 0.00%
FORMAT_ADHERENCE: 100.00%
SCIENTIFIC_GROUNDING_ACCURACY: 63.12%
ORIGINAL_ACCURACY: 64.00%
BLACK_ACCURACY: 50.00%
MASK_ACCURACY: 46.00%
NOISE_ACCURACY: 51.00%
TEXT_ONLY_ACCURACY: 47.00%
VDI: 1.28
VDI_THRESHOLD: 3.0
VDI_PASS: NO
ID_HALLUCINATION_RATE: 0.00%
TRAINING_ID_REUSE_RATE: 0.00%
REPRODUCIBILITY: PASS (20/20 bit-exact)
HUMAN_BLIND_EVALUATION: NOT_PERFORMED
BASELINE_COMPARISON: COMPLETED
RUN_021_UNMODIFIED: YES
MASTER_DATASET_UNMODIFIED: YES
GOLD_SET_UNMODIFIED: YES
BASELINE_COMMIT_UNMODIFIED: YES
FINAL_ADAPTER_UNMODIFIED: YES
ARTIFACTS_HASHED: YES
DOCUMENTATION_COMPLETE: YES
SCIENTIFIC_CONCLUSION: Grounding and visual dependency evaluated across all 6 core spatial tasks.
LIMITATIONS: Text-only baseline exploitation on discrete closed prompts; manual human visual review not performed.
NEXT_STEP: Await explicit human validation before progressing to Phase 7.
========================================
```

---

## 2. Spatial Task Performance Breakdown (1,006 Samples)

| Task Dimension | Base Model (Zero-Shot) | RUN-019 (Real Data Pilot) | RUN-022 (Spatial Pilot) | Delta (RUN-022 vs Base) |
| :--- | :---: | :---: | :---: | :---: |
| **Directional Relations** | 3.2% | 10.4% | 98.4% | +95.2% |
| **Door Connectivity (Positive)** | 100.0% | 98.4% | 92.8% | -7.2% |
| **Door Connectivity (Negative)** | 0.0% | 2.4% | 95.2% | +95.2% |
| **Room Cardinality** | 7.2% | 6.4% | 67.2% | +60.0% |
| **Door Cardinality** | 5.6% | 9.6% | 71.2% | +65.6% |
| **Multi-Hop Reachability** | 0.0% | 0.0% | 80.0% | +80.0% |
| **Circulation Hub Identification** | 0.0% | 0.0% | 0.0% | +0.0% |
| **Largest Room Identification** | 0.0% | 0.0% | 0.0% | +0.0% |
| **BIM Cardinality** | 16.7% | 0.0% | 66.7% | +50.0% |
| **Overall Scientific Grounding** | **14.51%** | **15.81%** | **63.12%** | **+48.61%** |
| **Overall Format Adherence** | **65.61%** | **56.06%** | **100.00%** | **+34.39%** |

---

## 3. Directional Relations Detailed Analysis

- **Macro-F1:** 0.7322
- **Confusion Matrix:**
```json
{
  "ABOVE": {
    "ABOVE": 90,
    "BELOW": 0,
    "LEFT_OF": 1,
    "RIGHT_OF": 1,
    "UNKNOWN": 0
  },
  "BELOW": {
    "ABOVE": 0,
    "BELOW": 0,
    "LEFT_OF": 0,
    "RIGHT_OF": 0,
    "UNKNOWN": 0
  },
  "LEFT_OF": {
    "ABOVE": 0,
    "BELOW": 0,
    "LEFT_OF": 19,
    "RIGHT_OF": 0,
    "UNKNOWN": 0
  },
  "RIGHT_OF": {
    "ABOVE": 0,
    "BELOW": 0,
    "LEFT_OF": 0,
    "RIGHT_OF": 14,
    "UNKNOWN": 0
  }
}
```

---

## 4. Visual Dependency Index (VDI) Analysis

Evaluated on 100 deterministic test samples across 5 conditions:

| Perturbation Condition | Grounding Accuracy | Format Adherence | Hallucination Rate |
| :--- | :---: | :---: | :---: |
| **`ORIGINAL`** | 64.00% | 100.00% | 0.00% |
| **`BLACK`** | 50.00% | 100.00% | 0.00% |
| **`ARCHITECTURAL_MASK`** | 46.00% | 96.00% | 0.00% |
| **`UNIFORM_NOISE`** | 51.00% | 88.00% | 0.00% |
| **`TEXT_ONLY`** | 47.00% | 63.00% | 0.00% |

$$	ext{VDI} = rac{	ext{Acc}_{	ext{original}}}{\max(	ext{Acc}_{	ext{black}}, 	ext{Acc}_{	ext{text\_only}})} = rac{0.64}{0.5} = 1.28$$

- **VDI Status:** **NO** (Threshold: $\ge 3.0$)

---

## 5. Hallucination Analysis

- **ID Hallucination Rate:** 0.00%
- **Training ID Reuse Rate:** 0.00%
- **Any Hallucination Rate:** 0.00%
