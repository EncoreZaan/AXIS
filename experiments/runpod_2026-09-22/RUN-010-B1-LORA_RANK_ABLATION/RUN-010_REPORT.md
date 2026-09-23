# AXIS Experiment Report: RUN-010-B1-LORA_RANK_ABLATION

> **Run ID:** `RUN-010-B1-LORA_RANK_ABLATION`  
> **Date:** 2026-09-22 22:25:00 UTC  
> **Status:** **PASS**  
> **Base Model:** `Qwen/Qwen2-VL-7B-Instruct` (4-bit NF4)  
> **LoRA Rank:** $r=16, \alpha=32$ (Scaling $\alpha/r = 2.0$)  
> **Baseline Reference:** `RUN-002-PHASE-B` ($r=8, \alpha=16$)

## 1. Objective
Assess the empirical trade-offs of doubling LoRA rank ($r=8 \to 16$) in terms of trainable parameters, memory allocation, execution speed, loss trajectory, and adapter footprint on an RTX 3090 (24 GB).

## 2. Quantitative Comparison
| Parameter | Baseline (r=8, RUN-002) | Candidate (r=16, RUN-010) | Delta |
| :--- | :---: | :---: | :---: |
| **Trainable Parameters** | 20,185,088 (0.243%) | **40,370,176** (0.485%) | +100.0% (+20.2M params) |
| **Peak VRAM** | 11,756.7 MiB | **11,962.5 MiB** | +205.8 MiB (+1.7%) |
| **Training Runtime (2 epochs)** | 66.24s | **67.90s** | +1.66s (+2.5%) |
| **Throughput (samples/s)** | 0.604 | **0.589** | -0.015 samples/s |
| **Initial Train Loss** | 1.9618 | **1.9701** | +0.0083 |
| **Final Train Loss** | 1.8799 | **1.8841** | +0.0042 |
| **Final Eval Loss** | 1.9337 | **1.8879** | **-0.0458 (Improved)** |
| **Adapter Safetensors Size** | 80,797,976 B (~80.8 MB) | **161,539,072 B** (~161.5 MB) | +100.0% |
| **Adapter SHA256** | `bbfca98b48d88a4e...` | `fdc1cd3b322e4d229e2a3483c575d7d67def5a0a1fe5c9fc460336cb5a5bea6f` | Distinct |

## 3. Engineering Findings
* Doubling rank to $r=16$ only increases training peak VRAM by ~206 MiB (<1% of the 24 GB GPU budget).
* Training throughput penalty is negligible (-2.5% runtime difference).
* Higher rank enabled superior capacity fit, yielding a lower validation loss (1.8879 vs 1.9337).
