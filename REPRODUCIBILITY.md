# AXIS — Experimental Reproducibility Guide

> **Standard:** Bit-exact reproducibility, deterministic seeds, verified cryptographic hashes.

---

## 1. Physical Hardware & Software Profile

The published benchmarks were produced and verified across two verified configurations:

### Configuration 1: Local Engineering Workstation
- **GPU:** NVIDIA GeForce RTX 4060 Ti (8,188 MiB VRAM, Ada Lovelace, Compute Capability 8.9)
- **CPU:** Intel(R) Core(TM) i5-14400F (10 cores, 16 threads)
- **RAM:** 16 GB DDR5 (15.72 GB total)
- **OS:** Windows 11 Pro (Build 26200)
- **Driver:** NVIDIA 616.92, CUDA 13.4 compatible
- **Python:** 3.11.9

### Configuration 2: Remote / Cluster Node
- **GPU:** NVIDIA GeForce RTX 3090 (24 GB GDDR6X)
- **Software Stack:** PyTorch 2.6.0+cu124, Transformers 5.17.0, PEFT 0.21.0, BitsAndBytes 0.50.2

---

## 2. Reproducing Phase 4 Step 6 (Gold Set V3 Evaluation)

### Step 1: Verify Gold Set V3 Integrity
Before evaluation, verify that your local manifest matches the certified cryptographic hash:

```python
import hashlib

def verify_file_sha256(path, expected_hash):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    computed = hasher.hexdigest()
    assert computed == expected_hash, f"Hash mismatch: {computed} != {expected_hash}"
    print(f"PASSED: {path} SHA256 verified.")

# Target manifest
verify_file_sha256(
    "dataset/supervision/v1/manifests/GOLD_V3_MANIFEST.jsonl",
    "81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca"
)
```

### Step 2: Run Baseline 0 Calibration
```bash
python scripts/evaluate_baseline.py \
    --manifest dataset/supervision/v1/manifests/GOLD_V3_MANIFEST.jsonl \
    --task CLEARANCE_CHECK
```
**Expected Output:**
- MAE: `2.7739 m` ($\pm 0.0001$ m)
- Accuracy: `99.00%` (Majority class predictor)

### Step 3: Run Model Evaluation on Checkpoint `ARCHI-AI-P4-005`
```bash
python scripts/evaluate_baseline.py \
    --checkpoint experiments/phase4_micro_pilot/runs/ARCHI-AI-P4-005/checkpoint/checkpoint_best_validation.pt \
    --manifest dataset/supervision/v1/manifests/GOLD_V3_MANIFEST.jsonl \
    --seed 42
```
**Expected Output:**
- MAE on `CLEARANCE_CHECK`: `0.0517 m` (95% CI: `[0.0428, 0.0616]`)
- Classification Accuracy: `100.00%`
- F1-Score: `100.00%`

---

## 3. Reproducing VLM Proof-of-Concept Dry-Run

```bash
# Execute safe dry-run (1 forward pass, no backward, no model updates)
python scripts/train_qlora.py --config configs/qlora_experiment.yaml --dry-run
```
**Expected Output:**
- Model loaded in 4-bit NF4: 730/730 tensors
- Trainable parameters: `20,185,088` (0.2429%)
- Dry-run forward loss: `1.9771`
- Backward pass: Skipped (safe mode)
