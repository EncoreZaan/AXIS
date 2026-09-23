# AXIS — Authoritative Current Project & Scientific Status

> **Document Version:** 2.0.0  
> **Last Updated:** 2026-09-23  
> **Governing Commit:** `f4d5e949053743d97091ea35080de5d365899df7` (`f4d5e94`)  
> **Scientific Integrity Policy:** Strictly verifiable, falsifiable, and traceable against physical artifacts.

---

## 1. Executive Summary

**AXIS** (*Architectural eXtensible Intelligence System*) is an open-source, reproducible artificial intelligence research initiative developing vision-language foundation models for architectural reasoning, spatial grounding, and multimodal 2D/3D building understanding.

As of **September 23, 2026**, AXIS has concluded the **Phase 6B Spatial Grounding Pilot** (`RUN-022`) and its comprehensive evaluation (`RUN-023`), establishing significant measurable gains in discrete spatial reasoning while honestly identifying critical methodological boundaries regarding visual dependency.

```text
======================================================================
AXIS RESEARCH CAMPAIGN STATUS SUMMARY (2026-09-23)
======================================================================
LATEST MILESTONE:              RUN-023-SPATIAL-GENERALIZATION-EVAL
BASE MODEL:                    Qwen/Qwen2-VL-7B-Instruct (4-bit NF4)
CHECKPOINT EVALUATED:          RUN-022 final_adapter (LoRA r=16, alpha=32)
ADAPTER SHA-256:               71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479
HELD-OUT TEST SET:             1,006 samples (AXIS_SPATIAL_SUPERVISION_V1)
----------------------------------------------------------------------
OVERALL GROUNDING ACCURACY:    63.12% (+48.61 pp vs 14.51% Base Model)
SYNTAX & FORMAT ADHERENCE:     100.00%
DIRECTIONAL REASONING:         98.40%
DOOR CONNECTIVITY:             94.00% (Positive: 92.80%, Negative: 95.20%)
ROOM & DOOR CARDINALITY:       69.20%
MULTI-HOP REACHABILITY:        80.00%
ID HALLUCINATION RATE:         0.00% (Eradicated vs 100% in RUN-019)
BIT-EXACT REPRODUCIBILITY:     PASS (20/20 bit-exact concordance, seed 42)
----------------------------------------------------------------------
VISUAL DEPENDENCY INDEX (VDI): 1.28
VDI THRESHOLD REQUIRED:        >= 3.0
VDI OFFICIAL VERDICT:          VDI_PASS = NO (Visual dependency unproven)
CIRCULATION HUB ACCURACY:      0.00% (Strict integer bbox equality sensitivity)
HUMAN BLIND EVALUATION:        NOT_PERFORMED (Automated side-by-side)
======================================================================
SANCTUARIES:                   ALL 5 STRICTLY UNMODIFIED & AUDITED
CURRENT OPERATIONAL STATE:     TRAINING_ALLOWED: NO | EVALUATION_COMPLETED
NEXT AUTHORIZED STEP:          AWAIT HUMAN VALIDATION BEFORE PHASE 7
======================================================================
```

---

## 2. Mandatory Status Answers (11 Core Invariants)

1. **What is AXIS?**  
   An AI research initiative building verifiable multimodal foundation models for architectural plan understanding, spatial topology, and metric reasoning.
2. **What has been completed?**  
   Phases 1 through 6B, encompassing dataset sanitization, GPU profiling (RUN-001–RUN-014), real-data pilot (RUN-019), scientific falsification (RUN-020), spatial supervision engineering (RUN-021), 2,310-step pilot training with deterministic resumption (RUN-022), and comprehensive 1,006-sample evaluation (RUN-023).
3. **What is the current scientific state?**  
   Significant empirical advancement on discrete architectural queries (63.12% accuracy vs 14.51% base); however, **causal visual dependency has not been proven** under the official VDI protocol ($\text{VDI} = 1.28 < 3.0$).
4. **What experiments have been run?**  
   RUN-001 through RUN-023. See full registry in [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) and [`docs/SCIENTIFIC_TIMELINE.md`](docs/SCIENTIFIC_TIMELINE.md).
5. **What has been proven?**  
   100% format discipline, elimination of ID hallucinations (0.00%), high directional precision (98.40%), door connectivity (94.00%), multi-hop path reachability (80.00%), and exact numerical reproducibility (20/20 bit-exact).
6. **What has NOT been proven?**  
   Visual grounding / pixel dependency has NOT been proven. General architectural autonomy and metric surface regression have NOT been proven.
7. **What datasets are locked?**  
   `Master Dataset v2` (65,342 assets), `Gold Set V3` (200 items), `REAL_DATA_PILOT` (1,000 assets), and `AXIS_SPATIAL_SUPERVISION_V1` (7,950 examples, config hash `9c0908c4...`).
8. **What checkpoints are locked?**  
   `RUN-019 final_adapter` and `RUN-022 final_adapter` (bit-identical to `checkpoint-2310`, SHA-256: `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`).
9. **What are the current limitations?**  
   VDI 50% binary chance floor; bounding-box text prompt confounding; circulation hub strict integer equality sensitivity; lack of human review.
10. **What is the next authorized step?**  
    Await explicit human validation before launching Phase 7.
11. **Which experiments must NOT be rerun?**  
    RUN-019, RUN-020, RUN-021, RUN-022, and RUN-023 must never be rerun or retrofitted.

---

## 3. Navigation to Canonical Documentation

- **Full Project Status & Q&A:** [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md)
- **Chronological Timeline:** [`docs/SCIENTIFIC_TIMELINE.md`](docs/SCIENTIFIC_TIMELINE.md)
- **Gates & Decision Records:** [`docs/GATES_AND_DECISIONS.md`](docs/GATES_AND_DECISIONS.md)
- **Documentation Policy:** [`docs/DOCUMENTATION_POLICY.md`](docs/DOCUMENTATION_POLICY.md)
- **Detailed Experiment Reports:**
  - [`RUN-019 First Real-Data QLoRA`](docs/experiments/RUN-019/README.md)
  - [`RUN-020 Scientific Falsification`](docs/experiments/RUN-020/README.md)
  - [`RUN-021 Spatial Supervision Dataset`](docs/experiments/RUN-021/README.md)
  - [`RUN-022 Spatial Grounding Pilot`](docs/experiments/RUN-022/README.md)
  - [`RUN-023 Grounding Evaluation`](docs/experiments/RUN-023/README.md)
