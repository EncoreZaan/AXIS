# AXIS — RunPod Experimental Campaign & GPU Utilization Report (`RUNPOD_EXPERIMENTAL_CAMPAIGN_REPORT.md`)

> **Date:** 2026-09-22  
> **Session Type:** RunPod Single-Session Experimental Campaign & GPU Utilization  
> **Pod Name:** `territorial_green_minnow` (`kqgdq6zb1022eu`)  
> **Host / Port:** `213.181.122.2:57661`  
> **Baseline Commit:** `f4d5e949053743d97091ea35080de5d365899df7` (`f4d5e94`)  
> **Target Base Model:** `Qwen/Qwen2-VL-7B-Instruct` (Revision: `eed13092ef92e448dd6875b2a00151bd3f7db0ac`)  
> **Total Active Session Time:** ~35 minutes  
> **Estimated Hardware Cost:** ~€0.29 (€0.50/hour rate)  

---

## 1. Infrastructure Summary

| Parameter | Specification | Measured State |
| :--- | :--- | :--- |
| **GPU Model** | 24 GB VRAM Class Target | NVIDIA GeForce RTX 3090 |
| **Total VRAM** | >= 22.0 GiB required | 24,576 MiB total (23.56 GiB PyTorch addressable) |
| **Driver / CUDA** | Driver >= 535 / CUDA >= 12.1 | Driver 580.159.04 / CUDA Runtime 12.4 |
| **Host System** | AMD EPYC-Rome (26 vCPUs), 445 GiB RAM | Ubuntu 24.04.3 LTS (Kernel 6.8.0-124-generic) |
| **Python Stack** | Python 3.12.3 in isolated `.venv` | PyTorch `2.6.0+cu124`, Torchvision `0.21.0+cu124` |
| **Hugging Face / PEFT** | Pinned reproduction stack | `transformers==5.17.0`, `peft==0.21.0`, `bitsandbytes==0.50.2` |
| **Disk Storage** | 50 GB overlay filesystem | 23 GB used, 28 GB free |

---

## 2. Experimental Campaign Summary Table

| Run ID | Scientific / Engineering Purpose | Duration | Steps | Peak VRAM | Throughput | Validation (Eval Loss) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **RUN-001-PHASE-A** | Hardware stability, thermal response & memory profiling | 15.0s benchmark | 1,846 matmuls | 10,566.8 MiB | 123.0 matmuls/s | N/A (profiling) | **PASS** |
| **RUN-002-PHASE-B** | End-to-end training path validation smoke test (2 epochs) | 82.8s | 6 opt steps | 11,756.7 MiB | 0.60 samples/s | Initial: 1.9597<br>Final: **1.9337** | **PASS** |
| **RUN-003-PHASE-C** | Operating envelope characterization (BS, SeqLen, MaxPx) | 71.0s | 5 configs | 18,810.4 MiB (max) | 0.30–0.65 samples/s | N/A (characterization) | **PASS** |
| **RUN-004-D1** | Learning trajectory & loss monotonicity over 3 epochs | 105.2s | 9 opt steps | 11,756.7 MiB | 0.60 samples/s | Ep 1: 1.9591<br>Ep 2: 1.9066<br>Ep 3: **1.8941** | **PASS** |
| **RUN-005-D2** | Cross-seed numerical stability (Seed 123 vs 42) | 71.1s | 6 opt steps | 11,756.7 MiB | 0.60 samples/s | Ep 1: 1.9595<br>Ep 2: **1.9333** | **PASS** |
| **RUN-006-F** | Checkpoint save, stop, reload & resume verification | 68.0s | 3+3 opt steps | 11,756.7 MiB | 0.60 samples/s | Resumed: **1.9582** | **PASS** |
| **RUN-007-E1** | Extended controlled training (8 epochs) & qualitative eval | 271.5s | 24 opt steps | 11,756.7 MiB | 0.60 samples/s | Ep 1: 1.9584<br>Ep 8: **1.7271** | **PASS** |

---

## 3. Empirical Findings & Analysis

### 3.1. Hardware & Thermal Envelope
* **Thermal Response:** Under sustained matrix operations (15s continuous 4096x4096 matmuls), GPU temperature rose from 24.0°C to a peak of 58.0°C, well below the 80.0°C thermal throttle threshold.
* **Power Consumption:** Peak power observed was 320.5W against the 350.0W board limit.
* **CUDA Kernel Stability:** Zero crashes, zero unaligned memory exceptions, zero driver resets across the entire multi-run sequence.

### 3.2. Memory Profile Breakdown
Through exact step-by-step profiling in `RUN-001-PHASE-A`:
* **System Idle:** 8.1 MiB allocated (298.0 MiB in `nvidia-smi`).
* **Model in 4-bit NF4:** 5,695.0 MiB allocated (6,074.0 MiB in `nvidia-smi`).
* **LoRA Injected:** 7,857.5 MiB allocated (10,314.0 MiB in `nvidia-smi`).
* **First Forward Pass:** 9,506.8 MiB allocated.
* **First Backward Pass (Peak):** 10,566.8 MiB allocated (~10.3 GiB).
* **Headroom:** On the 24.5 GiB RTX 3090, ~13.0 GiB of unallocated VRAM remains during approved micro-batch training.

