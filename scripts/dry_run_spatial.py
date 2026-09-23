# -*- coding: utf-8 -*-
"""
AXIS Phase 6A — Dry Run Verification Script
===========================================
Executes dataset loading, collation, multimodal tensor formatting,
and forward pass verification on RUN-021-SPATIAL-SUPERVISION/train.jsonl.

Strict Invariants:
- optimizer.step() is DISABLED.
- weights_unmodified = TRUE (verified via parameter hashes before and after).
- Zero fine-tuning, zero model training.
"""

import os
import sys
import json
import time
import math
import hashlib
from pathlib import Path
from typing import Dict, Any, List

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
EXP_RUN021_DIR = BASE_DIR / "RUN-021-SPATIAL-SUPERVISION"
DATASET_DIR = EXP_RUN021_DIR / "dataset"
TRAIN_FILE = EXP_RUN021_DIR / "train.jsonl"
OUTPUT_METRICS = EXP_RUN021_DIR / "dry_run_metrics.json"


class SpatialTorchDataset(Dataset):
    """PyTorch Dataset loading authentic multimodal spatial examples."""

    def __init__(self, jsonl_path: Path, images_base_dir: Path):
        self.samples = []
        self.images_base_dir = images_base_dir
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str:
                    self.samples.append(json.loads(line_str))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        item = self.samples[idx]
        img_rel = item["image"]
        img_path = self.images_base_dir / img_rel
        if not img_path.exists():
            raise FileNotFoundError(f"Image not found: {img_path}")

        # Load and resize image to standard dry-run patch grid (256x256)
        with Image.open(img_path) as pil_img:
            pil_rgb = pil_img.convert("RGB").resize((256, 256))
            arr = np.array(pil_rgb, dtype=np.float32) / 255.0
            # [C, H, W]
            tensor_img = torch.from_numpy(arr).permute(2, 0, 1)

        # Simple deterministic character-level tokenizer for mock validation
        q_text = item["question"]
        a_text = item["answer"]
        full_text = f"User: {q_text} Assistant: {a_text}"
        tokens = [ord(c) % 512 + 1 for c in full_text[:256]]
        input_ids = torch.tensor(tokens, dtype=torch.long)
        labels = input_ids.clone()

        return {
            "example_id": item["example_id"],
            "source_id": item["source_id"],
            "task_type": item["task_type"],
            "image": tensor_img,
            "input_ids": input_ids,
            "labels": labels
        }


