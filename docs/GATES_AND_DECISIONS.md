# AXIS — Stage Gates & Decision Records Index

> **Registry ID:** `AXIS-GATE-REG-001`  
> **Last Synchronized:** 2026-09-23T17:45:00Z  
> **Governance:** AXIS Research & Engineering Steering Committee  

---

## Stage Gate & Decision Ledger

| Gate ID | Date | Scope / Phase | Verdict / Status | Cryptographic & Empirical Evidence | Blocking Issues | Decision Taken | Authorized Next Step |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| **GATE-01** | 2026-09-22 | Master Dataset v2 Sanctification | **PASS** | 65,342 assets across 19 sources; 0 cross-split hash leaks; project group isolation verified (`DATASET_SPLIT_REPORT.md`). | None. | Freeze Master Dataset v2 as immutable baseline. | Proceed to environment readiness audit. |
| **GATE-02** | 2026-09-22 | FloorPlanCAD Licensing Review (`PDR-2026-001`) | **QUARANTINED** | Hugging Face metadata (`cc-by-sa-4.0`) vs README lines 109 & 130 (`CC-BY-NC 4.0`). Host site closed in 2022. | Upstream intellectual property contradiction. | Quarantined and permanently excluded from active training corpus (`configs/training_corpus_cleared.json`). | Do not train on FloorPlanCAD until written legal clearance. |
| **GATE-03** | 2026-09-22 | RunPod Environment Readiness | **PASS** | NVIDIA RTX 3090 (24GB), Driver 580.159.04, PyTorch 2.6.0+cu124, commit `f4d5e949053743d97091ea35080de5d365899df7`. | `TRAINING_ALLOWED: NO` at gate time. | Environment declared sound and approved for controlled pilots. | Authorize single-session hardware characterization. |
| **GATE-04** | 2026-09-22 | Phase 2 Pilot Campaign Signoff | **PASS** | RUN-001 through RUN-014 executed; thermal max 58°C; $r=16$ selected; 512px resolution selected. | Runtime test corpus used (25 images, 1 unique hash). | Approved architecture hyperparameter bounds for real data. | Ingest and lock real multi-image dataset. |
| **GATE-05** | 2026-09-22 | RUN-017 Real Data Dataset Lock | **PASS** | 1,000 real assets (990 RPLAN, 10 RESBIM paired). Train: 775, Val: 98, Test: 127. Hashes locked in `RUN-017/hashes.json`. | None. | Formally seal `REAL_DATA_PILOT`. | Execute pre-training dry run. |
| **GATE-06** | 2026-09-22 | RUN-018 Pre-Training Dry Run | **PASS** | Collation validated, forward pass loss finite (1.769), zero optimizer steps, parameter hashes unchanged. | None. | Training pipeline certified functional. | Authorize RUN-019 execution. |
| **GATE-07** | 2026-09-23 | RUN-019 Post-Training Gate | **PASS** | 194 steps (2 epochs). Train loss: 0.0245, Val loss: 0.0232 (-98.59%). Adapter `246e22...` preserved. | None. | Training executed cleanly; certify run completion. | Mandate Phase 5 scientific generalization audit. |
| **GATE-08** | 2026-09-23 | RUN-020 Scientific Falsification Gate | **FALSIFIED** | 85.3% template similarity, 100% ID hallucination, black image similarity 92.0%, text-only similarity 95.7%, $\text{VDI} \approx 1.0$. | Complete lack of visual dependency; template memorization shortcut. | Reject RUN-019 as a valid visual model; halt language prior training. | Design Phase 6A spatial supervision dataset. |
| **GATE-09** | 2026-09-23 | RUN-021 Phase 6A Dataset Lock Gate | **PASS** | 7,950 discrete examples (Train: 6,160, Val: 784, Test: 1,006). 100% VISUAL_REQUIRED. Config SHA256: `9c0908c4...`. | Note: `MANUAL_AUDIT_HUMAN = NOT_PERFORMED`; `AUTOMATED_GEOMETRIC_AUDIT = PASS`. | Formally lock `AXIS_SPATIAL_SUPERVISION_V1`. | Prepare RUN-022 training pilot. |
| **GATE-10** | 2026-09-23 | RUN-022 Pre-Training Preflight Gate | **PASS** | Script `scripts/verify_preflight_gate.py` passed: config verified, GPU addressable, sanctuaries untouched. | None. | Authorize RUN-022 pilot training launch. | Begin training on Qwen2-VL-7B. |
| **GATE-11** | 2026-09-23 | RUN-022 Post-Interruption Resumption Gate | **PASS** | Forensic inspection at step 1000: GPU idle, zero OOM, no crash. Resumed from `checkpoint-750`. Loss matching confirmed. | Loss of unpersisted step 751-1000 buffer (recomputed). | Authorize resumption to step 2310. | Continue training to completion. |
| **GATE-12** | 2026-09-23 | RUN-022 Post-Training Completion Gate | **PASS** | Step 2310/2310 completed. Final train loss: 0.1218, eval loss: 0.1397. Final adapter bit-identical to `checkpoint-2310` (`71c3f3e...`). | Invariant enforced: loss convergence $\ne$ grounding. | Certify training completion; lock RUN-023 protocol. | Execute RUN-023 evaluation suite. |
| **GATE-13** | 2026-09-23 | RUN-023 Pre-Evaluation Audit Gate | **PASS** | Test split verified (1,006 samples, SHA256: `aaba734...`). Zero overlap with train/val. Adapter hash verified (`71c3f3e...`). | None. | Certify evaluation testbed as hermetic and untainted. | Execute smoke test. |
| **GATE-14** | 2026-09-23 | RUN-023 Smoke Test Gate | **PASS** | Model, adapter, processor loaded cleanly. 392 LoRA tensors attached. Test inference executed. Zero parameter drift. | None. | Evaluation pipeline operational. | Launch full 1,006 sample evaluation. |
| **GATE-15** | 2026-09-23 | RUN-023 Post-Evaluation Decision Gate | **CONDITIONAL** | Grounding accuracy 63.12% (+48.61 pp vs base), format 100%, 0% hallucination. BUT $\text{VDI} = 1.28 < 3.0$ threshold (`VDI_PASS: NO`). | Visual dependency not established under current VDI protocol; circulation hub 0% (strict metric sensitivity); human audit not performed. | Accept spatial progress; refuse claim of visual grounding. Freeze repo. | Await explicit human validation before Phase 7. |

