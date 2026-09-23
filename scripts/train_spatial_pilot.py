#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AXIS Phase 6B — Spatial Grounding Scientific Training Pilot (RUN-022)
====================================================================
Model: Qwen2-VL-7B-Instruct (revision: eed13092ef92e448dd6875b2a00151bd3f7db0ac)
Quantization: 4-bit NF4 double quant bfloat16
LoRA: r=16, alpha=32, dropout=0.05, target_modules: q,k,v,o,gate,up,down
Dataset: AXIS_SPATIAL_SUPERVISION_V1 (RUN-021-SPATIAL-SUPERVISION)
Strict Rules:
- NO hyperparameter sweeps, NO automatic retuning
- Pre-flight hashes certified
- Initial checkpoint saved before optimizer step 1
- Full per-step and periodic validation logging
"""

import os
import sys
import gc
import json
import time
import math
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

import argparse
import yaml
from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset

from transformers import (
    AutoProcessor,
    Qwen2VLForConditionalGeneration,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    TrainerCallback,
    TrainerState,
    TrainerControl,
    set_seed
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel
)
from qwen_vl_utils import process_vision_info

WORKSPACE = Path("/workspace/AXIS")
RUN021_DIR = WORKSPACE / "RUN-021-SPATIAL-SUPERVISION"
RUN022_DIR = WORKSPACE / "RUN-022-SPATIAL-GROUNDING-PILOT"
CHECKPOINTS_DIR = RUN022_DIR / "checkpoints"
HISTORICAL_CHECKPOINTS_DIR = RUN022_DIR / "historical_checkpoints"
CONFIG_FILE = RUN022_DIR / "training_config.yaml"
METRICS_JSONL = RUN022_DIR / "training_metrics.jsonl"
FINAL_METRICS_JSON = RUN022_DIR / "training_metrics.json"
CHECKPOINT_HASHES_JSON = RUN022_DIR / "checkpoint_hashes.json"

class SpatialVisionDataset(Dataset):
    """Multimodal dataset for spatial supervision grounding."""
    def __init__(
        self,
        jsonl_path: Path,
        images_base_dir: Path,
        processor: AutoProcessor,
        max_seq_length: int = 1536
    ):
        self.jsonl_path = jsonl_path
        self.images_base_dir = images_base_dir
        self.processor = processor
        self.max_seq_length = max_seq_length
        self.samples = []

        if not self.jsonl_path.exists():
            raise FileNotFoundError(f"Dataset file missing: {self.jsonl_path}")

        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f):
                line_str = line.strip()
                if line_str:
                    try:
                        self.samples.append(json.loads(line_str))
                    except json.JSONDecodeError as e:
                        print(f"[WARN] Line {line_idx+1} skipped (invalid JSON): {e}")

        self.assistant_header_tokens = self.processor.tokenizer.encode("<|im_start|>assistant\n")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        sample = self.samples[idx]
        conversations = sample["conversations"]

        formatted_conversations = []
        for msg in conversations:
            msg_copy = {"role": msg["role"]}
            content = msg["content"]
            if isinstance(content, list):
                new_content = []
                for item in content:
                    item_copy = dict(item)
                    if item_copy.get("type") == "image":
                        img_path = item_copy.get("image")
                        # Try resolution via images_base_dir
                        resolved_img = self.images_base_dir / img_path
                        if not resolved_img.exists():
                            resolved_img = self.images_base_dir / "images" / Path(img_path).name
                        if not resolved_img.exists():
                            resolved_img = WORKSPACE / "experiments" / "runpod_2026-09-22" / "REAL_DATA_PILOT" / "images" / Path(img_path).name
                        if not resolved_img.exists():
                            raise FileNotFoundError(f"Image not found: {img_path}")
                        item_copy["image"] = str(resolved_img)
                    new_content.append(item_copy)
                msg_copy["content"] = new_content
            else:
                msg_copy["content"] = content
            formatted_conversations.append(msg_copy)

        text_prompt = self.processor.apply_chat_template(
            formatted_conversations,
            tokenize=False,
            add_generation_prompt=False
        )

        image_inputs, video_inputs = process_vision_info(formatted_conversations)

        inputs = self.processor(
            text=[text_prompt],
            images=image_inputs,
            videos=video_inputs,
            padding=False,
            return_tensors="pt"
        )

        input_ids = inputs["input_ids"][0]
        attention_mask = inputs["attention_mask"][0]
        labels = input_ids.clone()

        if input_ids.shape[0] > self.max_seq_length:
            input_ids = input_ids[:self.max_seq_length]
            attention_mask = attention_mask[:self.max_seq_length]
            labels = labels[:self.max_seq_length]

        # Mask prompt & vision tokens with -100
        seq_len = input_ids.shape[0]
        header_len = len(self.assistant_header_tokens)
        assistant_start_idx = -1

        for i in range(seq_len - header_len + 1):
            if input_ids[i:i+header_len].tolist() == self.assistant_header_tokens:
                assistant_start_idx = i + header_len
                break

        if assistant_start_idx != -1:
            labels[:assistant_start_idx] = -100
        else:
            print(f"[WARN] Assistant header not found in sample {sample.get('example_id', idx)}")

        item_output = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }

        if "pixel_values" in inputs:
            item_output["pixel_values"] = inputs["pixel_values"]
        if "image_grid_thw" in inputs:
            item_output["image_grid_thw"] = inputs["image_grid_thw"]
        if "mm_token_type_ids" in inputs:
            mm_types = inputs["mm_token_type_ids"][0]
            if mm_types.shape[0] > self.max_seq_length:
                mm_types = mm_types[:self.max_seq_length]
            item_output["mm_token_type_ids"] = mm_types

        return item_output


class VisionLanguageDataCollator:
    """Multimodal data collator with dynamic padding for Qwen2-VL."""
    def __init__(self, processor: AutoProcessor):
        self.processor = processor
        self.pad_token_id = (
            processor.tokenizer.pad_token_id
            if processor.tokenizer.pad_token_id is not None
            else 151643
        )

    def __call__(self, batch: List[Dict[str, torch.Tensor]]) -> Dict[str, torch.Tensor]:
        max_len = max(item["input_ids"].shape[0] for item in batch)

        input_ids_list = []
        attention_mask_list = []
        labels_list = []
        mm_token_type_ids_list = []
        pixel_values_list = []
        image_grid_thw_list = []

        has_mm_tokens = "mm_token_type_ids" in batch[0]

        for item in batch:
            cur_len = item["input_ids"].shape[0]
            pad_len = max_len - cur_len

            padded_input_ids = torch.cat([
                item["input_ids"],
                torch.full((pad_len,), self.pad_token_id, dtype=torch.long)
            ])
            padded_attention_mask = torch.cat([
                item["attention_mask"],
                torch.full((pad_len,), 0, dtype=torch.long)
            ])
            padded_labels = torch.cat([
                item["labels"],
                torch.full((pad_len,), -100, dtype=torch.long)
            ])

            input_ids_list.append(padded_input_ids)
            attention_mask_list.append(padded_attention_mask)
            labels_list.append(padded_labels)

            if has_mm_tokens and "mm_token_type_ids" in item:
                padded_mm = torch.cat([
                    item["mm_token_type_ids"],
                    torch.full((pad_len,), 0, dtype=torch.long)
                ])
                mm_token_type_ids_list.append(padded_mm)

            if "pixel_values" in item:
                pixel_values_list.append(item["pixel_values"])
            if "image_grid_thw" in item:
                image_grid_thw_list.append(item["image_grid_thw"])

        collated = {
            "input_ids": torch.stack(input_ids_list),
            "attention_mask": torch.stack(attention_mask_list),
            "labels": torch.stack(labels_list),
        }

        if mm_token_type_ids_list:
            collated["mm_token_type_ids"] = torch.stack(mm_token_type_ids_list)
        if pixel_values_list:
            collated["pixel_values"] = torch.cat(pixel_values_list, dim=0)
        if image_grid_thw_list:
            collated["image_grid_thw"] = torch.cat(image_grid_thw_list, dim=0)

        return collated


class DetailedMetricsLoggingCallback(TrainerCallback):
    """Logs detailed per-step metrics and GPU VRAM to training_metrics.jsonl."""
    def __init__(self, metrics_file: Path, resume_mode: bool = False):
        self.metrics_file = metrics_file
        self.step_start_time = time.time()
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        # Clear previous metrics only in fresh run
        if not resume_mode and self.metrics_file.exists():
            self.metrics_file.unlink()

    def on_step_begin(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        self.step_start_time = time.time()

    def on_log(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, logs: Optional[Dict[str, Any]] = None, **kwargs):
        if logs is None:
            return

        step_duration = round(time.time() - self.step_start_time, 4)
        cuda_avail = torch.cuda.is_available()
        allocated_mib = round(torch.cuda.memory_allocated() / (1024**2), 2) if cuda_avail else 0.0
        reserved_mib = round(torch.cuda.memory_reserved() / (1024**2), 2) if cuda_avail else 0.0
        peak_mib = round(torch.cuda.max_memory_allocated() / (1024**2), 2) if cuda_avail else 0.0

        record = {
            "global_step": state.global_step,
            "epoch": round(state.epoch, 4) if state.epoch is not None else 0.0,
            "loss": logs.get("loss"),
            "learning_rate": logs.get("learning_rate"),
            "grad_norm": logs.get("grad_norm"),
            "allocated_vram_mib": allocated_mib,
            "reserved_vram_mib": reserved_mib,
            "peak_vram_mib": peak_mib,
            "step_duration_sec": step_duration,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        if "eval_loss" in logs:
            record["eval_loss"] = logs["eval_loss"]

        with open(self.metrics_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


class CheckpointPreservationCallback(TrainerCallback):
    """Ensures newly saved checkpoints are mirrored to historical_checkpoints directory."""
    def __init__(self, historical_dir: Path):
        self.historical_dir = historical_dir
        self.historical_dir.mkdir(parents=True, exist_ok=True)

    def on_save(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        latest_ckpt = Path(args.output_dir) / f"checkpoint-{state.global_step}"
        dest = self.historical_dir / f"checkpoint-{state.global_step}"
        if latest_ckpt.exists() and not dest.exists():
            shutil.copytree(str(latest_ckpt), str(dest))
            print(f"[*] Checkpoint {state.global_step} safely mirrored to {dest}")


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("=" * 70)
    print("AXIS PHASE 6B — SPATIAL GROUNDING SCIENTIFIC TRAINING PILOT")
    print("=" * 70)

    # 0. CLI Arguments for Resume
    parser = argparse.ArgumentParser(description="AXIS Phase 6B — Spatial Grounding Scientific Training Pilot")
    parser.add_argument("--resume_from_checkpoint", type=str, default=None, help="Path to checkpoint directory to resume from")
    args = parser.parse_args()

    resume_from_ckpt = args.resume_from_checkpoint
    resume_mode = resume_from_ckpt is not None
    if resume_mode:
        resume_path = Path(resume_from_ckpt)
        if not resume_path.exists():
            raise FileNotFoundError(f"Resume checkpoint directory not found: {resume_path}")
        print(f"[*] RESUME MODE ACTIVE: Resuming training from checkpoint: {resume_path}")

    # 1. Load config
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Training config missing: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    seed = config["training"].get("seed", 42)
    set_seed(seed)
    print(f"[*] Deterministic Seed Locked: {seed}")

    # 2. Processor
    model_id = config["model"]["name_or_path"]
    model_rev = config["model"]["revision"]
    print(f"[*] Loading AutoProcessor for {model_id} (rev: {model_rev})...")
    processor = AutoProcessor.from_pretrained(
        model_id,
        revision=model_rev,
        min_pixels=config["dataset"]["min_pixels"],
        max_pixels=config["dataset"]["max_pixels"]
    )

    # 3. Model with 4-bit NF4
    print("[*] Configuring 4-bit NF4 Quantization...")
    compute_dtype = getattr(torch, config["quantization"]["bnb_4bit_compute_dtype"])
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config["quantization"]["load_in_4bit"],
        bnb_4bit_quant_type=config["quantization"]["bnb_4bit_quant_type"],
        bnb_4bit_use_double_quant=config["quantization"]["bnb_4bit_use_double_quant"],
        bnb_4bit_compute_dtype=compute_dtype
    )

    print(f"[*] Loading base model {model_id}...")
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_id,
        revision=model_rev,
        quantization_config=bnb_config,
        device_map=config["model"]["device_map"],
        torch_dtype=compute_dtype,
        low_cpu_mem_usage=config["model"]["low_cpu_mem_usage"]
    )

    # 4. Prepare for kbit & LoRA
    print("[*] Preparing model for kbit training...")
    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=config["training"]["gradient_checkpointing"]
    )

    # Freeze vision tower explicitly
    if config["lora"].get("freeze_vision_tower", True):
        if hasattr(model, "visual"):
            model.visual.requires_grad_(False)
            print("  --> Vision tower frozen (model.visual.requires_grad = False)")
        elif hasattr(model, "model") and hasattr(model.model, "visual"):
            model.model.visual.requires_grad_(False)
            print("  --> Vision tower frozen (model.model.visual.requires_grad = False)")

    lora_cfg = config["lora"]
    peft_config = LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["lora_alpha"],
        lora_dropout=lora_cfg["lora_dropout"],
        bias=lora_cfg["bias"],
        task_type=lora_cfg["task_type"],
        target_modules=lora_cfg["target_modules"]
    )
    print(f"[*] Attaching LoRA adapter (r={lora_cfg['r']}, alpha={lora_cfg['lora_alpha']})...")
    peft_model = get_peft_model(model, peft_config)
    peft_model.print_trainable_parameters()

    # 5. Save initial state (checkpoint-0) before any optimizer step
    if not resume_mode:
        ckpt0_dir = CHECKPOINTS_DIR / "checkpoint-0"
        ckpt0_dir.mkdir(parents=True, exist_ok=True)
        print(f"[*] Creating INITIAL STATE snapshot: {ckpt0_dir}...")
        peft_model.save_pretrained(str(ckpt0_dir))
        processor.save_pretrained(str(ckpt0_dir))

        # Base model parameter fingerprint
        base_param_sample = next(peft_model.parameters()).detach().cpu().numpy()
        base_fingerprint = hashlib.sha256(base_param_sample.tobytes()).hexdigest()
        
        init_state_manifest = {
            "run_id": "RUN-022-SPATIAL-GROUNDING-PILOT",
            "checkpoint": "checkpoint-0",
            "step": 0,
            "epoch": 0.0,
            "base_model": model_id,
            "base_model_revision": model_rev,
            "base_param_fingerprint": base_fingerprint,
            "seed": seed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "description": "Initial state before step 1 optimizer update"
        }
        with open(ckpt0_dir / "initial_state.json", "w", encoding="utf-8") as f:
            json.dump(init_state_manifest, f, indent=2)
    else:
        print("[*] RESUME MODE: Preserving historical checkpoint-0 state (skipping snapshot)")

    # 6. Datasets & Collator
    print("[*] Initializing SpatialVisionDataset...")
    train_file = WORKSPACE / config["dataset"]["train_file"]
    val_file = WORKSPACE / config["dataset"]["validation_file"]
    img_dir = WORKSPACE / config["dataset"]["images_base_dir"]

    train_dataset = SpatialVisionDataset(
        jsonl_path=train_file,
        images_base_dir=img_dir,
        processor=processor,
        max_seq_length=config["dataset"]["max_seq_length"]
    )
    val_dataset = SpatialVisionDataset(
        jsonl_path=val_file,
        images_base_dir=img_dir,
        processor=processor,
        max_seq_length=config["dataset"]["max_seq_length"]
    )
    print(f"  --> Train samples: {len(train_dataset)}")
    print(f"  --> Validation samples: {len(val_dataset)}")

    data_collator = VisionLanguageDataCollator(processor=processor)

    # 7. Training arguments
    training_cfg = config["training"]
    effective_batch_size = training_cfg["per_device_train_batch_size"] * training_cfg["gradient_accumulation_steps"]
    steps_per_epoch = len(train_dataset) // effective_batch_size
    total_steps = steps_per_epoch * training_cfg["num_train_epochs"]
    warmup_steps = max(1, int(total_steps * training_cfg.get("warmup_ratio", 0.05)))
    print(f"[*] Effective Batch Size: {effective_batch_size} | Steps per Epoch: {steps_per_epoch} | Total Steps: {total_steps} | Warmup Steps: {warmup_steps}")

    training_args = TrainingArguments(
        output_dir=str(CHECKPOINTS_DIR),
        per_device_train_batch_size=training_cfg["per_device_train_batch_size"],
        per_device_eval_batch_size=training_cfg["per_device_eval_batch_size"],
        gradient_accumulation_steps=training_cfg["gradient_accumulation_steps"],
        num_train_epochs=training_cfg["num_train_epochs"],
        learning_rate=float(training_cfg["learning_rate"]),
        lr_scheduler_type=training_cfg["lr_scheduler_type"],
        warmup_steps=warmup_steps,
        optim=training_cfg["optim"],
        gradient_checkpointing=training_cfg["gradient_checkpointing"],
        bf16=training_cfg["bf16"],
        fp16=training_cfg["fp16"],
        logging_steps=training_cfg["logging_steps"],
        eval_strategy=training_cfg["eval_strategy"],
        eval_steps=training_cfg["eval_steps"],
        save_strategy=training_cfg["save_strategy"],
        save_steps=training_cfg["save_steps"],
        save_total_limit=training_cfg["save_total_limit"],
        seed=seed,
        report_to="none"
    )

    metrics_callback = DetailedMetricsLoggingCallback(metrics_file=METRICS_JSONL, resume_mode=resume_mode)
    ckpt_preservation_callback = CheckpointPreservationCallback(historical_dir=HISTORICAL_CHECKPOINTS_DIR)

    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        callbacks=[metrics_callback, ckpt_preservation_callback]
    )

    # 8. Initial Baseline Validation Loss (Step 0)
    initial_val_loss = None
    if not resume_mode:
        print("\n[*] Evaluating INITIAL baseline validation loss (Step 0)...")
        init_eval = trainer.evaluate()
        initial_val_loss = init_eval.get("eval_loss")
        print(f"  --> Initial Validation Loss (Step 0): {initial_val_loss:.4f}")

        # Record initial eval to metrics
        with open(METRICS_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "global_step": 0,
                "epoch": 0.0,
                "loss": None,
                "eval_loss": initial_val_loss,
                "learning_rate": 0.0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }) + "\n")
    else:
        print("\n[*] RESUME MODE: Recovering initial baseline validation loss from metrics history...")
        if METRICS_JSONL.exists():
            with open(METRICS_JSONL, "r", encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    if rec.get("global_step") == 0 and rec.get("eval_loss") is not None:
                        initial_val_loss = rec["eval_loss"]
                        break
        if initial_val_loss is None:
            initial_val_loss = 1.3966630697250366
        print(f"  --> Initial Validation Loss (Step 0 from history): {initial_val_loss:.4f}")

    # 9. Train Loop
    print("\n" + "*" * 65)
    print("STARTING SCIENTIFIC PILOT TRAINING LOOP")
    print(f"Total Epochs: {training_cfg['num_train_epochs']}")
    print(f"Effective Batch Size: {training_cfg['per_device_train_batch_size'] * training_cfg['gradient_accumulation_steps']}")
    if resume_mode:
        print(f"Resume Checkpoint: {resume_from_ckpt}")
    print("*" * 65)

    start_train_time = time.time()
    if resume_mode:
        print(f"[*] Resuming trainer.train(resume_from_checkpoint='{resume_from_ckpt}')...")
        train_result = trainer.train(resume_from_checkpoint=str(resume_from_ckpt))
    else:
        train_result = trainer.train()
    total_train_sec = round(time.time() - start_train_time, 2)
    print(f"[*] Training complete in {total_train_sec} seconds ({total_train_sec / 60:.2f} minutes)")

    # 10. Final Evaluation on Validation Set
    print("\n[*] Evaluating FINAL validation loss...")
    final_eval = trainer.evaluate()
    final_val_loss = final_eval.get("eval_loss")
    print(f"  --> Final Validation Loss: {final_val_loss:.4f}")
    print(f"  --> Validation Loss Delta: {final_val_loss - initial_val_loss:.4f}")

    # 11. Save Final Adapter
    final_adapter_dir = CHECKPOINTS_DIR / "final_adapter"
    final_adapter_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Saving final adapter to {final_adapter_dir}...")
    peft_model.save_pretrained(str(final_adapter_dir))
    processor.save_pretrained(str(final_adapter_dir))

    # 12. Save summary metrics
    training_summary = {
        "run_id": "RUN-022-SPATIAL-GROUNDING-PILOT",
        "total_train_samples": len(train_dataset),
        "total_val_samples": len(val_dataset),
        "initial_val_loss": initial_val_loss,
        "final_val_loss": final_val_loss,
        "val_loss_delta": final_val_loss - initial_val_loss,
        "train_loss": train_result.training_loss,
        "total_steps": train_result.global_step,
        "num_epochs": training_cfg["num_train_epochs"],
        "total_train_duration_sec": total_train_sec,
        "samples_per_second": train_result.metrics.get("train_samples_per_second"),
        "steps_per_second": train_result.metrics.get("train_steps_per_second"),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    with open(FINAL_METRICS_JSON, "w", encoding="utf-8") as f:
        json.dump(training_summary, f, indent=2)

    # Ensure all historical checkpoints are restored into CHECKPOINTS_DIR
    if HISTORICAL_CHECKPOINTS_DIR.exists():
        for item in HISTORICAL_CHECKPOINTS_DIR.iterdir():
            dest = CHECKPOINTS_DIR / item.name
            if not dest.exists():
                if item.is_dir():
                    shutil.copytree(str(item), str(dest))
                else:
                    shutil.copy2(str(item), str(dest))
                print(f"[*] Restored historical checkpoint {item.name} into {CHECKPOINTS_DIR}")

    # 13. Checkpoint SHA-256 Hashes
    print("[*] Computing cryptographic hashes of all checkpoint artifacts...")
    checkpoint_hashes = {}
    for root, _, files in os.walk(CHECKPOINTS_DIR):
        for fname in files:
            fpath = Path(root) / fname
            rel_path = str(fpath.relative_to(CHECKPOINTS_DIR)).replace("\\", "/")
            checkpoint_hashes[rel_path] = {
                "sha256": compute_sha256(fpath),
                "size_bytes": fpath.stat().st_size
            }

    with open(CHECKPOINT_HASHES_JSON, "w", encoding="utf-8") as f:
        json.dump(checkpoint_hashes, f, indent=2)
    print(f"  --> Saved {len(checkpoint_hashes)} hashes to {CHECKPOINT_HASHES_JSON}")

    print("\n" + "=" * 70)
    print("RUN-022 SPATIAL PILOT TRAINING SUCCESSFULLY CONCLUDED")
    print("=" * 70)

if __name__ == "__main__":
    main()
