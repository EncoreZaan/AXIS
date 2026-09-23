# AXIS ? RunPod Phase 2: Campaign Forensic Analysis (`CAMPAIGN_ANALYSIS.md`)

> **Run ID:** `RUN-008-CAMPAIGN_ANALYSIS`  
> **Timestamp:** 2026-09-22 22:30:00 UTC  
> **Target Model:** `Qwen/Qwen2-VL-7B-Instruct` (Revision: `eed13092ef92e448dd6875b2a00151bd3f7db0ac`)  
> **Host Environment:** NVIDIA GeForce RTX 3090 (24 GB VRAM) | CUDA 12.4 | PyTorch 2.6.0+cu124  
> **Audit Status:** **COMPLETE**

---

## 1. Executive Summary

This forensic analysis rigorously evaluates the outcomes of experimental runs `RUN-001-PHASE-A` through `RUN-007-E1` executed on the RunPod instance `territorial_green_minnow`. It delineates verified engineering milestones from scientific claims, scrutinizes the convergence dynamics of previous runs, and establishes the strict boundaries for subsequent experiments.

---

## 2. Answers to the Core Forensic Inquiries

### 1. What has already been proven?
The preceding campaign established beyond technical doubt the integrity and stability of the runtime execution pipeline:
* **Hardware & Thermal Stability:** The RTX 3090 operated stably under 15 seconds of sustained $4096 \times 4096$ matrix multiplications, peaking at 58.0?C and 320.5W board power without thermal throttling.
* **Quantization & Model Loading:** 4-bit NormalFloat4 (NF4) loading with double quantization and bfloat16 compute dtype functions correctly, consuming 5,695.0 MiB of VRAM.
* **LoRA Parameter Injection:** PEFT LoRA targeting attention and MLP projections (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) with frozen vision tower injects cleanly, occupying 7,857.5 MiB VRAM.
* **Autograd & Optimizer Execution:** The forward-backward execution cycle with activation checkpointing and `paged_adamw_8bit` optimizer executes without CUDA errors or NaNs (peak 11,756.7 MiB VRAM at micro-batch size 1, sequence length 1536).
* **Operating Envelope Parameterization:** Systematic parameter scans mapped memory limits across batch sizes (1, 2, 4), sequence lengths (1536, 2048), and image resolutions (512x512, 768x768).
* **State Recovery & Resume:** In `RUN-006-F`, halting at step 3, clearing memory, and reloading restored exact optimizer states, learning rate schedules, and reproduced identical evaluation loss (`1.9582`).
* **Deterministic Optimization:** Seed stability tests (seed 42 vs seed 123) demonstrated identical descent slopes.
* **Qualitative Generation:** Multimodal vision-to-text decoding generated well-structured French architectural critique output.

### 2. What has NOT been proven?
* **Multimodal Spatial Reasoning:** No evidence exists that the model has learned spatial, geometric, or dimensional relationships from images.
* **Generalization Across Visual Distributions:** The model has not been evaluated on diverse floor plans, elevations, cross-sections, or exterior architectural views.
* **Domain Adaptation on Full AXIS Corpus:** Zero training has taken place on the certified 14-source Master Dataset v2 (65,342 samples).
* **Prevention of Catastrophic Forgetting:** The impact of LoRA fine-tuning on general visual question answering and text comprehension has not been quantified.

### 3. Which previous experiment results are scientifically meaningful?
Strictly speaking, the previous experiments represent **engineering and operational validations** rather than scientific discoveries in architecture AI. The only result with scientific character is `RUN-005-D2` (seed stability), which demonstrates that low-rank adaptation with `paged_adamw_8bit` exhibits deterministic convergence dynamics on small batches.

### 4. Which results are only engineering/runtime evidence?
* `RUN-001-PHASE-A`: Pure hardware profiling and memory boundary measurement.
* `RUN-002-PHASE-B`: Pipeline integrity smoke test (forward pass, backward pass, loss logging).
* `RUN-003-PHASE-C`: Empirical VRAM and throughput profiling across hyperparameters.
* `RUN-004-D1`: Demonstration that the loss function decreases monotonically.
* `RUN-006-F`: Checkpoint serialization and deserialization integrity.
* `RUN-007-E1`: Proof that the Trainer loop can execute for 8 consecutive epochs without memory leakage or NaN gradients.

### 5. Is the observed loss decrease consistent with genuine learning or explained by the dataset?
* **Observation:** In `RUN-007-E1`, training loss fell from `1.9618` to `1.5130` (step 24) and eval loss dropped monotonically from `1.9584` to `1.7271`.
* **Scientific Verdict:** **Explained by text template memorization and language-model prior adaptation.**
* **Mechanism:** All 25 image files in the dataset are byte-for-byte identical duplicates of a single image (`sample_interior.jpg`). Consequently, the vision encoder produced an invariant, static token prefix across every single training and validation example. The LoRA adapter did not learn multimodal correlation; it adapted its language generation heads to output the highly repetitive syntactic conventions of the French architectural critique prompt structure ("OBSERVATION / ANALYSE / POINTS FORTS / POINTS DE VIGILANCE / RECOMMANDATION"). The validation loss decreased because the validation samples shared the identical image and identical textual scaffolding.

### 6. What experiment would provide the highest information value next?
Given that a multi-image dataset is unavailable on the Pod, large-scale training cannot produce scientific domain progress. The highest information value lies in **systematic engineering ablations (Path B)**:
1. **LoRA Rank Ablation ($r=8$ vs $r=16$):** Quantify parameter count, VRAM impact, throughput, and capacity scaling.
2. **Learning Rate Sensitivity ($\eta = 5 \times 10^{-5}, 1 \times 10^{-4}, 2 \times 10^{-4}$):** Evaluate gradient norm stability, convergence rate, and numerical sensitivity.
3. **Resolution & Patch Count Sensitivity ($512\times 512$ vs $768\times 768$):** Quantify multi-step throughput penalties and token scaling.
4. **Inference Latency & Decoding Benchmark:** Rigorously profile tokens/sec, time-to-first-token (TTFT), VRAM footprint during decoding, and deterministic vs stochastic generation across base model and trained adapters.

### 7. What dataset is actually available on the Pod?
* Training records: 20 (`experiment_package/dataset/train.jsonl`)
* Validation records: 5 (`experiment_package/dataset/validation.jsonl`)
* Test records: 0
* Image files: 25 (`experiment_package/dataset/images/archi_001.jpg` to `archi_025.jpg`)
* Unique image SHA256: Exactly 1 (`e6b036c6081a5c4f4219173c238d02beec00e00216e3dbbc5782230b95f3e350`)
* Dataset classification: **`RUNTIME_TEST_CORPUS`**

### 8. Can a real cleared AXIS training corpus be reconstructed/accessed?
* **No.** The full Master Dataset v2 (53,720 training assets across 14 cleared sources) consists of multi-gigabyte image and drawing archives that are intentionally excluded from git for copyright and provenance protection. No external storage bucket or network volume is attached to this instance.

### 9. What is the largest scientifically valid run possible during this GPU session?
* A structured sequence of controlled engineering ablations and inference benchmarks under **Path B**. Pretending that the runtime test fixture represents the Master Dataset would violate Absolute Rule #3.

---

## 3. Forensic Conclusion

The campaign must transition cleanly to **Path B (High-Value Engineering Experiments)** to extract maximum empirical utility from the remaining GPU session while preserving scientific integrity.
