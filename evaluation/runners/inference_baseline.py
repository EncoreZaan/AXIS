import os
import sys
import time
import subprocess
import torch
from PIL import Image
from transformers import (
    Qwen2VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig
)
from qwen_vl_utils import process_vision_info

def get_nvidia_smi_vram():
    """Query nvidia-smi for current total GPU memory used by all processes."""
    try:
        res = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,nounits,noheader"],
            encoding="utf-8"
        ).strip().split(",")
        used = float(res[0].strip())
        total = float(res[1].strip())
        return used, total
    except Exception as e:
        return None, None

def main():
    print("=" * 60)
    print("ARCHI-AI: Initial Inference Baseline (Qwen2-VL-7B-Instruct)")
    print("=" * 60)

    # 1. Hardware & Environment Check
    if not torch.cuda.is_available():
        print("CRITICAL ERROR: CUDA is not available. Aborting.")
        sys.exit(1)

    device_name = torch.cuda.get_device_name(0)
    total_gpu_mem_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    sys_used_start, sys_total = get_nvidia_smi_vram()
    
    print(f"Device: {device_name}")
    print(f"Total VRAM: {total_gpu_mem_gb:.2f} GB")
    if sys_used_start is not None:
        print(f"System VRAM already in use: {sys_used_start:.1f} MB / {sys_total:.1f} MB")
    
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Version (PyTorch): {torch.version.cuda}")

    # 2. Test Image Verification
    image_path = os.path.join(os.path.dirname(__file__), "test_images", "sample_interior.jpg")
    if not os.path.exists(image_path):
        print(f"CRITICAL ERROR: Test image not found at {image_path}")
        sys.exit(1)
    
    img = Image.open(image_path)
    print(f"Test Image loaded: {image_path} (Resolution: {img.size[0]}x{img.size[1]}, Format: {img.format})")

    # 3. Model Configuration (4-bit NF4 Quantization for 8GB VRAM)
    model_id = "Qwen/Qwen2-VL-7B-Instruct"
    print("\n[Configuration]")
    print(f"Model ID: {model_id}")
    print("Quantization: 4-bit NormalFloat (NF4) via BitsAndBytes")
    print("Compute Dtype: torch.bfloat16")
    print("Double Quant: True")
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True
    )

    # Reset PyTorch peak memory stats
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.empty_cache()

    # 4. Loading Processor and Model
    print("\n[1/3] Loading Processor and Model weights (downloading if needed)...")
    load_start_time = time.time()
    
    # Cap image resolution tokens to max 1024x768 to keep vision activations well within 8GB VRAM
    processor = AutoProcessor.from_pretrained(
        model_id,
        min_pixels=256 * 28 * 28,
        max_pixels=1024 * 768
    )

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )
    
    load_end_time = time.time()
    load_duration = load_end_time - load_start_time
    print(f"--> Model loaded in {load_duration:.2f} seconds.")

    # Measure memory right after loading
    torch_alloc_after_load = torch.cuda.memory_allocated() / (1024 ** 2)
    torch_res_after_load = torch.cuda.memory_reserved() / (1024 ** 2)
    sys_used_after_load, _ = get_nvidia_smi_vram()
    
    print(f"VRAM PyTorch Allocated (Model Weights): {torch_alloc_after_load:.1f} MB ({torch_alloc_after_load / 1024:.2f} GB)")
    print(f"VRAM PyTorch Reserved: {torch_res_after_load:.1f} MB ({torch_res_after_load / 1024:.2f} GB)")
    if sys_used_after_load is not None:
        print(f"VRAM Total System Used: {sys_used_after_load:.1f} MB ({sys_used_after_load / 1024:.2f} GB)")

    # 5. Preparing the Multimodal Prompt
    prompt_french = (
        "Décris cette pièce en tant qu'architecte d'intérieur : "
        "précise le type d'espace, le style décoratif dominant, "
        "les matériaux identifiables et l'ambiance lumineuse."
    )
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {"type": "text", "text": prompt_french}
            ]
        }
    ]

    print("\n[2/3] Preparing prompt inputs...")
    print(f"Question posée : \"{prompt_french}\"")
    
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    )
    inputs = inputs.to("cuda")

    input_token_count = inputs.input_ids.shape[1]
    print(f"Total Input Tokens (text + vision patches): {input_token_count}")

    # 6. Running Inference
    print("\n[3/3] Running Inference...")
    torch.cuda.reset_peak_memory_stats()
    infer_start_time = time.time()

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=350,
            do_sample=False  # Greedy decoding for stable baseline benchmark
        )

    infer_end_time = time.time()
    infer_duration = infer_end_time - infer_start_time

    # Trim input tokens to isolate newly generated tokens
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )[0].strip()

    num_generated_tokens = len(generated_ids_trimmed[0])
    tokens_per_sec = num_generated_tokens / infer_duration if infer_duration > 0 else 0

    # Memory metrics during inference peak
    peak_alloc = torch.cuda.max_memory_allocated() / (1024 ** 2)
    peak_res = torch.cuda.max_memory_reserved() / (1024 ** 2)
    sys_used_after_infer, _ = get_nvidia_smi_vram()

    # 7. Print Results Summary
    print("\n" + "=" * 60)
    print("RÉSULTAT DE L'INFÉRENCE")
    print("=" * 60)
    print(output_text)
    print("=" * 60)

    print("\n" + "=" * 60)
    print("MÉTRIQUES DE PERFORMANCE & MÉMOIRE")
    print("=" * 60)
    print(f"- Temps de chargement modèle : {load_duration:.2f} s")
    print(f"- Temps d'inférence          : {infer_duration:.2f} s")
    print(f"- Tokens d'entrée (total)    : {input_token_count}")
    print(f"- Tokens générés             : {num_generated_tokens}")
    print(f"- Vitesse de génération      : {tokens_per_sec:.2f} tokens/s")
    print(f"- VRAM PyTorch au repos      : {torch_alloc_after_load:.1f} MB ({torch_alloc_after_load / 1024:.2f} GB)")
    print(f"- VRAM PyTorch Pic Inférence : {peak_alloc:.1f} MB ({peak_alloc / 1024:.2f} GB)")
    print(f"- VRAM PyTorch Pic Réservée  : {peak_res:.1f} MB ({peak_res / 1024:.2f} GB)")
    if sys_used_after_infer is not None:
        print(f"- VRAM Système Totale Utilisée : {sys_used_after_infer:.1f} MB ({sys_used_after_infer / 1024:.2f} GB / {sys_total / 1024:.2f} GB)")
        free_headroom = sys_total - sys_used_after_infer
        print(f"- VRAM Marge restante libre    : {free_headroom:.1f} MB ({free_headroom / 1024:.2f} GB)")
    print("=" * 60)

if __name__ == "__main__":
    main()
