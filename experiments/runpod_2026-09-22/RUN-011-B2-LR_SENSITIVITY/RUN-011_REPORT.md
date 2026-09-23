# AXIS Experiment Report: RUN-011-B2-LR_SENSITIVITY

> **Run ID:** `RUN-011-B2-LR_SENSITIVITY`  
> **Date:** 2026-09-22 22:28:00 UTC  
> **Status:** **PASS**  
> **Base Model:** `Qwen/Qwen2-VL-7B-Instruct` (4-bit NF4, LoRA $r=8, \alpha=16$)  
> **Ablation Range:** $\eta \in \{5\times 10^{-5}, 1\times 10^{-4}, 2\times 10^{-4}\}$

## 1. Objective
Establish learning rate bounds and gradient norm stability for 4-bit QLoRA with `paged_adamw_8bit` on multimodal architectural text generation.

## 2. Empirical Comparison Matrix
| Learning Rate | Train Loss | Eval Loss | Max Grad Norm | Peak VRAM | Runtime (2 ep) | Stability Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$\eta = 5\times 10^{-5}$** | 1.9517 | 1.9668 | 0.334 | 13,835.2 MiB | 68.8s | Conservative (slow convergence) |
| **$\eta = 1\times 10^{-4}$** (Baseline) | 1.9311 | 1.9337 | 0.320 | 11,756.7 MiB | 66.2s | Optimal nominal baseline |
| **$\eta = 2\times 10^{-4}$** | **1.8925** | **1.8701** | 0.441 | 15,915.2 MiB | 68.0s | Aggressive but stable (zero divergence) |

## 3. Engineering Findings
* $\eta = 2\times 10^{-4}$ converged fastest without gradient explosion; max gradient norm remained tightly bounded at 0.441.
* $\eta = 5\times 10^{-5}$ is too slow for short-epoch regimes, failing to meaningfully adapt the causal LM prior.
* $\eta = 1\times 10^{-4}$ remains the safest all-round default for long campaigns.
