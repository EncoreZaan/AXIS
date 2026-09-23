# AXIS Experiment Report: RUN-013-B6-INFERENCE_BENCHMARK

> **Run ID:** `RUN-013-B6-INFERENCE_BENCHMARK`  
> **Date:** 2026-09-22 22:33:00 UTC  
> **Status:** **PASS**  
> **Models Evaluated:** Base Unadapted, RUN-007-E1 ($r=8, 8$ ep), RUN-010-B1 ($r=16, 2$ ep)

## 1. Objective
Rigorously benchmark generation latency, tokens/sec throughput, VRAM footprint, and output determinism across diverse architectural prompt modalities (image+text, text-only, clearance evaluation).

## 2. Empirical Benchmark Matrix
| Model Variant | Prompt Case | Modality | Greedy Tok/s | Sampling Tok/s | Peak VRAM | Determinism Hash Verified |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Base Qwen2-VL-7B** | T1 Interior Analysis | Image+Text | **23.8 tok/s** | 20.8 tok/s | 14,195.0 MiB | YES |
| **Base Qwen2-VL-7B** | T2 Clearance Check | Image+Text | **21.1 tok/s** | 21.8 tok/s | 14,196.6 MiB | YES |
| **Base Qwen2-VL-7B** | T3 Normes PMR | Text-Only | **23.7 tok/s** | 26.2 tok/s | 14,004.8 MiB | YES |
| **RUN-007-E1 (r=8)** | T1 Interior Analysis | Image+Text | **11.9 tok/s** | 11.7 tok/s | 14,272.0 MiB | YES |
| **RUN-007-E1 (r=8)** | T2 Clearance Check | Image+Text | **10.6 tok/s** | 11.5 tok/s | 14,273.6 MiB | YES |
| **RUN-007-E1 (r=8)** | T3 Normes PMR | Text-Only | **14.6 tok/s** | 15.3 tok/s | 14,085.6 MiB | YES |
| **RUN-010-B1 (r=16)**| T1 Interior Analysis | Image+Text | **11.9 tok/s** | 12.0 tok/s | 14,354.9 MiB | YES |
| **RUN-010-B1 (r=16)**| T2 Clearance Check | Image+Text | **11.8 tok/s** | 11.8 tok/s | 14,357.1 MiB | YES |
| **RUN-010-B1 (r=16)**| T3 Normes PMR | Text-Only | **12.7 tok/s** | 13.5 tok/s | 14,168.2 MiB | YES |

## 3. Engineering Findings
* Base 4-bit model decodes at 21?24 tokens/sec on RTX 3090.
* Dynamic PEFT LoRA adapter dispatch adds forward hook overhead, resulting in 11?13 tokens/sec decoding speed.
* VRAM usage during generation remains ~14.1?14.3 GB, leaving >10 GB headroom.
* Greedy decoding exhibits 100% bitwise determinism across repeated executions.
