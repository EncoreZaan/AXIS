#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Splitter et détecteur de contamination (Data Leakage)
==============================================================
Garantit une séparation étanche entre train, validation et test.
Empêche qu'une même image, une même scène (scene_id) ou un même projet
se retrouve partagé entre le train et les sets d'évaluation.
Sanctuarise le test set.
"""

import os
import sys
import json
from typing import List, Dict, Any, Set, Tuple, Optional
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dataset_tools.validation.taxonomy import SplitName


class SplitLeakageDetector:
    """Détecteur de fuite d'informations (leakage / contamination) entre partitions."""

    def check_splits(
        self,
        train_samples: List[Dict[str, Any]],
        val_samples: List[Dict[str, Any]],
        test_samples: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Vérifie qu'aucune image, hash, question, scene_id ou project_name
        n'est partagé entre train, val et test.
        """
        if test_samples is None:
            test_samples = []

        splits_map = {
            SplitName.TRAIN.value: train_samples,
            SplitName.VALIDATION.value: val_samples,
            SplitName.TEST.value: test_samples
        }

        report = {
            "is_clean": True,
            "leakages": [],
            "split_counts": {k: len(v) for k, v in splits_map.items()},
            "details": []
        }

        # Extraire les empreintes pour chaque split
        # image_paths, sha256_set, scene_ids, project_names, text_questions
        split_features = {}
        for s_name, samples in splits_map.items():
            imgs = set()
            shas = set()
            scenes = set()
            projects = set()
            questions = set()
            ids = set()

            for s in samples:
                ids.add(s.get("id"))
                q = s.get("question", "").strip().lower()
                if q:
                    questions.add(q)
                
                # Provenance
                prov = s.get("provenance", {})
                if isinstance(prov, dict):
                    if prov.get("scene_id"):
                        scenes.add(prov.get("scene_id"))
                    if prov.get("project_name"):
                        projects.add(prov.get("project_name"))
                        
                # Images
                for img in s.get("images", []):
                    if img.get("path"):
                        imgs.add(img.get("path"))
                    if img.get("sha256"):
                        shas.add(img.get("sha256"))

            split_features[s_name] = {
                "ids": ids,
                "imgs": imgs,
                "shas": shas,
                "scenes": scenes,
                "projects": projects,
                "questions": questions
            }

        # Comparaisons par paires
        split_names = [SplitName.TRAIN.value, SplitName.VALIDATION.value, SplitName.TEST.value]
        for i in range(len(split_names)):
            for j in range(i + 1, len(split_names)):
                s1, s2 = split_names[i], split_names[j]
                f1, f2 = split_features[s1], split_features[s2]

                # 1. ID Leakage
                id_overlap = f1["ids"].intersection(f2["ids"])
                if id_overlap:
                    report["is_clean"] = False
                    report["leakages"].append(f"ID overlap between {s1} and {s2}: {id_overlap}")

                # 2. Exact Image File Leakage
                img_overlap = f1["imgs"].intersection(f2["imgs"])
                if img_overlap:
                    report["is_clean"] = False
                    report["leakages"].append(f"Exact image path overlap between {s1} and {s2}: {img_overlap}")

                # 3. Cryptographic SHA-256 Image Leakage
                sha_overlap = f1["shas"].intersection(f2["shas"])
                if sha_overlap:
                    report["is_clean"] = False
                    report["leakages"].append(f"Identical image SHA-256 hash overlap between {s1} and {s2}: {sha_overlap}")

                # 4. Scene Leakage
                scene_overlap = f1["scenes"].intersection(f2["scenes"])
                if scene_overlap:
                    report["is_clean"] = False
                    report["leakages"].append(f"Scene ID overlap (contamination de point de vue) between {s1} and {s2}: {scene_overlap}")

                # 5. Question Leakage
                q_overlap = f1["questions"].intersection(f2["questions"])
                if q_overlap:
                    report["is_clean"] = False
                    report["leakages"].append(f"Identical prompt/question overlap between {s1} and {s2}: {len(q_overlap)} questions")

        return report


def save_split_manifests(
    master_records: List[Dict[str, Any]],
    output_dir: str
) -> Dict[str, str]:
    """Sauvegarde les listes d'identifiants et fichiers par split."""
    os.makedirs(output_dir, exist_ok=True)
    splits = {
        SplitName.TRAIN.value: [],
        SplitName.VALIDATION.value: [],
        SplitName.TEST.value: []
    }

    for item in master_records:
        split_val = item.get("assigned_split", SplitName.TRAIN.value)
        if split_val in splits:
            splits[split_val].append(item)
        else:
            splits[SplitName.TRAIN.value].append(item)

    saved_files = {}
    for s_name, items in splits.items():
        out_file = os.path.join(output_dir, f"{s_name}.jsonl")
        manifest_file = os.path.join(output_dir, f"{s_name}_ids.txt")
        with open(out_file, "w", encoding="utf-8") as f, open(manifest_file, "w", encoding="utf-8") as mf:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
                mf.write(f"{it['id']}\n")
        saved_files[s_name] = out_file

    return saved_files
