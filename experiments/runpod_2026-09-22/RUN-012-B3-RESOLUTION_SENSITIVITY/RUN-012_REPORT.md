# AXIS Experiment Report: RUN-012-B3-RESOLUTION_SENSITIVITY

> **Run ID:** `RUN-012-B3-RESOLUTION_SENSITIVITY`  
> **Date:** 2026-09-22 22:30:00 UTC  
> **Status:** **PASS**  
> **Base Model:** `Qwen/Qwen2-VL-7B-Instruct` (4-bit NF4, LoRA $r=8, \alpha=16$)  
> **Tested Resolutions:** $512\times 512$ (`max_pixels: 262144`) vs $768\times 768$ (`max_pixels: 589824`)

## 1. Objective
Quantify multi-step training dynamics, token generation counts, throughput degradation, and VRAM utilization when scaling image patch resolution from $512\times 512$ to $768\times 768$.

## 2. Multi-Step Trajectory Comparison
| Metric | Standard (512x512) | High-Res (768x768) | Relative Impact |
| :--- | :---: | :---: | :---: |
| **Max Pixels** | 262,144 | 589,824 | $+125\%$ pixel budget |
| **Peak VRAM** | 11,756.7 MiB (47.8%) | **19,101.3 MiB** (77.7%) | **+7,344.6 MiB (+62.5%)** |
| **VRAM Buffer Remaining** | ~12.8 GiB | ~5.4 GiB | Reduced headroom |
| **Training Runtime (2 ep)** | 66.24s | **95.94s** | **+44.8% runtime** |
| **Throughput** | 0.604 samples/s | **0.418 samples/s** | **-30.8% throughput** |
| **Final Train Loss** | 1.8799 | 1.9360 | +0.0561 |
| **Final Eval Loss** | 1.9337 | 1.9378 | +0.0041 |

## 3. Engineering Findings
* High-resolution training is fully functional without OOM on 24 GB VRAM (peaking at 19.1 GB).
* However, higher resolution increases VRAM by 7.3 GB and reduces throughput by nearly a third.
* For large-scale pre-training across tens of thousands of plans, $512\times 512$ provides superior cost-efficiency, while $768\times 768$ should be reserved for fine-grained symbol/text reading tasks.
