#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Évaluation Baseline de Référence (Qwen2-VL-7B-Instruct non entraîné)
=============================================================================
Ce script exécute l'inférence sur les 5 exemples de validation du dataset ARCHI-AI
afin d'établir le benchmark initial (point zéro) avant tout entraînement QLoRA.

Contraintes strictes :
- Modèle de base : Qwen/Qwen2-VL-7B-Instruct
- Quantification : 4-bit NF4, double quantization, bfloat16 compute
- Résolution visuelle : max_pixels = 512 x 512 (262,144 pixels)
- Aucune rétropropagation, aucun entraînement, aucun poids modifié
- Réponses attendues non fournies au modèle (inférence aveugle)
- Génération déterministe (greedy decoding do_sample=False, seed=42)
"""

import os
import sys
import time
import json
import torch
from PIL import Image

from transformers import (
    Qwen2VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig
)
from qwen_vl_utils import process_vision_info


def set_deterministic(seed: int = 42):
    """Fixe les graines pour une reproductibilité maximale."""
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def main():
    print("=" * 70)
    print("ARCHI-AI : BENCHMARK BASELINE INITIAL (Qwen2-VL-7B-Instruct)")
    print("=" * 70)

    # 1. Vérification environnement matériel
    if not torch.cuda.is_available():
        print("ERREUR CRITIQUE : CUDA non disponible.")
        sys.exit(1)

    device_name = torch.cuda.get_device_name(0)
    total_vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    print(f"Périphérique GPU : {device_name}")
    print(f"VRAM Totale      : {total_vram_gb:.2f} GB")

    set_deterministic(seed=42)

    # 2. Chemins des fichiers
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "dataset")
    validation_path = os.path.join(dataset_dir, "validation.jsonl")
    eval_dir = os.path.join(base_dir, "evaluation")
    results_json_path = os.path.join(eval_dir, "baseline_results.json")
    results_md_path = os.path.join(eval_dir, "BASELINE_EVALUATION.md")

    if not os.path.exists(validation_path):
        print(f"ERREUR : Fichier validation introuvable : {validation_path}")
        sys.exit(1)

    os.makedirs(eval_dir, exist_ok=True)

    # 3. Chargement du dataset de validation
    val_samples = []
    with open(validation_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                val_samples.append(json.loads(line))

    print(f"Exemples de validation chargés : {len(val_samples)} / 5 attendus.")
    if len(val_samples) != 5:
        print(f"ATTENTION : Le dataset contient {len(val_samples)} exemples (attendu : 5).")

    # 4. Configuration d'inférence validée (4-bit NF4, double quant, bfloat16)
    model_id = "Qwen/Qwen2-VL-7B-Instruct"
    print("\n[Configuration d'inférence validée]")
    print(f"- Modèle de base   : {model_id}")
    print(f"- Quantification   : 4-bit NF4 (BitsAndBytes)")
    print(f"- Double Quant     : True")
    print(f"- Compute Dtype    : torch.bfloat16")
    print(f"- max_pixels       : 512 x 512 (262,144 pixels)")
    print(f"- min_pixels       : 256 x 28 x 28 (200,704 pixels)")
    print(f"- Mode génération  : Déterministe (do_sample=False, max_new_tokens=512, seed=42)")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True
    )

    print("\nChargement du processeur et du modèle...")
    load_start = time.time()

    processor = AutoProcessor.from_pretrained(
        model_id,
        min_pixels=256 * 28 * 28,
        max_pixels=512 * 512
    )

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True
    )
    model.eval()  # Mode évaluation strict : aucun calcul de gradient
    load_duration = time.time() - load_start
    print(f"--> Modèle chargé avec succès en {load_duration:.2f} s")

    # 5. Inférence sur chacun des 5 exemples
    print("\n" + "=" * 70)
    print("DÉBUT DU BENCHMARK BASELINE (5 EXEMPLES)")
    print("=" * 70)

    results = []
    total_tokens = 0
    total_time = 0.0

    for idx, sample in enumerate(val_samples, start=1):
        sample_id = sample["id"]
        category = sample.get("category", "")
        rel_img_path = sample["image"]
        img_path = os.path.join(dataset_dir, rel_img_path)
        question = sample["question"]
        context = sample.get("context", "")
        expected_answer = sample.get("answer", "")

        # Construction du texte utilisateur exact du dataset
        # (Contexte + Question, sans jamais fournir l'assistant answer)
        if context:
            user_text = f"Contexte : {context}\n\nQuestion : {question}"
        else:
            user_text = question

        print(f"\n[{idx}/5] Traitement de l'exemple : {sample_id} ({category})")
        print(f"      Image    : {rel_img_path}")
        print(f"      Question : {question}")

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image introuvable : {img_path}")

        # Format multimodal Qwen2-VL (rôle user uniquement)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": img_path},
                    {"type": "text", "text": user_text}
                ]
            }
        ]

        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)

        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to("cuda")

        # Synchronisation et mesure du temps d'inférence
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        infer_start = time.perf_counter()

        with torch.inference_mode():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False  # Greedy decoding pour reproductibilité stricte
            )

        torch.cuda.synchronize()
        infer_duration = time.perf_counter() - infer_start

        # Découpage des tokens d'entrée pour isoler les tokens générés
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        generated_text = processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0].strip()

        num_tokens = len(generated_ids_trimmed[0])
        speed = num_tokens / infer_duration if infer_duration > 0 else 0.0

        total_tokens += num_tokens
        total_time += infer_duration

        print(f"      -> Tokens générés : {num_tokens}")
        print(f"      -> Durée inférence: {infer_duration:.2f} s ({speed:.2f} tok/s)")

        # Enregistrement structuré du résultat
        record = {
            "id": sample_id,
            "catégorie": category,
            "categorie": category,
            "image": rel_img_path,
            "context": context,
            "question": question,
            "réponse générée": generated_text,
            "reponse_generée": generated_text,
            "reponse_generee": generated_text,
            "réponse attendue": expected_answer,
            "reponse_attendue": expected_answer,
            "temps d’inférence": round(infer_duration, 3),
            "temps_inference": round(infer_duration, 3),
            "temps_inference_s": round(infer_duration, 3),
            "nombre de tokens générés": num_tokens,
            "nombre_tokens_generes": num_tokens,
            "tokens_generes": num_tokens,
            "vitesse_tok_s": round(speed, 2)
        }
        results.append(record)

    # 6. Synthèse globale
    avg_time = total_time / len(results) if results else 0.0
    avg_tokens_per_sec = total_tokens / total_time if total_time > 0 else 0.0

    print("\n" + "=" * 70)
    print("SYNTHÈSE DU BENCHMARK BASELINE")
    print("=" * 70)
    print(f"Nombre d'exemples évalués : {len(results)} / 5")
    print(f"Temps total d'inférence   : {total_time:.2f} s")
    print(f"Temps moyen par exemple   : {avg_time:.2f} s")
    print(f"Nombre total de tokens    : {total_tokens}")
    print(f"Vitesse moyenne (tok/s)   : {avg_tokens_per_sec:.2f} tok/s")
    print("=" * 70)

    # 7. Sauvegarde dans baseline_results.json
    output_data = {
        "benchmark": "BASELINE_INITIALE",
        "model_id": model_id,
        "date": "2026-09-21",
        "configuration": {
            "quantization": "4-bit NF4 (BitsAndBytes)",
            "double_quant": True,
            "compute_dtype": "torch.bfloat16",
            "max_pixels": 512 * 512,
            "min_pixels": 256 * 28 * 28,
            "do_sample": False,
            "max_new_tokens": 512,
            "seed": 42
        },
        "metrics_globales": {
            "nombre_exemples": len(results),
            "temps_total_s": round(total_time, 3),
            "temps_moyen_s": round(avg_time, 3),
            "tokens_total": total_tokens,
            "tokens_par_seconde_moyen": round(avg_tokens_per_sec, 2)
        },
        "exemples": results
    }

    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Résultats sauvegardés dans : {results_json_path}")


if __name__ == "__main__":
    main()
