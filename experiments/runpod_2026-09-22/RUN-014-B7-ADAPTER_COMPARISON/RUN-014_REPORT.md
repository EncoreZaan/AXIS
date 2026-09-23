# AXIS Experiment Report: RUN-014-B7-ADAPTER_COMPARISON

> **Run ID:** `RUN-014-B7-ADAPTER_COMPARISON`  
> **Date:** 2026-09-22 22:33:00 UTC  
> **Status:** **PASS**

## 1. Objective
Establish an authoritative inventory of all trained adapter checkpoints, verify physical existence, file sizes, and cryptographic SHA256 hashes to guarantee provenance and zero overwrites.

## 2. Checkpoint Registry
| Run ID | LoRA Rank | LR | Resolution | Epochs | File Size (Bytes) | SHA256 Checksum | Location |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **RUN-002-PHASE-B** | 8 | 1e-4 | 512 | 2 | 80,797,976 | `bbfca98b48d88a4e8d3568770281ef51e70cfa319806b3fa1060938cf18d1847` | `experiments/runpod_2026-09-22/RUN-002-PHASE-B/outputs` |
| **RUN-007-E1** | 8 | 1e-4 | 512 | 8 | 80,797,976 | `aff4e7f5761f5e3240e53a5fb291244e8c148bb5749f7d2427f7112ea1ef9f12` | `experiments/runpod_2026-09-22/RUN-007-E1/outputs` |
| **RUN-010-B1** | 16 | 1e-4 | 512 | 2 | 161,539,072 | `fdc1cd3b322e4d229e2a3483c575d7d67def5a0a1fe5c9fc460336cb5a5bea6f` | `experiments/runpod_2026-09-22/RUN-010-B1-LORA_RANK_ABLATION/outputs` |
| **RUN-011-LR5e-5** | 8 | 5e-5 | 512 | 2 | 80,797,976 | `304c930d5f4799c6802e2124564c783dbd0bbbf9a2e6f498c41496a75f2845c4` | `experiments/runpod_2026-09-22/RUN-011-B2-LR_SENSITIVITY/outputs_lr_5e5` |
| **RUN-011-LR2e-4** | 8 | 2e-4 | 512 | 2 | 80,797,976 | `d0e8cda1c019401341c59910d54a20e2ef648d7120710602f37cbbcf3b1464c8` | `experiments/runpod_2026-09-22/RUN-011-B2-LR_SENSITIVITY/outputs_lr_2e4` |
| **RUN-012-Res768** | 8 | 1e-4 | 768 | 2 | 80,797,976 | `5834ec7445fe2e9b0bc9fc855b771e7215f793b8909fa0d3d5fc02ba7c64eb3d` | `experiments/runpod_2026-09-22/RUN-012-B3-RESOLUTION_SENSITIVITY/outputs` |

## 3. Provenance Verdict
All 6 adapter safetensors are 100% verified, physically isolated in distinct folders, and cryptographically unique. Zero checkpoints were overwritten.
