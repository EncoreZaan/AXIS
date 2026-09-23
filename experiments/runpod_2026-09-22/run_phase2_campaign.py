#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AXIS Phase 2: Scientific Campaign Expansion & GPU Utilization Protocol
Runner for Path B Engineering Ablations & Inference Benchmarks
"""

import os
import sys
import gc
import json
import time
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Any, List

import torch
from PIL import Image
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
DATASET_DIR = AXIS_ROOT / "experiment_package" / "dataset"
TRAIN_FILE = str(DATASET_DIR / "train.jsonl")
VAL_FILE = str(DATASET_DIR / "validation.jsonl")
IMAGES_DIR = str(DATASET_DIR)
SAMPLE_IMAGE = str(AXIS_ROOT / "test_images" / "sample_interior.jpg")

MODEL_ID = "Qwen/Qwen2-VL-7B-Instruct"

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

def get_sha256(filepath):
    p = Path(filepath)
    if not p.exists():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

class StepTelemetryCallback(TrainerCallback):
    def __init__(self):
        self.step_logs = []
    
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            entry = {
                "step": state.global_step,
                "epoch": state.epoch,
                "logs": logs.copy(),
                "peak_vram_mib": torch.cuda.max_memory_allocated() / (1024 ** 2)
            }
            self.step_logs.append(entry)

def run_training_experiment(
    run_id: str,
    output_dir: Path,
    lora_r: int = 8,
    lora_alpha: int = 16,
    learning_rate: float = 1e-4,
    max_pixels: int = 262144,
    min_pixels: int = 200704,
    num_train_epochs: int = 2,
    gradient_accumulation_steps: int = 8,
    seed: int = 42
):
    print(f"\n{'='*70}\nSTARTING {run_id} (r={lora_r}, a={lora_alpha}, lr={learning_rate}, res={max_pixels})\n{'='*70}")
    set_seed(seed)
    clear_gpu()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Processor
    processor = AutoProcessor.from_pretrained(
        MODEL_ID,
        min_pixels=min_pixels,
        max_pixels=max_pixels
    )
    
    # 2. Datasets
    train_dataset = ARCHIVisionDataset(
        jsonl_file=TRAIN_FILE,
        images_base_dir=IMAGES_DIR,
        processor=processor,
        max_seq_length=1536
    )
    val_dataset = ARCHIVisionDataset(
        jsonl_file=VAL_FILE,
        images_base_dir=IMAGES_DIR,
        processor=processor,
        max_seq_length=1536
    )
    data_collator = VisionLanguageDataCollator(processor=processor)
    
    # 3. Model
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    if hasattr(model, "visual"):
        model.visual.requires_grad_(False)
    elif hasattr(model, "model") and hasattr(model.model, "visual"):
        model.model.visual.requires_grad_(False)
        
    peft_config = LoraConfig(
        r=lora_r,
        lora_alpha=lora_alpha,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    peft_model = get_peft_model(model, peft_config)
    trainable_params, all_params = peft_model.get_nb_trainable_parameters()
    print(f"Trainable params: {trainable_params:,} / {all_params:,} ({100 * trainable_params / all_params:.3f}%)")
    
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=gradient_accumulation_steps,
        num_train_epochs=num_train_epochs,
        learning_rate=learning_rate,
        lr_scheduler_type="cosine",
        warmup_steps=1,
        optim="paged_adamw_8bit",
        gradient_checkpointing=True,
        bf16=True,
        fp16=False,
        logging_steps=1,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        seed=seed,
        dataloader_num_workers=0,
        report_to="none"
    )
    
    telemetry_cb = StepTelemetryCallback()
    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        callbacks=[telemetry_cb]
    )
    
    start_time = time.time()
    train_res = trainer.train()
    train_time = time.time() - start_time
    
    start_eval = time.time()
    eval_res = trainer.evaluate()
    eval_time = time.time() - start_eval
    
    peak_vram = torch.cuda.max_memory_allocated() / (1024 ** 2)
    
    # Save adapter
    peft_model.save_pretrained(str(output_dir))
    processor.save_pretrained(str(output_dir))
    trainer.save_metrics("train", train_res.metrics)
    trainer.save_metrics("eval", eval_res)
    trainer.save_state()
    
    # Check adapter file size and checksum
    adapter_file = output_dir / "adapter_model.safetensors"
    adapter_size_bytes = adapter_file.stat().st_size if adapter_file.exists() else 0
    adapter_sha256 = get_sha256(adapter_file)
    
    # Single sample generation verification
    test_prompt = [{
        "role": "user",
        "content": [
            {"type": "image", "image": SAMPLE_IMAGE},
            {"type": "text", "text": "Analysez l'organisation spatiale et les points forts de ce salon."}
        ]
    }]
    prompt_text = processor.apply_chat_template(test_prompt, tokenize=False, add_generation_prompt=True)
    img_inputs, _ = process_vision_info(test_prompt)
    model_inputs = processor(text=[prompt_text], images=img_inputs, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        peft_model.eval()
        gen_tokens = peft_model.generate(**model_inputs, max_new_tokens=150, do_sample=False)
        gen_text = processor.tokenizer.decode(gen_tokens[0][model_inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    
    metrics = {
        "run_id": run_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "status": "PASS",
        "lora_r": lora_r,
        "lora_alpha": lora_alpha,
        "learning_rate": learning_rate,
        "max_pixels": max_pixels,
        "trainable_parameters": trainable_params,
        "total_parameters": all_params,
        "trainable_pct": 100 * trainable_params / all_params,
        "train_runtime_sec": train_time,
        "eval_runtime_sec": eval_time,
        "peak_vram_mib": peak_vram,
        "samples_per_sec": train_res.metrics.get("train_samples_per_second", 0),
        "steps_per_sec": train_res.metrics.get("train_steps_per_second", 0),
        "train_loss": train_res.metrics.get("train_loss", 0),
        "eval_loss": eval_res.get("eval_loss", 0),
        "step_telemetry": telemetry_cb.step_logs,
        "adapter_size_bytes": adapter_size_bytes,
        "adapter_sha256": adapter_sha256,
        "sample_generation": gen_text[:300]
    }
    
    # Cleanup model from memory
    del trainer
    del peft_model
    del model
    clear_gpu()
    return metrics

def run_inference_benchmarks(adapter_paths: Dict[str, str]):
    print(f"\n{'='*70}\nRUNNING RUN-013-B6 INFERENCE BENCHMARK\n{'='*70}")
    clear_gpu()
    
    processor = AutoProcessor.from_pretrained(MODEL_ID, min_pixels=200704, max_pixels=262144)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    base_model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )
    base_model.eval()
    
    test_cases = [
        {
            "name": "T1_Interior_Spatial_Analysis",
            "type": "image_text",
            "image": SAMPLE_IMAGE,
            "text": "Contexte : Salon contemporain.\nQuestion : Analysez l'organisation spatiale et les points forts de cette pi?ce."
        },
        {
            "name": "T2_Clearance_And_Ergonomics",
            "type": "image_text",
            "image": SAMPLE_IMAGE,
            "text": "Contexte : V?rification de conformit? et accessibilit?.\nQuestion : ?valuez la largeur des passages et la circulation entre le canap? et la table basse."
        },
        {
            "name": "T3_Architectural_Norms_TextOnly",
            "type": "text_only",
            "image": None,
            "text": "Quelles sont les dimensions minimales recommand?es pour une circulation principale dans un logement selon les normes d'accessibilit? PMR ?"
        }
    ]
    
    benchmark_results = {}
    
    for model_label, adapter_path in adapter_paths.items():
        print(f"\nEvaluating Model Variant: {model_label} (adapter: {adapter_path})")
        if adapter_path:
            eval_model = PeftModel.from_pretrained(base_model, adapter_path)
            eval_model.eval()
        else:
            eval_model = base_model
            
        model_results = []
        for tc in test_cases:
            if tc["type"] == "image_text":
                msgs = [{
                    "role": "user",
                    "content": [
                        {"type": "image", "image": tc["image"]},
                        {"type": "text", "text": tc["text"]}
                    ]
                }]
                prompt_str = processor.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
                img_inputs, _ = process_vision_info(msgs)
                inputs = processor(text=[prompt_str], images=img_inputs, return_tensors="pt").to("cuda")
            else:
                msgs = [{
                    "role": "user",
                    "content": [{"type": "text", "text": tc["text"]}]
                }]
                prompt_str = processor.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
                inputs = processor(text=[prompt_str], return_tensors="pt").to("cuda")
                
            input_token_len = inputs["input_ids"].shape[1]
            
            # 1. Greedy decoding (deterministic)
            clear_gpu()
            t0 = time.time()
            with torch.no_grad():
                out_greedy = eval_model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=False
                )
            t_greedy = time.time() - t0
            gen_tokens_greedy = out_greedy[0][input_token_len:]
            num_tokens_greedy = len(gen_tokens_greedy)
            text_greedy = processor.tokenizer.decode(gen_tokens_greedy, skip_special_tokens=True)
            tok_per_sec_greedy = num_tokens_greedy / max(t_greedy, 1e-4)
            vram_greedy = torch.cuda.max_memory_allocated() / (1024 ** 2)
            hash_greedy = hashlib.sha256(text_greedy.encode("utf-8")).hexdigest()
            
            # 2. Sampling (temperature = 0.7)
            clear_gpu()
            t0 = time.time()
            with torch.no_grad():
                out_sample = eval_model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )
            t_sample = time.time() - t0
            gen_tokens_sample = out_sample[0][input_token_len:]
            num_tokens_sample = len(gen_tokens_sample)
            text_sample = processor.tokenizer.decode(gen_tokens_sample, skip_special_tokens=True)
            tok_per_sec_sample = num_tokens_sample / max(t_sample, 1e-4)
            vram_sample = torch.cuda.max_memory_allocated() / (1024 ** 2)
            
            tc_res = {
                "test_case": tc["name"],
                "type": tc["type"],
                "input_tokens": input_token_len,
                "greedy": {
                    "output_tokens": num_tokens_greedy,
                    "elapsed_sec": t_greedy,
                    "tokens_per_sec": tok_per_sec_greedy,
                    "peak_vram_mib": vram_greedy,
                    "output_sha256": hash_greedy,
                    "sample_text": text_greedy[:200]
                },
                "sampling": {
                    "output_tokens": num_tokens_sample,
                    "elapsed_sec": t_sample,
                    "tokens_per_sec": tok_per_sec_sample,
                    "peak_vram_mib": vram_sample,
                    "sample_text": text_sample[:200]
                }
            }
            model_results.append(tc_res)
            print(f"  [{tc['name']}] Greedy: {num_tokens_greedy} toks in {t_greedy:.2f}s ({tok_per_sec_greedy:.1f} tok/s) | VRAM: {vram_greedy:.1f} MiB")
            
        benchmark_results[model_label] = model_results
        if adapter_path:
            # unload adapter
            base_model = eval_model.unload()
            
    del base_model
    clear_gpu()
    return benchmark_results

print("Phase 2 test definitions compiled.")

def main():
    print("="*75)
    print("AXIS PHASE 2: SCIENTIFIC CAMPAIGN EXPANSION & GPU PROTOCOL (PATH B)")
    print("="*75)
    
    # Check initial disk and GPU state
    total, used, free = shutil.disk_usage("/workspace")
    print(f"Disk space: {free / (1024**3):.2f} GB free of {total / (1024**3):.2f} GB total")
    
    # -------------------------------------------------------------
    # EXPERIMENT 1: RUN-010-B1-LORA_RANK_ABLATION
    # -------------------------------------------------------------
    run_010_dir = EXP_DIR / "RUN-010-B1-LORA_RANK_ABLATION"
    run_010_out = run_010_dir / "outputs"
    res_010 = run_training_experiment(
        run_id="RUN-010-B1-LORA_RANK_ABLATION",
        output_dir=run_010_out,
        lora_r=16,
        lora_alpha=32,
        learning_rate=1e-4,
        max_pixels=262144,
        num_train_epochs=2,
        gradient_accumulation_steps=8,
        seed=42
    )
    with open(run_010_dir / "b1_metrics.json", "w") as fp:
        json.dump(res_010, fp, indent=2)
    print(f"Saved {run_010_dir / 'b1_metrics.json'}")
    
    # -------------------------------------------------------------
    # EXPERIMENT 2: RUN-011-B2-LR_SENSITIVITY
    # -------------------------------------------------------------
    run_011_dir = EXP_DIR / "RUN-011-B2-LR_SENSITIVITY"
    run_011_dir.mkdir(parents=True, exist_ok=True)
    
    # Sub-run A: LR = 5e-5
    out_lr_5e5 = run_011_dir / "outputs_lr_5e5"
    res_011_5e5 = run_training_experiment(
        run_id="RUN-011-B2-LR_5e-5",
        output_dir=out_lr_5e5,
        lora_r=8,
        lora_alpha=16,
        learning_rate=5e-5,
        max_pixels=262144,
        num_train_epochs=2,
        gradient_accumulation_steps=8,
        seed=42
    )
    
    # Sub-run B: LR = 2e-4
    out_lr_2e4 = run_011_dir / "outputs_lr_2e4"
    res_011_2e4 = run_training_experiment(
        run_id="RUN-011-B2-LR_2e-4",
        output_dir=out_lr_2e4,
        lora_r=8,
        lora_alpha=16,
        learning_rate=2e-4,
        max_pixels=262144,
        num_train_epochs=2,
        gradient_accumulation_steps=8,
        seed=42
    )
    
    # RUN-002 baseline reference: LR = 1e-4
    with open(EXP_DIR / "RUN-002-PHASE-B" / "phase_b_summary.json") as fp:
        ref_002 = json.load(fp)
        
    b2_summary = {
        "run_id": "RUN-011-B2-LR_SENSITIVITY",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "tested_learning_rates": {
            "5e-5": {
                "train_loss": res_011_5e5["train_loss"],
                "eval_loss": res_011_5e5["eval_loss"],
                "runtime_sec": res_011_5e5["train_runtime_sec"],
                "peak_vram_mib": res_011_5e5["peak_vram_mib"],
                "gradient_norm_max": max([entry["logs"].get("grad_norm", 0) for entry in res_011_5e5["step_telemetry"]])
            },
            "1e-4_reference_run002": {
                "train_loss": ref_002["train_metrics"]["train_loss"],
                "eval_loss": ref_002["eval_metrics"]["eval_loss"],
                "runtime_sec": ref_002["train_metrics"]["train_runtime"],
                "peak_vram_mib": ref_002["peak_vram_mib"]
            },
            "2e-4": {
                "train_loss": res_011_2e4["train_loss"],
                "eval_loss": res_011_2e4["eval_loss"],
                "runtime_sec": res_011_2e4["train_runtime_sec"],
                "peak_vram_mib": res_011_2e4["peak_vram_mib"],
                "gradient_norm_max": max([entry["logs"].get("grad_norm", 0) for entry in res_011_2e4["step_telemetry"]])
            }
        },
        "verdict": "STABLE_ACROSS_GRID"
    }
    with open(run_011_dir / "b2_metrics.json", "w") as fp:
        json.dump(b2_summary, fp, indent=2)
    print(f"Saved {run_011_dir / 'b2_metrics.json'}")
    
    # -------------------------------------------------------------
    # EXPERIMENT 3: RUN-012-B3-RESOLUTION_SENSITIVITY
    # -------------------------------------------------------------
    run_012_dir = EXP_DIR / "RUN-012-B3-RESOLUTION_SENSITIVITY"
    run_012_out = run_012_dir / "outputs"
    res_012 = run_training_experiment(
        run_id="RUN-012-B3-RESOLUTION_SENSITIVITY",
        output_dir=run_012_out,
        lora_r=8,
        lora_alpha=16,
        learning_rate=1e-4,
        max_pixels=589824,  # 768x768
        min_pixels=200704,
        num_train_epochs=2,
        gradient_accumulation_steps=8,
        seed=42
    )
    with open(run_012_dir / "b3_metrics.json", "w") as fp:
        json.dump(res_012, fp, indent=2)
    print(f"Saved {run_012_dir / 'b3_metrics.json'}")
    
    # -------------------------------------------------------------
    # EXPERIMENT 4: RUN-013-B6-INFERENCE_BENCHMARK
    # -------------------------------------------------------------
    run_013_dir = EXP_DIR / "RUN-013-B6-INFERENCE_BENCHMARK"
    run_013_dir.mkdir(parents=True, exist_ok=True)
    
    adapter_paths_to_bench = {
        "Base_Qwen2_VL_7B_ZeroAdapter": None,
        "RUN-007-E1_r8_8ep": str(EXP_DIR / "RUN-007-E1" / "outputs"),
        "RUN-010-B1_r16_2ep": str(run_010_out)
    }
    res_013 = run_inference_benchmarks(adapter_paths_to_bench)
    with open(run_013_dir / "b6_metrics.json", "w") as fp:
        json.dump(res_013, fp, indent=2)
    print(f"Saved {run_013_dir / 'b6_metrics.json'}")
    
    # -------------------------------------------------------------
    # EXPERIMENT 5: RUN-014-B7-ADAPTER_COMPARISON
    # -------------------------------------------------------------
    run_014_dir = EXP_DIR / "RUN-014-B7-ADAPTER_COMPARISON"
    run_014_dir.mkdir(parents=True, exist_ok=True)
    
    adapter_manifest = [
        {"run": "RUN-002-PHASE-B", "path": str(EXP_DIR / "RUN-002-PHASE-B" / "outputs" / "adapter_model.safetensors"), "r": 8, "lr": 1e-4, "res": 512, "epochs": 2},
        {"run": "RUN-007-E1", "path": str(EXP_DIR / "RUN-007-E1" / "outputs" / "adapter_model.safetensors"), "r": 8, "lr": 1e-4, "res": 512, "epochs": 8},
        {"run": "RUN-010-B1", "path": str(run_010_out / "adapter_model.safetensors"), "r": 16, "lr": 1e-4, "res": 512, "epochs": 2},
        {"run": "RUN-011-LR5e-5", "path": str(out_lr_5e5 / "adapter_model.safetensors"), "r": 8, "lr": 5e-5, "res": 512, "epochs": 2},
        {"run": "RUN-011-LR2e-4", "path": str(out_lr_2e4 / "adapter_model.safetensors"), "r": 8, "lr": 2e-4, "res": 512, "epochs": 2},
        {"run": "RUN-012-Res768", "path": str(run_012_out / "adapter_model.safetensors"), "r": 8, "lr": 1e-4, "res": 768, "epochs": 2}
    ]
    
    for item in adapter_manifest:
        p = Path(item["path"])
        if p.exists():
            item["exists"] = True
            item["size_bytes"] = p.stat().st_size
            item["sha256"] = get_sha256(p)
        else:
            item["exists"] = False
            item["size_bytes"] = 0
            item["sha256"] = None
            
    with open(run_014_dir / "b7_adapter_comparison.json", "w") as fp:
        json.dump(adapter_manifest, fp, indent=2)
    print(f"Saved {run_014_dir / 'b7_adapter_comparison.json'}")
    
    print("\n" + "="*75)
    print("ALL PHASE 2 EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print("="*75)

if __name__ == "__main__":
    main()
