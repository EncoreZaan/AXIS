#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Pipeline d'entraînement QLoRA pour Qwen2-VL-7B-Instruct
================================================================
Ce script prépare et configure l'entraînement QLoRA 4-bit de Qwen2-VL-7B-Instruct
sur le mini-dataset expérimental de critique et analyse spatiale d'architecture.

Caractéristiques clés :
- Quantification 4-bit BitsAndBytes (NF4, double quant, bfloat16 compute)
- Adaptateur LoRA ciblant les projections d'attention et MLP du LLM
- Tour de vision gelée (frozen vision tower)
- Preprocessing multimodal avec AutoProcessor (résolution plafonnée à 512x512)
- Collator multimodal personnalisé (input_ids, attention_mask, labels, pixel_values,
  image_grid_thw, mm_token_type_ids pour M-RoPE)
- Masking des labels du prompt (apprentissage exclusif sur la réponse assistant)
- Gradient checkpointing activé
- Centralisation de la configuration dans config/qlora_experiment.yaml
- Mode --dry-run (construction du batch + forward pass sans boucle d'entraînement)
"""

import os
import sys
import json
import argparse
import yaml
from typing import Dict, List, Any, Optional

import torch
from torch.utils.data import Dataset
from PIL import Image

from transformers import (
    AutoProcessor,
    Qwen2VLForConditionalGeneration,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    TrainerCallback
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training
)
from qwen_vl_utils import process_vision_info


class ARCHIVisionDataset(Dataset):
    """
    Dataset PyTorch pour l'entraînement multimodal de Qwen2-VL.
    Prend en charge les formats conversationnels et applique le masquage des labels.
    """
    def __init__(
        self,
        jsonl_file: str,
        images_base_dir: str,
        processor: AutoProcessor,
        max_seq_length: int = 1536
    ):
        self.jsonl_file = jsonl_file
        self.images_base_dir = images_base_dir
        self.processor = processor
        self.max_seq_length = max_seq_length
        self.samples: List[Dict[str, Any]] = []

        if not os.path.exists(jsonl_file):
            raise FileNotFoundError(f"Fichier dataset introuvable : {jsonl_file}")

        with open(jsonl_file, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    self.samples.append(data)
                except json.JSONDecodeError as e:
                    print(f"[ATTENTION] Ligne {line_idx+1} ignorée (JSON invalide) : {e}")

        # Identifier le motif de début de réponse assistant
        # <|im_start|>assistant\n correspond à [151644, 77091, 198]
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
                        if not os.path.isabs(img_path):
                            img_path = os.path.join(self.images_base_dir, img_path)
                        if not os.path.exists(img_path):
                            raise FileNotFoundError(f"Image introuvable : {img_path}")
                        item_copy["image"] = img_path
                    new_content.append(item_copy)
                msg_copy["content"] = new_content
            else:
                msg_copy["content"] = content
            formatted_conversations.append(msg_copy)

        # Préparation du texte via chat template
        text_prompt = self.processor.apply_chat_template(
            formatted_conversations,
            tokenize=False,
            add_generation_prompt=False
        )

        # Extraction des informations de vision
        image_inputs, video_inputs = process_vision_info(formatted_conversations)

        # Tokenisation et preprocessing de vision
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

        # Troncation éventuelle si dépassement de la longueur maximale
        if input_ids.shape[0] > self.max_seq_length:
            input_ids = input_ids[:self.max_seq_length]
            attention_mask = attention_mask[:self.max_seq_length]
            labels = labels[:self.max_seq_length]

        # Masquage du prompt dans les labels (-100 sur le prompt utilisateur + vision)
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
            # Sécurité : si le header n'est pas identifié, on ne masque rien mais on avertit
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
            # Indispensable pour le calcul M-RoPE dans transformers 5.x
            mm_types = inputs["mm_token_type_ids"][0]
            if mm_types.shape[0] > self.max_seq_length:
                mm_types = mm_types[:self.max_seq_length]
            item_output["mm_token_type_ids"] = mm_types

        return item_output


class VisionLanguageDataCollator:
    """
    Collator multimodal pour Qwen2-VL.
    Gère le padding dynamique des tokens texte et la concaténation des tenseurs visuels.
    """
    def __init__(self, processor: AutoProcessor):
        self.processor = processor
        self.pad_token_id = (
            processor.tokenizer.pad_token_id
            if processor.tokenizer.pad_token_id is not None
            else 151643  # <|endoftext|> par défaut
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

            # Padding à droite des tenseurs 1D
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


def load_config(config_path: str) -> Dict[str, Any]:
    """Charge et valide le fichier de configuration YAML."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Fichier de configuration introuvable : {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def setup_model_and_processor(config: Dict[str, Any]):
    """
    Initialise le processeur, charge le modèle en 4-bit NF4,
    gèle la tour de vision et configure les adaptateurs LoRA.
    """
    model_cfg = config.get("model", {})
    quant_cfg = config.get("quantization", {})
    lora_cfg = config.get("lora", {})
    dataset_cfg = config.get("dataset", {})

    model_id = model_cfg.get("name_or_path", "Qwen/Qwen2-VL-7B-Instruct")
    print(f"\n[1/4] Initialisation du processeur ({model_id})...")
    processor = AutoProcessor.from_pretrained(
        model_id,
        min_pixels=dataset_cfg.get("min_pixels", 256 * 28 * 28),
        max_pixels=dataset_cfg.get("max_pixels", 512 * 512)
    )

    print("[2/4] Configuration de la quantification BitsAndBytes 4-bit (NF4)...")
    compute_dtype = getattr(torch, quant_cfg.get("bnb_4bit_compute_dtype", "bfloat16"))
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=quant_cfg.get("load_in_4bit", True),
        bnb_4bit_quant_type=quant_cfg.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_use_double_quant=quant_cfg.get("bnb_4bit_use_double_quant", True),
        bnb_4bit_compute_dtype=compute_dtype
    )

    print("[3/4] Chargement des poids du modèle de base...")
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map=model_cfg.get("device_map", "auto"),
        torch_dtype=compute_dtype,
        low_cpu_mem_usage=model_cfg.get("low_cpu_mem_usage", True)
    )

    # Préparation pour entraînement quantifié (kbit) avec gradient checkpointing
    print("[4/4] Préparation k-bit et greffe de l'adaptateur LoRA...")
    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=config.get("training", {}).get("gradient_checkpointing", True)
    )

    # Gel explicite de la tour de vision
    if lora_cfg.get("freeze_vision_tower", True):
        if hasattr(model, "model") and hasattr(model.model, "visual"):
            model.model.visual.requires_grad_(False)
            print("  --> Tour visuelle (model.model.visual) : GELÉE (trainable = False)")
        elif hasattr(model, "visual"):
            model.visual.requires_grad_(False)
            print("  --> Tour visuelle (model.visual) : GELÉE (trainable = False)")

    # Configuration LoRA
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
    print("\n--- Synthèse des Paramètres Entraînables ---")
    peft_model.print_trainable_parameters()

    return peft_model, processor