---

## Detailed Gate Charters & Invariants

### Gate 8 (RUN-020 Falsification Decision)
- **Forensic Question:** *Did RUN-019 acquire genuine architectural visual grounding?*
- **Empirical Evidence:** Counterfactual perturbation benchmarks (black, masked, noise, text-only) yielded $>90\%$ response similarity. Response format memorized 5-heading text template with fabricated training IDs.
- **Decision:** Terminate naive end-to-end critique training. Pivot project to discrete, falsifiable spatial supervision tasks (Phase 6A).

### Gate 12 (RUN-022 Post-Training Completion Gate)
- **Forensic Question:** *Are the training artifacts complete, uncorrupted, and reproducible?*
- **Empirical Evidence:** 2,310 steps completed, loss converged monotonically (eval loss 1.3967 $\to$ 0.1397), final adapter SHA-256: `71c3f3eaf8de758bc9c843fdb70c6c03538789a7c1fddc7ab1af198b40ee8479`.
- **Decision:** Training complete. Do **not** declare grounding. Proceed to RUN-023.

### Gate 15 (RUN-023 Post-Evaluation Decision Gate)
- **Forensic Question:** *Does RUN-022 satisfy the pre-registered scientific criteria for visual grounding?*
- **Empirical Evidence:**
  - Format Adherence: 100.0% (**PASS**)
  - ID Hallucination: 0.00% (**PASS**)
  - Directional Accuracy: 98.40% (**PASS**)
  - Door Connectivity: 94.00% (**PASS**)
  - Cardinality: 69.20% (**PASS**)
  - Multi-Hop Reachability: 80.00% (**PASS**)
  - Overall Grounding Accuracy: 63.12% vs 14.51% Base (**PASS**, +48.61 pp)
  - Visual Dependency Index: $\text{VDI} = 1.28$ vs $\ge 3.0$ threshold (**FAIL / VDI_PASS = NO**)
  - Circulation Hub: 0.00% (**METRIC SENSITIVITY LIMITATION**)
  - Human Blind Evaluation: **NOT_PERFORMED**
- **Decision:** Mark Phase 6B as complete. Formally record that visual dependency is **unproven** under the current protocol. Prohibit launching Phase 7 without human steering signoff.
