#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Exportateur Master Dataset vers format Qwen2-VL JSONL
==============================================================
Convertit les annotations Master (ou un split donné) en format JSONL
strictement compatible avec train_qlora.py et Qwen2VLForConditionalGeneration.

MASTER DATASET
      ↓
VALIDATION
      ↓
    SPLIT
      ↓
   EXPORT
      ↓
QWEN2-VL JSONL
      ↓
train_qlora.py
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dataset_tools.validation.taxonomy import SplitName


def export_master_to_qwen_vl(
    input_file: str,
    output_file: str,
    images_base_prefix: str = "dataset/"
) -> int:
    """
    Exporte un ensemble d'annotations Master vers le schéma conversationnel Qwen2-VL attendu par train_qlora.py:
    {
       "id": "archi_001",
       "category": "...",
       "space_type": "...",
       "style": "...",
       "image": "images/archi_001.jpg",
       "context": "...",
       "question": "...",
       "answer": "...",
       "conversations": [
          {"role": "user", "content": [{"type": "image", "image": "images/..."}, {"type": "text", "text": "..."}]},
          {"role": "assistant", "content": [{"type": "text", "text": "..."}]}
       ]
    }
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Fichier d'entrée introuvable: {input_file}")

    exported_count = 0
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as in_f, open(output_file, "w", encoding="utf-8") as out_f:
        for line in in_f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)

            # Résoudre le chemin de l'image principale pour Qwen2-VL
            images = item.get("images", [])
            if not images:
                continue

            primary_img = images[0]["path"]
            # Normaliser pour correspondre au format attendu (ex: "images/archi_001.jpg")
            if primary_img.startswith("dataset/"):
                relative_img_path = primary_img[len("dataset/"):]
            else:
                relative_img_path = primary_img

            # Construction du prompt utilisateur
            context_str = item.get("context", "").strip()
            question_str = item.get("question", "").strip()
            if context_str:
                user_text = f"Contexte : {context_str}\n\nQuestion : {question_str}"
            else:
                user_text = f"Question : {question_str}"

            answer_str = item.get("answer", "").strip()

            # Multi-images support si plusieurs images
            user_content = []
            for img_obj in images:
                p = img_obj["path"]
                if p.startswith("dataset/"):
                    p = p[len("dataset/"):]
                user_content.append({"type": "image", "image": p})
            user_content.append({"type": "text", "text": user_text})

            # Format conversation standard compatible Hugging Face / train_qlora
            conversations = [
                {
                    "role": "user",
                    "content": user_content
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": answer_str
                        }
                    ]
                }
            ]

            qwen_record = {
                "id": item["id"],
                "category": item.get("category", "ANALYSE D'ESPACE"),
                "space_type": item.get("space_type", ""),
                "style": item.get("style", ""),
                "image": relative_img_path,
                "context": context_str,
                "question": question_str,
                "answer": answer_str,
                "conversations": conversations
            }

            out_f.write(json.dumps(qwen_record, ensure_ascii=False) + "\n")
            exported_count += 1

    return exported_count


def export_splits_to_qwen(base_dir: str):
    """Exporte les splits train et validation vers dataset/export_qwen/ pour vérification."""
    splits_dir = os.path.join(base_dir, "dataset", "splits")
    export_dir = os.path.join(base_dir, "dataset", "export_qwen")
    os.makedirs(export_dir, exist_ok=True)

    for split_name in ["train", "validation"]:
        src = os.path.join(splits_dir, f"{split_name}.jsonl")
        dst = os.path.join(export_dir, f"{split_name}.jsonl")
        if os.path.exists(src):
            cnt = export_master_to_qwen_vl(src, dst)
            print(f"Export {split_name} terminé : {cnt} enregistrements écrits dans {dst}")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    export_splits_to_qwen(base_dir)