### 3.3. Operating Envelope (Phase C)
Five parameter combinations were tested systematically:
1. `BS=1, Seq=1536, MaxPx=512x512` (Approved Baseline): Peak VRAM **10,546.2 MiB** (42.9%), Step Time **1.704s**, Throughput **0.59 samples/s**, Loss finite (`1.8007`).
2. `BS=2, Seq=1536, MaxPx=512x512`: Peak VRAM **13,325.4 MiB** (54.2%), Step Time **3.269s**, Throughput **0.61 samples/s**.
3. `BS=4, Seq=1536, MaxPx=512x512`: Peak VRAM **18,810.4 MiB** (76.5%), Step Time **6.198s**, Throughput **0.65 samples/s**.
4. `BS=2, Seq=2048, MaxPx=512x512`: Peak VRAM **13,509.2 MiB** (55.0%), Step Time **3.307s**, Throughput **0.60 samples/s**.
5. `BS=1, Seq=1536, MaxPx=768x768`: Peak VRAM **11,984.0 MiB** (48.8%), Step Time **3.346s**, Throughput **0.30 samples/s** (throughput halved due to $4\times$ image patches).
* **Boundary Conclusion:** The 24 GB hardware can comfortably scale up to batch size 4 (18.8 GB peak VRAM). However, `BS=1` with gradient accumulation 8 provides the highest memory stability margin (>13 GB buffer) with minimal throughput penalty (0.59 vs 0.65 samples/s).

### 3.4. Learning Signal & Monotonic Convergence
In `RUN-007-E1` (8-epoch controlled run, 24 optimization steps):
* **Training Loss:** Decreased consistently from **1.9618** (step 1) down to **1.5130** (step 24).
* **Validation Loss:** Strictly monotonic improvement across every epoch:
  - Epoch 1.0: `1.9584`
  - Epoch 2.0: `1.8881`
  - Epoch 3.0: `1.8238`
  - Epoch 4.0: `1.7771`
  - Epoch 5.0: `1.7488`
  - Epoch 6.0: `1.7345`
  - Epoch 7.0: `1.7274`
  - Epoch 8.0: `1.7271`
* **Zero Divergence:** Gradient norms remained tightly bounded between `0.28` and `0.58` throughout all steps.

### 3.5. Qualitative Generation Verification
Inference on held-out validation sample `archi_021.jpg` using the adapter trained in `RUN-007-E1`:
```text
"L'organisation spatiale de cette pièce est bien pensée et offre un espace de vie confortable et fonctionnel. 
Voici les points forts de cette pièce :
1. **Lumière naturelle abondante** : Les grandes fenêtres latérales permettent une entrée de lumière naturelle intense, créant une ambiance chaleureuse et accueillante.
2. **Vue panoramique** : La présence d'une grande fenêtre arrière offre une vue..."
```
Demonstrates clean adoption of architectural terminology, structured bullet points, and spatial grounding from the vision prompt.

### 3.6. Checkpoint Recovery (Phase F)
* In `RUN-006-F`, training was halted after saving `checkpoint-3`.
* Model instance and memory were destroyed and cleared.
* Resuming from `checkpoint-3` restored adapter weights, optimizer states (`paged_adamw_8bit`), and lr scheduler without numerical drift (`eval_loss: 1.9582`).

---

## 4. Dataset & Gold Set Protection Verification

* **Master Dataset v2:** Immutable, uncorrupted, zero modification.
* **Gold Set V3:** Manifest SHA256 `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca` strictly isolated; zero Gold Set samples were touched or exposed.
* **FloorPlanCAD:** Hermetically quarantined under `LEGAL_REVIEW_REQUIRED`. Zero assets admitted.
* **ResPlan:** Metric quarantine preserved.
* **Separation:** All generated run artifacts reside strictly inside isolated directories (`experiments/runpod_2026-09-22/RUN-*`).

---

## 5. Recommendations for the Next Scientifically Justified AXIS Run

1. **Approved Architecture Configuration:**
   * Keep base model `Qwen/Qwen2-VL-7B-Instruct` in 4-bit NF4 + bfloat16.
   * Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` with $r=8, \alpha=16$.
   * Frozen visual tower (`model.visual.requires_grad = False`).
2. **Batch & Accumulation Strategy:**
   * The configuration `batch_size: 1`, `gradient_accumulation_steps: 8` (effective batch 8) is the most robust on 24 GB hardware (11.7 GiB peak VRAM, leaving >12 GiB margin against accidental OOM on complex floorplans).
   * For larger training sets, `batch_size: 2`, `gradient_accumulation_steps: 4` can be used to achieve slightly faster step rates (0.61 samples/s) with 13.3 GiB peak VRAM.
3. **Sequence & Image Resolution:**
   * `max_pixels: 262144` (512x512) yields the optimal trade-off between architectural spatial feature resolution and token throughput.
   * `max_seq_length: 1536` comfortably covers all 5-part architectural structured responses without truncation.
4. **Pre-Training Gate Status:**
   * Remote environment, execution path, training dynamics, checkpoint recoverability, and inference pipeline are now fully certified and technically validated on remote cloud infrastructure.
