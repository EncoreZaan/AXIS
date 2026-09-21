#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Détecteur de doublons et near-duplicates
==================================================
Analyse les collisions exactes (SHA-256) et quasi-doublons perceptuels (pHash).
Signale les cas suspects sans suppression arbitraire : un même espace peut servir
à enseigner deux compétences différentes.
"""

import os
import sys
import json
from typing import List, Dict, Any, Tuple
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dataset_tools.deduplication.hasher import hamming_distance


class DeduplicationAnalyzer:
    """Analyseur de doublons et near-duplicates."""

    def __init__(self, hamming_threshold: int = 5):
        self.hamming_threshold = hamming_threshold

    def analyze(self, master_annotations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Détecte les doublons d'images, de textes et les collisions d'identifiants.
        """
        results = {
            "total_records": len(master_annotations),
            "id_collisions": [],
            "exact_image_duplicates": [],
            "near_image_duplicates": [],
            "exact_text_duplicates": [],
            "same_image_different_skills": [],
            "warnings_count": 0
        }

        # 1. Vérification ID collisions
        seen_ids = {}
        for idx, item in enumerate(master_annotations):
            item_id = item.get("id")
            if item_id in seen_ids:
                results["id_collisions"].append({
                    "id": item_id,
                    "first_index": seen_ids[item_id],
                    "duplicate_index": idx
                })
            else:
                seen_ids[item_id] = idx

        # 2. Vérification d'images exactes et quasi-doublons
        images_info = [] # list of dict(id=..., path=..., sha256=..., phash=..., skills=...)
        for item in master_annotations:
            for img in item.get("images", []):
                images_info.append({
                    "id": item.get("id"),
                    "path": img.get("path"),
                    "sha256": img.get("sha256"),
                    "phash": img.get("phash"),
                    "skills": item.get("skills", []),
                    "question": item.get("question", "")
                })

        # Exact SHA-256 matches
        sha_map = defaultdict(list)
        for img in images_info:
            if img["sha256"]:
                sha_map[img["sha256"]].append(img)

        for sha, group in sha_map.items():
            if len(group) > 1:
                # Vérifier si ce sont des exemples distincts
                distinct_ids = list({g["id"] for g in group})
                if len(distinct_ids) > 1:
                    # Distinction : doublon textuel ou cas pédagogique multi-compétences ?
                    distinct_questions = list({g["question"] for g in group})
                    if len(distinct_questions) == 1:
                        results["exact_image_duplicates"].append({
                            "sha256": sha,
                            "items": [g["id"] for g in group],
                            "type": "EXACT_DUPLICATE"
                        })
                    else:
                        results["same_image_different_skills"].append({
                            "sha256": sha,
                            "items": [g["id"] for g in group],
                            "type": "LEGITIMATE_MULTI_SKILL_REUSE"
                        })

        # Near-duplicate perceptual matches (Hamming distance)
        n = len(images_info)
        for i in range(n):
            for j in range(i + 1, n):
                img1 = images_info[i]
                img2 = images_info[j]
                if img1["id"] == img2["id"]:
                    continue
                # Si déjà identique en SHA-256, ignoré ici
                if img1["sha256"] and img1["sha256"] == img2["sha256"]:
                    continue
                if img1["phash"] and img2["phash"]:
                    dist = hamming_distance(img1["phash"], img2["phash"])
                    if dist <= self.hamming_threshold:
                        results["near_image_duplicates"].append({
                            "id_a": img1["id"],
                            "id_b": img2["id"],
                            "path_a": img1["path"],
                            "path_b": img2["path"],
                            "hamming_distance": dist
                        })

        # Exact text matches
        question_map = defaultdict(list)
        for item in master_annotations:
            q_clean = item.get("question", "").strip().lower()
            if q_clean:
                question_map[q_clean].append(item.get("id"))

        for q, ids in question_map.items():
            if len(ids) > 1:
                results["exact_text_duplicates"].append({
                    "question_snippet": q[:80],
                    "ids": ids
                })

        results["warnings_count"] = (
            len(results["id_collisions"]) +
            len(results["exact_image_duplicates"]) +
            len(results["near_image_duplicates"])
        )
        return results


def run_deduplication_cli(master_file: str):
    """Exécution en ligne de commande."""
    if not os.path.exists(master_file):
        print(f"Fichier introuvable: {master_file}")
        return
    with open(master_file, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    analyzer = DeduplicationAnalyzer()
    res = analyzer.analyze(records)
    print(f"--- RÉSULTATS DÉDUPLICATION ({res['total_records']} exemples) ---")
    print(f"Collisions d'identifiants : {len(res['id_collisions'])}")
    print(f"Doublons stricts d'images : {len(res['exact_image_duplicates'])}")
    print(f"Near-duplicates suspects : {len(res['near_image_duplicates'])}")
    print(f"Images réutilisées pour compétences différentes : {len(res['same_image_different_skills'])}")
    print(f"Doublons exacts de questions : {len(res['exact_text_duplicates'])}")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    master_file = os.path.join(base_dir, "dataset", "master", "annotations", "master_annotations.jsonl")
    run_deduplication_cli(master_file)
