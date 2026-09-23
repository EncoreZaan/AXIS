# RUN-023 — Scientific Evaluation & Spatial Generalization Protocol

> **Target Experiment:** `RUN-023-SPATIAL-GENERALIZATION-EVAL`  
> **Status:** **PREPARED — NOT YET LAUNCHED** (`RUN-023_STARTED: NO`)  
> **Governing Script:** `scripts/evaluate_phase6b.py`  
> **Target Checkpoint:** `RUN-022-SPATIAL-GROUNDING-PILOT/final_adapter` (`71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`)  
> **Baseline Model:** `Qwen/Qwen2-VL-7B-Instruct` @ `eed13092ef92e448dd6875b2a00151bd3f7db0ac`  
> **Comparison Adapter:** `RUN-019-FIRST-REAL-DATA-QLORA/final_adapter`  
> **Baseline Commit:** `f4d5e949053743d97091ea35080de5d365899df7`  

---

## 1. Scientific Objectives

RUN-023 is designed to empirically evaluate whether the spatial supervision fine-tuning in RUN-022 produced genuine architectural visual grounding or merely memorized statistical co-occurrences.

The protocol rigorously tests:
1. Spatial task accuracy across 6 fine-grained architectural tasks;
2. Visual Dependency Index (VDI) across 5 visual ablation conditions;
3. Hallucination rate regarding non-existent rooms or connectivity;
4. Adherence to structured JSON schemas;
5. Cross-model comparison against Base Model (zero-shot) and RUN-019 (unsupervised real-data pilot);
6. Qualitative blind evaluation.

---

## 2. Test Dataset Isolation & Sanctuary

- **Held-Out Test Set:** `RUN-021-SPATIAL-SUPERVISION/test.jsonl`
- **Total Test Samples:** 1,006 instances
- **Test Set SHA-256:** `aaba73433c9ccea7a5c6134154577ea80591e23755665794bec603ebdf53053f`
- **Isolation Guarantee:** Zero test samples were present in the training set (`train.jsonl`) or validation set (`validation.jsonl`).
- **No Test Contamination:** No test data has been or will ever be exposed during training or hyperparameter tuning.

---

## 3. Evaluated Tasks

The test benchmark evaluates 6 fundamental spatial reasoning capabilities:

1. **Directional Relations:**
   - Spatial orientations (`ABOVE`, `BELOW`, `LEFT_OF`, `RIGHT_OF`) between annotated rooms.
2. **Door Connectivity:**
   - Direct physical door access between two designated spaces (positive and negative pairs).
3. **Room Adjacency:**
   - Topological wall-sharing and immediate spatial contiguity.
4. **Cardinality:**
   - Accurate counting of total rooms and total exterior/interior doors without hallucination.
5. **Shortest Path Reachability:**
   - Multi-hop discrete pathfinding across architectural floor plans (number of intervening doors).
6. **Circulation Hub Identification:**
   - Detection and bounding box localization of primary circulation spaces (corridors, vestibules) with maximum connectivity.

---

## 4. Visual Dependency Index (VDI) Protocol

To confirm causal dependency on image pixels rather than language prior exploitation, models are subjected to 5 image perturbation conditions on a deterministic 100-sample test subset (Seed 42):

1. **`ORIGINAL`:** Untouched floor plan image.
2. **`BLACK`:** Complete zero-fill image ablation ($0 \times 0 \times 0$).
3. **`MASKED`:** Architectural boundary mask (walls preserved, interior furnishings/labels removed).
4. **`NOISE`:** High-entropy Gaussian noise perturbation.
5. **`TEXT_ONLY`:** Vision encoder bypassed; question text and metadata provided alone.

### Formal VDI Formulation
Strictly derived from `RUN-021-SPATIAL-SUPERVISION/SCIENTIFIC_DESIGN_REPORT.md` (§ "Indicateur de Dépendance Visuelle (VDI)"):

$$\text{VDI} = \frac{\text{Acc}_{\text{original}}}{\max(\text{Acc}_{\text{black}}, \text{Acc}_{\text{text\_only}})}$$

- **Threshold for Passing Visual Grounding:** $\text{VDI} \ge 3.0$
- **Baseline Expectation:** $\text{VDI} \approx 1.0$ indicates zero visual dependence (language prior shortcut).

---

## 5. Hallucination & Format Adherence Metrics

1. **Hallucination Rate:**
   - Fraction of responses referencing invalid, unannotated, or out-of-range room IDs, non-existent doors, or imaginary connections.
2. **Format Adherence:**
   - Percentage of responses matching valid JSON parseable syntax matching task schema.

---

## 6. Blind Qualitative Evaluation

- 10 deterministic test samples across diverse floor plan topologies.
- Outputs from Base Model, RUN-019, and RUN-022 will be anonymized and evaluated side-by-side.

---

## 7. Execution Gate Invariants

Prior to executing RUN-023:
1. `RUN_022_POST_TRAINING_GATE: PASS`
2. `FINAL_CHECKPOINT_HASH: 71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`
3. `RUN_021_UNMODIFIED: YES`
4. `MASTER_DATASET_UNMODIFIED: YES`
5. `GOLD_SET_UNMODIFIED: YES`
6. `BASELINE_COMMIT_UNMODIFIED: YES`
7. Explicit user approval to launch the evaluation.
