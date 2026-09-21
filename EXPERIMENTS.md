# AXIS — Complete Experimental Registry

> **Standard:** Complete traceability, zero fabricated experiments, verified artifact paths.

---

## 1. Registry of Phase 4 Controlled Micro-Pilot Runs

All runs were executed with fixed seed configurations and evaluated on locked validation sets prior to Gold Set benchmarking.

| Run Identifier | Model Architecture | Dataset & Scale | Seed | Selection Metric | Validation Score | Status |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| `ARCHI-AI-P4-001` | `SpatialRelationMLP` | Dataset A (Small, 800 ex) | 42 | MAE (m) | 0.5545 m | Completed |
| `ARCHI-AI-P4-002` | `SpatialRelationMLP` | Dataset A (Small, 800 ex) | 123 | Multi-seed stability | 0.5612 m | Completed |
| `ARCHI-AI-P4-003` | `SpatialRelationMLP` | Dataset A (Small, 800 ex) | 999 | Multi-seed stability | 0.5501 m | Completed |
| `ARCHI-AI-P4-004` | `SpatialRelationMLP` | Dataset A (Medium, 2,400 ex) | 42 | Scaling test | 0.1742 m | Completed |
| `ARCHI-AI-P4-005` | `SpatialRelationMLP` | Dataset A (Full, 6,000 ex) | 42 | Best Validation | **0.0481 m** | **SELECTED CHECKPOINT** |
| `ARCHI-AI-P4-ABL-B` | `SpatialRelationMLP` | Dataset A (Sanitized Meta) | 42 | Shortcut audit | 0.0483 m | Signal intact (no shortcut) |
| `ARCHI-AI-P4-ABL-C` | `SpatialRelationMLP` | Dataset A (Scrambled Inputs)| 42 | Falsification audit | 2.7610 m | Signal collapsed (= Baseline 0) |
| `ARCHI-AI-P4-OVERFIT` | `SpatialRelationMLP` | Synthetic Mini-Batch (10 ex) | 42 | Sanity check | 0.0001 m | Perfect memorization verified |

### Selected Checkpoint Specification:
- **Identifier:** `ARCHI-AI-P4-005`
- **Checkpoint SHA256:** `69f00c211e1db63181bf7c6f4ae624c3aa312856f7d8b2191bc9c8b84a680d54`
- **Config SHA256:** `b16859bddc4971a59a3bd06fa514f1a0249b0e1c16cb631f4ad5915531a10411`
- **Gold Set MAE:** **0.0517 m** (Generalization gap: $+0.0036$ m)

---

## 2. Micro-Experiment: VLM Adaptation Proof-of-Concept

> [!WARNING]
> **Status: FEASIBILITY / PROOF-OF-CONCEPT ONLY.**  
> This micro-experiment demonstrates technical feasibility on local/remote GPUs without OOM. It is **NOT** a trained production model and does not claim general architectural reasoning.

### Experimental Configuration:
- **Base Model:** `Qwen/Qwen2-VL-7B-Instruct`
- **Quantization:** 4-bit NormalFloat (`nf4`), double quant, compute dtype `torch.bfloat16`
- **LoRA Parameters:** $r=8$, $\alpha=16$, dropout $0.05$, target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- **Trainable Parameters:** **20,185,088** / 8,311,560,704 (**0.2429%**)
- **Hardware Profile:** Tested on remote 24 GB GPU (RTX 3090) and dry-run on local RTX 4060 Ti
- **Software Stack:** PyTorch 2.6.0+cu124, Transformers 5.17.0, PEFT 0.21.0, BitsAndBytes 0.50.2

### Optimization Dynamics (6 Steps, 2 Epochs):
| Step | Epoch | Learning Rate | Grad Norm | Train Loss | Eval Loss | Notes |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | 0.4 | 0.00000 | 0.3247 | 1.8931 | - | Warmup phase |
| 2 | 0.8 | 0.00010 | 0.2851 | 1.8463 | - | Linear descent |
| 3 | 1.0 | 0.00009 | 0.3143 | 1.8701 | 1.8537 | Epoch 1 evaluation |
| 4 | 1.4 | 0.00007 | 0.2971 | 1.7988 | - | Steady convergence |
| 5 | 1.8 | 0.00003 | 0.3086 | 1.8294 | - | Cosine decay |
| 6 | 2.0 | 0.00001 | 0.3877 | **1.7692** | **1.8288** | Epoch 2 evaluation |

- **Loss Evolution:** Train loss $1.893 \to 1.769$, Eval loss $1.854 \to 1.829$
- **Runtime Metrics:** Total FLOPs $1.77 \times 10^{15}$, Total runtime: $63.27$ s, 0 OOM, 0 NaN
- **Artifacts Location:** `outputs/archi_ai_micro_experiment/`