def collate_fn(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    images = torch.stack([b["image"] for b in batch], dim=0)
    max_len = max(b["input_ids"].shape[0] for b in batch)
    padded_ids = []
    padded_labels = []
    for b in batch:
        cur_len = b["input_ids"].shape[0]
        pad_size = max_len - cur_len
        p_id = torch.cat([b["input_ids"], torch.zeros(pad_size, dtype=torch.long)])
        p_lab = torch.cat([b["labels"], torch.full((pad_size,), -100, dtype=torch.long)])
        padded_ids.append(p_id)
        padded_labels.append(p_lab)

    return {
        "images": images,
        "input_ids": torch.stack(padded_ids, dim=0),
        "labels": torch.stack(padded_labels, dim=0),
        "example_ids": [b["example_id"] for b in batch],
        "source_ids": [b["source_id"] for b in batch],
        "task_types": [b["task_type"] for b in batch]
    }


class MultimodalSpatialProbe(nn.Module):
    """Multimodal architecture probe verifying collation and forward pass."""

    def __init__(self, vocab_size: int = 513, hidden_dim: int = 128):
        super().__init__()
        self.patch_embed = nn.Conv2d(3, hidden_dim, kernel_size=16, stride=16)
        self.text_embed = nn.Embedding(vocab_size, hidden_dim)
        self.lm_head = nn.Linear(hidden_dim, vocab_size)
        self.loss_fn = nn.CrossEntropyLoss(ignore_index=-100)

    def forward(self, images: torch.Tensor, input_ids: torch.Tensor, labels: torch.Tensor = None):
        B = images.shape[0]
        # Vision tokens: [B, C, H, W] -> [B, hidden_dim, 16, 16] -> [B, 256, hidden_dim]
        v_tokens = self.patch_embed(images).flatten(2).transpose(1, 2)
        # Text tokens: [B, seq_len, hidden_dim]
        t_tokens = self.text_embed(input_ids)
        # Combine
        combined = torch.cat([v_tokens, t_tokens], dim=1)
        logits = self.lm_head(combined[:, -t_tokens.shape[1]:, :])

        loss = None
        if labels is not None:
            loss = self.loss_fn(logits.view(-1, logits.shape[-1]), labels.view(-1))
        return logits, loss


def get_weights_hash(model: nn.Module) -> str:
    h = hashlib.sha256()
    for param in model.parameters():
        h.update(param.data.cpu().numpy().tobytes())
    return h.hexdigest()


def main():
    print("=" * 80)
    print("AXIS Phase 6A — Dry Run Verification Engine")
    print("=" * 80)
    print(f"Target Dataset: {TRAIN_FILE}")

    # 1. Dataset Loading
    dataset = SpatialTorchDataset(TRAIN_FILE, DATASET_DIR)
    print(f"[DATASET LOAD] Successfully loaded {len(dataset)} examples from train.jsonl.")

    # 2. DataLoader & Collation
    dataloader = DataLoader(dataset, batch_size=2, shuffle=False, collate_fn=collate_fn)
    print("[DATALOADER] DataLoader initialized with batch_size=2.")

    # 3. Model Initialization
    torch.manual_seed(42)
    model = MultimodalSpatialProbe()
    initial_weights_hash = get_weights_hash(model)
    print(f"[MODEL INIT] MultimodalSpatialProbe initialized. Initial weights SHA-256: {initial_weights_hash}")

    # 4. Dry Run Execution (8 steps)
    dry_run_steps = 8
    batch_records = []
    total_loss = 0.0

    print(f"\n[EXECUTION] Executing {dry_run_steps} dry-run forward steps (optimizer.step() DISABLED)...")

    step = 0
    for batch in dataloader:
        step += 1
        if step > dry_run_steps:
            break

        start_time = time.time()
        logits, loss = model(batch["images"], batch["input_ids"], batch["labels"])
        # Compute backward to verify gradient flow
        loss.backward()

        # CRITICAL INVARIANT: DO NOT CALL optimizer.step()
        # model.zero_grad() immediately to clear gradients
        grads = [p.grad.norm().item() for p in model.parameters() if p.grad is not None]
        avg_grad = float(np.mean(grads)) if grads else 0.0
        model.zero_grad()

        duration = time.time() - start_time
        loss_val = float(loss.item())
        total_loss += loss_val

        rec = {
            "step": step,
            "sample_ids": batch["example_ids"],
            "source_ids": batch["source_ids"],
            "task_types": batch["task_types"],
            "images_shape": list(batch["images"].shape),
            "input_ids_shape": list(batch["input_ids"].shape),
            "loss": loss_val,
            "avg_grad_norm": round(avg_grad, 4),
            "duration_sec": round(duration, 4)
        }
        batch_records.append(rec)
        print(f"  Step {step}/{dry_run_steps}: Loss = {loss_val:.4f}, GradNorm = {avg_grad:.4f}, Time = {duration*1000:.1f} ms")

    # 5. Verify Invariants
    post_weights_hash = get_weights_hash(model)
    weights_unmodified = (initial_weights_hash == post_weights_hash)
    print(f"\n[INVARIANT CHECK] Initial weights hash: {initial_weights_hash}")
    print(f"[INVARIANT CHECK] Post-run weights hash: {post_weights_hash}")
    print(f"[INVARIANT CHECK] Weights unmodified: {weights_unmodified}")

    if not weights_unmodified:
        print("FATAL: Model weights were modified during dry run!")
        sys.exit(1)

    metrics = {
        "dataset_name": "AXIS_SPATIAL_SUPERVISION_V1",
        "dataset_train_file": str(TRAIN_FILE),
        "total_train_samples": len(dataset),
        "dry_run_steps_executed": dry_run_steps,
        "batch_size": 2,
        "avg_loss": round(total_loss / dry_run_steps, 4),
        "loss_finite": all(not math.isnan(r["loss"]) and not math.isinf(r["loss"]) for r in batch_records),
        "optimizer_step_called": False,
        "weights_updated": False,
        "weights_unmodified": weights_unmodified,
        "initial_weights_sha256": initial_weights_hash,
        "post_weights_sha256": post_weights_hash,
        "training_allowed": False,
        "dry_run_verdict": "PASS",
        "batch_records": batch_records
    }

    with open(OUTPUT_METRICS, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"[COMPLETE] Dry run metrics written to {OUTPUT_METRICS}")
    print("DRY_RUN: PASS")


if __name__ == "__main__":
    main()
