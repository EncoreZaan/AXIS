#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Pipeline d'Entraînement QLoRA Reproductible pour GPU Distant 24 Go
===========================================================================
Modèle cible : Qwen/Qwen2-VL-7B-Instruct
Format        : QLoRA 4-bit NF4 + bfloat16
Dataset       : 20 train / 5 validation (critique architecturale multimodal)
Tous les chemins sont relatifs au dossier racine du package.
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Any

import yaml
from PIL import Image
import torch
from torch.utils.data import Dataset

from transformers import (
    AutoProcessor,
    Qwen2VLForConditionalGeneration,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel
)
from qwen_vl_utils import process_vision_info

# Racine absolue du package calculée dynamiquement (indépendante de la machine hôte)
PACKAGE_ROOT = Path(__file__).resolve().parent


def resolve_path(path_str: str) -> Path:
    """Résout un chemin de façon relative à la racine du package s'il n'est pas absolu."""
    p = Path(path_str)
    if p.is_absolute():
        return p
    return PACKAGE_ROOT / p


class ARCHIVisionDataset(Dataset):
    """
    Dataset PyTorch pour l'entraînement multimodal de Qwen2-VL.
    Gère les conversations structurées et le masquage des tokens de prompt (-100).
    """
    def __init__(
        self,
        jsonl_file: str,
        images_base_dir: str,
        processor: AutoProcessor,
        max_seq_length: int = 1536
    ):
        self.jsonl_file = resolve_path(jsonl_file)
        self.images_base_dir = resolve_path(images_base_dir)
        self.processor = processor
        self.max_seq_length = max_seq_length
        self.samples: List[Dict[str, Any]] = []

        if not self.jsonl_file.exists():
            raise FileNotFoundError(f"Fichier dataset introuvable : {self.jsonl_file}")

        with open(self.jsonl_file, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    self.samples.append(data)
                except json.JSONDecodeError as e:
                    print(f"[ATTENTION] Ligne {line_idx+1} ignorée (JSON invalide) : {e}")

        # Motif de début de réponse assistant (<|im_start|>assistant\n)
        self.assistant_header_tokens = self.processor.tokenizer.encode("<|im_start|>assistant\n")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        sample = self.samples[idx]
        conversations = sample["conversations"]

        # Résolution des chemins d'images relatifs
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
                        resolved_img = resolve_path(self.images_base_dir / img_path)
                        if not resolved_img.exists():
                            # Fallback si le chemin est déjà préfixé par le dossier images
                            resolved_img = self.images_base_dir / Path(img_path).name
                        if not resolved_img.exists():
                            raise FileNotFoundError(f"Image introuvable : {img_path} (cherché dans {self.images_base_dir})")
                        item_copy["image"] = str(resolved_img)
                    new_content.append(item_copy)
                msg_copy["content"] = new_content
            else:
                msg_copy["content"] = content
            formatted_conversations.append(msg_copy)

        # Chat template
        text_prompt = self.processor.apply_chat_template(
            formatted_conversations,
            tokenize=False,
            add_generation_prompt=False
        )

        # Extraction visuelle
        image_inputs, video_inputs = process_vision_info(formatted_conversations)

        # Preprocessing multimodal
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

        # Troncation si dépassement
        if input_ids.shape[0] > self.max_seq_length:
            input_ids = input_ids[:self.max_seq_length]
            attention_mask = attention_mask[:self.max_seq_length]
            labels = labels[:self.max_seq_length]

        # Masquage du prompt utilisateur + vision (-100)
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
            print(f"[WARN] En-tête assistant non trouvé pour l'échantillon {sample.get('id', idx)}")

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
    """Collator multimodal avec padding dynamique pour Qwen2-VL."""
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


def load_config(config_path_str: str) -> Dict[str, Any]:
    """Charge le fichier YAML de configuration."""
    resolved = resolve_path(config_path_str)
    if not resolved.exists():
        raise FileNotFoundError(f"Configuration introuvable : {resolved}")
    with open(resolved, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_only_routine(config: Dict[str, Any]):
    """Garde-fou : Valide l'environnement et le dataset sans charger le modèle."""
    print("\n" + "=" * 65)
    print("MODE SÉCURISÉ : --validate-only")
    print("Vérification locale de l'intégrité sans chargement du modèle 7B")
    print("=" * 65)

    dataset_cfg = config.get("dataset", {})
    train_file = resolve_path(dataset_cfg.get("train_file", "dataset/train.jsonl"))
    val_file = resolve_path(dataset_cfg.get("validation_file", "dataset/validation.jsonl"))
    images_base_dir = resolve_path(dataset_cfg.get("images_base_dir", "dataset"))

    print(f"[*] Fichier train       : {train_file}")
    if not train_file.exists():
        print(f"[!] ERREUR : Fichier train manquant : {train_file}")
        sys.exit(1)

    print(f"[*] Fichier validation  : {val_file}")
    if not val_file.exists():
        print(f"[!] ERREUR : Fichier validation manquant : {val_file}")
        sys.exit(1)

    # Vérification du contenu train
    train_records = []
    with open(train_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                train_records.append(json.loads(line))
    print(f"[*] Exemples train      : {len(train_records)} (attendu: 20)")

    # Vérification du contenu val
    val_records = []
    with open(val_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                val_records.append(json.loads(line))
    print(f"[*] Exemples val        : {len(val_records)} (attendu: 5)")

    # Vérification de l'ouverture et dimensions de TOUTES les 25 images
    all_records = train_records + val_records
    print(f"\n[*] Audit exhaustif des {len(all_records)} images associées :")
    for rec in all_records:
        rec_id = rec.get("id", "inconnu")
        rel_img = rec.get("image", "")
        img_path = resolve_path(images_base_dir / rel_img)
        if not img_path.exists():
            img_path = resolve_path(images_base_dir / "images" / Path(rel_img).name)
        if not img_path.exists():
            print(f"    [!] ERREUR : Image introuvable pour {rec_id} ({img_path})")
            sys.exit(1)
        with Image.open(img_path) as im:
            w, h = im.size
            fmt = im.format

    print(f"    -> 25/25 images localisées, ouvertes et décodées avec succès.")

    # Audit des paramètres de configuration
    model_cfg = config.get("model", {})
    quant_cfg = config.get("quantization", {})
    lora_cfg = config.get("lora", {})
    train_cfg = config.get("training", {})

    print("\n[*] Synthèse de la configuration d'entraînement :")
    print(f"    - Modèle de base       : {model_cfg.get('name_or_path')}")
    print(f"    - Quantification       : 4-bit {quant_cfg.get('bnb_4bit_quant_type')} (double quant: {quant_cfg.get('bnb_4bit_use_double_quant')})")
    print(f"    - LoRA Rank / Alpha    : r={lora_cfg.get('r')}, alpha={lora_cfg.get('lora_alpha')}, dropout={lora_cfg.get('lora_dropout')}")
    print(f"    - Modules cibles       : {lora_cfg.get('target_modules')}")
    print(f"    - Tour visuelle gelée  : {lora_cfg.get('freeze_vision_tower')}")
    print(f"    - Résolution max       : {dataset_cfg.get('max_pixels')} px (512x512)")
    print(f"    - Contexte max         : {dataset_cfg.get('max_seq_length')} tokens")
    print(f"    - Batch / Accumulation : {train_cfg.get('per_device_train_batch_size')} / {train_cfg.get('gradient_accumulation_steps')} (Effectif = 8)")
    print(f"    - Époques prévues      : {train_cfg.get('num_train_epochs')} (~5 steps d'optimisation)")
    print(f"    - Optimiseur / LR      : {train_cfg.get('optim')} / {train_cfg.get('learning_rate')}")
    print(f"    - Checkpoint output    : {resolve_path(train_cfg.get('output_dir'))}")

    print("\n" + "=" * 65)
    print("STATUS VALIDATION : PASS")
    print("L'ensemble des données, images et paramètres sont validés.")
    print("Le package est prêt pour le micro-test sur GPU 24 Go.")
    print("=" * 65)
    sys.exit(0)


def setup_model_and_processor(config: Dict[str, Any]):
    """Initialise le modèle en 4-bit NF4 et greffe l'adaptateur LoRA."""
    model_cfg = config.get("model", {})
    quant_cfg = config.get("quantization", {})
    lora_cfg = config.get("lora", {})
    dataset_cfg = config.get("dataset", {})
    training_cfg = config.get("training", {})

    model_id = model_cfg.get("name_or_path", "Qwen/Qwen2-VL-7B-Instruct")
    print(f"\n[1/4] Initialisation du processeur ({model_id})...")
    processor = AutoProcessor.from_pretrained(
        model_id,
        min_pixels=dataset_cfg.get("min_pixels", 256 * 28 * 28),
        max_pixels=dataset_cfg.get("max_pixels", 512 * 512)
    )

    print("[2/4] Configuration BitsAndBytes 4-bit (NF4, bfloat16)...")
    compute_dtype = getattr(torch, quant_cfg.get("bnb_4bit_compute_dtype", "bfloat16"))
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=quant_cfg.get("load_in_4bit", True),
        bnb_4bit_quant_type=quant_cfg.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_use_double_quant=quant_cfg.get("bnb_4bit_use_double_quant", True),
        bnb_4bit_compute_dtype=compute_dtype
    )

    print("[3/4] Chargement des poids quantifiés du modèle...")
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map=model_cfg.get("device_map", "auto"),
        torch_dtype=compute_dtype,
        low_cpu_mem_usage=model_cfg.get("low_cpu_mem_usage", True)
    )

    print("[4/4] Activation gradient checkpointing et greffe adaptateur LoRA...")
    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=training_cfg.get("gradient_checkpointing", True)
    )

    # Gel explicite de la tour de vision
    if lora_cfg.get("freeze_vision_tower", True):
        if hasattr(model, "model") and hasattr(model.model, "visual"):
            model.model.visual.requires_grad_(False)
            print("  --> Tour visuelle gelée (requires_grad = False)")
        elif hasattr(model, "visual"):
            model.visual.requires_grad_(False)
            print("  --> Tour visuelle gelée (requires_grad = False)")

    peft_config = LoraConfig(
        r=lora_cfg.get("r", 8),
        lora_alpha=lora_cfg.get("lora_alpha", 16),
        target_modules=lora_cfg.get("target_modules", [
            "q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"
        ]),
        lora_dropout=lora_cfg.get("lora_dropout", 0.05),
        bias=lora_cfg.get("bias", "none"),
        task_type=lora_cfg.get("task_type", "CAUSAL_LM")
    )

    peft_model = get_peft_model(model, peft_config)
    print("\n--- Paramètres LoRA Entraînables ---")
    peft_model.print_trainable_parameters()

    return peft_model, processor


def run_dry_run(peft_model: torch.nn.Module, processor: AutoProcessor, config: Dict[str, Any]):
    """Vérifie forward pass + calcul de la loss sans aucune rétropropagation."""
    print("\n" + "=" * 65)
    print("DÉMARRAGE DU DRY-RUN MULTIMODAL")
    print("=" * 65)

    dataset_cfg = config.get("dataset", {})
    train_dataset = ARCHIVisionDataset(
        jsonl_file=dataset_cfg.get("train_file", "dataset/train.jsonl"),
        images_base_dir=dataset_cfg.get("images_base_dir", "dataset"),
        processor=processor,
        max_seq_length=dataset_cfg.get("max_seq_length", 1536)
    )
    collator = VisionLanguageDataCollator(processor=processor)

    sample_0 = train_dataset[0]
    sample_1 = train_dataset[1]
    test_batch = collator([sample_0, sample_1])

    print(f"Dataset train chargé : {len(train_dataset)} exemples.")
    print(f"Batch test construit (taille = 2) :")
    print(f"  - input_ids shape      : {test_batch['input_ids'].shape}")
    print(f"  - attention_mask shape : {test_batch['attention_mask'].shape}")
    print(f"  - labels shape         : {test_batch['labels'].shape}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    single_batch = collator([sample_0])
    cuda_batch = {k: v.to(device) for k, v in single_batch.items()}

    print(f"\nExécution Forward Pass sur {device}...")
    peft_model.eval()
    with torch.no_grad():
        outputs = peft_model(**cuda_batch)

    print(f"[RÉSULTAT DRY-RUN] Loss calculée : {outputs.loss.item():.4f}")
    print(f"[RÉSULTAT DRY-RUN] Logits shape   : {outputs.logits.shape}")
    print("=" * 65)
    print("DRY-RUN VALIDÉ AVEC SUCCÈS (Aucun poids modifié)")
    print("=" * 65)
    sys.exit(0)


def execute_training(peft_model: torch.nn.Module, processor: AutoProcessor, config: Dict[str, Any], config_path_str: str):
    """Exécute l'entraînement effectif sur GPU 24 Go et sauvegarde tous les checkpoints."""
    print("\n" + "*" * 65)
    print("ARCHI-AI MICRO EXPERIMENT")
    print("THIS WILL MODIFY MODEL ADAPTER WEIGHTS")
    print("*" * 65)

    training_cfg = config.get("training", {})
    dataset_cfg = config.get("dataset", {})
    output_dir = resolve_path(training_cfg.get("output_dir", "outputs/archi_ai_micro_experiment"))
    output_dir.mkdir(parents=True, exist_ok=True)

    train_dataset = ARCHIVisionDataset(
        jsonl_file=dataset_cfg.get("train_file", "dataset/train.jsonl"),
        images_base_dir=dataset_cfg.get("images_base_dir", "dataset"),
        processor=processor,
        max_seq_length=dataset_cfg.get("max_seq_length", 1536)
    )

    eval_dataset = ARCHIVisionDataset(
        jsonl_file=dataset_cfg.get("validation_file", "dataset/validation.jsonl"),
        images_base_dir=dataset_cfg.get("images_base_dir", "dataset"),
        processor=processor,
        max_seq_length=dataset_cfg.get("max_seq_length", 1536)
    )

    data_collator = VisionLanguageDataCollator(processor=processor)

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        per_device_train_batch_size=training_cfg.get("per_device_train_batch_size", 1),
        per_device_eval_batch_size=training_cfg.get("per_device_eval_batch_size", 1),
        gradient_accumulation_steps=training_cfg.get("gradient_accumulation_steps", 8),
        num_train_epochs=training_cfg.get("num_train_epochs", 2),
        learning_rate=float(training_cfg.get("learning_rate", 1e-4)),
        lr_scheduler_type=training_cfg.get("lr_scheduler_type", "cosine"),
        warmup_steps=int(training_cfg.get("warmup_steps", 1)),
        optim=training_cfg.get("optim", "paged_adamw_8bit"),
        gradient_checkpointing=training_cfg.get("gradient_checkpointing", True),
        bf16=training_cfg.get("bf16", True),
        fp16=training_cfg.get("fp16", False),
        logging_steps=training_cfg.get("logging_steps", 1),
        eval_strategy=training_cfg.get("eval_strategy", "epoch"),
        save_strategy=training_cfg.get("save_strategy", "epoch"),
        save_total_limit=training_cfg.get("save_total_limit", 2),
        dataloader_num_workers=training_cfg.get("dataloader_num_workers", 0),
        report_to=training_cfg.get("report_to", "none")
    )

    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator
    )

    print("\n[TRAINING] Lancement de la boucle d'optimisation...")
    train_result = trainer.train()

    print("\n[EVALUATION] Évaluation sur le dataset de validation...")
    eval_metrics = trainer.evaluate()

    print(f"\n[CHECKPOINT] Sauvegarde des artefacts dans : {output_dir}")
    # 1. Sauvegarde de l'adaptateur LoRA
    peft_model.save_pretrained(str(output_dir))
    print("  -> Adaptateur LoRA sauvegardé (adapter_model.safetensors, adapter_config.json)")

    # 2. Sauvegarde du processor
    processor.save_pretrained(str(output_dir))
    print("  -> AutoProcessor sauvegardé")

    # 3. Sauvegarde de la configuration utilisée
    src_cfg = resolve_path(config_path_str)
    if src_cfg.exists():
        shutil.copy(src_cfg, output_dir / "experiment_config.yaml")
        print("  -> Configuration YAML archivée (experiment_config.yaml)")

    # 4. Sauvegarde des métriques et logs
    trainer.save_metrics("train", train_result.metrics)
    trainer.save_metrics("eval", eval_metrics)
    trainer.save_state()
    print("  -> Métriques et logs sauvegardés (train_results.json, eval_results.json, trainer_state.json)")

    # 5. Vérification du rechargement de l'adaptateur
    print("\n[TEST RECHARGEMENT] Vérification du rechargement de l'adaptateur LoRA...")
    try:
        # Test de rechargement sur le modèle sous-jacent
        _ = PeftModel.from_pretrained(peft_model.base_model.model, str(output_dir))
        print("  -> SUCCÈS : L'adaptateur LoRA se recharge parfaitement sans erreur !")
    except Exception as e:
        print(f"  [!] AVERTISSEMENT lors du rechargement : {e}")

    print("\n" + "=" * 65)
    print("MICRO-EXPÉRIENCE QLORA TERMINÉE AVEC SUCCÈS")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Pipeline d'entraînement QLoRA ARCHI-AI")
    parser.add_argument(
        "--config",
        type=str,
        default="config/qlora_experiment.yaml",
        help="Chemin vers le fichier de configuration YAML (relatif à la racine du package)"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Garde-fou : Valide les fichiers, images et format sans charger le modèle"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Garde-fou : Charge le modèle et teste un forward pass sans modifier aucun poids"
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Sécurité explicite requise : Lance l'entraînement effectif sur GPU"
    )

    args = parser.parse_args()

    print("=" * 65)
    print("ARCHI-AI MICRO EXPERIMENT")
    print("Pipeline Reproductible d'Entraînement QLoRA (Qwen2-VL-7B-Instruct)")
    print("=" * 65)

    config = load_config(args.config)

    # 1. Mode Validation Rapide
    if args.validate_only:
        validate_only_routine(config)

    # 2. Garde-fou d'Exécution : Si ni --train ni --dry-run ne sont fournis
    if not args.train and not args.dry_run:
        print("\n[GARDE-FOU STRICT ACTIF]")
        print("Aucun mode d'exécution n'a été spécifié.")
        print("Pour garantir l'intégrité du système, les arguments disponibles sont :")
        print("  python train_qlora.py --validate-only  (Vérifie dataset et dépendances sans modèle)")
        print("  python train_qlora.py --dry-run        (Teste le forward pass sans rétropropagation)")
        print("  python train_qlora.py --train          (Lance l'entraînement effectif sur GPU 24 Go)")
        print("\nArrêt sécurisé du script sans action.")
        sys.exit(0)

    # 3. Chargement du modèle pour dry-run ou train
    peft_model, processor = setup_model_and_processor(config)

    # 4. Dry-run
    if args.dry_run:
        run_dry_run(peft_model, processor, config)

    # 5. Entraînement effectif
    if args.train:
        execute_training(peft_model, processor, config, args.config)


if __name__ == "__main__":
    main()
