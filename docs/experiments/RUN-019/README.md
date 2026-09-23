# RUN-019 — First Real-Data QLoRA Training Pilot

> **Canonical Run ID:** `RUN-019-FIRST-REAL-DATA-QLORA`  
> **Scientific Phase:** Phase 4 — Real-Data Architectural Adaptation Pilot  
> **Date:** 2026-09-22 / 2026-09-23  
> **Baseline Commit:** `f4d5e949053743d97091ea35080de5d365899df7`  
> **Status:** **COMPLETE** | **POST-TRAINING GATE: PASS**  
> **Evidence Directory:** [`RUN-019-FIRST-REAL-DATA-QLORA/`](../../../RUN-019-FIRST-REAL-DATA-QLORA/)  

---

## 1. Objective

To execute the first real-data architectural fine-tuning pilot of AXIS using a locked set of 1,000 real architectural plans and paired BIM entities. The pre-registered experimental hypothesis tested whether 4-bit NF4 QLoRA on `Qwen/Qwen2-VL-7B-Instruct` could achieve stable optimization without NaN loss or memory overflow while monotonically minimizing loss on real architectural data.

---

## 2. Dataset

- **Corpus:** `REAL_DATA_PILOT` (locked in `experiments/runpod_2026-09-22/REAL_DATA_PILOT/` and `RUN-017-DATASET_LOCK/`).
- **Total Physical Assets:** 1,000 unique architectural assets.
  - `CORE_RPLAN`: 990 2D raster floorplans.
  - `CORE_RESBIM_PAIRED`: 10 certified paired 2D/3D units.
- **Partitions:**
  - `train.jsonl`: 775 assets (77.5%) — SHA-256: `246e22b372180a6b4be6c61eeea77e10a2c2d35b7128503463d32d6185ec3c47`
  - `validation.jsonl`: 98 assets (9.8%) — SHA-256: `23a0f44ec54a98202d2e47f582b901010f286f7ad83be990447317e0029cee0e`
  - `test.jsonl`: 127 assets (12.7%) — SHA-256: `113b7313340d1026c6a693f6fb2e8b00fd41dde06485f299b13add1018f37eb1` (Held-out sanctuary)
- **Data Properties:** Supervision consisted of detailed, structured French architectural critiques formatted into 5 standardized sections (`OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`).

---

## 3. Model & Architecture

- **Base Model:** `Qwen/Qwen2-VL-7B-Instruct`
- **Revision:** `eed13092ef92e448dd6875b2a00151bd3f7db0ac`
- **Quantization:** 4-bit NormalFloat (NF4), double quantization, compute in `bfloat16`.
- **LoRA Parameters:** Rank $r=16$, Alpha $\alpha=32$, Dropout $0.05$.
- **Target Modules:** `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` (40,370,176 trainable parameters, 0.485% of total).
- **Vision Tower:** Frozen (`visual.requires_grad = False`).

---

## 4. Training Configuration & Environment

- **Resolution:** `min_pixels: 200704`, `max_pixels: 262144` (~512x512).
- **Batch Size:** Micro-batch 1, Gradient accumulation 8 (Effective batch size = 8).
- **Optimization:** `paged_adamw_8bit`, Gradient checkpointing enabled, sequence length 1,536 tokens.
- **Budget:** 2 full epochs, 194 optimizer steps.
- **Learning Rate:** $1.0\times 10^{-4}$ with cosine decay, 9 warmup steps (~5%).
- **Hardware:** NVIDIA GeForce RTX 3090 (24 GB VRAM), Driver 580.159.04, CUDA 12.4, PyTorch 2.6.0+cu124, Ubuntu 24.04 LTS (26 AMD EPYC vCPUs).

---

## 5. Execution & Numerical Results

- **Run Status:** Completed without interruption in 770.8 seconds (~12.8 minutes).
- **Peak VRAM:** 11,962.5 MiB (~11.7 GiB, 49.6% capacity).
- **Loss Descent:**
  - Initial Train Loss: 1.769 $\to$ Final Train Loss: **0.0245**
  - Initial Eval Loss: 1.644 $\to$ Final Eval Loss: **0.0232** (**-98.59% drop**)
- **Checkpoints Saved:** `checkpoint-97` (epoch 1.0), `checkpoint-194` (epoch 2.0), `final_adapter`.

---

## 6. Cryptographic Hashes

From [`RUN-019-FIRST-REAL-DATA-QLORA/checkpoint_hashes.json`](../../../RUN-019-FIRST-REAL-DATA-QLORA/checkpoint_hashes.json):
- `checkpoint-97/adapter_model.safetensors`: `a2e5d79679dd43fb6086705d2105151b72e5058cf5f4ffc0411d7fcfe232da16` (161,539,072 B)
- `checkpoint-194/adapter_model.safetensors`: `7f53f938d6df23b6b100bb1163470ae9a909be0eeef9ca92e4be8c772c3d555c` (161,539,072 B)
- `final_adapter/adapter_model.safetensors`: `7f53f938d6df23b6b100bb1163470ae9a909be0eeef9ca92e4be8c772c3d555c` (Bit-identical to step 194)

---

## 7. Critical Scientific Limitations

> [!WARNING]
> **Subsequent Falsification in RUN-020:**  
> Although the training metrics and loss descent appeared exceptional, subsequent scientific testing in `RUN-020` proved that this run suffered from severe failure modes:
> 1. **Template Memorization:** The model memorized a deterministic linguistic critique template rather than understanding plans.
> 2. **ID Hallucination (100%):** The model systematically hallucinated training set numerical IDs when prompted with unseen plans.
> 3. **Visual Blindness ($\text{VDI} \approx 1.0$):** Response generation was virtually identical with real images, black images, or no images at all.

---

## 8. Conclusion & Next Step

- **Conclusion:** RUN-019 successfully proved the engineering feasibility of stable 4-bit QLoRA training on real architectural data. However, naive natural language supervision led to text template memorization and zero visual dependency.
- **Next Step:** Proceed to Phase 5 (`RUN-020`) to formally evaluate generalization and visual dependency on the held-out test split.
