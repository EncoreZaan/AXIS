# AXIS RUN-023 — Pre-Evaluation Audit Report (`PRE_AUDIT.md`)

> **Run Identifier:** `RUN-023-SPATIAL-GENERALIZATION-EVAL`  
> **Audit Date:** 2026-09-23T13:08:00Z  
> **Target Checkpoint:** `RUN-022-SPATIAL-GROUNDING-PILOT/final_adapter`  
> **Audit Status:** **PASS (ALL PRE-CONDITIONS VERIFIED)**  

---

## 1. Cryptographic Forensics & Target Alignment

```text
============================================================
RUN-023 PRE-EVALUATION AUDIT
============================================================
BASELINE_COMMIT:               f4d5e949053743d97091ea35080de5d365899df7
BASE_MODEL:                    Qwen/Qwen2-VL-7B-Instruct
MODEL_REVISION:                eed13092ef92e448dd6875b2a00151bd3f7db0ac
FINAL_ADAPTER_HASH:            71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479
DATASET_CONFIG_HASH:           9c0908c4c2bc25c647cfde7d885e4d8fe9ba507fb00fb79ce42852942ea60d6c
TEST_SET_FILE:                 RUN-021-SPATIAL-SUPERVISION/test.jsonl
TEST_SET_HASH:                 aaba73433c9ccea7a5c6134154577ea80591e23755665794bec603ebdf53053f
TEST_SET_EXAMPLES:             1,006
------------------------------------------------------------
CROSS-SPLIT LEAKAGE VERIFICATION:
  TRAIN ∩ TEST (Examples):     0 (PASS)
  VALIDATION ∩ TEST:           0 (PASS)
  ASSET_ID INTERSECTION:       0 (PASS)
  IMAGE_HASH INTERSECTION:     0 (PASS)
  GOLD_SET_V3 INTERSECTION:    0 (PASS)
============================================================
AUDIT VERDICT:                 PASS (HERMETIC ISOLATION CONFIRMED)
============================================================
```

---

## 2. Integrity Certification

1. **Adapter Immutability:** The adapter weights were verified against the locked SHA-256 hash recorded upon RUN-022 completion.
2. **Hermetic Test Set:** The 1,006 test samples were derived exclusively from `RUN-021-SPATIAL-SUPERVISION/test.jsonl`, having zero exposure during RUN-022 training or validation.
3. **Execution Authorization:** Certified for immediate smoke test execution.