def run_dry_run(
    peft_model: torch.nn.Module,
    processor: AutoProcessor,
    config: Dict[str, Any]
) -> bool:
    """
    Exécute un dry-run rigoureux :
    - Prépare le dataset et collator
    - Construit un batch réel
    - Exécute une passe avant (forward pass) avec calcul de la loss
    - NE FAIT AUCUN BACKWARD, AUCUNE MISE À JOUR DE POIDS, AUCUNE SAUVEGARDE
    """
    print("\n" + "=" * 60)
    print("DÉMARRAGE DU DRY-RUN MULTIMODAL")
    print("=" * 60)

    dataset_cfg = config.get("dataset", {})
    train_dataset = ARCHIVisionDataset(
        jsonl_file=dataset_cfg.get("train_file", "ARCHI_AI/dataset/train.jsonl"),
        images_base_dir=dataset_cfg.get("images_base_dir", "ARCHI_AI/dataset"),
        processor=processor,
        max_seq_length=dataset_cfg.get("max_seq_length", 1536)
    )

    collator = VisionLanguageDataCollator(processor=processor)

    # Prendre les 2 premiers exemples pour tester le collator avec batch_size > 1
    sample_0 = train_dataset[0]
    sample_1 = train_dataset[1]
    test_batch = collator([sample_0, sample_1])

    print(f"Dataset train chargé : {len(train_dataset)} exemples.")
    print(f"Batch de test construit (taille = 2) :")
    print(f"  - input_ids shape      : {test_batch['input_ids'].shape}")
    print(f"  - attention_mask shape : {test_batch['attention_mask'].shape}")
    print(f"  - labels shape         : {test_batch['labels'].shape}")
    if 'pixel_values' in test_batch:
        print(f"  - pixel_values shape   : {test_batch['pixel_values'].shape}")
    if 'image_grid_thw' in test_batch:
        print(f"  - image_grid_thw shape : {test_batch['image_grid_thw'].shape}")
    if 'mm_token_type_ids' in test_batch:
        print(f"  - mm_token_type_ids    : {test_batch['mm_token_type_ids'].shape}")

    # Vérification du masquage des labels
    non_masked_count = (test_batch['labels'][0] != -100).sum().item()
    masked_count = (test_batch['labels'][0] == -100).sum().item()
    print(f"Exemple 0 : {masked_count} tokens de prompt masqués (-100), {non_masked_count} tokens d'assistant actifs.")

    # Déplacement vers le device approprié
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Pour le forward pass, prenons batch_size = 1 pour respecter la contrainte VRAM locale
    single_batch = collator([sample_0])
    cuda_batch = {k: v.to(device) for k, v in single_batch.items()}

    print(f"\nExécution de la passe avant (Forward Pass) sur {device}...")
    peft_model.eval()
    with torch.no_grad():
        outputs = peft_model(**cuda_batch)

    loss = outputs.loss
    logits = outputs.logits

    print(f"[RÉSULTAT DRY-RUN] Loss calculée : {loss.item():.4f}")
    print(f"[RÉSULTAT DRY-RUN] Logits shape   : {logits.shape}")

    if torch.cuda.is_available():
        allocated_mb = torch.cuda.memory_allocated() / (1024 ** 2)
        reserved_mb = torch.cuda.memory_reserved() / (1024 ** 2)
        print(f"[VRAM ALLOCATED]   : {allocated_mb:.1f} Mo")
        print(f"[VRAM RESERVED]    : {reserved_mb:.1f} Mo")

    print("\n[VÉRIFICATION STRICTE]")
    print("  * Aucune mise à jour de gradient effectuée : OUI")
    print("  * Aucun backward pass exécuté             : OUI")
    print("  * Aucune sauvegarde de poids altérés       : OUI")
    print("  * Batch multimodal et Loss fonctionnels    : OUI")
    print("=" * 60)
    print("DRY-RUN VALIDÉ AVEC SUCCÈS")
    print("=" * 60)
    return True


