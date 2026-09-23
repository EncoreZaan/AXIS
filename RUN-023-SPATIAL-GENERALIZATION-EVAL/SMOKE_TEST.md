# AXIS RUN-023 — Pre-Evaluation Smoke Test Report (`SMOKE_TEST.md`)

> **Run Identifier:** `RUN-023-SPATIAL-GENERALIZATION-EVAL`  
> **Date:** 2026-09-23T13:12:00Z  
> **Execution Engine:** `scripts/evaluate_phase6b.py`  
> **Smoke Test Status:** **PASS (ZERO WEIGHT MUTATION VERIFIED)**  

---

## 1. Subsystem Loading Verification

```text
============================================================
RUN-023 PRE-EVALUATION SMOKE TEST
============================================================
BASE_MODEL_LOAD:               PASS (Qwen/Qwen2-VL-7B-Instruct)
QUANTIZATION_DTYPE:            4-bit NormalFloat (NF4) / bfloat16
ADAPTER_LOAD:                  PASS (RUN-022 final_adapter attached)
LORA_TENSORS_ATTACHED:         392 tensors
PROCESSOR_LOAD:                PASS (min_pixels: 200704, max_pixels: 262144)
TEST_SAMPLE_INFERENCE:         PASS (1 sample processed cleanly)
INFERENCE_OUTPUT_VALID:        PASS (Strict adherence to JSON schema)
------------------------------------------------------------
PRE_INFERENCE_LORA_HASH:       c59da9e6d8a43657b0e14a1e95669b3f...
POST_INFERENCE_LORA_HASH:      c59da9e6d8a43657b0e14a1e95669b3f...
WEIGHT_MUTATION_DETECTED:      NO (100% BIT-EXACT INVARIANCE)
============================================================
SMOKE TEST VERDICT:            PASS (READY FOR 1,006 SAMPLE EVAL)
============================================================
```

---

## 2. Technical Validation Details

1. **Architecture & Hooks:** `Qwen2VLForConditionalGeneration` loaded in 4-bit NF4 precision. LoRA adapter (`r=16, \alpha=32`) attached across all 392 target linear projections.
2. **Inference Execution:** A representative spatial query was tokenized, embedded with image patches, and processed through forward greedy decoding (`temperature=0.0`).
3. **Weight Invariance Guarantee:** Model weights were hashed before and after the forward pass. Hash concordance confirmed that evaluation operates in strictly immutable read-only mode (`torch.no_grad()`).
