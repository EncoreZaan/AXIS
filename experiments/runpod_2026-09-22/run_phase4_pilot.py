#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AXIS Phase 4 — Controlled Scientific Training — First Real-Data Pilot
RUN-019-FIRST-REAL-DATA-QLORA Execution Engine
Protocol-Compliant Implementation
"""

import os
import sys
import gc
import json
import time
import shutil
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Any, List

import yaml
from PIL import Image
import torch
from transformers import (
    AutoProcessor,
    Qwen2VLForConditionalGeneration,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    TrainerCallback,
    set_seed
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel
)
from qwen_vl_utils import process_vision_info

# Setup paths
AXIS_ROOT = Path("/workspace/AXIS")
sys.path.insert(0, str(AXIS_ROOT / "experiment_package"))
from train_qlora import ARCHIVisionDataset, VisionLanguageDataCollator

EXP_DIR = AXIS_ROOT / "experiments" / "runpod_2026-09-22"
PILOT_DIR = EXP_DIR / "REAL_DATA_PILOT"
TRAIN_FILE = str(PILOT_DIR / "train.jsonl")
VAL_FILE = str(PILOT_DIR / "validation.jsonl")
IMAGES_BASE = str(PILOT_DIR)
CONFIG_YAML = PILOT_DIR / "pilot_training_config.yaml"

RUN_ID = "RUN-019-FIRST-REAL-DATA-QLORA"
OUTPUT_DIR = EXP_DIR / RUN_ID
ROOT_RUN_DIR = AXIS_ROOT / RUN_ID

MODEL_ID = "Qwen/Qwen2-VL-7B-Instruct"
MODEL_REVISION = "eed13092ef92e448dd6875b2a00151bd3f7db0ac"
EXPECTED_COMMIT = "f4d5e949053743d97091ea35080de5d365899df7"

EXPECTED_DATASET_HASHES = {
    "train.jsonl": "246e22b372180a6b4be6c61eeea77e10a2c2d35b7128503463d32d6185ec3c47",
    "validation.jsonl": "23a0f44ec54a98202d2e47f582b901010f286f7ad83be990447317e0029cee0e",
    "test.jsonl": "113b7313340d1026c6a693f6fb2e8b00fd41dde06485f299b13add1018f37eb1",
    "manifest.jsonl": "340ce603432d0057837b6aab9484ad369895d0279023b79169f6ce62ab69564a",
    "dataset_config.json": "1d07982755f61200614039912b498c2df5e29f8701599e3ef8da605a55f18996",
    "README.md": "12b9af24029546580f77dfbfaa131e1bc5355ab247cb8059ee104651c8f06546"
}


def file_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def get_gpu_telemetry():
    allocated = torch.cuda.memory_allocated() / (1024 ** 2)
    reserved = torch.cuda.memory_reserved() / (1024 ** 2)
    max_allocated = torch.cuda.max_memory_allocated() / (1024 ** 2)
    return {
        "allocated_mib": allocated,
        "reserved_mib": reserved,
        "max_allocated_mib": max_allocated
    }


def clear_gpu():
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()


class ScientificMetricsCallback(TrainerCallback):
    def __init__(self, metrics_jsonl_path: Path):
        self.metrics_jsonl_path = metrics_jsonl_path
        self.metrics_file = open(metrics_jsonl_path, "w", encoding="utf-8")
        self.step_start_time = time.time()
        self.last_log_time = time.time()
        self.all_logs = []
        self.abort_reason = None
        self.has_nan_inf = False
        self.oom_occurred = False

    def on_step_begin(self, args, state, control, **kwargs):
        self.step_start_time = time.time()

    def on_log(self, args, state, control, logs=None, **kwargs):
        if not logs:
            return
        now = time.time()
        step_dur = now - self.last_log_time
        self.last_log_time = now

        loss = logs.get("loss")
        lr = logs.get("learning_rate")
        grad_norm = logs.get("grad_norm")

        # Invariant checks: NaN / Inf
        if loss is not None:
            if torch.isnan(torch.tensor(loss)) or torch.isinf(torch.tensor(loss)):
                self.abort_reason = f"FATAL: NaN/Inf loss ({loss}) at step {state.global_step}"
                self.has_nan_inf = True
                print(f"[FAIL] {self.abort_reason}")
                control.should_training_stop = True

        telem = get_gpu_telemetry()
        entry = {
            "global_step": state.global_step,
            "epoch": round(state.epoch, 4) if state.epoch is not None else None,
            "loss": float(loss) if loss is not None else None,
            "learning_rate": float(lr) if lr is not None else None,
            "grad_norm": float(grad_norm) if grad_norm is not None else None,
            "allocated_vram_mib": round(telem["allocated_mib"], 2),
            "reserved_vram_mib": round(telem["reserved_mib"], 2),
            "peak_vram_mib": round(telem["max_allocated_mib"], 2),
            "step_duration_sec": round(step_dur, 4),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        }
        self.metrics_file.write(json.dumps(entry) + "\n")
        self.metrics_file.flush()
        self.all_logs.append(entry)

        if loss is not None:
            gn_str = f"{grad_norm:.4f}" if grad_norm is not None else "N/A"
            lr_str = f"{lr:.2e}" if lr is not None else "N/A"
            ep_str = f"{state.epoch:.2f}" if state.epoch is not None else "N/A"
            print(f"[RUN-019 | Step {state.global_step:03d} | Ep {ep_str}] Loss: {loss:.4f} | LR: {lr_str} | GradNorm: {gn_str} | VRAM: {telem['allocated_mib']:.1f} MiB (Peak: {telem['max_allocated_mib']:.1f} MiB)")

    def close(self):
        if not self.metrics_file.closed:
            self.metrics_file.close()


def main():
    print(f"\n{'='*75}")
    print(f"AXIS PHASE 4 — SCIENTIFIC TRAINING ENGINE")
    print(f"RUN ID: {RUN_ID}")
    print(f"{'='*75}\n")

    run_start_time = time.time()
    set_seed(42)
    clear_gpu()

    # 1. PRE-FLIGHT VERIFICATIONS
    print("[1/9] Verifying Immutable Pre-Flight Invariants...")
    # Git
    commit_res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(AXIS_ROOT), capture_output=True, text=True)
    actual_commit = commit_res.stdout.strip()
    if actual_commit != EXPECTED_COMMIT:
        raise RuntimeError(f"GIT_COMMIT_MISMATCH: expected {EXPECTED_COMMIT}, got {actual_commit}")

    # Dataset Hashes
    for fn, exp_hash in EXPECTED_DATASET_HASHES.items():
        act_hash = file_sha256(PILOT_DIR / fn)
        if act_hash != exp_hash:
            raise RuntimeError(f"DATASET_HASH_MISMATCH: {fn} actual {act_hash} != expected {exp_hash}")

    print("Pre-flight invariants verified successfully.")

    # Prepare output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    checkpoints_dir = OUTPUT_DIR / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)

    # Copy training config to output dir
    shutil.copy2(CONFIG_YAML, OUTPUT_DIR / "training_config.yaml")

    # 2. LOAD PROCESSOR
    print(f"[2/9] Loading AutoProcessor from {MODEL_ID} (rev: {MODEL_REVISION})...")
    processor = AutoProcessor.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        min_pixels=200704,
        max_pixels=262144
    )

    # 3. LOAD DATASETS
    print(f"[3/9] Ingesting Real Pilot Datasets...")
    train_dataset = ARCHIVisionDataset(
        jsonl_file=TRAIN_FILE,
        images_base_dir=IMAGES_BASE,
        processor=processor,
        max_seq_length=1536
    )
    val_dataset = ARCHIVisionDataset(
        jsonl_file=VAL_FILE,
        images_base_dir=IMAGES_BASE,
        processor=processor,
        max_seq_length=1536
    )
    data_collator = VisionLanguageDataCollator(processor=processor)
    print(f"Datasets loaded: Train={len(train_dataset)}, Validation={len(val_dataset)}")
    assert len(train_dataset) == 775, f"Expected 775 train samples, got {len(train_dataset)}"
    assert len(val_dataset) == 98, f"Expected 98 validation samples, got {len(val_dataset)}"

    # 4. LOAD MODEL (4-bit NF4)
    print(f"[4/9] Initializing Qwen2-VL Model in 4-bit NF4...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

    # Freeze vision tower explicitly
    if hasattr(model, "visual"):
        model.visual.requires_grad_(False)
    elif hasattr(model, "model") and hasattr(model.model, "visual"):
        model.model.visual.requires_grad_(False)

    # 5. ATTACH LoRA ADAPTER
    print(f"[5/9] Attaching LoRA Adapters (r=16, alpha=32)...")
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)
    trainable_params, all_params = model.get_nb_trainable_parameters()
    print(f"Trainable Parameters: {trainable_params:,} / {all_params:,} ({100 * trainable_params / all_params:.3f}%)")

    # 6. BASELINE EVALUATION (Zero-shot / Untrained LoRA on Validation Set)
    print(f"\n[6/9] Computing Initial Baseline Validation Loss on all 98 validation assets...")
    eval_training_args = TrainingArguments(
        output_dir=str(checkpoints_dir),
        per_device_eval_batch_size=1,
        dataloader_num_workers=0,
        bf16=True,
        fp16=False,
        report_to="none"
    )
    eval_trainer = Trainer(
        model=model,
        args=eval_training_args,
        eval_dataset=val_dataset,
        data_collator=data_collator
    )
    baseline_eval_start = time.time()
    baseline_eval_results = eval_trainer.evaluate()
    baseline_eval_duration = time.time() - baseline_eval_start
    baseline_val_loss = float(baseline_eval_results.get("eval_loss", 0.0))
    print(f"Baseline Validation Loss (initial state): {baseline_val_loss:.4f} (computed in {baseline_eval_duration:.2f}s)")

    # Baseline Qualitative Generation on 5 fixed validation items (indices: 0, 20, 40, 60, 80)
    qualitative_indices = [0, 20, 40, 60, 80]
    qualitative_records = []
    print(f"Running baseline qualitative inference on {len(qualitative_indices)} fixed validation assets...")
    model.eval()

    for idx in qualitative_indices:
        raw_sample = val_dataset.samples[idx]
        image_path = PILOT_DIR / raw_sample["image"]
        img = Image.open(image_path).convert("RGB")
        question = raw_sample["question"]
        context = raw_sample["context"]
        ref_answer = raw_sample["answer"]

        prompt_text = f"Contexte : {context}\n\nQuestion : {question}"
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": str(image_path)},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ]
        text_prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text_prompt],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to("cuda")

        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False
            )
            trimmed_ids = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            base_generated_text = processor.batch_decode(
                trimmed_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]

        qualitative_records.append({
            "index": idx,
            "id": raw_sample["id"],
            "source_id": raw_sample.get("source_id", "CORE_RPLAN"),
            "image": raw_sample["image"],
            "context": context,
            "question": question,
            "reference_answer": ref_answer,
            "base_model_response": base_generated_text,
            "trained_model_response": None
        })

    clear_gpu()

    # 7. TRAINING EXECUTION
    print(f"\n[7/9] Launching Controlled Training: 2 Epochs, Micro-batch=1, GradAccum=8, LR=1.0e-4...")
    training_args = TrainingArguments(
        output_dir=str(checkpoints_dir),
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=2,
        learning_rate=1.0e-4,
        lr_scheduler_type="cosine",
        warmup_steps=9,
        optim="paged_adamw_8bit",
        gradient_checkpointing=True,
        bf16=True,
        fp16=False,
        logging_steps=1,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        seed=42,
        dataloader_num_workers=0,
        report_to="none"
    )

    metrics_cb = ScientificMetricsCallback(OUTPUT_DIR / "training_metrics.jsonl")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        callbacks=[metrics_cb]
    )

    train_start = time.time()
    train_result = trainer.train()
    train_duration = time.time() - train_start
    metrics_cb.close()

    print(f"\nTraining completed in {train_duration:.2f} seconds ({train_duration/60:.2f} minutes).")
    print(f"Total training steps: {trainer.state.global_step}")

    # 8. POST-TRAINING VALIDATION EVALUATION & QUALITATIVE INFERENCE
    print(f"\n[8/9] Executing Post-Training Validation Evaluation on 98 validation assets...")
    trained_eval_start = time.time()
    trained_eval_results = trainer.evaluate()
    trained_eval_duration = time.time() - trained_eval_start
    trained_val_loss = float(trained_eval_results.get("eval_loss", 0.0))
    print(f"Trained Validation Loss: {trained_val_loss:.4f} (computed in {trained_eval_duration:.2f}s)")

    val_loss_delta = trained_val_loss - baseline_val_loss
    val_loss_relative_pct = (val_loss_delta / baseline_val_loss) * 100.0
    print(f"Validation Loss Delta: {val_loss_delta:+.4f} ({val_loss_relative_pct:+.2f}%)")

    # Qualitative Inference with Trained Model
    print(f"Running qualitative inference on trained model across {len(qualitative_indices)} fixed assets...")
    model.eval()
    for rec in qualitative_records:
        image_path = PILOT_DIR / rec["image"]
        prompt_text = f"Contexte : {rec['context']}\n\nQuestion : {rec['question']}"
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": str(image_path)},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ]
        text_prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text_prompt],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to("cuda")

        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False
            )
            trimmed_ids = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            trained_generated_text = processor.batch_decode(
                trimmed_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]
        rec["trained_model_response"] = trained_generated_text

    # 9. CHECKPOINT PRESERVATION, HASHING & METRICS PERSISTENCE
    print(f"\n[9/9] Persisting Checkpoints, Calculating SHA-256 and Generating Final Artifacts...")
    final_adapter_dir = checkpoints_dir / "final_adapter"
    model.save_pretrained(final_adapter_dir)
    processor.save_pretrained(final_adapter_dir)

    # Save validation metrics
    validation_metrics = {
        "run_id": RUN_ID,
        "dataset": "REAL_DATA_PILOT",
        "validation_samples": len(val_dataset),
        "baseline_val_loss": baseline_val_loss,
        "trained_val_loss": trained_val_loss,
        "val_loss_delta": val_loss_delta,
        "val_loss_relative_pct": val_loss_relative_pct,
        "baseline_eval_duration_sec": baseline_eval_duration,
        "trained_eval_duration_sec": trained_eval_duration,
        "training_duration_sec": train_duration,
        "total_global_steps": trainer.state.global_step,
        "train_loss_final": float(train_result.training_loss) if hasattr(train_result, "training_loss") else None,
        "log_history": trainer.state.log_history
    }
    with open(OUTPUT_DIR / "validation_metrics.json", "w", encoding="utf-8") as f:
        json.dump(validation_metrics, f, indent=2)

    # Save qualitative evaluation
    with open(OUTPUT_DIR / "qualitative_eval.json", "w", encoding="utf-8") as f:
        json.dump(qualitative_records, f, indent=2)

    # Checkpoint hashing
    checkpoint_hashes = {}
    for root, dirs, files in os.walk(checkpoints_dir):
        for file in files:
            full_path = Path(root) / file
            rel_path = str(full_path.relative_to(OUTPUT_DIR))
            checkpoint_hashes[rel_path] = {
                "sha256": file_sha256(full_path),
                "size_bytes": full_path.stat().st_size
            }
    with open(OUTPUT_DIR / "checkpoint_hashes.json", "w", encoding="utf-8") as f:
        json.dump(checkpoint_hashes, f, indent=2)

    # Environment snapshot
    import transformers
    import peft
    import bitsandbytes
    env_snapshot = {
        "run_id": RUN_ID,
        "git_commit": EXPECTED_COMMIT,
        "gpu": torch.cuda.get_device_name(0),
        "gpu_total_vram_mib": torch.cuda.get_device_properties(0).total_memory / (1024 ** 2),
        "cuda_version": torch.version.cuda,
        "python_version": sys.version.split()[0],
        "pytorch_version": torch.__version__,
        "transformers_version": transformers.__version__,
        "peft_version": peft.__version__,
        "bitsandbytes_version": bitsandbytes.__version__,
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION
    }
    with open(OUTPUT_DIR / "environment_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(env_snapshot, f, indent=2)

    # Run Manifest
    total_run_duration = time.time() - run_start_time
    run_manifest = {
        "run_id": RUN_ID,
        "git_commit": EXPECTED_COMMIT,
        "dataset_sha256": EXPECTED_DATASET_HASHES,
        "model_revision": MODEL_REVISION,
        "python_version": sys.version.split()[0],
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "gpu_name": torch.cuda.get_device_name(0),
        "transformers_version": transformers.__version__,
        "peft_version": peft.__version__,
        "bitsandbytes_version": bitsandbytes.__version__,
        "seed": 42,
        "lora_r": 16,
        "lora_alpha": 32,
        "learning_rate": 1.0e-4,
        "min_pixels": 200704,
        "max_pixels": 262144,
        "micro_batch_size": 1,
        "gradient_accumulation_steps": 8,
        "max_sequence_length": 1536,
        "optimizer": "paged_adamw_8bit",
        "gradient_checkpointing": True,
        "num_train_epochs": 2,
        "total_train_samples": len(train_dataset),
        "total_validation_samples": len(val_dataset),
        "total_global_steps": trainer.state.global_step,
        "training_duration_sec": train_duration,
        "total_run_duration_sec": total_run_duration,
        "baseline_val_loss": baseline_val_loss,
        "trained_val_loss": trained_val_loss,
        "val_loss_delta": val_loss_delta,
        "val_loss_relative_pct": val_loss_relative_pct,
        "status": "COMPLETE"
    }
    with open(OUTPUT_DIR / "run_manifest.json", "w", encoding="utf-8") as f:
        json.dump(run_manifest, f, indent=2)

    # Mirror output directory to /workspace/AXIS/RUN-019-FIRST-REAL-DATA-QLORA
    if ROOT_RUN_DIR.exists():
        shutil.rmtree(ROOT_RUN_DIR)
    shutil.copytree(OUTPUT_DIR, ROOT_RUN_DIR)

    print(f"\n{'='*75}")
    print(f"RUN-019 EXECUTION COMPLETED SUCCESSFULLY IN {total_run_duration:.1f}s")
    print(f"All artifacts created in: {OUTPUT_DIR}")
    print(f"{'='*75}\n")


if __name__ == "__main__":
    main()