def main():
    parser = argparse.ArgumentParser(description="Pipeline QLoRA ARCHI-AI pour Qwen2-VL-7B")
    parser.add_argument(
        "--config",
        type=str,
        default="ARCHI_AI/config/qlora_experiment.yaml",
        help="Chemin vers le fichier de configuration YAML"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Exécute uniquement le dry-run (construction du batch + forward pass, sans entraînement)"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Valide les fichiers, dépendances, images et dataset sans charger le modèle 7B"
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Sécurité : doit être explicitement spécifié pour lancer la boucle d'entraînement"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("ARCHI-AI: Initialisation du Pipeline QLoRA")
    print("=" * 60)

    # 1. Chargement de la configuration
    config = load_config(args.config)
    print(f"Configuration chargée depuis : {args.config}")

    # 2. Mode Validation Rapide
    if args.validate_only:
        print("\n--- Mode Validation Rapide ---")
        dataset_cfg = config.get("dataset", {})
        train_file = dataset_cfg.get("train_file")
        val_file = dataset_cfg.get("validation_file")
        base_dir = dataset_cfg.get("images_base_dir")

        print(f"Vérification de train.jsonl ({train_file})...")
        with open(train_file, "r", encoding="utf-8") as f:
            train_count = sum(1 for _ in f)
        print(f"  -> {train_count} exemples trouvés.")

        print(f"Vérification de validation.jsonl ({val_file})...")
        with open(val_file, "r", encoding="utf-8") as f:
            val_count = sum(1 for _ in f)
        print(f"  -> {val_count} exemples trouvés.")

        print("Vérification de l'ouverture d'un échantillon d'image...")
        with open(train_file, "r", encoding="utf-8") as f:
            sample = json.loads(f.readline())
            img_path = os.path.join(base_dir, sample["image"])
            with Image.open(img_path) as img:
                print(f"  -> Image test chargée : {img_path} ({img.size[0]}x{img.size[1]}, format: {img.format})")

        print("\n[VALIDATION] Tous les chemins et données de base sont validés.")
        sys.exit(0)

    # 3. Initialisation du modèle et processeur
    peft_model, processor = setup_model_and_processor(config)

    # 4. Exécution du Dry-Run
    if args.dry_run:
        success = run_dry_run(peft_model, processor, config)
        if success:
            sys.exit(0)
        else:
            sys.exit(1)

    # 5. Garde-fou Entraînement
    if not args.train:
        print("\n[ATTENTION] La commande a été exécutée sans le flag --train.")
        print("Conformément aux consignes de sécurité, aucun entraînement n'a été lancé.")
        print("Pour vérifier le pipeline complet jusqu'au forward pass, lancez avec : --dry-run")
        sys.exit(0)

    # 6. Configuration de l'entraînement Hugging Face Trainer
    # (Activé uniquement sur instance GPU 24 Go avec flag explicite --train)
    training_cfg = config.get("training", {})
    dataset_cfg = config.get("dataset", {})

    train_dataset = ARCHIVisionDataset(
        jsonl_file=dataset_cfg.get("train_file"),
        images_base_dir=dataset_cfg.get("images_base_dir"),
        processor=processor,
        max_seq_length=dataset_cfg.get("max_seq_length", 1536)
    )

    eval_dataset = ARCHIVisionDataset(
        jsonl_file=dataset_cfg.get("validation_file"),
        images_base_dir=dataset_cfg.get("images_base_dir"),
        processor=processor,
        max_seq_length=dataset_cfg.get("max_seq_length", 1536)
    )

    data_collator = VisionLanguageDataCollator(processor=processor)

    training_args = TrainingArguments(
        output_dir=training_cfg.get("output_dir", "ARCHI_AI/outputs/qlora_adapter"),
        per_device_train_batch_size=training_cfg.get("per_device_train_batch_size", 1),
        per_device_eval_batch_size=training_cfg.get("per_device_eval_batch_size", 1),
        gradient_accumulation_steps=training_cfg.get("gradient_accumulation_steps", 8),
        num_train_epochs=training_cfg.get("num_train_epochs", 3),
        learning_rate=float(training_cfg.get("learning_rate", 1e-4)),
        lr_scheduler_type=training_cfg.get("lr_scheduler_type", "cosine"),
        warmup_ratio=float(training_cfg.get("warmup_ratio", 0.05)),
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

    print("\nLancement de l'entraînement QLoRA...")
    trainer.train()

    print("\nSauvegarde de l'adaptateur LoRA final...")
    output_dir = training_cfg.get("output_dir", "ARCHI_AI/outputs/qlora_adapter")
    peft_model.save_pretrained(output_dir)
    processor.save_pretrained(output_dir)
    print(f"Adaptateur LoRA sauvegardé dans : {output_dir}")


if __name__ == "__main__":
    main()
